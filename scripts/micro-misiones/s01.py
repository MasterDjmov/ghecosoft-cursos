import textwrap


def m(**kw):
    for k in ("inicial", "solucion"):
        kw[k] = textwrap.dedent(kw[k]).lstrip("\n")
    return kw


ARENA = "La Arena del Valle"
G = "Mia, Gheco, la Guardiana de la Arena"

NODOS = [
    {
        "titulo": "S01-N01 · La Arena: ventana y bucle de juego",
        "misiones": [
            m(id="S01-N01-P1", titulo="Mirar, mover, dibujar",
              lugar=ARENA, personajes=G,
              carta="Bucle de juego | while jugando: mirar (eventos) · mover (actualizar) · dibujar · una vuelta = un frame",
              recompensa="xp 10, oro 10",
              escena="""
                  El Coliseo del Valle es enorme, de piedra negra con runas verdes en las gradas. En el centro te espera una mujer alta, con una cresta verde y una cicatriz en la ceja: **la Guardiana de la Arena**.
                  —Acá todo late al mismo ritmo: mirar, mover, dibujar. La ventana de verdad la vas a abrir en tu compu; pero el **corazón** del juego es Python puro, y ese lo entrenamos acá.
              """,
              sugiere="Un juego es un **bucle**: en cada vuelta (un *frame*) mira qué pasó, mueve las cosas y las dibuja. Acá «dibujar» es mostrar la posición con `print`.",
              desafio="Completá el paso que mueve al slime en cada frame.",
              inicial='''
                  x = 0
                  velocidad = 3
                  for frame in range(1, 4):
                      ___
                      print(f"Frame {frame}: el slime está en x={x}")
              ''',
              solucion='''
                  x = 0
                  velocidad = 3
                  for frame in range(1, 4):
                      x += velocidad
                      print(f"Frame {frame}: el slime está en x={x}")
              ''',
              solucion_txt="`x += velocidad`.",
              al_superar="En la arena, un slime de práctica avanza a saltitos: uno, dos, tres. La Guardiana asiente. —Ese es el pulso. Ahora, que no dependa de la compu.",
              imagen=["El Coliseo del Valle de noche: gradas de piedra negra con runas verdes, auroras cian en el cielo.",
                      "La Guardiana de la Arena (cresta verde, armadura negra con placas verdes) en el centro.",
                      "Un slime de práctica con tres posiciones fantasma marcadas en el piso.",
                      "Mia con el pergamino, Gheco en el hombro."]),
            m(id="S01-N01-P2", titulo="El tiempo de cada frame",
              lugar=ARENA, personajes=G,
              carta="dt | x += velocidad * dt · velocidad en píxeles por SEGUNDO · igual en una compu rápida o lenta",
              recompensa="xp 10, oro 10",
              escena="—En una compu rápida hay 120 vueltas por segundo; en una lenta, 30 —dice la Guardiana—. Si movés un poco en cada vuelta, en una corre el doble que en la otra. Medí el **tiempo** de cada frame.",
              sugiere="`dt` es el tiempo que pasó desde el frame anterior (en segundos). Si la velocidad está en píxeles **por segundo**, `x += velocidad * dt` avanza lo mismo en cualquier compu.",
              desafio="Mové con `dt`: en un segundo, las dos compus tienen que llegar al mismo lugar.",
              inicial='''
                  def recorrer(fps, velocidad=120):
                      x = 0.0
                      dt = 1 / fps
                      for _ in range(fps):          # un segundo de juego
                          x += ___
                      return round(x)

                  print(f"Compu rápida (120 fps): {recorrer(120)}")
                  print(f"Compu lenta (30 fps): {recorrer(30)}")
              ''',
              solucion='''
                  def recorrer(fps, velocidad=120):
                      x = 0.0
                      dt = 1 / fps
                      for _ in range(fps):          # un segundo de juego
                          x += velocidad * dt
                      return round(x)

                  print(f"Compu rápida (120 fps): {recorrer(120)}")
                  print(f"Compu lenta (30 fps): {recorrer(30)}")
              ''',
              solucion_txt="`x += velocidad * dt`.",
              al_superar="Dos slimes de práctica, uno en una compu rápida y otro en una lenta, llegan a la línea al mismo tiempo. Gheco mira de uno a otro, asombrado.",
              imagen=["Dos pistas paralelas en la arena; dos slimes llegan juntos a una línea verde.",
                      "Sobre cada pista, un número distinto de huellas (muchas en una, pocas en otra)."]),
            m(id="S01-N01-P3", titulo="Rebotar en el borde",
              lugar=ARENA, personajes=G,
              carta="Rebote | if x < 0 or x > ancho: velocidad = -velocidad · el signo cambia la dirección",
              recompensa="xp 10, oro 10",
              escena="El slime de práctica se va por el costado de la arena y desaparece. —En mi Arena nadie se escapa —dice la Guardiana—. Que **rebote**.",
              sugiere="Cuando la posición pasa un borde, dar vuelta el **signo** de la velocidad la hace ir para el otro lado: `velocidad = -velocidad`.",
              desafio="Hacé rebotar al slime en los dos bordes de una arena de 10 de ancho.",
              inicial='''
                  ancho = 10
                  x = 7
                  velocidad = 2
                  recorrido = []
                  for _ in range(8):
                      x += velocidad
                      if x < 0 or x > ancho:
                          ___
                          x += 2 * velocidad
                      recorrido.append(x)
                  print(recorrido)
              ''',
              solucion='''
                  ancho = 10
                  x = 7
                  velocidad = 2
                  recorrido = []
                  for _ in range(8):
                      x += velocidad
                      if x < 0 or x > ancho:
                          velocidad = -velocidad
                          x += 2 * velocidad
                      recorrido.append(x)
                  print(recorrido)
              ''',
              solucion_txt="`velocidad = -velocidad`.",
              al_superar="El slime choca contra la pared, vuelve, cruza toda la arena y rebota del otro lado. El público de las gradas aplaude.",
              imagen=["Un slime rebotando contra el muro de la arena, con una estela en zigzag.",
                      "Público de siluetas en las gradas, aplaudiendo."]),
            m(id="S01-N01-P4", titulo="Cuadros por segundo",
              lugar=ARENA, personajes=G,
              carta="FPS | fps = frames / segundos · a 60 fps cada frame dura 1/60 ≈ 0.017 s",
              recompensa="xp 15, oro 15",
              escena="—Último ejercicio de calentamiento —dice la Guardiana—. Tu juego tardó estos tiempos en cada frame. ¿A cuántos cuadros por segundo anda?",
              sugiere="Los **FPS** son cuántos frames entran en un segundo: la cantidad de frames dividida por el tiempo total. Con `sum()` sumás los `dt`.",
              desafio="Calculá los FPS con la suma de los tiempos.",
              inicial='''
                  tiempos = [0.016, 0.017, 0.016, 0.018, 0.016, 0.017]
                  total = ___
                  fps = len(tiempos) / total
                  print(f"Duró {total:.3f} s: {fps:.0f} fps")
              ''',
              solucion='''
                  tiempos = [0.016, 0.017, 0.016, 0.018, 0.016, 0.017]
                  total = sum(tiempos)
                  fps = len(tiempos) / total
                  print(f"Duró {total:.3f} s: {fps:.0f} fps")
              ''',
              solucion_txt="`total = sum(tiempos)`.",
              al_superar="—Sesenta. El pulso justo —dice la Guardiana—. Ahora andá a tu compu, abrí la ventana y hacé que este corazón se vea.",
              imagen=["Un contador de luz sobre la arena que marca «60 FPS».",
                      "La Guardiana señala la salida del Coliseo; Mia guarda el pergamino."]),
        ],
    },
    {
        "titulo": "S01-N02 · Teclado y movimiento",
        "misiones": [
            m(id="S01-N02-P1", titulo="Hacia dónde",
              lugar=ARENA, personajes=G,
              carta="Dirección del teclado | derecha - izquierda → -1, 0 o 1 · True - False vale 1",
              recompensa="xp 10, oro 10",
              escena="Tu primer combate: el rival se mueve rápido. Para seguirlo, tu personaje tiene que saber **hacia dónde** ir según las teclas apretadas.",
              sugiere="Cada eje sale de restar dos teclas: `derecha - izquierda`. Como `True` vale 1 y `False` vale 0, el resultado es -1, 0 o 1.",
              desafio="Calculá el eje horizontal y el vertical.",
              inicial='''
                  teclas = {"izquierda": False, "derecha": True, "arriba": True, "abajo": False}
                  dx = ___
                  dy = teclas["abajo"] - teclas["arriba"]
                  print(f"Dirección: ({dx}, {dy})")
              ''',
              solucion='''
                  teclas = {"izquierda": False, "derecha": True, "arriba": True, "abajo": False}
                  dx = teclas["derecha"] - teclas["izquierda"]
                  dy = teclas["abajo"] - teclas["arriba"]
                  print(f"Dirección: ({dx}, {dy})")
              ''',
              solucion_txt="`dx = teclas[\"derecha\"] - teclas[\"izquierda\"]`.",
              al_superar="Tu personaje sale en diagonal, hacia arriba y a la derecha. Y llega antes de lo que esperabas. Demasiado antes.",
              imagen=["En la arena, el personaje de Mia (una figura de luz) sale en diagonal.",
                      "Sobre ella, un vector de luz: (1, -1)."]),
            m(id="S01-N02-P2", titulo="La diagonal tramposa",
              lugar=ARENA, personajes=G,
              carta="Normalizar | largo = math.hypot(dx, dy) · si largo > 0: dx, dy = dx / largo, dy / largo · siempre mide 1",
              recompensa="xp 15, oro 15",
              escena="—En diagonal vas un 41 % más rápido —se ríe la Guardiana—. Eso en mi Arena es trampa.",
              sugiere="El vector `(1, 1)` mide `math.hypot(1, 1)` ≈ 1.41. Dividiendo cada eje por el largo (si no es cero), el vector mide **1** en cualquier dirección: eso es **normalizar**.",
              desafio="Normalizá la dirección para que la velocidad sea la misma en diagonal.",
              inicial='''
                  import math

                  def paso(dx, dy, velocidad=100):
                      largo = math.hypot(dx, dy)
                      if largo > 0:
                          ___
                      return round(math.hypot(dx * velocidad, dy * velocidad))

                  print(f"Derecho: {paso(1, 0)}")
                  print(f"En diagonal: {paso(1, 1)}")
                  print(f"Quieto: {paso(0, 0)}")
              ''',
              solucion='''
                  import math

                  def paso(dx, dy, velocidad=100):
                      largo = math.hypot(dx, dy)
                      if largo > 0:
                          dx, dy = dx / largo, dy / largo
                      return round(math.hypot(dx * velocidad, dy * velocidad))

                  print(f"Derecho: {paso(1, 0)}")
                  print(f"En diagonal: {paso(1, 1)}")
                  print(f"Quieto: {paso(0, 0)}")
              ''',
              solucion_txt="`dx, dy = dx / largo, dy / largo`.",
              al_superar="Ahora vas igual de rápido en cualquier dirección. El rival te mira de reojo: ya no es tan fácil escaparse.",
              imagen=["Un círculo de luz alrededor de la figura de Mia: todas las flechas de dirección miden lo mismo.",
                      "La Guardiana, de brazos cruzados, conforme."]),
            m(id="S01-N02-P3", titulo="Lo que acaba de pasar",
              lugar=ARENA, personajes=G,
              carta="Evento o estado | estado: ¿está apretada? · evento (flanco): ahora and not antes · saltar, disparar: eventos",
              recompensa="xp 10, oro 10",
              escena="—Si saltás mientras la tecla **está** apretada, saltás sesenta veces por segundo —dice la Guardiana—. Para saltar, preguntá si se **acaba de** apretar.",
              sugiere="El **estado** dice si la tecla está apretada ahora. El **evento** («se acaba de apretar») se detecta comparando con el frame anterior: `ahora and not antes`.",
              desafio="Contá los saltos: uno por cada vez que se aprieta, no por cada frame.",
              inicial='''
                  espacio = [False, True, True, True, False, False, True, True, False]
                  saltos = 0
                  antes = False
                  for ahora in espacio:
                      if ___:
                          saltos += 1
                      antes = ahora
                  print(f"Frames con la tecla apretada: {sum(espacio)}")
                  print(f"Saltos: {saltos}")
              ''',
              solucion='''
                  espacio = [False, True, True, True, False, False, True, True, False]
                  saltos = 0
                  antes = False
                  for ahora in espacio:
                      if ahora and not antes:
                          saltos += 1
                      antes = ahora
                  print(f"Frames con la tecla apretada: {sum(espacio)}")
                  print(f"Saltos: {saltos}")
              ''',
              solucion_txt="`ahora and not antes`.",
              al_superar="Dos saltos limpios, justo cuando querías. El rival, que esperaba que te quedaras rebotando, se tropieza.",
              imagen=["La figura de Mia en el aire, en pleno salto; el rival se tropieza abajo.",
                      "Una tira de frames de luz con dos marcas doradas donde empezó cada salto."]),
            m(id="S01-N02-P4", titulo="El dash con descanso",
              lugar=ARENA, personajes=G,
              carta="Cooldown | espera = max(0, espera - dt) · solo se puede si espera == 0 · al usarlo, espera = 1.0",
              recompensa="xp 15, oro 15",
              escena="—Tu dash es muy bueno —dice la Guardiana—. Tan bueno que si lo usás sin parar, no hay combate. Que tenga **descanso**: un segundo entre uno y otro.",
              sugiere="Un **cooldown** es un número que baja con el tiempo. La acción solo funciona cuando llegó a 0; al usarla, vuelve a 1 segundo.",
              desafio="Dejá usar el dash solo cuando el descanso terminó.",
              inicial='''
                  dt = 0.25
                  espera = 0.0
                  intentos = [True, True, False, True, True, True, False, True]
                  for frame, quiere in enumerate(intentos, start=1):
                      espera = max(0.0, espera - dt)
                      if quiere and ___:
                          espera = 1.0
                          print(f"Frame {frame}: ¡dash!")
              ''',
              solucion='''
                  dt = 0.25
                  espera = 0.0
                  intentos = [True, True, False, True, True, True, False, True]
                  for frame, quiere in enumerate(intentos, start=1):
                      espera = max(0.0, espera - dt)
                      if quiere and espera == 0:
                          espera = 1.0
                          print(f"Frame {frame}: ¡dash!")
              ''',
              solucion_txt="`espera == 0`.",
              al_superar="Dash, descanso, dash. Ganás el primer combate por poco. La Guardiana te tira una toalla. —Bien. Mañana la Arena se llena.",
              imagen=["La figura de Mia en un dash con estela verde; un pequeño reloj de luz se recarga sobre su cabeza.",
                      "La Guardiana le tira una toalla desde el borde de la arena."]),
        ],
    },
    {
        "titulo": "S01-N03 · Sprites y colisiones",
        "misiones": [
            m(id="S01-N03-P1", titulo="¿Se tocan?",
              lugar=ARENA, personajes=G,
              carta="Colisión de rectángulos | se tocan si se solapan en X Y en Y · a.x < b.x + b.ancho and b.x < a.x + a.ancho",
              recompensa="xp 15, oro 15",
              escena="La Arena se llena de gemas que brillan. Para juntarlas, el juego tiene que saber cuándo tu personaje **toca** una.",
              sugiere="Cada cosa del juego ocupa un **rectángulo** `(x, y, ancho, alto)`. Dos rectángulos se tocan si se solapan en el eje X **y** en el eje Y.",
              desafio="Completá la condición del eje Y.",
              inicial='''
                  def se_tocan(a, b):
                      ax, ay, aw, ah = a
                      bx, by, bw, bh = b
                      en_x = ax < bx + bw and bx < ax + aw
                      en_y = ___
                      return en_x and en_y

                  mia = (10, 10, 20, 30)
                  print(se_tocan(mia, (25, 30, 10, 10)))
                  print(se_tocan(mia, (25, 50, 10, 10)))
                  print(se_tocan(mia, (40, 10, 10, 10)))
              ''',
              solucion='''
                  def se_tocan(a, b):
                      ax, ay, aw, ah = a
                      bx, by, bw, bh = b
                      en_x = ax < bx + bw and bx < ax + aw
                      en_y = ay < by + bh and by < ay + ah
                      return en_x and en_y

                  mia = (10, 10, 20, 30)
                  print(se_tocan(mia, (25, 30, 10, 10)))
                  print(se_tocan(mia, (25, 50, 10, 10)))
                  print(se_tocan(mia, (40, 10, 10, 10)))
              ''',
              solucion_txt="`en_y = ay < by + bh and by < ay + ah`.",
              al_superar="La primera gema se ilumina al tocarla. Las otras dos, que estaban cerca pero no tanto, siguen en su lugar.",
              imagen=["Rectángulos de luz alrededor de Mia y de tres gemas; uno se superpone y brilla en verde.",
                      "Gheco señala la superposición con la cola."]),
            m(id="S01-N03-P2", titulo="Juntarlas de una",
              lugar=ARENA, personajes=G,
              carta="Grupos | quedan = [g for g in gemas if not toca(g)] · se sacan de a muchas por frame",
              recompensa="xp 10, oro 10",
              escena="—No revises cada gema a mano —dice la Guardiana—. Juntalas en un **grupo** y preguntale al grupo cuáles tocaste. Las tocadas se van; las otras quedan.",
              sugiere="Un grupo es una lista de cosas del mismo tipo. Con una comprehension te quedás con las que **no** tocaste, y las que faltan son las que juntaste.",
              desafio="Quedate con las gemas que no tocó Mia.",
              inicial='''
                  def toca(gema, mia_x):
                      return abs(gema - mia_x) <= 5

                  gemas = [3, 12, 40, 15, 70]
                  mia_x = 10
                  quedan = ___
                  print(f"Juntó {len(gemas) - len(quedan)} gemas")
                  print(f"Quedan en: {quedan}")
              ''',
              solucion='''
                  def toca(gema, mia_x):
                      return abs(gema - mia_x) <= 5

                  gemas = [3, 12, 40, 15, 70]
                  mia_x = 10
                  quedan = [g for g in gemas if not toca(g, mia_x)]
                  print(f"Juntó {len(gemas) - len(quedan)} gemas")
                  print(f"Quedan en: {quedan}")
              ''',
              solucion_txt="`[g for g in gemas if not toca(g, mia_x)]`.",
              al_superar="Dos gemas a la vez saltan a tu bolsa. Las demás siguen brillando lejos.",
              imagen=["Dos gemas que vuelan hacia la bolsa de Mia; tres siguen brillando a lo lejos."]),
            m(id="S01-N03-P3", titulo="Un respiro después del golpe",
              lugar=ARENA, personajes=G,
              carta="Invulnerabilidad | tras un golpe, invulnerable = 1.0 s · mientras > 0, los golpes no cuentan",
              recompensa="xp 15, oro 15",
              escena="Un enemigo te toca y, en el mismo segundo, te quita la vida entera: un golpe por frame. —Después de un golpe —dice la Guardiana— te doy un respiro.",
              sugiere="Después de recibir un golpe, el personaje queda **invulnerable** un rato (los *i-frames*). Mientras el contador es mayor que 0, los golpes no cuentan.",
              desafio="Que solo cuente el golpe si no está invulnerable.",
              inicial='''
                  dt = 0.25
                  vida = 5
                  invulnerable = 0.0
                  tocado = [True, True, True, True, False, True, True]
                  for toca in tocado:
                      invulnerable = max(0.0, invulnerable - dt)
                      if toca and ___:
                          vida -= 1
                          invulnerable = 1.0
                  print(f"Vida: {vida}")
              ''',
              solucion='''
                  dt = 0.25
                  vida = 5
                  invulnerable = 0.0
                  tocado = [True, True, True, True, False, True, True]
                  for toca in tocado:
                      invulnerable = max(0.0, invulnerable - dt)
                      if toca and invulnerable == 0:
                          vida -= 1
                          invulnerable = 1.0
                  print(f"Vida: {vida}")
              ''',
              solucion_txt="`invulnerable == 0`.",
              al_superar="Te quedan tres de vida en lugar de cero. Tu figura parpadea cuando te tocan, y el público entiende: está en su respiro.",
              imagen=["La figura de Mia parpadeando, semitransparente, mientras un enemigo la atraviesa.",
                      "Tres corazones de luz sobre su cabeza."]),
            m(id="S01-N03-P4", titulo="Que brillen",
              lugar=ARENA, personajes=G,
              carta="Animar por tiempo | cuadro = int(t / duracion) % cantidad · la animación no depende de los fps",
              recompensa="xp 10, oro 10",
              escena="Las gemas están quietas, y una gema quieta no invita a nadie. —Que **brillen** —pide la Guardiana—: cuatro cuadros de brillo, cada uno un décimo de segundo.",
              sugiere="Para animar, elegí el cuadro según el **tiempo**: `int(t / duracion)` cuenta cuántos cuadros pasaron, y `% cantidad` vuelve a empezar al terminar.",
              desafio="Calculá qué cuadro se ve en cada momento.",
              inicial='''
                  cuadros = ["✦", "✧", "★", "✧"]
                  duracion = 0.1
                  for t in [0.0, 0.05, 0.12, 0.25, 0.38, 0.41, 0.55]:
                      cuadro = ___
                      print(f"{t:.2f} s: {cuadros[cuadro]}")
              ''',
              solucion='''
                  cuadros = ["✦", "✧", "★", "✧"]
                  duracion = 0.1
                  for t in [0.0, 0.05, 0.12, 0.25, 0.38, 0.41, 0.55]:
                      cuadro = int(t / duracion) % len(cuadros)
                      print(f"{t:.2f} s: {cuadros[cuadro]}")
              ''',
              solucion_txt="`int(t / duracion) % len(cuadros)`.",
              al_superar="Las gemas empiezan a titilar, todas al mismo ritmo. Desde las gradas, alguien grita «¡qué lindo!».",
              imagen=["Gemas que titilan en cuatro fases de brillo, como una tira de animación.",
                      "Público en las gradas, maravillado."]),
        ],
    },
    {
        "titulo": "S01-N04 · Jefe de la Arena: Junta las Gemas",
        "misiones": [
            m(id="S01-N04-P1", titulo="La cámara que sigue",
              lugar=ARENA, personajes=G,
              carta="Cámara | camara = jugador - pantalla / 2 · limitada entre 0 y mundo - pantalla · se dibuja en x - camara",
              recompensa="xp 15, oro 15",
              escena="La Guardiana te da los planos de «Junta las Gemas»: un mundo de 1000 de ancho y una pantalla de 300. —Que la cámara te siga —dice—, pero que nunca muestre fuera del mundo.",
              sugiere="La cámara se centra en el jugador (`jugador - pantalla / 2`) y se **limita** entre 0 y `mundo - pantalla` con `max` y `min`.",
              desafio="Limitá la cámara a los bordes del mundo.",
              inicial='''
                  mundo, pantalla = 1000, 300
                  for jugador in [50, 500, 980]:
                      camara = jugador - pantalla // 2
                      camara = ___
                      print(f"Jugador en {jugador}: cámara en {camara}, se dibuja en {jugador - camara}")
              ''',
              solucion='''
                  mundo, pantalla = 1000, 300
                  for jugador in [50, 500, 980]:
                      camara = jugador - pantalla // 2
                      camara = max(0, min(camara, mundo - pantalla))
                      print(f"Jugador en {jugador}: cámara en {camara}, se dibuja en {jugador - camara}")
              ''',
              solucion_txt="`max(0, min(camara, mundo - pantalla))`.",
              al_superar="La cámara te sigue por todo el mundo y frena justo en los bordes, sin mostrar el vacío de afuera.",
              imagen=["Un mundo de juego ancho visto desde arriba, con un rectángulo de cámara que sigue a Mia.",
                      "En los bordes, la cámara frena contra muros de luz."]),
            m(id="S01-N04-P2", titulo="Enemigos que se multiplican",
              lugar=ARENA, personajes=G,
              carta="Oleadas por tiempo | cada = max(0.5, 3 - minuto * 0.5) · el juego se pone difícil de a poco",
              recompensa="xp 15, oro 15",
              escena="—Un juego que siempre es igual aburre —dice la Guardiana—. Que los enemigos aparezcan **cada vez más seguido**, pero nunca más de dos por segundo.",
              sugiere="El tiempo entre enemigos baja con los minutos, pero con un **piso**: `max(0.5, ...)` no deja que baje de medio segundo.",
              desafio="Calculá cada cuánto aparece un enemigo, con el piso de 0.5.",
              inicial='''
                  for minuto in range(7):
                      cada = ___
                      print(f"Minuto {minuto}: un enemigo cada {cada} s")
              ''',
              solucion='''
                  for minuto in range(7):
                      cada = max(0.5, 3 - minuto * 0.5)
                      print(f"Minuto {minuto}: un enemigo cada {cada} s")
              ''',
              solucion_txt="`max(0.5, 3 - minuto * 0.5)`.",
              al_superar="Las oleadas se aprietan minuto a minuto, pero nunca se vuelven imposibles.",
              imagen=["Un gráfico de luz en el cielo de la arena: el tiempo entre enemigos baja y se aplana.",
                      "Enemigos entrando por las puertas del Coliseo."]),
            m(id="S01-N04-P3", titulo="Menú, juego y fin",
              lugar=ARENA, personajes=G,
              carta="Estados del juego | estado = \"menu\" | \"jugando\" | \"fin\" · un diccionario de transiciones",
              recompensa="xp 15, oro 15",
              escena="—Un juego completo no arranca jugando —dice la Guardiana—: tiene un menú, el juego y una pantalla de fin. Y de cada pantalla se pasa a otra según lo que pase.",
              sugiere="Un **estado** dice en qué pantalla está el juego. Un diccionario de **transiciones** dice, para cada estado y cada evento, a qué estado se pasa: `(estado, evento) → nuevo`.",
              desafio="Buscá el estado nuevo en las transiciones (si el evento no cambia nada, se queda igual).",
              inicial='''
                  transiciones = {
                      ("menu", "enter"): "jugando",
                      ("jugando", "sin vida"): "fin",
                      ("fin", "enter"): "menu",
                  }
                  estado = "menu"
                  for evento in ["espacio", "enter", "gema", "sin vida", "enter"]:
                      estado = ___
                      print(f"{evento} → {estado}")
              ''',
              solucion='''
                  transiciones = {
                      ("menu", "enter"): "jugando",
                      ("jugando", "sin vida"): "fin",
                      ("fin", "enter"): "menu",
                  }
                  estado = "menu"
                  for evento in ["espacio", "enter", "gema", "sin vida", "enter"]:
                      estado = transiciones.get((estado, evento), estado)
                      print(f"{evento} → {estado}")
              ''',
              solucion_txt="`transiciones.get((estado, evento), estado)`.",
              al_superar="Menú, juego, fin y de nuevo menú: el juego ya tiene principio y final.",
              imagen=["Tres pantallas flotando sobre la arena (menú, juego, fin) unidas por flechas de luz."]),
            m(id="S01-N04-P4", titulo="El récord de la Arena",
              lugar=ARENA, personajes=G,
              carta="Récord | record = max(record, puntos) · se guarda en un archivo (json) para la próxima vez",
              recompensa="xp 15, oro 15",
              escena="—Lo que hace volver a un jugador es el **récord** —dice la Guardiana—. Guardalo, para que mañana alguien quiera superarlo.",
              sugiere="El récord es el máximo entre el que había y los puntos de la partida. Para que dure, se guarda en un archivo con `json` (como en R02-N04).",
              desafio="Actualizá el récord con cada partida y guardalo.",
              inicial='''
                  import json

                  record = 0
                  for puntos in [120, 340, 90, 410, 300]:
                      record = ___
                  with open("record.json", "w", encoding="utf-8") as f:
                      json.dump({"record": record}, f)
                  with open("record.json", encoding="utf-8") as f:
                      print(f"Récord de la Arena: {json.load(f)['record']}")
              ''',
              solucion='''
                  import json

                  record = 0
                  for puntos in [120, 340, 90, 410, 300]:
                      record = max(record, puntos)
                  with open("record.json", "w", encoding="utf-8") as f:
                      json.dump({"record": record}, f)
                  with open("record.json", encoding="utf-8") as f:
                      print(f"Récord de la Arena: {json.load(f)['record']}")
              ''',
              solucion_txt="`max(record, puntos)`.",
              al_superar="Un tablero de piedra se enciende en la entrada del Coliseo: «Récord: 410». Abajo, alguien ya está anotando su nombre para desafiarlo.",
              imagen=["Un tablero de piedra con runas verdes en la entrada del Coliseo: «Récord: 410».",
                      "Aldeanos haciendo fila para jugar."]),
            m(id="S01-N04-P5", titulo="Junta las Gemas",
              lugar=ARENA, personajes=G,
              carta="Todo junto | bucle + dt + colisión + estado + puntaje · el corazón del juego en Python puro",
              recompensa="xp 25, oro 30",
              item="Mando de Piedra",
              escena="""
                  La prueba final: el corazón de «Junta las Gemas» entero. Mia avanza por el mundo, junta las gemas que toca y suma puntos; si un enemigo la toca, pierde vida, y el juego termina cuando no le queda.
              """,
              sugiere="Es todo lo de la Senda junto: un bucle con `dt`, mover, revisar choques, sumar y cambiar de estado. Lo que falta es lo de siempre: si toca una gema, sumar y sacarla.",
              desafio="Completá lo que pasa al tocar una gema.",
              inicial='''
                  gemas = [30, 60, 90, 150]
                  enemigos = [75, 120]
                  x, vida, puntos, estado = 0.0, 3, 0, "jugando"
                  dt, velocidad = 0.5, 30
                  while estado == "jugando":
                      x += velocidad * dt
                      for g in gemas[:]:
                          if abs(g - x) <= 5:
                              ___
                      if any(abs(e - x) <= 5 for e in enemigos):
                          vida -= 1
                          enemigos = [e for e in enemigos if abs(e - x) > 5]
                      if vida == 0 or x >= 160:
                          estado = "fin"
                  print(f"Llegó a x={x:.0f} con {vida} de vida y {puntos} puntos")
              ''',
              solucion='''
                  gemas = [30, 60, 90, 150]
                  enemigos = [75, 120]
                  x, vida, puntos, estado = 0.0, 3, 0, "jugando"
                  dt, velocidad = 0.5, 30
                  while estado == "jugando":
                      x += velocidad * dt
                      for g in gemas[:]:
                          if abs(g - x) <= 5:
                              puntos += 10
                              gemas.remove(g)
                      if any(abs(e - x) <= 5 for e in enemigos):
                          vida -= 1
                          enemigos = [e for e in enemigos if abs(e - x) > 5]
                      if vida == 0 or x >= 160:
                          estado = "fin"
                  print(f"Llegó a x={x:.0f} con {vida} de vida y {puntos} puntos")
              ''',
              solucion_txt="Sumar y sacarla: `puntos += 10` y `gemas.remove(g)`.",
              al_superar="""
                  Mia llega al final con todas las gemas. El Coliseo entero se pone de pie. La Guardiana le entrega su **mando de piedra** con runas.
                  —Acá los hechizos no se leen: se juegan. Ahora ya sabés hacer los tuyos. Abrí la ventana en tu compu y que el Valle lo vea.
              """,
              imagen=["El Coliseo de pie, aplaudiendo; gemas de luz cayendo como confeti.",
                      "La Guardiana de la Arena entrega a Mia un mando de juego de piedra con runas verdes.",
                      "Gheco, eufórico, en la cabeza de Mia."]),
        ],
    },
]
