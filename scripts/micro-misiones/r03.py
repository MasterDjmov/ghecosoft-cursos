import textwrap


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


P1 = "La Torre del Reloj: el primer piso"
P2 = "La Torre del Reloj: el segundo piso"
P3 = "La Torre del Reloj: el tercer piso"
P4 = "El Gremio de Artífices"
P5 = "La cocina de la Torre"
P6 = "La Torre del Reloj: el último piso"
CIMA = "La cima de la Torre del Reloj"

NODOS = [
    {
        "titulo": "R03-N01 · Iteradores y generadores",
        "misiones": [
            m(id="R03-N01-P1", titulo="De a uno",
              lugar=P1, personajes="Mia, Gheco, Tilo",
              carta="iter y next | it = iter(lista) · next(it) da el siguiente · al final: StopIteration",
              recompensa="xp 10, oro 10",
              escena="""
                  La Torre del Reloj se levanta en el centro de la Gran Ciudadela, con sus engranajes a la vista. En el primer piso, de un portal no paran de salir enemigos.
                  —No los mires a todos juntos —dice Gheco—. Pedilos **de a uno**.
              """,
              sugiere="`iter(lista)` te da un **iterador**: algo que sabe por dónde va. Cada `next(it)` te da el siguiente. Un `for` hace eso por dentro.",
              desafio="Pedí los dos primeros enemigos de a uno.",
              inicial='''
                  enemigos = ["slime", "murciélago", "orco"]
                  it = iter(enemigos)
                  print(___(it))
                  print(___(it))
              ''',
              solucion='''
                  enemigos = ["slime", "murciélago", "orco"]
                  it = iter(enemigos)
                  print(next(it))
                  print(next(it))
              ''',
              solucion_txt="`next(it)` las dos veces.",
              al_superar="Un slime y un murciélago salen del portal, uno detrás del otro, y los esperás tranquila. Tilo, a tu lado, ya tiene la pértiga lista para el tercero.",
              imagen=["El primer piso de la Torre del Reloj: engranajes gigantes en las paredes y un portal de luz en el centro.",
                      "Un slime y un murciélago salen del portal en fila.",
                      "Mia con el pergamino; Tilo con la pértiga del farol verde en alto."]),
            m(id="R03-N01-P2", titulo="El portal que se pausa",
              lugar=P1, personajes="Mia, Gheco, Tilo",
              carta="Generador | def portal(): ... yield valor · entrega uno y se PAUSA · recuerda sus variables",
              recompensa="xp 10, oro 10",
              escena="""
                  —Este portal funciona como un hechizo que se **pausa** —dice Gheco—. Entrega un enemigo, se queda quieto, y cuando le pedís otro, sigue desde donde estaba.
              """,
              sugiere="Una función con `yield` es un **generador**. Llamarla no ejecuta nada: cada vuelta del `for` corre hasta el próximo `yield`, entrega ese valor y se pausa ahí.",
              desafio="Hacé que el portal **entregue** cada oleada en lugar de terminar.",
              inicial='''
                  def oleadas(n):
                      while n > 0:
                          ___ n
                          n -= 1

                  for oleada in oleadas(3):
                      print(f"Oleada {oleada}")
                  print("El portal descansa")
              ''',
              solucion='''
                  def oleadas(n):
                      while n > 0:
                          yield n
                          n -= 1

                  for oleada in oleadas(3):
                      print(f"Oleada {oleada}")
                  print("El portal descansa")
              ''',
              solucion_txt="`yield n`.",
              al_superar="Tres oleadas, cuenta regresiva, y el portal se apaga un momento. Tilo se sienta en el piso, resoplando.",
              imagen=["El portal se apaga un instante; en el aire, una cuenta regresiva de luz: 3, 2, 1.",
                      "Tilo sentado en el piso, resoplando; Gheco le abanica la cara con la cola."]),
            m(id="R03-N01-P3", titulo="Quizás infinitos",
              lugar=P1, personajes="Mia, Gheco, Tilo",
              carta="islice | while True: yield ... · itertools.islice(gen, 5) toma solo 5 · lo infinito no llena la memoria",
              recompensa="xp 15, oro 15",
              escena="""
                  El portal se vuelve a encender, y esta vez no para.
                  —¿Cuántos son? —pregunta Tilo.
                  —Quizás infinitos —dice Gheco—. No importa: tomá **los que necesitás**.
              """,
              sugiere="Un generador puede no terminar nunca (`while True:`). No pasa nada mientras **consumas solo lo necesario**: `itertools.islice(gen, 5)` toma los primeros 5.",
              desafio="Tomá solo los primeros 5 del portal infinito.",
              inicial='''
                  from itertools import islice

                  def portal():
                      while True:
                          yield "slime"
                          yield "murciélago"

                  for enemigo in ___(portal(), 5):
                      print(enemigo)
              ''',
              solucion='''
                  from itertools import islice

                  def portal():
                      while True:
                          yield "slime"
                          yield "murciélago"

                  for enemigo in islice(portal(), 5):
                      print(enemigo)
              ''',
              solucion_txt="`islice(portal(), 5)`.",
              al_superar="Cinco y listo. El portal sigue echando enemigos, pero vos ya no le pedís más, y se quedan del otro lado, esperando.",
              imagen=["Un portal que sigue brillando, con una fila infinita de siluetas esperando del otro lado.",
                      "Cinco enemigos vencidos en el piso, ordenados como fichas."]),
            m(id="R03-N01-P4", titulo="Sumar sin guardar",
              lugar=P1, personajes="Mia, Gheco, Tilo",
              carta="Expresión generadora | sum(v for v in vidas if v > 20) · como una comprehension, pero sin armar la lista",
              recompensa="xp 10, oro 10",
              escena="""
                  —Necesito saber cuánta vida tienen los fuertes —dice Tilo—, los de más de 20. Pero no me hagas otra lista, que ya no me entra nada en la cabeza.
              """,
              sugiere="Una **expresión generadora** es una comprehension con paréntesis: `(v for v in vidas)`. No arma la lista; va dando los valores de a uno. Adentro de `sum`, `max` o `any` ni siquiera hacen falta los paréntesis extra.",
              desafio="Sumá solo las vidas de más de 20, sin armar una lista.",
              inicial='''
                  vidas = [12, 30, 8, 45, 25]
                  total = sum(___)
                  print(f"Vida de los fuertes: {total}")
              ''',
              solucion='''
                  vidas = [12, 30, 8, 45, 25]
                  total = sum(v for v in vidas if v > 20)
                  print(f"Vida de los fuertes: {total}")
              ''',
              solucion_txt="`sum(v for v in vidas if v > 20)`.",
              al_superar="—Cien —dice Tilo—. Eso sí me entra.",
              imagen=["Tres siluetas fuertes iluminadas entre cinco; sobre ellas, el número 100.",
                      "Tilo se rasca la cabeza, contento."]),
            m(id="R03-N01-P5", titulo="Se gastan",
              lugar=P1, personajes="Mia, Gheco, Tilo, Maese Horas",
              carta="Se gastan | un generador se recorre UNA vez · para usarlo dos veces: list(gen)",
              recompensa="xp 15, oro 15",
              escena="""
                  Querés sumar las vidas y después buscar la más alta, con el mismo generador. La suma sale bien… y el máximo explota: `ValueError`, la secuencia está **vacía**.
                  Desde una escalera, un señor bajito, con lupa de relojero en un ojo, se ríe.
              """,
              sugiere="Un generador se **gasta**: después de recorrerlo, queda vacío. Si necesitás los valores dos veces, guardalos en una **lista** (`list(...)` o una comprehension con corchetes).",
              desafio="Arreglalo para poder usar las vidas dos veces.",
              inicial='''
                  vidas = (v * 2 for v in [10, 25, 15])
                  print(f"Total: {sum(vidas)}")
                  print(f"La más alta: {max(vidas)}")
              ''',
              solucion='''
                  vidas = [v * 2 for v in [10, 25, 15]]
                  print(f"Total: {sum(vidas)}")
                  print(f"La más alta: {max(vidas)}")
              ''',
              solucion_txt="Usar corchetes (una lista) en lugar de paréntesis: `vidas = [v * 2 for v in [10, 25, 15]]`.",
              al_superar="""
                  —Bien visto —dice el señor de la lupa, y baja de la escalera—. **Maese Horas**, relojero. Subí cuando puedas: el gran reloj atrasa desde que se perdió una pieza, y vos tenés cara de saber buscar.
              """,
              imagen=["Maese Horas, bajito, con lupa de relojero en un ojo y delantal lleno de herramientas, baja de una escalera de bronce.",
                      "Mia lo mira desde abajo; en el pergamino, `list(...)` brilla en verde.",
                      "Arriba, el gran reloj de la Torre, con una aguja torcida."]),
        ],
    },
    {
        "titulo": "R03-N02 · Programación funcional e itertools",
        "misiones": [
            m(id="R03-N02-P1", titulo="Ordenalas por peso",
              lugar=P2, personajes="Mia, Gheco, Maese Horas",
              carta="sorted con key | sorted(piezas, key=lambda p: p[1]) · lambda: una función de una línea",
              recompensa="xp 10, oro 10",
              escena="""
                  El segundo piso es un taller con cientos de piezas sobre una mesa. Maese Horas no las toca.
                  —Ordenalas por peso —dice, y espera.
              """,
              sugiere="`sorted(datos, key=f)` ordena según lo que devuelve `f` para cada elemento. `lambda p: p[1]` es una función sin nombre que recibe `p` y devuelve `p[1]`.",
              desafio="Ordená las piezas por peso (el segundo valor).",
              inicial='''
                  piezas = [("engranaje", 12), ("resorte", 3), ("péndulo", 40), ("tornillo", 1)]
                  for nombre, peso in sorted(piezas, key=___):
                      print(f"{nombre}: {peso}")
              ''',
              solucion='''
                  piezas = [("engranaje", 12), ("resorte", 3), ("péndulo", 40), ("tornillo", 1)]
                  for nombre, peso in sorted(piezas, key=lambda p: p[1]):
                      print(f"{nombre}: {peso}")
              ''',
              solucion_txt="`key=lambda p: p[1]`.",
              al_superar="Las piezas se acomodan solas sobre la mesa, de la más liviana a la más pesada. Maese Horas asiente. —No dije **cómo**. Dije **qué**.",
              imagen=["Un taller de relojería con cientos de piezas de bronce sobre una mesa larga.",
                      "Las piezas se ordenan solas en fila, de la más chica a la más grande.",
                      "Maese Horas, con los brazos cruzados, satisfecho."]),
            m(id="R03-N02-P2", titulo="Quedate con las doradas",
              lugar=P2, personajes="Mia, Gheco, Maese Horas",
              carta="filter y map | filter(f, datos) se queda con los que cumplen · map(f, datos) aplica f a cada uno",
              recompensa="xp 10, oro 10",
              escena="—Ahora quedate solo con las doradas —dice Maese Horas—, y decime sus nombres en mayúsculas, que no veo bien.",
              sugiere="`filter(f, datos)` deja pasar los elementos para los que `f` da `True`. `map(f, datos)` aplica `f` a cada uno. Los dos son perezosos, como los generadores.",
              desafio="Completá el filtro.",
              inicial='''
                  piezas = [
                      {"nombre": "rueda", "color": "dorada"},
                      {"nombre": "eje", "color": "gris"},
                      {"nombre": "aguja", "color": "dorada"},
                  ]
                  doradas = ___(lambda p: p["color"] == "dorada", piezas)
                  nombres = map(lambda p: p["nombre"].upper(), doradas)
                  print(list(nombres))
              ''',
              solucion='''
                  piezas = [
                      {"nombre": "rueda", "color": "dorada"},
                      {"nombre": "eje", "color": "gris"},
                      {"nombre": "aguja", "color": "dorada"},
                  ]
                  doradas = filter(lambda p: p["color"] == "dorada", piezas)
                  nombres = map(lambda p: p["nombre"].upper(), doradas)
                  print(list(nombres))
              ''',
              solucion_txt="`filter`.",
              al_superar="Las piezas grises se apartan y las doradas brillan solas. —Rueda y aguja —lee Maese Horas—. Ahora sí veo.",
              imagen=["Sobre la mesa, las piezas grises se corren a un costado; las doradas brillan.",
                      "Maese Horas se acerca la lupa, sonriendo."]),
            m(id="R03-N02-P3", titulo="Por tamaño y después por peso",
              lugar=P2, personajes="Mia, Gheco, Maese Horas",
              carta="Varias claves | key=lambda p: (p[\"tamaño\"], -p[\"peso\"]) · el - invierte un número",
              recompensa="xp 10, oro 10",
              escena="—Por tamaño —dice el relojero—. Y entre las del mismo tamaño, **la más pesada primero**.",
              sugiere="Si `key` devuelve una **tupla**, se ordena por el primer valor y, en los empates, por el segundo. Para invertir un número, ponele un `-` adelante.",
              desafio="Escribí la clave con los dos criterios.",
              inicial='''
                  piezas = [
                      {"nombre": "a", "tamaño": 2, "peso": 5},
                      {"nombre": "b", "tamaño": 1, "peso": 3},
                      {"nombre": "c", "tamaño": 2, "peso": 9},
                      {"nombre": "d", "tamaño": 1, "peso": 7},
                  ]
                  orden = sorted(piezas, key=lambda p: ___)
                  print([p["nombre"] for p in orden])
              ''',
              solucion='''
                  piezas = [
                      {"nombre": "a", "tamaño": 2, "peso": 5},
                      {"nombre": "b", "tamaño": 1, "peso": 3},
                      {"nombre": "c", "tamaño": 2, "peso": 9},
                      {"nombre": "d", "tamaño": 1, "peso": 7},
                  ]
                  orden = sorted(piezas, key=lambda p: (p["tamaño"], -p["peso"]))
                  print([p["nombre"] for p in orden])
              ''',
              solucion_txt="`(p[\"tamaño\"], -p[\"peso\"])`.",
              al_superar="Las piezas forman dos filas perfectas. Maese Horas silba bajito: la primera vez que alguien lo hace al primer intento esta semana.",
              imagen=["Dos filas de piezas de relojería, ordenadas por tamaño y por peso.",
                      "Maese Horas silba, con las manos en los bolsillos del delantal."]),
            m(id="R03-N02-P4", titulo="Agrupalas",
              lugar=P2, personajes="Mia, Gheco, Maese Horas",
              criatura="ogro",
              carta="groupby | itertools.groupby(datos, key) · agrupa los CONSECUTIVOS · ¡ordená antes!",
              recompensa="xp 15, oro 15",
              escena="""
                  —Agrupalas por tipo y contalas. —Lo hacés… y aparecen **dos** grupos de resortes. No hay error, pero está mal: un **ogro**.
              """,
              sugiere="`groupby` solo junta los elementos **consecutivos** con la misma clave. Si los datos no están ordenados por esa clave, el mismo grupo aparece varias veces. Ordená **antes** con la misma `key`.",
              desafio="Ordená antes de agrupar.",
              inicial='''
                  from itertools import groupby

                  piezas = ["resorte", "engranaje", "resorte", "aguja", "engranaje"]
                  for tipo, grupo in groupby(piezas):
                      print(f"{tipo}: {len(list(grupo))}")
              ''',
              solucion='''
                  from itertools import groupby

                  piezas = ["resorte", "engranaje", "resorte", "aguja", "engranaje"]
                  for tipo, grupo in groupby(sorted(piezas)):
                      print(f"{tipo}: {len(list(grupo))}")
              ''',
              solucion_txt="`groupby(sorted(piezas))`.",
              al_superar="Tres montoncitos, uno por tipo. El ogro se queda sin lugar donde esconderse.",
              imagen=["Tres montones prolijos de piezas: agujas, engranajes y resortes, con su número encima.",
                      "Un ogro chiquito que se va, sin lugar donde esconderse."]),
            m(id="R03-N02-P5", titulo="Todas las parejas",
              lugar=P2, personajes="Mia, Gheco, Maese Horas",
              carta="combinations | itertools.combinations(datos, 2) · todas las parejas sin repetir",
              recompensa="xp 10, oro 10",
              escena="—Tengo cuatro engranajes —dice Maese Horas—. Quiero probar cada pareja una vez, sin repetir. ¿Cuáles encajan, porque suman 10 dientes?",
              sugiere="`combinations(datos, 2)` da todas las **parejas** posibles, sin repetir y sin importar el orden.",
              desafio="Recorré todas las parejas.",
              inicial='''
                  from itertools import combinations

                  dientes = [3, 7, 4, 6]
                  for a, b in ___(dientes, 2):
                      if a + b == 10:
                          print(f"{a} y {b} encajan")
              ''',
              solucion='''
                  from itertools import combinations

                  dientes = [3, 7, 4, 6]
                  for a, b in combinations(dientes, 2):
                      if a + b == 10:
                          print(f"{a} y {b} encajan")
              ''',
              solucion_txt="`combinations(dientes, 2)`.",
              al_superar="Dos parejas de engranajes encajan y giran juntas, con un clic suave.",
              imagen=["Dos parejas de engranajes de bronce que encajan y giran juntas.",
                      "Maese Horas escucha el clic con el oído pegado a la mesa."]),
            m(id="R03-N02-P6", titulo="La que brilla distinto",
              lugar=P2, personajes="Mia, Gheco, Maese Horas",
              carta="max con key | max(piezas, key=lambda p: p[\"brillo\"]) · el que tiene el valor más grande",
              recompensa="xp 15, oro 15",
              item="Pieza de Vitral",
              escena="""
                  Entre todas las piezas hay una que **brilla distinto**, con colores. Maese Horas no la ve: tiene la lupa sucia.
              """,
              sugiere="`max(datos, key=f)` devuelve el **elemento** cuyo `f` es el más grande (no el número, el elemento entero).",
              desafio="Encontrá la pieza que más brilla.",
              inicial='''
                  piezas = [
                      {"nombre": "rueda dorada", "brillo": 6},
                      {"nombre": "plomo y vidrio de colores", "brillo": 9},
                      {"nombre": "eje gris", "brillo": 1},
                  ]
                  pieza = max(piezas, key=___)
                  print(pieza["nombre"])
              ''',
              solucion='''
                  piezas = [
                      {"nombre": "rueda dorada", "brillo": 6},
                      {"nombre": "plomo y vidrio de colores", "brillo": 9},
                      {"nombre": "eje gris", "brillo": 1},
                  ]
                  pieza = max(piezas, key=lambda p: p["brillo"])
                  print(pieza["nombre"])
              ''',
              solucion_txt="`key=lambda p: p[\"brillo\"]`.",
              al_superar="""
                  Una pieza de **plomo y vidrio de colores**. No es de ningún reloj. Es… un pedacito de **vitral**. Maese Horas se limpia la lupa y la mira mucho rato.
                  —Esto no lo hice yo. Guardala vos.
              """,
              imagen=["Mia sostiene a contraluz una pieza de plomo y vidrio de colores: un pedacito de vitral.",
                      "Los colores del vitral se proyectan sobre su cara y sobre Gheco.",
                      "Maese Horas, serio, con la lupa recién limpia."]),
        ],
    },
    {
        "titulo": "R03-N03 · Closures y decoradores",
        "misiones": [
            m(id="R03-N03-P1", titulo="La función que recuerda",
              lugar=P3, personajes="Mia, Gheco, Maese Horas",
              carta="Closure | una función adentro de otra recuerda sus variables · nonlocal para cambiarlas",
              recompensa="xp 10, oro 10",
              escena="""
                  En el tercer piso, cada reloj tiene una cuerda que **recuerda** cuántas vueltas le dieron, aunque nadie la mire.
                  —Hacé una igual —dice Maese Horas.
              """,
              sugiere="Una función definida **adentro** de otra recuerda las variables de la de afuera, aunque esa ya haya terminado. Para **cambiarlas** (no solo leerlas), declaralas con `nonlocal`.",
              desafio="Dejá que `girar` cambie las vueltas de afuera.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`nonlocal vueltas`.",
              al_superar="El relojito de práctica hace tres tics y se queda contando, satisfecho.",
              imagen=["Un relojito de práctica con la cuerda girando; sobre él, el número 3.",
                      "Relojes de todos los tamaños en las paredes del tercer piso."]),
            m(id="R03-N03-P2", titulo="La pieza que va encima",
              lugar=P3, personajes="Mia, Gheco, Maese Horas",
              carta="Decorador | def anunciar(func): def envoltura(*args): ... return envoltura · @anunciar = f = anunciar(f)",
              recompensa="xp 10, oro 10",
              escena="—No se desarma un reloj para mejorarlo —dice Maese Horas—. Se le pone una pieza **encima**. Esta hace «tic» antes de cada movimiento.",
              sugiere="Un **decorador** recibe una función y devuelve otra que la **envuelve**. Escribir `@anunciar` arriba de `def mover` es lo mismo que `mover = anunciar(mover)`.",
              desafio="Ponele la pieza encima a `mover`.",
              inicial='''
                  def anunciar(func):
                      def envoltura(*args):
                          print("tic")
                          return func(*args)
                      return envoltura

                  ___
                  def mover(aguja):
                      print(f"se mueve la aguja {aguja}")

                  mover("de las horas")
              ''',
              solucion='''
                  def anunciar(func):
                      def envoltura(*args):
                          print("tic")
                          return func(*args)
                      return envoltura

                  @anunciar
                  def mover(aguja):
                      print(f"se mueve la aguja {aguja}")

                  mover("de las horas")
              ''',
              solucion_txt="`@anunciar`.",
              al_superar="«Tic», y la aguja se mueve. El reloj es el mismo; ahora hace algo más.",
              imagen=["Una pieza nueva de bronce montada encima de un reloj; un «tic» de luz sale de ella.",
                      "Maese Horas le señala a Mia cómo encaja."]),
            m(id="R03-N03-P3", titulo="La pieza que se come el resultado",
              lugar=P3, personajes="Mia, Gheco, Maese Horas",
              criatura="ogro",
              carta="return resultado | la envoltura tiene que DEVOLVER lo que devuelve func · si no, da None",
              recompensa="xp 10, oro 10",
              escena="""
                  Le ponés la pieza al reloj que da la hora, y ahora la hora es `None`. Ningún error, todo corre… un **ogro**.
              """,
              sugiere="La envoltura llama a la función original, pero si **no devuelve** su resultado, la función decorada devuelve `None`. Guardalo y devolvelo: `resultado = func(*args)` y `return resultado`.",
              desafio="Que la envoltura devuelva lo que devuelve la función.",
              inicial='''
                  def anunciar(func):
                      def envoltura(*args):
                          print("tic")
                          func(*args)
                      return envoltura

                  @anunciar
                  def hora():
                      return "las siete"

                  print(f"Son {hora()}")
              ''',
              solucion='''
                  def anunciar(func):
                      def envoltura(*args):
                          print("tic")
                          return func(*args)
                      return envoltura

                  @anunciar
                  def hora():
                      return "las siete"

                  print(f"Son {hora()}")
              ''',
              solucion_txt="`return func(*args)` en la envoltura.",
              al_superar="«Son las siete», dice el reloj, y el ogro se va sin hacer ruido, como vino.",
              imagen=["Un reloj de pared que pasa de mostrar `None` a «las siete».",
                      "Un ogro que se va de puntillas."]),
            m(id="R03-N03-P4", titulo="Que no pierda su nombre",
              lugar=P3, personajes="Mia, Gheco, Maese Horas",
              carta="functools.wraps | @functools.wraps(func) sobre la envoltura · conserva el nombre y el docstring",
              recompensa="xp 10, oro 10",
              escena="—Ojo —dice Maese Horas—. Le pusiste la pieza encima y ahora el reloj **no sabe cómo se llama**. Dice «envoltura».",
              sugiere="La envoltura reemplaza a la función, con su nombre y todo. `@functools.wraps(func)` arriba de la envoltura copia el nombre y el docstring de la original. Ponelo siempre.",
              desafio="Que la función decorada conserve su nombre.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`@functools.wraps(func)`.",
              al_superar="El reloj recupera su nombre en la plaquita de bronce: «girar».",
              imagen=["Una plaquita de bronce en un reloj donde «envoltura» se borra y aparece «girar»."]),
            m(id="R03-N03-P5", titulo="La memoria del oráculo",
              lugar=P3, personajes="Mia, Gheco, Maese Horas",
              carta="lru_cache | @functools.lru_cache · guarda resultados por argumentos · la recursión lenta se vuelve instantánea",
              recompensa="xp 15, oro 20",
              escena="""
                  En una vitrina, el **oráculo del reloj** calcula las fases de la luna con una cuenta recursiva. Para la fase 25 hace casi un cuarto de millón de cuentas, y tarda tanto que el reloj se atrasa.
              """,
              sugiere="`@functools.lru_cache` es un decorador que ya viene con Python: **recuerda** el resultado para cada argumento. La segunda vez que se pide lo mismo, contesta sin calcular.",
              desafio="Ponele memoria al oráculo y mirá cuántas cuentas hace.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`@functools.lru_cache`.",
              al_superar="""
                  Veintiséis cuentas en vez de doscientas cuarenta mil. El oráculo contesta al instante.
                  Y al abrir la vitrina, ves un hueco con una forma conocida. Sacás la **pieza de vitral** de la mochila… y **encaja justo**. Maese Horas se queda mudo.
                  —Esta pieza la puso alguien hace mucho. Alguien que arregló este reloj antes que nosotros.
              """,
              imagen=["Una vitrina con un oráculo mecánico de la luna; en su centro, la pieza de vitral encaja y proyecta colores.",
                      "Mia con la mano todavía en la vitrina; Maese Horas, boquiabierto.",
                      "Gheco ilumina la escena con la cola."]),
        ],
    },
    {
        "titulo": "R03-N04 · Anotaciones de tipos y pruebas",
        "misiones": [
            m(id="R03-N04-P1", titulo="El plano dice qué va",
              lugar=P4, personajes="Mia, Gheco, Maese Horas",
              carta="Anotaciones | def curar(vida: int, cantidad: int) -> int: · son para las personas y el editor · Python no las verifica",
              recompensa="xp 10, oro 10",
              escena="""
                  En el cuarto piso trabaja el **Gremio de Artífices**. Sus planos no dicen «acá va una pieza»: dicen **qué clase** de pieza va.
                  —Tu hechizo también puede decir qué espera y qué devuelve —dice Gheco.
              """,
              sugiere="`vida: int` anota que el parámetro **debería** ser un entero, y `-> int`, que la función devuelve un entero. Python no lo comprueba al ejecutar: es para quien lee el código y para el editor.",
              desafio="Anotá lo que devuelve `curar`.",
              inicial='''
                  def curar(vida: int, cantidad: int) -> ___:
                      return min(100, vida + cantidad)

                  print(curar(80, 30))
                  print(curar.__annotations__["return"].__name__)
              ''',
              solucion='''
                  def curar(vida: int, cantidad: int) -> int:
                      return min(100, vida + cantidad)

                  print(curar(80, 30))
                  print(curar.__annotations__["return"].__name__)
              ''',
              solucion_txt="`-> int`.",
              al_superar="El plano de tu hechizo queda colgado en la pared del Gremio, al lado de los de bronce y acero.",
              imagen=["El Gremio de Artífices: mesas de dibujo con planos de relojes, cada pieza con una etiqueta de tipo.",
                      "El plano del hechizo de Mia, colgado en la pared, con `-> int` en dorado."]),
            m(id="R03-N04-P2", titulo="Puede que no esté",
              lugar=P4, personajes="Mia, Gheco, una artífice",
              carta="Tipos compuestos | dict[str, int] · list[str] · int | None: un entero o nada",
              recompensa="xp 10, oro 10",
              escena="Una artífice busca precios en su lista. A veces la pieza no está, y el plano tiene que decirlo: devuelve un número… **o nada**.",
              sugiere="Las anotaciones pueden describir colecciones: `dict[str, int]` es un diccionario de texto a entero. Y `int | None` dice «un entero **o** `None`».",
              desafio="Completá lo que devuelve `precio`.",
              inicial='''
                  def precio(lista: dict[str, int], pieza: str) -> ___ | None:
                      return lista.get(pieza)

                  lista = {"engranaje": 30, "resorte": 5}
                  print(precio(lista, "engranaje"))
                  print(precio(lista, "péndulo"))
              ''',
              solucion='''
                  def precio(lista: dict[str, int], pieza: str) -> int | None:
                      return lista.get(pieza)

                  lista = {"engranaje": 30, "resorte": 5}
                  print(precio(lista, "engranaje"))
                  print(precio(lista, "péndulo"))
              ''',
              solucion_txt="`-> int | None`.",
              al_superar="—Ahora el que use mi lista ya sabe que tiene que fijarse si vino `None` —dice la artífice—. Me ahorraste diez preguntas por día.",
              imagen=["Una artífice con gafas de aumento y guantes de cuero revisa una lista de precios.",
                      "Sobre la lista, el plano: `int | None`."]),
            m(id="R03-N04-P3", titulo="Probar en el taller",
              lugar=P4, personajes="Mia, Gheco, Maese Horas",
              criatura="ogro",
              carta="assert | assert curar(80, 30) == 100, \"mensaje\" · no hace nada si se cumple · si no: AssertionError",
              recompensa="xp 15, oro 15",
              escena="""
                  —Antes de montar un reloj en la plaza, se prueba acá —dice Maese Horas—. Si falla, que falle en el taller.
                  Las pruebas de tu hechizo de curar explotan: `AssertionError`. Había un **ogro** escondido.
              """,
              sugiere="`assert condicion, \"mensaje\"` no hace nada si se cumple y lanza `AssertionError` si no. Una **prueba** usa tu función con datos que conocés y comprueba el resultado. Cuando falla, arreglá la **función**, no la prueba.",
              desafio="Arreglá `curar` para que pasen las pruebas: la vida nunca supera 100.",
              inicial='''
                  def curar(vida, cantidad):
                      return vida + cantidad

                  assert curar(50, 20) == 70, "caso normal"
                  assert curar(80, 30) == 100, "no tiene que pasar de 100"
                  assert curar(100, 0) == 100, "borde: ya está llena"
                  print("Todas las pruebas pasaron")
              ''',
              solucion='''
                  def curar(vida, cantidad):
                      return min(100, vida + cantidad)

                  assert curar(50, 20) == 70, "caso normal"
                  assert curar(80, 30) == 100, "no tiene que pasar de 100"
                  assert curar(100, 0) == 100, "borde: ya está llena"
                  print("Todas las pruebas pasaron")
              ''',
              solucion_txt="`return min(100, vida + cantidad)`.",
              al_superar="Tres luces verdes en la mesa de pruebas. El ogro no llegó a la plaza.",
              imagen=["Una mesa de pruebas con tres luces verdes encendidas.",
                      "Maese Horas le da una palmada en el hombro a Mia."]),
            m(id="R03-N04-P4", titulo="Que falle bien",
              lugar=P4, personajes="Mia, Gheco, Maese Horas",
              carta="Probar errores | try: f(malo) · except ValueError: bien · else: la prueba falla",
              recompensa="xp 10, oro 10",
              escena="—Una buena prueba también revisa que tu hechizo **se queje** cuando le dan algo imposible —dice el relojero—. Una pieza de peso negativo no existe.",
              sugiere="Para probar que una función **lanza** un error: llamala con un dato malo dentro de un `try`. Si cae en el `except`, la prueba pasa; si no lanzó nada, cae en el `else`, y ahí la prueba falla.",
              desafio="Hacé que `pesar` lance `ValueError` con un peso negativo.",
              inicial='''
                  def pesar(gramos):
                      return f"{gramos} g"

                  assert pesar(12) == "12 g"
                  try:
                      pesar(-3)
                  except ValueError:
                      print("Se queja con -3: bien")
                  else:
                      raise AssertionError("tendría que lanzar ValueError")
              ''',
              solucion='''
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
              ''',
              solucion_txt="Agregar al principio de `pesar`: `if gramos < 0: raise ValueError(\"no hay pesos negativos\")`.",
              solucion_es_codigo=True,
              al_superar="La balanza del taller rechaza la pieza imposible con un zumbido. Maese Horas lo anota en la libreta de las pruebas.",
              imagen=["Una balanza de bronce que rechaza una pieza fantasma con un zumbido rojo.",
                      "Maese Horas anota en una libreta gastada."]),
            m(id="R03-N04-P5", titulo="La batería del Gremio",
              lugar=P4, personajes="Mia, Gheco, Maese Horas, la maestra del Gremio",
              carta="Batería de pruebas | casos = [(entrada, esperado), ...] · el normal, los bordes y los errores",
              recompensa="xp 15, oro 20",
              item="Escudo de las Aserciones",
              escena="""
                  La maestra del Gremio te deja probar su conversor de horas: de minutos a «h:mm». Te da una lista de casos, y quiere que los pruebes **todos de una**.
              """,
              sugiere="Una **batería** es una lista de casos `(entrada, esperado)` que se recorre con un `for`, con un `assert` por caso. Incluí el caso normal y los **bordes**: cero, justo una hora, un número grande.",
              desafio="Completá el `assert` de cada caso.",
              inicial='''
                  def a_horas(minutos: int) -> str:
                      return f"{minutos // 60}:{minutos % 60:02}"

                  casos = [(75, "1:15"), (0, "0:00"), (60, "1:00"), (605, "10:05")]
                  for entrada, esperado in casos:
                      assert ___, f"{entrada} tendría que dar {esperado}"
                  print(f"{len(casos)} pruebas: todas bien")
              ''',
              solucion='''
                  def a_horas(minutos: int) -> str:
                      return f"{minutos // 60}:{minutos % 60:02}"

                  casos = [(75, "1:15"), (0, "0:00"), (60, "1:00"), (605, "10:05")]
                  for entrada, esperado in casos:
                      assert a_horas(entrada) == esperado, f"{entrada} tendría que dar {esperado}"
                  print(f"{len(casos)} pruebas: todas bien")
              ''',
              solucion_txt="`assert a_horas(entrada) == esperado, ...`.",
              al_superar="""
                  Cuatro de cuatro. La maestra del Gremio te entrega un escudo redondo, de bronce, con una marca de verificación grabada: el **Escudo de las Aserciones**.
                  —Lo que se prueba, aguanta.
                  Arriba se escucha el ruido de una cocina con mil cosas al fuego.
              """,
              imagen=["La maestra del Gremio, mayor, con delantal de cuero, entrega un escudo de bronce con una marca de verificación grabada.",
                      "Mia lo recibe con las dos manos.",
                      "Por la escalera de arriba baja vapor y olor a pan."]),
        ],
    },
    {
        "titulo": "R03-N05 · asyncio: esperar sin frenar",
        "misiones": [
            m(id="R03-N05-P1", titulo="Esperar sin frenar",
              lugar=P5, personajes="Mia, Gheco, la cocinera de la Torre",
              carta="async y await | async def preparar(): · await asyncio.sleep(1) · asyncio.run(main())",
              recompensa="xp 10, oro 10",
              escena="""
                  La cocina de la Torre es un caos ordenado: ollas, hornos y una sola cocinera, de brazos fuertes y pañuelo en la cabeza.
                  —No me quedo mirando cómo hierve el agua —dice sin darse vuelta—. Pongo la olla y **espero sin frenar**.
              """,
              sugiere="`async def` define una **corrutina**. Adentro, `await` espera algo (como `asyncio.sleep`) **dejando que otras tareas avancen**. Todo arranca con `asyncio.run(...)`.",
              desafio="Esperá a que hierva la sopa.",
              inicial='''
                  import asyncio

                  async def preparar(plato, segundos):
                      ___ asyncio.sleep(segundos)
                      return f"{plato} lista"

                  print(asyncio.run(preparar("sopa", 0.01)))
              ''',
              solucion='''
                  import asyncio

                  async def preparar(plato, segundos):
                      await asyncio.sleep(segundos)
                      return f"{plato} lista"

                  print(asyncio.run(preparar("sopa", 0.01)))
              ''',
              solucion_txt="`await asyncio.sleep(segundos)`.",
              al_superar="—Sopa lista —dice la cocinera, y por fin te mira—. Pero una sola cosa no es un banquete, chiquita.",
              imagen=["La cocina de la Torre: ollas humeantes, hornos de piedra y engranajes en el techo.",
                      "La cocinera de pañuelo en la cabeza revuelve una olla sin mirar.",
                      "Mia con el pergamino, `await` brillando en verde."]),
            m(id="R03-N05-P2", titulo="Tres cosas a la vez",
              lugar=P5, personajes="Mia, Gheco, la cocinera de la Torre",
              carta="gather | await asyncio.gather(a(), b(), c()) · corren a la vez · devuelve en el orden en que se pidieron",
              recompensa="xp 10, oro 10",
              escena="—Sopa, pan y té —dice la cocinera—. **A la vez**. Una sola persona, muchas esperas.",
              sugiere="`await asyncio.gather(a(), b(), c())` corre las tres corrutinas a la vez y devuelve sus resultados **en el orden en que las pediste**, aunque terminen en otro orden.",
              desafio="Prepará los tres platos a la vez.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`asyncio.gather`.",
              al_superar="El pan sale primero, después el té, al final la sopa. Pero en la mesa quedan en el orden que pediste. La cocinera se seca las manos, conforme.",
              imagen=["Tres platos que terminan a destiempo: pan, té, sopa, cada uno con un reloj de vapor encima.",
                      "La mesa servida en orden: sopa, pan y té."]),
            m(id="R03-N05-P3", titulo="El asado que no llega",
              lugar=P5, personajes="Mia, Gheco, la cocinera de la Torre",
              carta="wait_for | await asyncio.wait_for(tarea(), timeout=2) · si tarda más: TimeoutError",
              recompensa="xp 10, oro 10",
              escena="—El asado tarda una eternidad —se queja la cocinera—. Si no está a tiempo, se sirve sin asado. No espero para siempre.",
              sugiere="`await asyncio.wait_for(tarea(), timeout=s)` espera como mucho `s` segundos. Si se pasa, cancela la tarea y lanza `TimeoutError`.",
              desafio="Ponele un límite de tiempo al asado.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`asyncio.wait_for`.",
              al_superar="El banquete se sirve a tiempo. El asado, cuando esté, será para la cena.",
              imagen=["Un horno con un asado que sigue cocinándose; un relojito de arena se vacía encima.",
                      "La cocinera sirve la mesa sin esperar."]),
            m(id="R03-N05-P4", titulo="El candado de la despensa",
              lugar=P5, personajes="Mia, Gheco, la cocinera de la Torre, Tilo",
              criatura="troll",
              carta="asyncio.Lock | async with candado: · de a una tarea por vez · evita que se pisen",
              recompensa="xp 15, oro 15",
              escena="""
                  Vos y Tilo cargan la despensa a la vez: cada uno lee cuántas bolsas hay, suma 10 y anota. Había 50; tendrían que quedar 70. El cartel dice **60**. Un **troll** se ríe desde atrás de los sacos.
              """,
              sugiere="Si dos tareas leen y modifican lo mismo con un `await` en el medio, se **pisan**: las dos leen 50. Con `async with candado:` (un `asyncio.Lock`), entran **de a una**.",
              desafio="Que cada uno cargue con el candado puesto.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`async with candado:`.",
              al_superar="Setenta, justas. El troll se queda sin bolsas que esconder y se va bajo la mesa, refunfuñando.",
              imagen=["Una despensa con sacos apilados y un candado de bronce en la puerta.",
                      "Mia y Tilo cargan sacos de a uno; el cartel dice 70.",
                      "Un troll refunfuña bajo la mesa."]),
            m(id="R03-N05-P5", titulo="Que un plato quemado no arruine el banquete",
              lugar=P5, personajes="Mia, Gheco, la cocinera de la Torre",
              carta="return_exceptions | gather(..., return_exceptions=True) · un error no cancela a los demás: queda como resultado",
              recompensa="xp 15, oro 15",
              escena="""
                  El pan se quema. Y como era parte del `gather`, el error cancela **todo** el banquete.
                  —Un plato quemado no es motivo para tirar los demás —dice la cocinera.
              """,
              sugiere="Con `return_exceptions=True`, si una de las tareas lanza un error, `gather` **no** cancela las demás: el error aparece en la lista de resultados, en su lugar.",
              desafio="Que el error del pan quede como resultado y el resto se sirva.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`return_exceptions=True`.",
              al_superar="""
                  Sopa y té a la mesa; el pan, al tacho. La cocinera te da una palmada que casi te tira al piso.
                  Y entonces, todo se queda **quieto**. El tic-tac de la Torre se apaga. **El gran reloj se paró del todo.** Y desde la cima llega un ruido de engranajes que despiertan.
              """,
              imagen=["La mesa servida con sopa y té; un pan quemado humea en un rincón.",
                      "Todos miran hacia arriba: el tic-tac se detuvo.",
                      "Por la escalera baja una luz roja y el ruido de engranajes enormes."]),
        ],
    },
    {
        "titulo": "R03-N06 · Rendimiento: medir antes de optimizar",
        "misiones": [
            m(id="R03-N06-P1", titulo="Unir runas",
              lugar=P6, personajes="Mia, Gheco, Maese Horas",
              carta="join | \"-\".join(partes) une una lista de textos · más rápido que += en un bucle",
              recompensa="xp 10, oro 10",
              escena="""
                  En el último piso, los aprendices discuten por qué atrasa el reloj. Uno pega las runas del registro de a una con `+=`, y el registro tarda una eternidad.
                  —Hay una forma de unirlas **de una sola vez** —dice Maese Horas.
              """,
              sugiere="`separador.join(lista)` une todos los textos de la lista con el separador en el medio, de una sola vez. Pegar con `+=` en un bucle crea un texto nuevo en cada vuelta.",
              desafio="Uní las runas con guiones.",
              inicial='''
                  runas = ["tic", "tac", "tic", "tac"]
                  registro = "-".___(runas)
                  print(registro)
              ''',
              solucion='''
                  runas = ["tic", "tac", "tic", "tac"]
                  registro = "-".join(runas)
                  print(registro)
              ''',
              solucion_txt="`\"-\".join(runas)`.",
              al_superar="El registro sale entero, de un tirón. El aprendiz que pegaba de a una se pone colorado.",
              imagen=["El último piso de la Torre: aprendices discutiendo frente al mecanismo del gran reloj, quieto.",
                      "Una tira de runas que se une de golpe: «tic-tac-tic-tac»."]),
            m(id="R03-N06-P2", titulo="¿Ya lo vi?",
              lugar=P6, personajes="Mia, Gheco, Maese Horas",
              carta="set | x in un_set es instantáneo · x in una_lista recorre todo · para «¿ya lo vi?», set",
              recompensa="xp 10, oro 10",
              escena="—Para cada pieza que revisás, te fijás si ya la viste —dice Maese Horas—. Si lo anotás en una lista, cada pregunta la recorre **entera**. Con miles de piezas…",
              sugiere="Preguntar `x in lista` revisa uno por uno. En un `set`, la pregunta es **instantánea**, tenga lo que tenga. Para «¿ya lo vi?», usá un `set`: se crea con `set()` y se le agrega con `.add(x)`.",
              desafio="Creá las piezas vistas como un `set`.",
              inicial='''
                  revisadas = ["eje", "rueda", "eje", "aguja", "rueda"]
                  vistas = ___()
                  for pieza in revisadas:
                      if pieza in vistas:
                          print(f"{pieza}: repetida")
                      vistas.add(pieza)
                  print(f"Distintas: {len(vistas)}")
              ''',
              solucion='''
                  revisadas = ["eje", "rueda", "eje", "aguja", "rueda"]
                  vistas = set()
                  for pieza in revisadas:
                      if pieza in vistas:
                          print(f"{pieza}: repetida")
                      vistas.add(pieza)
                  print(f"Distintas: {len(vistas)}")
              ''',
              solucion_txt="`vistas = set()`.",
              al_superar="Tres piezas distintas, dos repetidas. Maese Horas tacha «el péndulo» de la lista de sospechosos.",
              imagen=["Una pizarra con sospechosos: «péndulo», «engranajes», «aceite»; el péndulo, tachado."]),
            m(id="R03-N06-P3", titulo="La fila de las piezas",
              lugar=P6, personajes="Mia, Gheco, Maese Horas",
              carta="deque | from collections import deque · popleft() saca del principio al instante · pop(0) en una lista es lento",
              recompensa="xp 10, oro 10",
              escena="—Las piezas que llegan se revisan en orden: la primera que entra, la primera que sale —dice el relojero—. Sacarlas del principio de una lista obliga a correr todas las demás.",
              sugiere="Una `deque` es una fila de doble punta: `append` agrega al final y `popleft()` saca del principio, **sin** mover las demás. Se importa de `collections`.",
              desafio="Armá la fila con una `deque`.",
              inicial='''
                  from collections import deque

                  fila = ___(["resorte", "eje", "aguja"])
                  fila.append("rueda")
                  while fila:
                      print(f"Revisando: {fila.popleft()}")
              ''',
              solucion='''
                  from collections import deque

                  fila = deque(["resorte", "eje", "aguja"])
                  fila.append("rueda")
                  while fila:
                      print(f"Revisando: {fila.popleft()}")
              ''',
              solucion_txt="`deque([...])`.",
              al_superar="La fila avanza sin trabarse. Maese Horas tacha «los engranajes».",
              imagen=["Una cinta de piezas que avanza en fila hacia la mesa de revisión.",
                      "La pizarra de sospechosos: péndulo y engranajes, tachados."]),
            m(id="R03-N06-P4", titulo="Nunca adivines: medilo",
              lugar=P6, personajes="Mia, Gheco, Maese Horas",
              carta="Medir | contá o cronometrá cada parte · la culpable suele ser otra · Counter y max(..., key=...)",
              recompensa="xp 15, oro 15",
              escena="""
                  —Es el aceite —dice un aprendiz.
                  —No, es el péndulo —dice otro.
                  La Mia del principio habría leído todos los manuales. Ahora sacás un contador y **medís** cuántas veces se mueve cada pieza en una vuelta del reloj.
              """,
              sugiere="Antes de optimizar, **medí**. Un `Counter` cuenta cuántas veces aparece cada cosa, y `max(contador, key=contador.get)` da la que más aparece.",
              desafio="Encontrá la pieza que más trabaja.",
              inicial='''
                  from collections import Counter

                  movimientos = ["péndulo", "rueda", "corazón", "corazón", "eje", "corazón", "rueda", "corazón"]
                  conteo = Counter(movimientos)
                  culpable = max(conteo, key=___)
                  print(f"{culpable}: {conteo[culpable]} movimientos")
              ''',
              solucion='''
                  from collections import Counter

                  movimientos = ["péndulo", "rueda", "corazón", "corazón", "eje", "corazón", "rueda", "corazón"]
                  conteo = Counter(movimientos)
                  culpable = max(conteo, key=conteo.get)
                  print(f"{culpable}: {conteo[culpable]} movimientos")
              ''',
              solucion_txt="`key=conteo.get`.",
              al_superar="""
                  Ni el aceite ni el péndulo: una pieza que nadie nombró, **el corazón**, se mueve el doble que las demás. Maese Horas sonríe.
                  —Nunca adivines dónde se va el tiempo. Medilo.
              """,
              imagen=["Un gráfico de barras de luz sobre el mecanismo: la barra del «corazón» es el doble que las demás.",
                      "Los aprendices boquiabiertos; Maese Horas sonríe."]),
            m(id="R03-N06-P5", titulo="Del cuadrado a la línea",
              lugar=P6, personajes="Mia, Gheco, Maese Horas",
              carta="Complejidad | dos for anidados: O(n²) · con un set: O(n) · el doble de datos, el doble de pasos y no el cuádruple",
              recompensa="xp 20, oro 20",
              item="Reloj de Arena",
              se_abre="el **Reloj de Arena**: termina al instante una expedición en camino (se gasta al usarlo).",
              escena="""
                  El corazón busca, entre cien dientes, dos que sumen 197, y lo hace comparando **todos contra todos**: casi cinco mil pasos por vuelta. Por eso atrasa el reloj.
                  —Recorrelos **una sola vez** —dice Maese Horas—, y anotá los que ya pasaron.
              """,
              sugiere="Dos `for` anidados sobre la misma lista crecen como **n²**. Si por cada número preguntás si **ya viste su complemento** en un `set`, alcanza con recorrerlos una vez.",
              desafio="Completá la pregunta: ¿ya pasó el diente que le falta a este para llegar a 197?",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`objetivo - d`.",
              al_superar="""
                  Cien pasos en vez de cinco mil. El reloj da un tic-tac fuerte… y se vuelve a frenar. Maese Horas te pone en la mano un **reloj de arena** chiquito.
                  —Para cuando no haya tiempo. Se usa una vez.
                  Arriba, algo enorme se mueve: **el corazón del reloj es el corazón del Gólem**.
              """,
              imagen=["Maese Horas pone un reloj de arena chiquito, con arena verde luminosa, en la mano de Mia.",
                      "El mecanismo del gran reloj, con un corazón de engranajes que late en rojo.",
                      "Por el hueco de la escalera, arriba, se asoma un ojo enorme de bronce."]),
        ],
    },
    {
        "titulo": "R03-N07 · Jefe: el Golem del Reloj",
        "misiones": [
            m(id="R03-N07-P1", titulo="Las oleadas hasta el Gólem",
              lugar=CIMA, personajes="Mia, Gheco, Tilo, Ofidia",
              criatura="ogro",
              carta="return en un generador | lo termina · el for que lo recorre se detiene",
              recompensa="xp 15, oro 15",
              escena="""
                  La cima de la Torre es una plataforma abierta, con el cielo lleno de auroras. En el centro, el **Gólem del Reloj**: bronce, engranajes y un corazón rojo. De su pecho salen oleadas de piezas, una tras otra.
                  —Contalas sin guardarlas todas —dice {mentor}—. Y pará cuando llegue él.
              """,
              sugiere="Un `return` adentro de un generador lo **termina**: el `for` que lo recorre se detiene ahí, aunque queden datos.",
              desafio="Cortá el generador justo después de la oleada del Gólem.",
              inicial='''
                  def hasta_el_golem(oleadas):
                      for oleada in oleadas:
                          yield oleada
                          if oleada == "GÓLEM":
                              ___

                  oleadas = ["engranajes", "resortes", "péndulos", "GÓLEM", "engranajes", "resortes"]
                  for oleada in hasta_el_golem(oleadas):
                      print(oleada)
              ''',
              solucion='''
                  def hasta_el_golem(oleadas):
                      for oleada in oleadas:
                          yield oleada
                          if oleada == "GÓLEM":
                              return

                  oleadas = ["engranajes", "resortes", "péndulos", "GÓLEM", "engranajes", "resortes"]
                  for oleada in hasta_el_golem(oleadas):
                      print(oleada)
              ''',
              solucion_txt="`return`.",
              al_superar="Tres oleadas y el Gólem da un paso al frente. Detrás de él, las oleadas que vendrían se quedan quietas: no las pediste.",
              imagen=["La cima de la Torre bajo auroras cian; el Gólem del Reloj, de bronce, con un corazón rojo de engranajes.",
                      "Oleadas de piezas que salen de su pecho y se detienen en el aire.",
                      "Mia al frente, Tilo con la pértiga, Ofidia atrás, serena."]),
            m(id="R03-N07-P2", titulo="Ordenalas y agrupalas",
              lugar=CIMA, personajes="Mia, Gheco, Tilo",
              carta="Repaso | sorted + groupby + len(list(grupo)) · ordená por la misma clave antes de agrupar",
              recompensa="xp 15, oro 15",
              escena="El Gólem tira una lluvia de piezas mezcladas. Para saber qué viene, tenés que **agruparlas por tipo** y contarlas.",
              sugiere="Lo del segundo piso: `groupby` agrupa los consecutivos, así que primero `sorted`. Contá cada grupo con `len(list(grupo))`.",
              desafio="Agrupá las piezas por tipo y contalas.",
              inicial='''
                  from itertools import groupby

                  lluvia = ["péndulo", "resorte", "engranaje", "resorte", "engranaje", "engranaje"]
                  for tipo, grupo in groupby(___):
                      print(f"{tipo}: {len(list(grupo))}")
              ''',
              solucion='''
                  from itertools import groupby

                  lluvia = ["péndulo", "resorte", "engranaje", "resorte", "engranaje", "engranaje"]
                  for tipo, grupo in groupby(sorted(lluvia)):
                      print(f"{tipo}: {len(list(grupo))}")
              ''',
              solucion_txt="`groupby(sorted(lluvia))`.",
              al_superar="Tres engranajes, un péndulo y dos resortes. Ya sabés qué viene, y Tilo los va desviando con la pértiga.",
              imagen=["Una lluvia de piezas que se ordena en el aire en tres columnas.",
                      "Tilo desvía piezas con la pértiga del farol verde."]),
            m(id="R03-N07-P3", titulo="La torre probada",
              lugar=CIMA, personajes="Mia, Gheco, Tilo",
              carta="Repaso | assert antes de la batalla · si una pieza falla, que sea en el taller",
              recompensa="xp 15, oro 15",
              escena="Armás tres torres de defensa. Antes de ponerlas a disparar, las **probás**. Una dispara de más: hace el doble de daño contra todos, también contra Tilo.",
              sugiere="Probá la función con casos que conocés. Si el `assert` falla, arreglá la **función**.",
              desafio="Arreglá `danio`: el bonus de 2 es solo contra el Gólem.",
              inicial='''
                  def danio(base: int, objetivo: str) -> int:
                      return base * 2

                  assert danio(10, "GÓLEM") == 20, "doble contra el Gólem"
                  assert danio(10, "engranaje") == 10, "normal contra las piezas"
                  assert danio(0, "GÓLEM") == 0, "borde: sin daño"
                  print("Las torres están probadas")
              ''',
              solucion='''
                  def danio(base: int, objetivo: str) -> int:
                      if objetivo == "GÓLEM":
                          return base * 2
                      return base

                  assert danio(10, "GÓLEM") == 20, "doble contra el Gólem"
                  assert danio(10, "engranaje") == 10, "normal contra las piezas"
                  assert danio(0, "GÓLEM") == 0, "borde: sin daño"
                  print("Las torres están probadas")
              ''',
              solucion_txt="Duplicar solo si el objetivo es el Gólem: `if objetivo == \"GÓLEM\": return base * 2` y si no, `return base`.",
              al_superar="Las tres torres pasan las pruebas. Tilo suspira aliviado: ya no corre peligro.",
              imagen=["Tres torres de defensa de bronce con luces verdes de «probada».",
                      "Tilo, aliviado, se seca la frente."]),
            m(id="R03-N07-P4", titulo="Las tres torres a la vez",
              lugar=CIMA, personajes="Mia, Gheco, Tilo, Ofidia",
              criatura="troll",
              carta="asyncio.Queue | put_nowait agrega · await cola.get() saca · un None de fin por cada torre",
              recompensa="xp 20, oro 20",
              escena="""
                  —Que tus tres torres lo esperen **a la vez** —dice {mentor}—. Una fila de piezas, y cada torre toma la próxima.
                  Pero cuidado: un **troll** se esconde en las torres que quedan esperando para siempre.
              """,
              sugiere="Una `asyncio.Queue` es una fila compartida: `put_nowait` agrega y `await cola.get()` saca (y espera si está vacía). Para que cada torre sepa que terminó, mandá **un `None` por torre**.",
              desafio="Mandá una señal de fin para cada torre.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`range(3)`: un `None` por cada torre.",
              al_superar="Las tres torres derriban una pieza cada una, a la vez, y se apagan juntas. El Gólem, sin piezas, queda solo frente a vos.",
              imagen=["Tres torres que disparan a la vez a tres piezas distintas.",
                      "El Gólem, sin piezas a su alrededor, solo en la plataforma.",
                      "Ofidia asiente desde atrás."]),
            m(id="R03-N07-P5", titulo="El corazón del Gólem",
              lugar=CIMA, personajes="Mia, Gheco, Tilo, Ofidia, Maese Horas",
              criatura="dragón",
              carta="Todo junto | generador + decorador que cuenta · medir antes de golpear",
              recompensa="xp 25, oro 30",
              item="Túnica Encendida",
              escena="""
                  El corazón del Gólem late cada vez más rápido. Para llegar a él, tus golpes tienen que pasar por un decorador que los **cuenta**, y salir de un generador que los da **de a uno**.
              """,
              sugiere="Un decorador puede envolver un **generador**, si la envoltura también es generador: recorre el original con `for` y reenvía cada valor con `yield`. Si no reenvía, se «come» los golpes.",
              desafio="Reenviá cada golpe desde la envoltura.",
              inicial='''
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
              ''',
              solucion='''
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
              ''',
              solucion_txt="`yield golpe`.",
              al_superar="""
                  Tres golpes contados, y el corazón del Gólem se apaga. El gigante de bronce se arrodilla despacio y se queda quieto, como una estatua más de la Ciudadela.
                  Abajo, **el gran reloj vuelve a andar**: tic-tac, tic-tac, por todo el Valle.
                  Mirás tu túnica: las runas se encendieron **enteras**, de los pies a la capucha. Es la **Túnica Encendida**.
              """,
              imagen=["El Gólem del Reloj arrodillado y quieto, con el corazón apagado, bajo las auroras.",
                      "Mia de pie, con la túnica encendida entera en violeta, de los pies a la capucha.",
                      "Tilo, Gheco y Ofidia la miran; Maese Horas llega corriendo por la escalera.",
                      "El gran reloj de la Torre, con las agujas en movimiento."]),
        ],
    },
    {
        "titulo": "R03-N08 · La Encrucijada",
        "misiones": [
            m(id="R03-N08-P1", titulo="Lo que te llevás",
              lugar="La Encrucijada", personajes="Mia, Gheco, Tilo, Ofidia",
              carta="El camino | Fundamentos · Objetos y errores · Iteración y calidad · ya podés escribir programas completos",
              recompensa="xp 15, oro 20",
              escena="""
                  Al pie de la Ciudadela, el camino se abre en varios senderos. {mentor} se sienta al sol en una piedra del puente.
                  —Antes de elegir, mirá hacia atrás. ¿Cuántos lugares recorriste?
              """,
              sugiere="Todo lo que aprendiste sirve a la vez: un diccionario, un `for` sobre sus `.items()` y una expresión generadora adentro de `sum`.",
              desafio="Mostrá cada tramo del camino y el total de nodos.",
              inicial='''
                  camino = {"Fundamentos": 11, "Objetos y errores": 5, "Iteración y calidad": 8}
                  for tramo, nodos in camino.items():
                      print(f"{tramo}: {nodos} nodos")
                  print(f"En total: {___} nodos")
              ''',
              solucion='''
                  camino = {"Fundamentos": 11, "Objetos y errores": 5, "Iteración y calidad": 8}
                  for tramo, nodos in camino.items():
                      print(f"{tramo}: {nodos} nodos")
                  print(f"En total: {sum(n for n in camino.values())} nodos")
              ''',
              solucion_txt="`sum(n for n in camino.values())` (o `sum(camino.values())`).",
              al_superar="""
                  Veinticuatro nodos. {mentor} te mira un largo rato, y después cuenta lo que vio hace mucho:
                  —Hace mucho cruzó el Valle un viajero con las manos manchadas de plomo. Me preguntó cuál era la lengua más clara del mundo, la que cualquiera pudiera leer. Le dije que la mía. Sonrió y siguió camino hacia las Forjas.
              """,
              imagen=["La Encrucijada: un puente de piedra al pie de la Ciudadela, varios senderos que se abren.",
                      "Ofidia sentada al sol en una piedra del puente, contando.",
                      "Mia, Tilo y Gheco escuchan sentados en el pasto."]),
            m(id="R03-N08-P2", titulo="La marca de agua",
              lugar="La Encrucijada", personajes="Mia, Gheco, Tilo, Ofidia",
              carta="Para quien llegue | lo que se escribe claro, cualquiera lo puede leer",
              recompensa="xp 20, oro 25",
              escena="""
                  Levantás el pergamino, ya lleno, contra la luz del reloj. La marca de agua por fin se ve, pero **al revés**, como en un espejo.
              """,
              sugiere="Un texto se da vuelta con un corte con paso negativo: `texto[::-1]`.",
              desafio="Leé la marca de agua al derecho.",
              inicial='''
                  marca = "eugell neiuq arap"
                  print(marca___)
              ''',
              solucion='''
                  marca = "eugell neiuq arap"
                  print(marca[::-1])
              ''',
              solucion_txt="`marca[::-1]`.",
              al_superar="""
                  **Un vitral, y debajo: «para quien llegue».**
                  El pergamino nunca fue de nadie en particular. Lo dejó el viajero para quien llegara, y llegaste vos.
                  Tilo se queda en el Valle, como aprendiz de {mentor}. Gheco se te sube al hombro y señala los caminos: las **Sendas** del Valle, y el que baja hacia **las Forjas**, por donde siguió el viajero.
                  —¿Vamos?
              """,
              imagen=["Mia levanta el pergamino contra la luz del gran reloj: se ve la marca de agua de un vitral y la frase «para quien llegue».",
                      "Tilo, al lado de Ofidia, saluda con la pértiga.",
                      "Gheco en el hombro de Mia señala dos caminos: uno hacia el Coliseo y otro que baja hacia unas forjas humeantes a lo lejos."]),
        ],
    },
]
