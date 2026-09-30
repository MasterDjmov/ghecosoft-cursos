# RAMA S01 · Senda de la Arena: videojuegos con pygame

```meta
tipo: senda
posicion: 4
```

## S01-N01 · La Arena: ventana y bucle de juego

```meta
tipo: tema
padre: R03-N08
precio: 3
moneda: comodin
criatura: ogro
ejecutable: no
temas: graf.pygame, juegos.bucle
```

### Crónica

El sendero de la izquierda termina en un coliseo de piedra: **la Arena**. Acá los hechizos no se leen en un pergamino: se **ven**, se mueven, reaccionan. La guardiana de la Arena te da una sola regla:

—Todo lo que se mueve acá late al mismo ritmo, {heroe}: mirar, mover, dibujar. Mirar, mover, dibujar. Sesenta veces por segundo.

### Objetivos

- Abrir una ventana con pygame y dibujar formas.
- Escribir el **bucle de juego**: eventos → actualizar → dibujar.
- Mover cosas con velocidad × `dt`, igual en cualquier compu.

### Antes de empezar

Todo el camino principal. Clases (R02-N01) y módulos (R01-N10) ayudan mucho.

### Explicación

#### Instalar pygame

pygame no viene con Python y **no corre en el navegador** (abre una ventana propia), así que toda esta Senda se hace en tu compu:

```bash
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install pygame
python3 loop.py
```

En Ubuntu también sirve `sudo apt install python3-pygame`. Los ejemplos se muestran acá para leerlos y copiarlos; las misiones se entregan como archivo (.py o .zip).

#### El bucle de juego

Un juego es un programa que **nunca termina** hasta que lo cerrás. En cada vuelta (un *frame*):

1. **Eventos**: ¿cerraron la ventana? ¿apretaron una tecla?
2. **Actualizar**: mover lo que se mueve, revisar choques, sumar puntos.
3. **Dibujar**: pintar el fondo y todo lo demás, y mostrar el frame.

```python
while corriendo:
    dt = reloj.tick(60) / 1000     # segundos desde el frame anterior
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    x += velocidad * dt             # actualizar
    pantalla.fill(FONDO)            # dibujar
    pygame.draw.rect(pantalla, COLOR, (x, y, 48, 48))
    pygame.display.flip()
```

#### Las piezas

- `pygame.init()` arranca; `pygame.quit()` cierra.
- `pygame.display.set_mode((800, 600))` crea la ventana y devuelve la **superficie** donde se dibuja.
- Las coordenadas empiezan arriba a la izquierda: `x` crece hacia la derecha, `y` **hacia abajo**.
- Los colores son tuplas `(rojo, verde, azul)` de 0 a 255.
- `pygame.display.flip()` muestra lo dibujado de una vez (sin parpadeo).

#### El tiempo: `dt`

`reloj.tick(60)` frena el bucle para no pasar de 60 frames por segundo y devuelve los milisegundos desde el frame anterior. Si movés `x += 3` por frame, en una compu lenta todo va más lento. Si movés `x += velocidad * dt` (píxeles **por segundo** × segundos), se mueve igual en cualquier compu.

### Código de ejemplo

```python
"""pygame: ventana y game loop.

Todo juego repite el mismo patron: procesar eventos -> actualizar(dt) -> dibujar.

Necesita:  sudo apt install python3-pygame     (o ../crear-venv.sh)
Correr:    python3 loop.py       (Esc o cerrar la ventana para salir)
"""

import sys
import pygame

ANCHO, ALTO = 800, 600
FONDO = (18, 18, 28)
COLOR_CAJA = (137, 180, 250)


def main() -> None:
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Game loop")
    reloj = pygame.time.Clock()          # mide el tiempo entre frames

    # estado del juego
    x, y = ANCHO / 2, ALTO / 2
    vel = 180.0                          # pixeles por segundo
    dir_x, dir_y = 1, 1
    lado = 48

    corriendo = True
    while corriendo:
        # --- 1. tiempo: dt en SEGUNDOS (tick devuelve ms) ---
        dt = reloj.tick(60) / 1000.0     # limita a ~60 FPS y da el delta

        # --- 2. eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False

        # --- 3. actualizar (usando dt, independiente de los FPS) ---
        x += dir_x * vel * dt
        y += dir_y * vel * dt
        if x <= 0 or x + lado >= ANCHO:
            dir_x *= -1
            x = max(0, min(x, ANCHO - lado))
        if y <= 0 or y + lado >= ALTO:
            dir_y *= -1
            y = max(0, min(y, ALTO - lado))

        # --- 4. dibujar ---
        pantalla.fill(FONDO)
        pygame.draw.rect(pantalla, COLOR_CAJA, (x, y, lado, lado))
        # HUD con los FPS reales
        fps = int(reloj.get_fps())
        pygame.display.set_caption(f"Game loop  |  {fps} FPS")

        pygame.display.flip()            # muestra el frame dibujado

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

### ¿Para qué sirve?

El mismo bucle "eventos → actualizar → dibujar" está en todos los videojuegos, pero también en simuladores, visualizaciones de datos en vivo, programas de control de robots y hasta en la interfaz de tu celular. pygame es una gran puerta de entrada: lo que aprendés acá se traslada a Godot, Unity o cualquier motor.

### Errores habituales

**Ogro: la ventana "no responde"**: si no recorrés `pygame.event.get()` en cada vuelta, el sistema operativo cree que el programa se colgó.

**Ogro: todo queda "manchado"**: te olvidaste de `pantalla.fill(FONDO)` al principio de cada dibujo, y se ven todos los frames anteriores.

**Ogro: nada se ve**: falta `pygame.display.flip()` al final del dibujo.

**Esqueleto: `ModuleNotFoundError: No module named 'pygame'`**: no está instalado en el Python que estás usando (¿activaste el entorno virtual?).

**Ogro: la velocidad depende de la compu**: moviste por frame en lugar de por `dt`.

### Misión S01-N01-M1 · Dos cajas

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

A partir del ejemplo, agregá una **segunda caja** con otro color, otro tamaño y otra velocidad, que también rebote en los bordes. Organizá cada caja como un diccionario (o una clase) para no duplicar el código del rebote.

#### Criterio de aprobación

- Hay dos cajas con distinto color, tamaño y velocidad.
- Las dos rebotan en los cuatro bordes.
- El rebote está escrito una sola vez (una función o un método).

### Misión S01-N01-M2 · El rastro

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Hacé que la caja deje un **rastro**: guardá sus últimas 20 posiciones en un `collections.deque(maxlen=20)` y dibujá un círculo chico en cada una. Después cambiá `reloj.tick(60)` por `reloj.tick(30)`: ¿la caja va más lenta? Explicá por qué en un comentario.

#### Criterio de aprobación

- Usa un `deque` con `maxlen=20`.
- Dibuja el rastro antes que la caja.
- Un comentario explica por qué la velocidad no cambia a 30 FPS (el `dt`).

### Encargo S01-N01-E1 · El protector de pantalla

```meta
entrega: archivo
monedas: 1
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Hacé un protector de pantalla: el nombre de tu escuela (con `pygame.font.SysFont(...).render(...)`) rebota por la ventana y **cambia de color** cada vez que toca un borde.

#### Criterio de aprobación

- El texto rebota en los bordes usando su ancho y alto reales.
- Cambia de color en cada rebote.

### Prueba del sello

#### ¿Cuáles son los tres pasos de cada vuelta del bucle de juego?

Procesar eventos, actualizar el estado y dibujar.

#### ¿Qué devuelve `reloj.tick(60)`?

Los milisegundos desde el frame anterior (y frena para no pasar de 60 por segundo).

#### ¿Por qué se mueve con `velocidad * dt`?

Para que la velocidad sea en píxeles por segundo y no dependa de cuántos frames por segundo logre la compu.

#### ¿Hacia dónde crece la `y` en la pantalla?

Hacia abajo: el (0, 0) es la esquina de arriba a la izquierda.

### Soluciones (docente)

Material original: `17-Python/32-Pygame-Loop` (se limpiaron las referencias a SDL/C). Todo local: pygame no corre en Pyodide.

## S01-N02 · Teclado y movimiento

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: goblin
ejecutable: no
temas: juegos.entrada
usa: graf.pygame
```

### Crónica

Tu primer combate en la Arena. El rival se mueve rápido, esquiva, salta. Vos apretás las flechas y tu personaje… tarda, patina, va más rápido en diagonal.

—Hay dos formas de escuchar al teclado, {heroe} —dice la guardiana—: lo que **acaba de pasar** y lo que **está pasando**. Aprendé cuál usar para cada cosa.

### Objetivos

- Distinguir eventos de teclado (una vez por pulsación) del estado del teclado (mientras está apretada).
- Moverse con `pygame.math.Vector2` y normalizar la diagonal.
- Mostrar texto en pantalla.

### Antes de empezar

La Arena: ventana y bucle de juego (S01-N01).

### Explicación

#### Eventos o estado

- **Eventos** (`KEYDOWN`, `KEYUP` en `pygame.event.get()`): llegan **una vez** por pulsación. Para acciones puntuales: saltar, disparar, pausar.
- **Estado** (`pygame.key.get_pressed()`): dice qué teclas están apretadas **ahora**. Para movimiento continuo.

```python
teclas = pygame.key.get_pressed()
direccion = pygame.math.Vector2(teclas[pygame.K_d] - teclas[pygame.K_a],
                                teclas[pygame.K_s] - teclas[pygame.K_w])
```

El truco: `True - False` vale `1`, así que cada eje da -1, 0 o 1.

#### `Vector2` y la diagonal

`pygame.math.Vector2` es un vector con `+`, `*`, `.length()` y `.normalize()` (como el `Vec2` que armaste en R02-N01). Si sumás derecha y abajo, la dirección `(1, 1)` mide 1.41: en diagonal irías un 41 % más rápido. Normalizala (si no es cero) para que siempre mida 1:

```python
if direccion.length_squared() > 0:
    direccion = direccion.normalize()
posicion += direccion * velocidad * dt
```

#### Texto en pantalla

```python
fuente = pygame.font.SysFont(None, 28)
imagen = fuente.render(f"Vida: {vida}", True, (255, 255, 255))
pantalla.blit(imagen, (10, 10))
```

`render` crea una imagen con el texto y `blit` la pega en la pantalla.

#### Tiempos de espera (cooldown)

Para que una acción no se pueda repetir enseguida, guardá cuánto falta con un número que baja con `dt`: la acción solo funciona cuando llegó a cero.

### Código de ejemplo

```python
"""pygame: input y movimiento.

Dos formas de leer el teclado:
  - EVENTOS (KEYDOWN/KEYUP): para acciones puntuales (saltar, disparar, pausa).
  - ESTADO (key.get_pressed()): para movimiento continuo (mantener flecha).

Movimiento con velocidad*dt y diagonal normalizada (para no ir mas rapido
en diagonal).

Necesita:  sudo apt install python3-pygame
"""

import sys
import pygame
from pygame.math import Vector2

ANCHO, ALTO = 800, 600


def main() -> None:
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("18 - Input")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("monospace", 18)

    pos = Vector2(ANCHO / 2, ALTO / 2)
    velocidad = 260.0
    lado = 40
    dash_hasta = 0.0        # timestamp: hasta cuando dura el dash
    tiempo = 0.0
    disparos = 0

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0
        tiempo += dt

        # --- EVENTOS: acciones puntuales ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                corriendo = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    corriendo = False
                elif e.key == pygame.K_SPACE:
                    disparos += 1                       # se cuenta UNA vez por pulsacion
                elif e.key == pygame.K_LSHIFT:
                    dash_hasta = tiempo + 0.15          # dash de 150 ms

        # --- ESTADO: movimiento continuo ---
        teclas = pygame.key.get_pressed()
        direccion = Vector2(
            teclas[pygame.K_d] - teclas[pygame.K_a],
            teclas[pygame.K_s] - teclas[pygame.K_w],
        )
        if direccion.length_squared() > 0:
            direccion = direccion.normalize()          # diagonal no acelera

        vel = velocidad * (3.0 if tiempo < dash_hasta else 1.0)
        pos += direccion * vel * dt

        # limitar a la pantalla
        pos.x = max(0, min(pos.x, ANCHO - lado))
        pos.y = max(0, min(pos.y, ALTO - lado))

        # --- DIBUJAR ---
        pantalla.fill((18, 18, 28))
        color = (243, 139, 168) if tiempo < dash_hasta else (137, 180, 250)
        pygame.draw.rect(pantalla, color, (pos.x, pos.y, lado, lado))

        hud = fuente.render(
            f"WASD mover | Shift dash | Espacio disparar ({disparos})",
            True, (200, 200, 210))
        pantalla.blit(hud, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

### ¿Para qué sirve?

Leer bien la entrada es lo que hace que un juego "se sienta bien". Las mismas ideas sirven para controlar un brazo robótico con un joystick, mover la cámara en un programa de diseño 3D o manejar un dron desde la compu.

### Errores habituales

**Goblin: normalizar el vector cero**: `Vector2(0, 0).normalize()` da `ValueError: Can't normalize Vector of length Zero`. Revisá antes que la dirección no sea cero.

**Ogro: movimiento con eventos**: si movés solo en `KEYDOWN`, el personaje da un paso por pulsación y se frena aunque mantengas la tecla.

**Ogro: disparo con el estado**: si disparás con `get_pressed()`, sale un disparo **por frame** (¡60 por segundo!).

**Ogro: el cooldown que no baja**: te olvidaste de restarle `dt` en cada vuelta.

### Misión S01-N02-M1 · Flechas y WASD

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Hacé que el personaje se pueda mover **tanto con las flechas como con WASD** (las dos a la vez tienen que funcionar), sin ir más rápido en diagonal.

#### Criterio de aprobación

- Funcionan las flechas y WASD.
- La diagonal está normalizada.
- El movimiento usa `dt`.

### Misión S01-N02-M2 · El dash con descanso

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Agregá un **dash**: con la barra espaciadora (un evento `KEYDOWN`), el personaje avanza rápido en la dirección en que se mueve. Después tiene que esperar **1 segundo** antes de poder usarlo de nuevo. Mostrá en pantalla si el dash está listo o cuánto falta.

#### Criterio de aprobación

- El dash se activa con un evento, no con el estado del teclado.
- Tiene un cooldown de 1 s que baja con `dt`.
- La pantalla muestra si está listo o cuánto falta.

### Encargo S01-N02-E1 · El mando del Gremio

```meta
entrega: archivo
monedas: 1
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Sumá soporte de **joystick** con `pygame.joystick`: si hay uno conectado, que mueva al personaje con el eje izquierdo (ignorá valores muy chicos, la "zona muerta").

#### Criterio de aprobación

- Detecta si hay un joystick y funciona igual sin él.
- Aplica una zona muerta a los ejes.

### Prueba del sello

#### ¿Cuándo conviene usar eventos y cuándo el estado del teclado?

Eventos para acciones puntuales (saltar, disparar); estado para movimiento continuo.

#### ¿Por qué hay que normalizar la dirección?

Porque en diagonal el vector mide más que 1 y el personaje iría más rápido.

#### ¿Qué pasa si normalizás el vector (0, 0)?

Da error: no tiene dirección. Hay que revisar antes que no sea cero.

### Soluciones (docente)

Material original: `17-Python/33-Pygame-Input`.

## S01-N03 · Sprites y colisiones

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: orco
ejecutable: no
temas: juegos.sprites, juegos.colisiones
usa: graf.pygame
```

### Crónica

La Arena se llena: gemas que brillan, enemigos que persiguen, proyectiles. Manejar cada uno a mano es imposible.

—Cada cosa en la Arena es un **sprite**, {heroe} —dice la guardiana—: una imagen con su lugar. Juntalos en **grupos** y dejá que los grupos hagan el trabajo pesado.

### Objetivos

- Crear sprites con `pygame.sprite.Sprite` (una imagen y un rectángulo).
- Manejar muchos a la vez con `Group`: actualizar, dibujar y detectar choques.
- Animar por tiempo.

### Antes de empezar

Teclado y movimiento (S01-N02) y herencia (R02-N02): un sprite es una clase que hereda de `Sprite`.

### Explicación

#### Un sprite

```python
class Gema(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((80, 220, 255))
        self.rect = self.image.get_rect(center=(x, y))
```

Todo sprite necesita dos atributos: `image` (lo que se dibuja) y `rect` (un `pygame.Rect` con la posición y el tamaño, que se usa para dibujar y para chocar).

#### Grupos

`pygame.sprite.Group()` guarda muchos sprites:

- `grupo.update(dt)` llama al `update` de cada uno.
- `grupo.draw(pantalla)` los dibuja a todos.
- `sprite.kill()` lo saca de todos sus grupos.

#### Colisiones

- `pygame.sprite.spritecollide(jugador, gemas, True)`: la lista de gemas que tocan al jugador; con `True`, las saca del grupo (las "junta").
- `pygame.sprite.groupcollide(balas, enemigos, True, True)`: choques entre dos grupos.
- `rect.colliderect(otro)`: si dos rectángulos se tocan.

#### Animar por tiempo

Acumulá `dt` y, cuando pasa un umbral (por ejemplo 0,12 s), avanzá al siguiente cuadro de la animación. Así la animación va igual a cualquier velocidad.

#### Invulnerabilidad (i-frames)

Después de un golpe, el jugador queda invulnerable un rato (y suele parpadear): un contador que baja con `dt`, como el cooldown.

### Código de ejemplo

```python
"""pygame: sprites, grupos, colisiones y animacion.

pygame.sprite.Sprite + Group: la forma "con pilas" de manejar muchas entidades
(update de todas, draw de todas, colisiones entre grupos).
Las texturas se generan por codigo.

Necesita:  sudo apt install python3-pygame
"""

import sys
import random
import pygame
from pygame.math import Vector2

ANCHO, ALTO = 800, 600


def textura(color, w, h, borde=None):
    """Crea una Surface de color plano (opcional: borde de otro color)."""
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill(color)
    if borde:
        pygame.draw.rect(s, borde, s.get_rect(), 2)
    return s


class Jugador(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # animacion: dos "frames" que alternan
        self.frames = [textura((137, 180, 250), 40, 40, (200, 220, 255)),
                       textura((116, 160, 240), 40, 40, (200, 220, 255))]
        self.frame_i = 0
        self.anim_t = 0.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = 240.0

    def update(self, dt, teclas):
        d = Vector2(teclas[pygame.K_d] - teclas[pygame.K_a],
                    teclas[pygame.K_s] - teclas[pygame.K_w])
        moviendo = d.length_squared() > 0
        if moviendo:
            self.pos += d.normalize() * self.vel * dt
            self.pos.x = max(20, min(self.pos.x, ANCHO - 20))
            self.pos.y = max(20, min(self.pos.y, ALTO - 20))
            self.rect.center = self.pos

        # avanzar la animacion solo si se mueve (0.12 s por frame)
        self.anim_t += dt
        if moviendo and self.anim_t >= 0.12:
            self.anim_t = 0.0
            self.frame_i = (self.frame_i + 1) % len(self.frames)
        self.image = self.frames[self.frame_i if moviendo else 0]


class Gema(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = textura((166, 227, 161), 20, 20)
        self.rect = self.image.get_rect(
            center=(random.randint(30, ANCHO - 30), random.randint(30, ALTO - 30)))


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = textura((243, 139, 168), 34, 34)
        borde = random.choice(["arriba", "abajo", "izq", "der"])
        pos = {"arriba": (random.randint(0, ANCHO), -20),
               "abajo": (random.randint(0, ANCHO), ALTO + 20),
               "izq": (-20, random.randint(0, ALTO)),
               "der": (ANCHO + 20, random.randint(0, ALTO))}[borde]
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = random.uniform(60, 110)

    def update(self, dt, objetivo):
        d = objetivo - self.pos
        if d.length() > 0:
            self.pos += d.normalize() * self.vel * dt
            self.rect.center = self.pos


def main() -> None:
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("19 - Sprites")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("monospace", 20)

    jugador = Jugador((ANCHO / 2, ALTO / 2))
    grupo_jugador = pygame.sprite.GroupSingle(jugador)
    gemas = pygame.sprite.Group(Gema() for _ in range(6))
    enemigos = pygame.sprite.Group()

    puntos = 0
    spawn_t = 0.0
    vivo = True

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                corriendo = False

        if vivo:
            teclas = pygame.key.get_pressed()
            jugador.update(dt, teclas)
            enemigos.update(dt, jugador.pos)

            # spawn de enemigos cada 1.5 s
            spawn_t += dt
            if spawn_t >= 1.5:
                spawn_t = 0.0
                enemigos.add(Enemigo())

            # colision jugador-gema: recoge (dokill=True borra la gema)
            recogidas = pygame.sprite.spritecollide(jugador, gemas, dokill=True)
            puntos += len(recogidas)
            for _ in recogidas:
                gemas.add(Gema())

            # colision jugador-enemigo: game over
            if pygame.sprite.spritecollide(jugador, enemigos, dokill=False):
                vivo = False

        pantalla.fill((18, 18, 28))
        gemas.draw(pantalla)
        enemigos.draw(pantalla)
        grupo_jugador.draw(pantalla)
        hud = fuente.render(f"gemas: {puntos}" + ("" if vivo else "   -- GAME OVER --"),
                            True, (230, 230, 240))
        pantalla.blit(hud, (10, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

### ¿Para qué sirve?

Los sprites y las colisiones son la base de cualquier juego 2D, pero la misma idea (rectángulos que se superponen) se usa para saber si tocaste un botón en una pantalla táctil, si dos ventanas se pisan en un escritorio o si dos paquetes chocan en una simulación de un depósito.

### Errores habituales

**Orco: el sprite sin `rect` o sin `image`**: `AttributeError` al dibujar el grupo.

**Ogro: mover `x` e `y` sin mover el `rect`**: el sprite se dibuja y choca donde está el `rect`, no donde creés.

**Ogro: el golpe que mata de una**: sin invulnerabilidad, un enemigo que te toca durante 20 frames te pega 20 veces.

**Esqueleto: olvidar `super().__init__()`** en la clase del sprite: los grupos no lo reconocen.

### Misión S01-N03-M1 · Tres golpes

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

En lugar de perder al primer toque, dale al jugador **3 de vida**. Después de cada golpe, 1 segundo de invulnerabilidad en el que **parpadea** (se dibuja en frames alternos). Mostrá la vida en pantalla.

#### Criterio de aprobación

- El jugador tiene 3 de vida y la muestra.
- Tras un golpe, 1 s de invulnerabilidad con parpadeo.
- La invulnerabilidad baja con `dt`.

### Misión S01-N03-M2 · Proyectiles

```meta
entrega: archivo
monedas: 5
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Agregá un grupo de **proyectiles**: con la barra espaciadora, el jugador dispara hacia el enemigo más cercano. Usá `groupcollide` para que proyectil y enemigo desaparezcan al chocar, y sacá del grupo los proyectiles que salen de la pantalla.

#### Criterio de aprobación

- Los proyectiles son sprites en su propio grupo.
- Apuntan al enemigo más cercano (`min` con `key`).
- Usa `groupcollide` y elimina los que salen de la pantalla.

### Encargo S01-N03-E1 · Gemas que brillan

```meta
entrega: archivo
monedas: 1
xp: 15
entorno: local
extensiones: py, zip
```

#### Consigna

Hacé que las gemas **parpadeen**: alterná su `image` entre dos brillos cada 0,3 segundos, animando por tiempo.

#### Criterio de aprobación

- Alterna dos imágenes según el tiempo acumulado, no según los frames.

### Prueba del sello

#### ¿Qué dos atributos necesita todo sprite?

`image` (lo que se dibuja) y `rect` (posición y tamaño).

#### ¿Qué hace `spritecollide(jugador, gemas, True)`?

Devuelve las gemas que tocan al jugador y, por el `True`, las saca del grupo.

#### ¿Para qué sirve la invulnerabilidad después de un golpe?

Para que un mismo toque no reste vida en cada frame.

### Soluciones (docente)

Material original: `17-Python/34-Pygame-Sprites`.

## S01-N04 · Jefe de la Arena: Junta las Gemas

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
ejecutable: no
insignia: Campeón de la Arena
insignia_descripcion: Terminaste "Junta las Gemas": un videojuego completo en Python.
temas: juegos.estados, juegos.guardado
usa: graf.pygame, prog.modulos
```

### Crónica

La prueba final de la Arena no es un combate: es **construir** uno. La guardiana te entrega los planos de "Junta las Gemas": un mundo más grande que la pantalla, una cámara que te sigue, enemigos que se multiplican, un menú y una pantalla de fin.

—Ya tenés todas las piezas, {heroe}. Ahora hacelo tuyo.

### Objetivos

- Leer y entender un juego completo, organizado en estados (menú, jugando, fin).
- Modificarlo y extenderlo: módulos, power-ups y récord guardado.

### Antes de empezar

Toda la Senda de la Arena, módulos (R01-N10) y JSON (R02-N04).

### Explicación

#### Un juego completo

"Junta las Gemas" suma lo que viste en la Senda:

- **Estados**: el juego está en `MENU`, `JUGANDO` o `GAME_OVER`, y cada uno maneja sus propios eventos y su propio dibujo.
- **Cámara**: el mundo es más grande que la ventana. Todo se dibuja restando la posición de la cámara, que sigue al jugador.
- **Dificultad creciente**: aparecen más enemigos con el tiempo.
- **HUD**: gemas, vida, tiempo y FPS encima de todo.

#### Organizar en módulos

Un juego crece rápido. Separarlo en archivos (`entidades.py` con los sprites, `juego.py` con los estados, `juega.py` que arranca) hace que cada parte se pueda leer y cambiar sin romper las otras (R01-N10).

### Código de ejemplo

```python
"""Proyecto pygame: "Junta las Gemas".

"Junta las Gemas", el juego completo en Python:
- mundo mas grande que la pantalla, camara que sigue al jugador
- gemas para juntar, enemigos que aparecen con dificultad creciente
- vida con i-frames, colisiones AABB
- pantallas: MENU -> JUGANDO -> GAME OVER
- HUD (gemas, vida, tiempo, FPS)
- todo con texturas por codigo y sonido sintetizado

Necesita:  sudo apt install python3-pygame     (o ../crear-venv.sh)
Correr:    python3 juega.py
"""

import array
import math
import random
import sys

import pygame
from pygame.math import Vector2

ANCHO, ALTO = 900, 600
MUNDO = pygame.Rect(0, 0, 2400, 1600)
NEGRO = (14, 14, 22)
MAX_ENEMIGOS = 40          # tope: sin esto la lista crece sin fin y el juego se ralentiza


# --------------------------------------------------------------------------
# audio: un "blip" sintetizado (sin archivos)
# --------------------------------------------------------------------------
def tono(freq: float, ms: int, volumen: float = 0.3):
    try:
        rate = 22050
        n = int(rate * ms / 1000)
        buf = array.array("h")
        for i in range(n):
            env = 1.0 - i / n                      # decae
            s = math.sin(2 * math.pi * freq * i / rate)
            buf.append(int(32767 * volumen * env * s))
        snd = pygame.mixer.Sound(buffer=buf.tobytes())
        return snd
    except Exception:
        return None


# --------------------------------------------------------------------------
# entidades
# --------------------------------------------------------------------------
class Jugador:
    def __init__(self):
        self.pos = Vector2(MUNDO.width / 2, MUNDO.height / 2)
        self.vel = 300.0
        self.radio = 20
        self.vida = 5
        self.iframe = 0.0
        self.anim = 0.0

    @property
    def rect(self):
        return pygame.Rect(self.pos.x - self.radio, self.pos.y - self.radio,
                           self.radio * 2, self.radio * 2)

    def update(self, dt, teclas):
        d = Vector2(teclas[pygame.K_d] - teclas[pygame.K_a],
                    teclas[pygame.K_s] - teclas[pygame.K_w])
        if d.length_squared() > 0:
            self.pos += d.normalize() * self.vel * dt
            self.anim += dt * 10
        self.pos.x = max(self.radio, min(self.pos.x, MUNDO.width - self.radio))
        self.pos.y = max(self.radio, min(self.pos.y, MUNDO.height - self.radio))
        self.iframe = max(0.0, self.iframe - dt)

    def dibujar(self, sup, cam):
        p = self.pos - cam
        parpadea = self.iframe > 0 and int(self.iframe * 20) % 2 == 0
        color = (90, 90, 110) if parpadea else (137, 180, 250)
        pygame.draw.circle(sup, color, p, self.radio)
        # "ojo" que mira segun el bob de la animacion
        off = Vector2(math.sin(self.anim) * 4, -6)
        pygame.draw.circle(sup, NEGRO, p + off, 4)


class Enemigo:
    def __init__(self, alrededor: Vector2, vel: float):
        ang = random.uniform(0, math.tau)
        self.pos = alrededor + Vector2(math.cos(ang), math.sin(ang)) * 700
        self.pos.x = max(0, min(self.pos.x, MUNDO.width))
        self.pos.y = max(0, min(self.pos.y, MUNDO.height))
        self.vel = vel
        self.radio = 16

    @property
    def rect(self):
        return pygame.Rect(self.pos.x - self.radio, self.pos.y - self.radio,
                           self.radio * 2, self.radio * 2)

    def update(self, dt, objetivo: Vector2):
        d = objetivo - self.pos
        if d.length() > 0:
            self.pos += d.normalize() * self.vel * dt

    def dibujar(self, sup, cam):
        pygame.draw.circle(sup, (243, 139, 168), self.pos - cam, self.radio)


class Gema:
    def __init__(self):
        self.pos = Vector2(random.randint(40, MUNDO.width - 40),
                           random.randint(40, MUNDO.height - 40))
        self.radio = 10

    @property
    def rect(self):
        return pygame.Rect(self.pos.x - self.radio, self.pos.y - self.radio,
                           self.radio * 2, self.radio * 2)

    def dibujar(self, sup, cam, t):
        r = self.radio + math.sin(t * 4) * 2
        pygame.draw.circle(sup, (166, 227, 161), self.pos - cam, r)


# --------------------------------------------------------------------------
# juego
# --------------------------------------------------------------------------
class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=1)
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Junta las Gemas")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("monospace", 22)
        self.fuente_grande = pygame.font.SysFont("monospace", 48, bold=True)
        self.snd_gema = tono(880, 90)
        self.snd_golpe = tono(160, 200)
        self.estado = "MENU"
        self.reset()

    def reset(self):
        self.jugador = Jugador()
        self.gemas = [Gema() for _ in range(8)]
        self.enemigos: list[Enemigo] = []
        self.puntos = 0
        self.tiempo = 0.0
        self.spawn_t = 0.0

    # ---- camara: centra al jugador, con clamp al mundo ----
    def camara(self) -> Vector2:
        c = self.jugador.pos - Vector2(ANCHO / 2, ALTO / 2)
        c.x = max(0, min(c.x, MUNDO.width - ANCHO))
        c.y = max(0, min(c.y, MUNDO.height - ALTO))
        return c

    def sonar(self, snd):
        if snd:
            snd.play()

    def update(self, dt):
        self.tiempo += dt
        teclas = pygame.key.get_pressed()
        self.jugador.update(dt, teclas)

        # dificultad: mas enemigos y mas rapidos con el tiempo
        self.spawn_t += dt
        cada = max(0.5, 2.5 - self.tiempo * 0.03)
        if self.spawn_t >= cada and len(self.enemigos) < MAX_ENEMIGOS:
            self.spawn_t = 0.0
            self.enemigos.append(Enemigo(self.jugador.pos, 80 + self.tiempo * 2))

        for e in self.enemigos:
            e.update(dt, self.jugador.pos)

        # gemas
        for g in self.gemas[:]:
            if self.jugador.rect.colliderect(g.rect):
                self.gemas.remove(g)
                self.gemas.append(Gema())
                self.puntos += 1
                self.sonar(self.snd_gema)

        # daño
        if self.jugador.iframe <= 0:
            for e in self.enemigos:
                if self.jugador.rect.colliderect(e.rect):
                    self.jugador.vida -= 1
                    self.jugador.iframe = 1.2
                    self.sonar(self.snd_golpe)
                    break

        if self.jugador.vida <= 0:
            self.estado = "GAME_OVER"

    def dibujar(self):
        sup = self.pantalla
        sup.fill(NEGRO)
        cam = self.camara()

        # grilla del mundo para que se note el desplazamiento
        paso = 120
        for x in range(0, MUNDO.width, paso):
            pygame.draw.line(sup, (28, 28, 40), (x - cam.x, -cam.y),
                             (x - cam.x, MUNDO.height - cam.y))
        for y in range(0, MUNDO.height, paso):
            pygame.draw.line(sup, (28, 28, 40), (-cam.x, y - cam.y),
                             (MUNDO.width - cam.x, y - cam.y))

        for g in self.gemas:
            g.dibujar(sup, cam, self.tiempo)
        for e in self.enemigos:
            e.dibujar(sup, cam)
        self.jugador.dibujar(sup, cam)

        # HUD
        hud = self.fuente.render(
            f"gemas {self.puntos}   vida {'♥' * self.jugador.vida}   "
            f"t {self.tiempo:5.1f}s   {int(self.reloj.get_fps())} fps",
            True, (230, 230, 240))
        sup.blit(hud, (12, 10))

    def texto_centro(self, texto, fuente, y, color=(230, 230, 240)):
        img = fuente.render(texto, True, color)
        self.pantalla.blit(img, img.get_rect(center=(ANCHO / 2, y)))

    def salir(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            dt = self.reloj.tick(60) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.salir()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.salir()
                    if e.key == pygame.K_RETURN:
                        if self.estado == "MENU":
                            self.estado = "JUGANDO"
                        elif self.estado == "GAME_OVER":
                            self.reset()
                            self.estado = "JUGANDO"

            if self.estado == "JUGANDO":
                self.update(dt)
                self.dibujar()
            elif self.estado == "MENU":
                self.pantalla.fill(NEGRO)
                self.texto_centro("JUNTA LAS GEMAS", self.fuente_grande, 220,
                                  (166, 227, 161))
                self.texto_centro("WASD para moverte, junta gemas, esquiva a los rojos",
                                  self.fuente, 300)
                self.texto_centro("ENTER para empezar", self.fuente, 350)
            elif self.estado == "GAME_OVER":
                self.dibujar()
                s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
                s.fill((0, 0, 0, 170))
                self.pantalla.blit(s, (0, 0))
                self.texto_centro("GAME OVER", self.fuente_grande, 250,
                                  (243, 139, 168))
                self.texto_centro(f"gemas: {self.puntos}   tiempo: {self.tiempo:.1f}s",
                                  self.fuente, 320)
                self.texto_centro("ENTER para reintentar", self.fuente, 360)

            pygame.display.flip()


if __name__ == "__main__":
    Juego().run()
```

### ¿Para qué sirve?

Este es el tamaño de un juego de una *game jam*: un proyecto completo que se puede mostrar, compartir y seguir mejorando. Organizarlo en módulos y estados es exactamente lo que se hace en estudios de videojuegos (y en cualquier aplicación con pantallas).

### Errores habituales

- **Orco**: al separar en módulos, un import circular entre `juego.py` y `entidades.py` (R01-N10).
- **Ogro**: olvidar reiniciar el estado al volver a jugar desde el menú (los enemigos de la partida anterior siguen ahí).
- **Goblin**: el récord guardado como texto y comparado como número.

### Misión S01-N04-M1 · El juego en piezas

```meta
entrega: archivo
monedas: 6
xp: 30
entorno: local
extensiones: py, zip
```

#### Consigna

Partí `juega.py` en tres módulos: `entidades.py` (los sprites), `juego.py` (los estados y el bucle) y `juega.py` (solo arranca). Después agregá un **power-up** (un tercer tipo de sprite) que aparezca de vez en cuando y dé velocidad o vida por unos segundos.

#### Criterio de aprobación

- El juego está en tres módulos sin imports circulares.
- Hay un power-up con efecto temporal que baja con `dt`.
- El juego funciona igual que antes.

### Misión S01-N04-M2 · El récord de la Arena

```meta
entrega: archivo
monedas: 6
xp: 30
entorno: local
extensiones: py, zip
```

#### Consigna

Guardá el **mejor puntaje** en `record.json` (R02-N04) y mostralo en el menú. Si el archivo no existe o está roto, el récord arranca en 0 sin que el juego se corte (R02-N03).

#### Criterio de aprobación

- El récord se guarda y se lee con `json`.
- Un archivo inexistente o corrupto no corta el juego.
- El menú muestra el récord.

### Encargo S01-N04-E1 · Doscientos enemigos

```meta
entrega: archivo
monedas: 2
xp: 20
entorno: local
extensiones: py, zip
```

#### Consigna

Hacé que aparezcan **200 enemigos** y perfilá el juego con `cProfile` (R03-N06). Si la detección de choques es lo más lento, optimizala con celdas.

#### Criterio de aprobación

- Entrega la salida de `cProfile` antes y después.
- Explica qué optimizó y cuánto mejoró.

### Prueba del sello

#### ¿Para qué sirve organizar el juego en estados?

Para que cada pantalla (menú, juego, fin) maneje sus eventos y su dibujo sin mezclarse.

#### ¿Cómo funciona una cámara que sigue al jugador?

Todo se dibuja restando la posición de la cámara, que se mueve junto con el jugador.

### Soluciones (docente)

Material original: `17-Python/35-Pygame-Proyecto` (270 líneas). Conviene recorrer el código en clase antes de las misiones.
