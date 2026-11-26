# RAMA R04 · El Jardín de la Serpiente: Snake

```meta
tipo: tronco
posicion: 4
```

## R04-N01 · La grilla y la cabeza

```meta
tipo: tema
criatura: fantasma_fotograma
padre: R03-N07
precio: 10
temas: col.matrices
usa: juegos.bucle, juegos.entrada, prog.bucles
```

### Crónica

El cuarto pedazo de mapa lleva a un jardín escondido detrás de la plaza: canteros de flores de vidrio,
caminitos de baldosas y, en el medio, una máquina vieja con la pantalla dividida en cuadraditos, como un
cuaderno de matemática. —El Jardín de la Serpiente —dice {mentor}—. Acá no hay pelotas que rebotan: todo
se mueve de a un cuadradito, como las piezas de un tablero. Primero el tablero, después la serpiente.
Entre las flores, algo avanza a los saltos, unas veces rápido y otras lento: el **Fantasma del Fotograma**.

### Objetivos

Dibujar la **grilla** del jardín con dos `for`, poner la **cabeza** de la serpiente en una celda, hacerla
**avanzar de a una celda** cada un ratito con un reloj, cambiar la dirección con las **flechas** y que, si se
sale por un borde, **aparezca por el de enfrente**.

### Antes de empezar

Toda la escalera hasta acá. De R03: la grilla de la pared (N03). De R01: el delta time (N04) y las teclas
(N02).

### Explicación

#### Qué es el Snake
Una serpiente que avanza sola por un tablero de cuadraditos. Vos solo elegís para dónde dobla. Cada fruta que
come la hace más larga, y si se muerde la cola, perdiste. Todo se mueve **de a una celda**, no de a píxeles.

#### La grilla: celdas en lugar de píxeles
La ventana de 640 × 480 se divide en celdas de 20 × 20: 32 columnas y 24 filas. La cabeza no guarda dónde
está en píxeles, sino **en qué celda**: columna `x` y fila `y`. Recién al dibujar se pasa a píxeles,
multiplicando por `CELDA`: la celda `(5, 12)` empieza en el píxel `(100, 240)`.

#### Avanzar de a una celda: el reloj
Si la cabeza avanzara una celda en cada cuadro, cruzaría la pantalla en medio segundo. Se usa un reloj: en
cada cuadro se le suma el `dt`, y cuando junta `paso` segundos (0,15), la cabeza avanza **una** celda y al
reloj se le resta el paso. Así avanza siempre a la misma velocidad, en cualquier compu (el Fantasma del
Fotograma no puede hacer nada).

#### La dirección
`dx` y `dy` dicen para dónde va: `dx = 1` es una columna a la derecha en cada paso, `dy = -1` una fila para
arriba. Las flechas solo cambian esos dos números; el movimiento lo hace el reloj.

#### Del otro lado: el resto `%`
Si la cabeza pasa la columna 31, aparece en la 0; si baja de la 0, aparece en la 31. El operador `%` (el resto
de dividir) lo hace en una línea: `(x + COLS) % COLS`. Si `x` es 32, da 0; si es -1, da `31 % 32 = 31`. Se le
suma `COLS` antes para que nunca quede negativo.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }
        x = (x + COLS) % COLS;
        y = (y + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Pensar el mundo en **celdas** es la base del Tetris, del Pac-Man y de los juegos de tablero. Y el reloj que
junta tiempo para hacer algo «cada tanto» lo vas a usar para los enemigos, las oleadas y las animaciones.

### Errores habituales

**Mezclar celdas con píxeles.** `x += 20` mueve la cabeza 20 **celdas**, no una. En la grilla se suma de a 1 y
se multiplica por `CELDA` solo al dibujar.

**Avanzar en cada cuadro.** Sin el reloj, la serpiente va a 60 celdas por segundo y nadie la puede manejar.

**`reloj = 0` en lugar de `reloj -= paso`.** Se pierde el tiempo que sobró y la serpiente va un poquito más
lenta en las compus lentas: es el Fantasma del Fotograma.

**El resto de un negativo.** En C, `-1 % 32` da `-1`, no 31. Por eso se suma `COLS` antes: `(x + COLS) % COLS`.

### Micro-misión R04-N01-P1 · El tablero del jardín

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Grilla | for i hasta COLS: línea en x = i * CELDA · for j hasta FILAS: línea en y = j * CELDA
recompensa: xp 10, oro 10
```

#### Escena
{mentor} sopla el polvo de la pantalla: está toda negra, sin una sola línea. —Las máquinas del jardín
tenían el tablero dibujado, como baldosas —dice—. Treinta y dos de ancho, veinticuatro de alto.

#### Gheco sugiere
Las celdas miden `CELDA` (20) píxeles. Una línea vertical cada 20 píxeles y una horizontal cada 20 arman la
grilla. `SDL_RenderLine(lapiz, x1, y1, x2, y2)` dibuja una línea de un punto a otro:
```c
SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);   /* un verde apenas más claro que el fondo */
for (int i = 0; i <= COLS; i++) {
    SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);   /* de arriba abajo */
}
for (int j = 0; j <= FILAS; j++) {
    SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);   /* de izquierda a derecha */
}
```
`i * CELDA` es 0, 20, 40, 60… Va `<=` para dibujar también la línea del borde.

#### Desafío
Dibujá la grilla del jardín: una línea cada 20 píxeles, vertical y horizontal.

#### Pasos
1. Buscá el comentario `/* acá: las líneas de la grilla, una cada CELDA píxeles */`.
2. Debajo, escribí el color y los dos `for` de la sugerencia.
3. Tocá **Jugar**: tiene que verse el tablero. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;


        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        /* acá: las líneas de la grilla, una cada CELDA píxeles */
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 3
```

#### Estado
```
buscar #1e3228
```

#### Salida esperada
```
── Estado ──
buscar #1e3228: x 0, y 0, ancho 640, alto 480
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;


        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La pantalla se llena de cuadraditos verdes, parejitos, como las baldosas del caminito. Gheco salta de una
baldosa a otra del jardín, contando: —¡Uno, dos, tres…!

#### Imagen
- La pantalla de la máquina del jardín con una grilla de cuadraditos verdes sobre fondo oscuro.
- Arcadia sopla el polvo de la pantalla; Kira mira con curiosidad.
- Gheco salta de baldosa en baldosa en el caminito del jardín, contando con los dedos.

### Micro-misión R04-N01-P2 · Un paso cada tanto

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Reloj | reloj += dt · si reloj >= paso: reloj -= paso y la cabeza avanza una celda
recompensa: xp 10, monedas 4
```

#### Escena
En la pantalla hay un cuadradito verde claro: la cabeza de la serpiente. Pero está quieta, dormida. —La
serpiente del jardín no corre —dice {mentor}—: da pasitos. Uno cada un ratito, siempre igual.

#### Gheco sugiere
Ya están `reloj` (el tiempo juntado) y `paso` (0,15 segundos). En cada cuadro:
```c
reloj += dt;              /* junta el tiempo que pasó */
if (reloj >= paso) {      /* ¿ya juntó un paso? */
    reloj -= paso;        /* lo gasta */
    x += dx;              /* y avanza una celda */
    y += dy;
}
```
- `dt` es el tiempo del cuadro (unos 0,016 segundos): hacen falta unos 9 cuadros para juntar 0,15.
- Se le **resta** el paso, no se pone en 0: así no se pierde el pedacito que sobró.
- `dx` vale 1 y `dy` vale 0: avanza para la derecha.

#### Desafío
Hacé que la cabeza avance una celda cada 0,15 segundos, con un reloj que junta el tiempo.

#### Pasos
1. Buscá `/* acá: juntar el tiempo y, cada «paso» segundos, avanzar una celda */`.
2. Debajo, escribí las líneas del reloj de la sugerencia.
3. Tocá **Jugar**: la cabeza tiene que avanzar a pasitos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* acá: juntar el tiempo y, cada «paso» segundos, avanzar una celda */

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 60
```

#### Estado
```
buscar #78ff8c
```

#### Salida esperada
```
── Estado ──
buscar #78ff8c: x 220, y 240, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La cabeza avanza: *tic, tic, tic*, un cuadradito por vez, siempre al mismo ritmo. El Fantasma del Fotograma
trata de apurarla y de frenarla, pero el reloj no se deja. Se va a buscar otra máquina.

#### Imagen
- La pantalla con la grilla verde y un cuadradito verde claro avanzando de celda en celda, con huellas.
- Un fantasma redondo y translúcido, borroso, se aleja entre las flores, aburrido.
- Kira mira la pantalla; Arcadia lleva el ritmo con el pie; Gheco, sobre la máquina, mueve la cabeza al compás.

### Micro-misión R04-N01-P3 · Doblar con las flechas

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Dirección | flecha arriba: dx = 0, dy = -1 · abajo: dy = 1 · izquierda: dx = -1 · derecha: dx = 1
recompensa: xp 10, monedas 4
```

#### Escena
La cabeza avanza derecho hasta el borde, como si no tuviera volante. Kira aprieta las flechas, pero la
serpiente ni se entera. —Vos no la empujás —dice {mentor}—: le decís para dónde mirar.

#### Gheco sugiere
La cabeza siempre avanza `dx` columnas y `dy` filas en cada paso. Las flechas solo cambian esos dos números,
en los eventos (una vez por apretada):
```c
if (evento.type == SDL_EVENT_KEY_DOWN) {
    if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }      /* para arriba */
    if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }     /* para abajo */
    if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }    /* a la izquierda */
    if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }    /* a la derecha */
}
```
Si va para arriba, no va de costado: por eso siempre se cambian los dos. El movimiento lo sigue haciendo
el reloj. El robot va a apretar la flecha de arriba.

#### Desafío
Hacé que las flechas cambien hacia dónde avanza la cabeza.

#### Pasos
1. Buscá `/* acá: las flechas cambian hacia dónde va */` (en el `while` de los eventos).
2. Debajo, escribí el `if` con las cuatro flechas de la sugerencia.
3. Tocá **Jugar**, hacé clic en el juego y doblá con las flechas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: las flechas cambian hacia dónde va */
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Arriba
cuadros 40
```

#### Estado
```
buscar #78ff8c
```

#### Salida esperada
```
── Estado ──
buscar #78ff8c: x 100, y 160, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Kira aprieta la flecha de arriba y la cabeza dobla, obediente. Después a la izquierda, después abajo: dibuja
un cuadrado entero en el tablero. Gheco aplaude con la cola.

#### Imagen
- La pantalla con la grilla y el recorrido de la cabeza verde dibujando una esquina, con una flecha.
- Kira aprieta las flechas, concentrada; Arcadia sonríe.
- Gheco aplaude con la cola, sentado arriba de la máquina.

### Micro-misión R04-N01-P4 · Del otro lado

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Dar la vuelta | x = (x + COLS) % COLS · y = (y + FILAS) % FILAS
recompensa: xp 10, monedas 4
```

#### Escena
La cabeza llega al borde derecho… y se va de la pantalla. Gheco la busca detrás de la máquina, entre las
flores. —En el jardín del Vidriero no había cerco —dice {mentor}—: si salías por un lado, entrabas por el
otro.

#### Gheco sugiere
El resto de una división, `%`, sirve para «dar la vuelta». `33 % 32` es 1; `32 % 32` es 0. Si la columna se
pasa de 31, vuelve a empezar:
```c
x = (x + COLS) % COLS;
y = (y + FILAS) % FILAS;
```
¿Por qué `+ COLS`? Porque si la cabeza va para la izquierda y llega a -1, en C `-1 % 32` da -1. Sumando 32
antes, queda `31 % 32 = 31`: la última columna.

Va en cada cuadro, después del reloj. El robot va a dejar que la cabeza llegue al borde derecho.

#### Desafío
Hacé que si la cabeza sale por un borde, aparezca por el de enfrente.

#### Pasos
1. Buscá `/* acá: si se sale por un borde, aparece por el de enfrente */`.
2. Debajo, escribí las dos líneas con `%` de la sugerencia.
3. Tocá **Jugar** y dejá que llegue al borde. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }
        /* acá: si se sale por un borde, aparece por el de enfrente */

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 300
```

#### Estado
```
buscar #78ff8c
```

#### Salida esperada
```
── Estado ──
buscar #78ff8c: x 120, y 240, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }
        x = (x + COLS) % COLS;
        y = (y + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La cabeza se va por la derecha y aparece por la izquierda, como si nada. Gheco sale de atrás de la máquina,
desconcertado, y la encuentra del otro lado. —Un jardín sin cerco —se ríe Kira.

#### Imagen
- La pantalla con la cabeza verde saliendo por el borde derecho y apareciendo por el izquierdo, con flechas curvas.
- Gheco se asoma por detrás de la máquina, desconcertado.
- Kira se ríe; Arcadia señala el otro lado de la pantalla.

## R04-N02 · La cola que sigue

```meta
tipo: tema
criatura: glitch
padre: R04-N01
precio: 10
temas: col.arrays
usa: prog.bucles, juegos.entrada
```

### Crónica

Una cabeza sola no es una serpiente. {mentor} saca de un cantero cinco anillos de vidrio verde, enganchados
uno detrás del otro como un tren. —El cuerpo va siguiendo a la cabeza —explica—: cada anillo pisa donde estaba
el de adelante. Si lo armás mal, la cola se queda atrás o aparece donde no tiene que estar. Sobre la pantalla,
un **glitch** acomoda los anillos en un rincón, todos encimados, y se ríe.

### Objetivos

Guardar la serpiente en **dos arreglos** (la columna y la fila de cada parte), dibujar **todas** las partes,
armarla al empezar con cinco partes en fila, hacer que **cada parte siga a la de adelante** y que la serpiente
**no pueda dar media vuelta**.

### Antes de empezar

R04-N01 (la grilla y la cabeza). De R03: los arreglos y los `for` (N02). Del curso de C: recorrer un arreglo
de atrás para adelante.

### Explicación

#### La serpiente en dos arreglos
Cada parte de la serpiente está en una celda: tiene su columna y su fila. Dos arreglos las guardan:
`cx[i]` es la columna de la parte `i` y `cy[i]` su fila. La parte 0 es la **cabeza**; la última, la punta de la
cola. `largo` dice cuántas partes se usan. Los arreglos tienen lugar para `MAX` partes (todas las celdas del
jardín), porque la serpiente va a crecer.

#### Armarla en fila
Al empezar, la cabeza está en la columna 5 y las demás partes, una a la izquierda de la otra: 4, 3, 2 y 1. Es
`cx[i] = 5 - i`, todas en la fila 12.

#### Cada parte, adonde estaba la de adelante
El truco del Snake: en cada paso, **la cola sigue a la cabeza**. La parte 4 va adonde estaba la 3, la 3 adonde
estaba la 2… y la 1 adonde estaba la cabeza. Recién después la cabeza avanza a una celda nueva.

Hay que hacerlo **de atrás para adelante** (`i` desde `largo - 1` hasta 1): si se empezara por adelante, la
parte 1 copiaría la cabeza, la 2 copiaría a la 1 (que ya es la cabeza)… y todas terminarían encimadas en el
mismo lugar.

#### No dar media vuelta
Si la serpiente va para la derecha y se aprieta la izquierda, la cabeza se metería en su propio cuello. Por eso
cada flecha pregunta antes: la de la izquierda solo funciona si **no** va para la derecha (`dx != 1`).

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Mover una fila de cosas donde cada una sigue a la anterior sirve para colas de enemigos, para los vagones de un
tren y para los rastros de luz. Y recorrer un arreglo **de atrás para adelante** para no pisar datos es un truco
que se usa siempre que se corren elementos de lugar.

### Errores habituales

**Glitch: todas las partes en el rincón.** Si se dibujan todas las partes pero no se arman, las que no tienen
lugar quedan en `(0, 0)`: el rincón de arriba a la izquierda.

**Correr de adelante para atrás.** `for (i = 1; i < largo; i++)` copia la cabeza en todas: la serpiente queda
hecha una sola celda.

**Mover la cabeza antes que el cuerpo.** Si la cabeza avanza primero, la parte 1 copia la cabeza **nueva** y
quedan las dos encimadas.

**Media vuelta.** Sin las condiciones `dy != 1` y compañía, una flecha hacia atrás mete la cabeza en el cuello.

### Micro-misión R04-N02-P1 · Todas las partes

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Dibujar el cuerpo | for i < largo: rectángulo en (cx[i] * CELDA, cy[i] * CELDA) · la cabeza más clara
recompensa: xp 10, oro 10
```

#### Escena
La pantalla muestra solo la cabeza, aunque la serpiente ya tiene cinco partes guardadas. —Están, pero no se
ven —dice {mentor}—. Dibujalas todas, cada una en su celda.

#### Gheco sugiere
Ahora la serpiente está en dos arreglos, `cx` y `cy`, y `largo` dice cuántas partes tiene (5). En lugar de
dibujar solo la cabeza, un `for` dibuja cada parte en su celda:
```c
for (int i = 0; i < largo; i++) {
    SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
    if (i == 0) {
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
    } else {
        SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
    }
    SDL_RenderFillRect(lapiz, &parte);
}
```
Ojo: todavía no armamos las partes, así que puede pasar algo raro. Lo arreglamos en la que sigue.

#### Desafío
Dibujá todas las partes de la serpiente con un for, con la cabeza más clara que el cuerpo.

#### Pasos
1. Buscá `/* acá: dibujar todas las partes, no solo la cabeza */` y borrá las tres líneas de abajo (las de `cabeza`).
2. En su lugar, escribí el `for` de la sugerencia.
3. Tocá **Jugar** y mirá bien toda la pantalla. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    cx[0] = 5;
    cy[0] = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        /* acá: dibujar todas las partes, no solo la cabeza */
        SDL_FRect cabeza = { cx[0] * CELDA, cy[0] * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 3
```

#### Estado
```
buscar #28be5a
```

#### Salida esperada
```
── Estado ──
buscar #28be5a: x 0, y 0, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    cx[0] = 5;
    cy[0] = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Aparece el cuerpo… pero todo encimado en el rincón de arriba a la izquierda. Un glitch se ríe sentado
arriba de los anillos. —Se dibujan bien —dice {mentor}—. El problema es que no les dijimos dónde van.

#### Imagen
- La pantalla con la grilla, la cabeza verde clara en el medio y unos cuadraditos verdes encimados en el rincón de arriba a la izquierda.
- Un glitch pixelado se ríe sentado arriba de los cuadraditos del rincón.
- Kira se rasca la cabeza; Arcadia sostiene cinco anillos de vidrio verde enganchados; Gheco señala el rincón.

### Micro-misión R04-N02-P2 · Cinco en fila

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: Armar | for i < largo: cx[i] = 5 - i · cy[i] = 12
recompensa: xp 10, monedas 4
```

#### Escena
{mentor} acomoda los cinco anillos de vidrio en el caminito, uno detrás del otro. —La cabeza adelante y
el resto atrás, en fila —dice—. Así tiene que arrancar la serpiente.

#### Gheco sugiere
Las partes que no se armaron valen 0: por eso aparecían en la celda `(0, 0)`, el rincón. Al empezar, se
arman en fila:
```c
for (int i = 0; i < largo; i++) {
    cx[i] = 5 - i;   /* la cabeza en la 5, las demás en 4, 3, 2 y 1 */
    cy[i] = 12;      /* todas en la fila 12 */
}
```
Reemplaza a las dos líneas que armaban solo la cabeza.

#### Desafío
Armá la serpiente al empezar: cinco partes en fila, con la cabeza adelante.

#### Pasos
1. Buscá `/* acá: armar la serpiente: cinco partes en fila, con la cabeza adelante */` y borrá las dos líneas de abajo.
2. En su lugar, escribí el `for` de la sugerencia.
3. Tocá **Jugar**: la serpiente tiene que aparecer entera, en fila. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    /* acá: armar la serpiente: cinco partes en fila, con la cabeza adelante */
    cx[0] = 5;
    cy[0] = 12;
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 3
```

#### Estado
```
buscar #28be5a
```

#### Salida esperada
```
── Estado ──
buscar #28be5a: x 20, y 240, ancho 80, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La serpiente aparece entera en el medio del jardín, cinco cuadraditos en fila. El glitch se queda sin
rincón donde esconderse y se deshace en píxeles.

#### Imagen
- La pantalla con la grilla y una serpiente de cinco cuadraditos verdes en fila, la cabeza más clara.
- Un glitch pixelado se deshace en píxeles al costado de la pantalla.
- Arcadia acomoda cinco anillos de vidrio verde en fila sobre el caminito; Kira y Gheco miran.

### Micro-misión R04-N02-P3 · La cola que sigue

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Seguir | for i desde largo - 1 hasta 1: cx[i] = cx[i - 1] · cy[i] = cy[i - 1] · después avanza la cabeza
recompensa: xp 10, monedas 4
```

#### Escena
La cabeza avanza, pero el cuerpo se queda quieto atrás, como un tren sin enganche. Gheco se ríe tan fuerte
que se cae de la máquina. —Cada anillo tiene que pisar donde estaba el de adelante —dice {mentor}.

#### Gheco sugiere
En cada paso, **antes** de que la cabeza avance, cada parte se corre adonde estaba la de adelante:
```c
for (int i = largo - 1; i > 0; i--) {
    cx[i] = cx[i - 1];   /* la parte i va adonde estaba la i - 1 */
    cy[i] = cy[i - 1];
}
```
- Empieza por la **última** (`largo - 1`) y termina en la 1. La cabeza (0) no se copia: avanza después.
- ¿Por qué de atrás para adelante? Si se empezara por la 1, copiaría la cabeza; la 2 copiaría a la 1 (que
  ya es la cabeza)… y todas quedarían encimadas.

#### Desafío
Hacé que en cada paso cada parte vaya adonde estaba la de adelante, antes de mover la cabeza.

#### Pasos
1. Buscá `/* acá: cada parte va adonde estaba la de adelante (de atrás para adelante) */` (adentro del `if` del reloj).
2. Debajo, escribí el `for` de la sugerencia, que va de `largo - 1` hasta 1.
3. Tocá **Jugar** y doblá con las flechas: el cuerpo tiene que seguir a la cabeza. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            /* acá: cada parte va adonde estaba la de adelante (de atrás para adelante) */
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 60
```

#### Estado
```
buscar #28be5a
```

#### Salida esperada
```
── Estado ──
buscar #28be5a: x 140, y 240, ancho 80, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Ahora el cuerpo sigue a la cabeza por cada esquina, como un tren enganchado. Kira dibuja una S en la
pantalla y la serpiente la copia, anillo por anillo.

#### Imagen
- La pantalla con una serpiente verde doblando una esquina, el cuerpo siguiendo exactamente el camino de la cabeza.
- Kira dobla con las flechas, contenta; Arcadia asiente.
- Gheco, recién caído de la máquina, se ríe en el piso del jardín.

### Micro-misión R04-N02-P4 · Sin media vuelta

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Solo doblar | izquierda si dx != 1 · derecha si dx != -1 · arriba si dy != 1 · abajo si dy != -1
recompensa: xp 10, monedas 4
```

#### Escena
Kira aprieta la flecha de la izquierda mientras la serpiente va para la derecha, y la cabeza se da vuelta y
se mete en su propio cuello. —Eso no lo hace ninguna serpiente —dice {mentor}—. Doblan, pero no dan media
vuelta.

#### Gheco sugiere
Cada flecha tiene que preguntar antes si no es justo **la contraria** de hacia dónde va:
```c
if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }      /* arriba, si no iba para abajo */
if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }    /* abajo, si no iba para arriba */
if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }    /* izquierda, si no iba a la derecha */
if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }   /* derecha, si no iba a la izquierda */
```
`!=` es «distinto de». El robot va a apretar la izquierda mientras la serpiente va para la derecha.

#### Desafío
Hacé que la serpiente pueda doblar pero no dar media vuelta.

#### Pasos
1. Buscá `/* acá: no se puede dar media vuelta, solo doblar */` y borrá las cuatro líneas de abajo.
2. En su lugar, escribí las cuatro de la sugerencia, con su condición cada una.
3. Tocá **Jugar** y probá apretar la flecha contraria. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                /* acá: no se puede dar media vuelta, solo doblar */
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Izquierda
cuadros 30
```

#### Estado
```
buscar #78ff8c
```

#### Salida esperada
```
── Estado ──
buscar #78ff8c: x 160, y 240, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La flecha contraria ya no hace nada: la serpiente sigue su camino, tranquila. Kira dobla para arriba, después
a la izquierda, y recién ahí vuelve: en dos esquinas, como una serpiente de verdad.

#### Imagen
- La pantalla con la serpiente verde haciendo una vuelta en U por dos esquinas, con flechas curvas.
- Kira prueba las flechas, divertida; Arcadia le explica con las manos cómo dobla una serpiente.
- Gheco imita una serpiente con su cola, sentado arriba de la máquina.

## R04-N03 · La fruta y crecer

```meta
tipo: tema
criatura: fuga_texturas
padre: R04-N02
precio: 10
usa: col.arrays, prog.matematica-azar, juegos.bucle
```

### Crónica

La serpiente ya pasea por el jardín, pero no tiene para qué. {mentor} arranca una fruta roja de vidrio de un
arbolito y la deja en el caminito. —En el Snake se juega a comer —dice—. Cada fruta, un punto. Y cada fruta,
la serpiente crece un anillo. Cuanto más larga, más difícil no morderse. Sobre las flores flota una niebla de
frutas repetidas, todas iguales: la **Fuga de Texturas**, que dibuja cada fruta mil veces sin borrar ninguna.

### Objetivos

Poner una **fruta** en una celda, que la serpiente **se la coma** (un punto y una fruta nueva en un lugar al
azar), que **crezca** un anillo con cada fruta y que vaya **cada vez más rápido**, sin pasarse de un tope.

### Antes de empezar

R04-N02 (la cola). De R01: el azar con `SDL_rand` (N10). De R03: la pelota que se apura con un tope (N04).

### Explicación

#### La fruta
Una celda más, con su columna `fx` y su fila `fy`. Arranca en `(20, 12)`, justo en el camino de la serpiente,
para que la primera sea fácil. Se dibuja igual que una parte de la serpiente, pero roja.

#### Comer
La cabeza se come la fruta cuando están **en la misma celda**: `cx[0] == fx && cy[0] == fy`. En la grilla no
hace falta la prueba de los dos rectángulos: alcanza con comparar dos números. Se suma un punto y la fruta pasa a
otra celda al azar: `SDL_rand(COLS)` da una columna de 0 a 31 y `SDL_rand(FILAS)` una fila de 0 a 23.

#### Crecer
La parte nueva aparece **encima de la última** (`cx[largo] = cx[largo - 1]`) y recién después se suma uno a
`largo`. En el paso siguiente, todo el cuerpo se corre y la última parte se queda donde estaba: la parte nueva
queda atrás, en la punta de la cola. Así la serpiente crece sin que se vea ningún salto.

#### Cada vez más rápido
Con cada fruta, `paso` se multiplica por 0,9 (un 10 % menos de espera entre pasos). `SDL_max(0.06f, …)` lo frena
en 0,06 segundos: más rápido que eso, nadie podría doblar a tiempo.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Comparar celdas para saber si dos cosas se tocan, poner premios al azar y hacer que el juego se acelere a medida
que ganás son tres ideas que vas a usar en todos los juegos de tablero y de laberinto.

### Errores habituales

**Crecer sin copiar la última parte.** Si solo se hace `largo++`, la parte nueva tiene lo que haya en el arreglo
(un 0): aparece un cuadradito suelto en el rincón por un instante.

**Usar `SDL_rand(32)` a mano.** Funciona, pero si mañana cambiás el tamaño de la grilla, la fruta puede caer
afuera. Mejor `SDL_rand(COLS)`.

**Acelerar sin tope.** Después de 30 frutas, `paso` sería tan chico que la serpiente cruzaría la pantalla en un
segundo.

**Fuga de Texturas.** Si se dibujara la fruta cargando una imagen nueva en cada cuadro sin liberarla, la memoria
se llenaría. Acá se dibuja un rectángulo: no hay nada que liberar.

### Micro-misión R04-N03-P1 · Una fruta en el camino

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Dibujar la fruta | SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA } · roja
recompensa: xp 10, oro 10
```

#### Escena
{mentor} deja la fruta de vidrio en el caminito, justo delante de la serpiente. En la pantalla, en cambio,
no hay nada. —La máquina sabe dónde está —dice—, pero no la dibuja.

#### Gheco sugiere
Ya están `fx` y `fy`: la columna y la fila de la fruta (20 y 12, en el camino). Se dibuja como una parte de
la serpiente, pasando de celda a píxeles, pero roja. Va **antes** de la serpiente, para que la serpiente
quede arriba cuando pasa:
```c
SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);   /* rojo frutilla */
SDL_RenderFillRect(lapiz, &fruta);
```

#### Desafío
Dibujá la fruta roja en su celda, antes que la serpiente.

#### Pasos
1. Buscá `/* acá: dibujar la fruta en su celda, roja */`.
2. Debajo, escribí las tres líneas de la sugerencia.
3. Tocá **Jugar**: tiene que aparecer la fruta en el camino. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        /* acá: dibujar la fruta en su celda, roja */
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 3
```

#### Estado
```
buscar #ff465a
```

#### Salida esperada
```
── Estado ──
buscar #ff465a: x 400, y 240, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Un cuadradito rojo se enciende en el camino de la serpiente. Gheco se relame. —Esa no es para vos —le dice
Kira, riéndose.

#### Imagen
- La pantalla con la grilla verde, la serpiente en fila y un cuadradito rojo más adelante, en su camino.
- Arcadia deja una fruta roja de vidrio en el caminito del jardín; Kira mira la pantalla.
- Gheco se relame mirando la fruta, sentado arriba de la máquina.

### Micro-misión R04-N03-P2 · ¡A comer!

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Comer | si cx[0] == fx y cy[0] == fy: puntos++ · fx = SDL_rand(COLS) · fy = SDL_rand(FILAS)
recompensa: xp 10, monedas 4
```

#### Escena
La serpiente pasa por encima de la fruta y la fruta sigue ahí, como si fuera de vidrio de verdad. —Tiene que
comérsela —dice {mentor}—. Y después, que aparezca otra en cualquier lado.

#### Gheco sugiere
Ya está el `if` que pregunta si la cabeza está en la misma celda que la fruta: `cx[0] == fx && cy[0] == fy`.
En la grilla alcanza con comparar números. Adentro falta lo que pasa al comer:
```c
puntos++;                 /* un punto más */
fx = SDL_rand(COLS);      /* una columna al azar, de 0 a 31 */
fy = SDL_rand(FILAS);     /* una fila al azar, de 0 a 23 */
```
Y los puntos, arriba a la izquierda:
```c
SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
```

#### Desafío
Hacé que la serpiente se coma la fruta: un punto y una fruta nueva en un lugar al azar.

#### Pasos
1. Buscá `/* acá: un punto y una fruta nueva en un lugar al azar */` (adentro del `if` de la fruta) y escribí las tres líneas.
2. Buscá `/* acá: los puntos arriba a la izquierda */` y escribí las dos líneas de los puntos.
3. Tocá **Jugar** y dejá que la serpiente llegue a la fruta. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            /* acá: un punto y una fruta nueva en un lugar al azar */
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        /* acá: los puntos arriba a la izquierda */
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 160
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 1
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
*¡Ñam!* La fruta desaparece, arriba se enciende **PUNTOS 1** y otra fruta aparece en otra punta del jardín.
Kira ya está doblando para ir a buscarla.

#### Imagen
- La pantalla con la serpiente verde comiéndose la fruta roja con unas chispitas, y otra fruta roja lejos.
- Kira dobla con las flechas, decidida; Arcadia aplaude.
- Gheco, sentado arriba de la máquina, hace como que mastica.

### Micro-misión R04-N03-P3 · Un anillo más

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Crecer | cx[largo] = cx[largo - 1] · cy[largo] = cy[largo - 1] · largo++
recompensa: xp 10, monedas 4
```

#### Escena
La serpiente come y come, pero sigue igual de cortita. —En el Snake, cada fruta es un anillo más —dice
{mentor}, y engancha un anillo de vidrio nuevo en la cola de la serpiente del caminito.

#### Gheco sugiere
Crecer es sumar una parte al final. La parte nueva aparece **encima de la última** y después se agranda el
largo:
```c
cx[largo] = cx[largo - 1];   /* la nueva, donde está la última */
cy[largo] = cy[largo - 1];
largo++;
```
- `cx[largo]` es el primer lugar libre del arreglo (si hay 5 partes, son de la 0 a la 4: la 5 está libre).
- En el paso siguiente el cuerpo se corre, pero la parte nueva copia a la que estaba en su mismo lugar:
  así queda atrás, en la punta de la cola.

Va adentro del `if` de la fruta, después de los puntos.

#### Desafío
Hacé que la serpiente crezca una parte cada vez que come una fruta.

#### Pasos
1. Buscá `/* acá: crecer: una parte nueva, encima de la última */` (adentro del `if` de la fruta).
2. Debajo, escribí las tres líneas de la sugerencia.
3. Tocá **Jugar**, comé la fruta y mirá la cola. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            /* acá: crecer: una parte nueva, encima de la última */
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 160
```

#### Estado
```
buscar #28be5a
```

#### Salida esperada
```
── Estado ──
buscar #28be5a: x 360, y 240, ancho 100, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La serpiente se come la fruta y, un paso después, tiene un anillo más en la cola. Kira cuenta: seis. —Cuanto
más larga, más cuidado —le avisa {mentor}.

#### Imagen
- La pantalla con la serpiente verde un poco más larga, con un anillo nuevo brillando en la punta de la cola.
- Arcadia engancha un anillo de vidrio verde nuevo a la cola de la serpiente de anillos del caminito.
- Kira cuenta con los dedos; Gheco, sobre la máquina, levanta seis dedos.

### Micro-misión R04-N03-P4 · Cada vez más rápido

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Apurar con tope | paso = SDL_max(0.06f, paso * 0.9f)
recompensa: xp 10, monedas 4
```

#### Escena
Con diez frutas, Kira juega con una mano. —Muy fácil —dice, y bosteza. {mentor} sonríe: —En el jardín del
Vidriero, la serpiente se apuraba con cada fruta. Al final había que tener reflejos de gato.

#### Gheco sugiere
`paso` es cuánto espera la serpiente entre un paso y otro. Si se achica, va más rápido. Con cada fruta:
```c
paso = SDL_max(0.06f, paso * 0.9f);
```
- `paso * 0.9f` es un 10 % menos de espera: 0,15, después 0,135, después 0,12…
- `SDL_max(a, b)` da el más grande de los dos: si `paso * 0.9f` baja de 0,06, queda en 0,06. Es el tope:
  más rápido que eso, nadie podría doblar.

Va adentro del `if` de la fruta. El robot va a dejar que coma la primera y a mirar dónde llega después.

#### Desafío
Hacé que la serpiente vaya un 10 % más rápido con cada fruta, sin bajar de 0,06 segundos por paso.

#### Pasos
1. Buscá `/* acá: cada fruta, un poco más rápido (con un tope) */`.
2. Debajo, escribí la línea con `SDL_max` de la sugerencia.
3. Tocá **Jugar** y comé varias frutas: tiene que ir cada vez más rápido. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            /* acá: cada fruta, un poco más rápido (con un tope) */
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 300
```

#### Estado
```
buscar #78ff8c
```

#### Salida esperada
```
── Estado ──
buscar #78ff8c: x 160, y 240, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Fruta tras fruta, la serpiente se apura. Kira deja de bostezar y agarra el teclado con las dos manos. La
niebla de frutas repetidas de la Fuga de Texturas no alcanza a seguirla y se deshace en el aire.

#### Imagen
- La pantalla con una serpiente verde larga avanzando rápido, con líneas de velocidad, hacia una fruta roja.
- Una niebla de frutas repetidas, todas iguales, se deshace en el aire entre las flores.
- Kira juega con las dos manos, concentrada; Arcadia se ríe; Gheco se agarra de la máquina.

## R04-N04 · Morderse, menú y revancha

```meta
tipo: tema
criatura: bucle_eterno
padre: R04-N03
precio: 10
temas: juegos.estados
usa: juegos.sonido, col.arrays
```

### Crónica

La serpiente ya es larguísima y Kira la enrosca por todo el jardín. En una curva cerrada, la cabeza pasa por
encima de su propia cola… y no pasa nada: sigue como si fuera un fantasma. Debajo de la máquina, una serpiente de
luz violeta se muerde la cola y da vueltas sin parar: el **Bucle Eterno**. —Así no se pierde nunca —dice
{mentor}—. Y un juego en el que no se puede perder se termina aburriendo.

### Objetivos

Que la serpiente **pierda si se muerde** (y se quede quieta con un cartel), que el juego arranque en un **menú**,
que se pueda **volver a jugar** con la R dejando todo como al principio y que **suene** al empezar y al comer.

### Antes de empezar

R04-N03. De R03: los estados con `enum` y la revancha (N05) y el sonido con `pitido` (N06).

### Explicación

#### Morderse
La serpiente se muerde cuando la cabeza está en la misma celda que **alguna otra parte** de su cuerpo. Un `for`
recorre las partes de la 1 en adelante (la 0 es la propia cabeza) y compara: si alguna coincide, perdiste.

#### Estados
Como en el Arkanoid: un `enum` con `MENU`, `JUGANDO` y `PERDISTE`. El reloj solo junta tiempo mientras se juega:
en el menú y después de perder, la serpiente se queda quieta.

#### La revancha
Con la R, si perdiste, todo vuelve a como empezó: cinco partes en fila, para la derecha, 0 puntos, la velocidad
del principio y la fruta en su lugar. Es el mismo código del comienzo, copiado en el `if` de la R.

#### El sonido
La función `pitido` de siempre: un *tin* al empezar la partida y un *ñam* agudo cada vez que come.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Detectar que algo choca contra sí mismo (una cola, un rastro, una fila) aparece en muchos juegos: el Tron, los
trenes, las carreras de motos de luz. Y el menú, el fin y la revancha ya son el esqueleto de todos tus juegos.

### Errores habituales

**Compararse con la cabeza.** Si el `for` empieza en 0, la cabeza siempre «coincide» consigo misma y se pierde
al instante.

**Bucle Eterno: no poder perder.** Sin el chequeo, la serpiente pasa por encima de sí misma para siempre.

**Seguir moviéndose después de perder.** Si el reloj no mira el estado, la serpiente sigue avanzando con el
cartel puesto.

**Revancha a medias.** Si la R no devuelve la velocidad, la partida nueva arranca rapidísima.

### Micro-misión R04-N04-P1 · Te mordiste

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
criatura: bucle_eterno
carta: Morderse | for i desde 1: si cx[i] == cx[0] y cy[i] == cy[0]: PERDISTE · el reloj solo corre si JUGANDO
recompensa: xp 10, oro 10
```

#### Escena
La cabeza pasa por encima de la cola como si nada. El Bucle Eterno se ríe, enroscado debajo de la máquina.
—Una serpiente que se muerde, se enreda —dice {mentor}—. Y ahí termina la partida.

#### Gheco sugiere
Ya están el `enum Estado { JUGANDO, PERDISTE };` y la variable `estado`. Tres cosas:
1. **Morderse:** después de mover, un `for` compara la cabeza con cada parte del cuerpo:
```c
for (int i = 1; i < largo; i++) {          /* desde la 1: la 0 es la cabeza */
    if (cx[i] == cx[0] && cy[i] == cy[0]) {
        estado = PERDISTE;
    }
}
```
2. **Quedarse quieta:** el reloj solo junta tiempo si se está jugando:
```c
if (estado == JUGANDO) {
    reloj += dt;
}
```
3. **El cartel:** `if (estado == PERDISTE)`, el texto `TE MORDISTE` en `(276, 220)`.

El robot va a doblar arriba, izquierda y abajo, bien cerrado, para que se muerda.

#### Desafío
Hacé que la serpiente pierda si la cabeza pisa su cuerpo, que se quede quieta y que aparezca el cartel.

#### Pasos
1. Buscá `/* acá: si la cabeza pisa una parte de su cuerpo, perdiste */` y escribí el `for` de la sugerencia.
2. Buscá `/* acá: el reloj solo corre mientras se juega */` y envolvé `reloj += dt;` con el `if (estado == JUGANDO)`.
3. Buscá `/* acá: el cartel si te mordiste */` y escribí el `if` con `TE MORDISTE`.
4. Tocá **Jugar** y hacé una vuelta bien cerrada. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

enum Estado { JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = JUGANDO;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* acá: el reloj solo corre mientras se juega */
        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* acá: si la cabeza pisa una parte de su cuerpo, perdiste */

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        /* acá: el cartel si te mordiste */
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Arriba
cuadros 10
tecla Izquierda
cuadros 10
tecla Abajo
cuadros 30
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0 | TE MORDISTE
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

enum Estado { JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = JUGANDO;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La cabeza se choca con la cola, la serpiente se queda quieta y aparece **TE MORDISTE**. El Bucle Eterno suelta
su propia cola, mareado, y se escurre entre las flores.

#### Imagen
- La pantalla con la serpiente verde enroscada, la cabeza tocando su propio cuerpo, quieta, con un cartel blanco en el medio (sin texto legible).
- Una serpiente de luz violeta suelta su propia cola, mareada, debajo de la máquina.
- Kira se tapa la cara riéndose; Gheco, sobre la máquina, se enreda la cola a propósito.

### Micro-misión R04-N04-P2 · El menú del jardín

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco
carta: Menú | enum { MENU, JUGANDO, PERDISTE } · arrancar en MENU · espacio en el menú: JUGANDO
recompensa: xp 10, monedas 4
```

#### Escena
La serpiente arranca apenas se prende la máquina, antes de que nadie agarre el teclado. Un chico del barrio
llega corriendo y ya perdió. —Que espere —dice Kira—. Con un cartel, como el Muro.

#### Gheco sugiere
Como en el Arkanoid: un estado nuevo, el **primero** del `enum`. Cuatro cosas:
1. El `enum`: `enum Estado { MENU, JUGANDO, PERDISTE };`
2. Arrancar en el menú: `enum Estado estado = MENU;`
3. En los eventos, el espacio empieza:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
    estado = JUGANDO;
}
```
4. El menú, al final del dibujo:
```c
if (estado == MENU) {
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_SetRenderScale(lapiz, 5, 5);
    SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
    SDL_SetRenderScale(lapiz, 1, 1);
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
    SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
}
```
Como el reloj solo corre jugando, en el menú la serpiente espera sola.

#### Desafío
Hacé que el juego empiece en un menú y que el espacio arranque la partida.

#### Pasos
1. Buscá `/* acá: un estado más, el primero: el menú */` y cambiá el `enum` de abajo.
2. Buscá `/* acá: arrancar en el menú */` y cambiá `JUGANDO` por `MENU`.
3. Buscá `/* acá: en el menú, el espacio empieza la partida */` y escribí el `if` del espacio.
4. Buscá `/* acá: el menú: el nombre grande y cómo empezar */` y escribí el `if (estado == MENU)`.
5. Tocá **Jugar**: tiene que esperar en el menú. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

/* acá: un estado más, el primero: el menú */
enum Estado { JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    /* acá: arrancar en el menú */
    enum Estado estado = JUGANDO;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: en el menú, el espacio empieza la partida */
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        /* acá: el menú: el nombre grande y cómo empezar */
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 5
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0 | EL JARDIN | ESPACIO: JUGAR
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La pantalla se enciende con **EL JARDIN** en letras amarillas y la serpiente quieta abajo, esperando. El chico
aprieta el espacio cuando está listo y sonríe.

#### Imagen
- La pantalla de la máquina del jardín con un título enorme de bloques amarillos (sin texto legible) y la serpiente quieta abajo.
- Un chico del barrio con abrigo cerrado, listo, con el dedo sobre la barra espaciadora.
- Kira le muestra cómo; Gheco, arriba de la máquina, levanta los brazos.

### Micro-misión R04-N04-P3 · Otra vuelta

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Revancha | R si PERDISTE: largo = 5 y en fila · dx = 1, dy = 0 · puntos = 0 · paso = 0.15f · fruta en (20, 12) · JUGANDO
recompensa: xp 10, monedas 4
```

#### Escena
El chico se muerde y se queda mirando el cartel. —¿Y ahora? —pregunta. Hay que apagar la máquina para volver
a jugar. —Una vuelta más —dice {mentor}—. Con la R, como en el Muro.

#### Gheco sugiere
Con la R, si perdiste, todo vuelve a como empezó. Es el mismo código del principio, en un `if`:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
    largo = 5;
    for (int i = 0; i < largo; i++) {   /* otra vez en fila */
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    dx = 1;          /* para la derecha */
    dy = 0;
    puntos = 0;
    paso = 0.15f;    /* la velocidad del principio */
    fx = 20;         /* la fruta en su lugar */
    fy = 12;
    estado = JUGANDO;
}
```
Y un cartelito que avise, `R: OTRA VEZ` en `(276, 244)`, cuando `estado == PERDISTE`.

#### Desafío
Hacé que con la R se vuelva a jugar con todo como al principio.

#### Pasos
1. Buscá `/* acá: con la R, todo como al principio */` (en los eventos) y escribí el `if` de la sugerencia.
2. Buscá `/* acá: cómo volver a jugar */` y escribí el cartel `R: OTRA VEZ`.
3. Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            /* acá: con la R, todo como al principio */
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        /* acá: cómo volver a jugar */
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Espacio
tecla Arriba
cuadros 10
tecla Izquierda
cuadros 10
tecla Abajo
cuadros 30
tecla R
cuadros 5
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
El chico aprieta la R y la serpiente vuelve a aparecer cortita, en fila, lista. Juega otra vez, y otra, y
otra. Detrás de él ya se armó una fila.

#### Imagen
- La máquina del jardín con la serpiente cortita otra vez en fila en la pantalla.
- Un chico del barrio con abrigo cerrado aprieta una tecla, feliz; detrás, una fila de chicos espera.
- Kira y Arcadia chocan los cinco; Gheco, arriba de la máquina, saluda a los chicos.

### Micro-misión R04-N04-P4 · Ñam

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia
carta: Sonido | al empezar: pitido 440 · al comer: pitido 660
recompensa: xp 10, monedas 4
```

#### Escena
La máquina funciona, pero en silencio. —En el jardín se escuchaba un *ñam* cada vez que la serpiente comía
—recuerda {mentor}—. Los chicos lo imitaban.

#### Gheco sugiere
Ya está todo para el sonido: el parlante abierto y la función `pitido` de siempre. Faltan dos llamadas:
1. Al empezar la partida: un `if` igual al del menú, que va **antes** que él (después ya no está en el
   menú):
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
    pitido(parlante, 440, 0.08f);
}
```
2. Al comer, adentro del `if` de la fruta: `pitido(parlante, 660, 0.06f);` (más agudo).

El robot va a apretar el espacio y escuchar.

#### Desafío
Hacé que suene un tin al empezar y un ñam agudo cada vez que la serpiente come.

#### Pasos
1. Buscá `/* acá: un tin al empezar (el espacio en el menú) */` y escribí el `if` con el `pitido` de la sugerencia.
2. Buscá `/* acá: el ñam de la fruta */` y escribí `pitido(parlante, 660, 0.06f);`.
3. Tocá **Jugar** (con el volumen prendido) y escuchá. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: un tin al empezar (el espacio en el menú) */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            /* acá: el ñam de la fruta */
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Espacio
cuadros 5
```

#### Estado
```
sonido
```

#### Salida esperada
```
── Estado ──
sonido: sí
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
*Tin*… y después *ñam, ñam, ñam*. Los chicos de la fila hacen *ñam* cada vez que la serpiente come, y se
ríen. Hasta Arcadia lo hace.

#### Imagen
- La máquina del jardín con anillos de sonido saliendo de la pantalla mientras la serpiente se come una fruta.
- Chicos del barrio con abrigos cerrados hacen como que mastican, riéndose.
- Kira juega; Arcadia se ríe; Gheco, sobre la máquina, abre grande la boca.

## R04-N05 · Jefe: La Serpiente Jardinera

```meta
tipo: jefe
criatura: glitch
padre: R04-N04
precio: 10
insignia: Sello del Jardín de la Serpiente
insignia_descripcion: Despertaste a la Serpiente Jardinera: un Snake entero, con la grilla, la cola que sigue, la fruta al azar en un lugar libre, la fruta dorada, las macetas, el menú, la revancha y el sonido.
temas: prog.funciones
usa: juegos.estados, col.arrays, prog.matematica-azar, juegos.bucle
```

### Crónica

Cuando la serpiente de la pantalla llega a doce anillos, las flores de vidrio se apagan todas juntas. Del cantero
más grande se desenrosca una serpiente de luz enorme, verde y dorada, con un sombrerito de paja de jardinera y una
regadera colgada de la cola. —¡Por fin alguien que cuida mi jardín! —dice, con voz de abuela contenta—. Treinta
años sin que nadie juegue. Pero mi jardín tiene macetas, y frutas que se esconden, y frutas de oro que no esperan
a nadie. Llegá a quince anillos y mis flores se vuelven a encender. Es **la Serpiente Jardinera**, la que el
Vidriero dejó cuidando el jardín.

### Objetivos

Terminar el Snake completo contra la Serpiente Jardinera: **macetas** que estorban (chocarlas es perder), una
**función** que dice si una celda está libre para que la fruta nunca caiga encima de nada, una **fruta dorada**
que aparece cada tanto y se va si no la agarrás, y un **cartel final centrado** que dice si el jardín floreció.

### Antes de empezar

Toda la rama R04. De R03: el temporizador (N07) y el cartel centrado. Del curso de C: las funciones que devuelven
`bool` y el `do … while`.

### Explicación

#### Las macetas
Seis macetas en celdas fijas, en dos arreglos constantes `MX` y `MY` (como la serpiente, pero no se mueven). Se
dibujan marrones y, si la cabeza llega a la celda de una, perdiste: igual que morderse, pero contra una maceta.

#### Una función que pregunta
`libre(x, y, …)` devuelve `true` si en la celda `(x, y)` no hay ninguna parte de la serpiente ni ninguna maceta.
Recorre las dos cosas y, apenas encuentra algo ahí, devuelve `false` (`return` corta la función en el momento).
Si llega al final sin encontrar nada, devuelve `true`.

#### Probar hasta que salga bien: `do … while`
Para poner la fruta, se elige una celda al azar y, **si no está libre, se elige otra**, hasta que salga una libre.
`do { … } while (condición);` hace el bloque **por lo menos una vez** y lo repite mientras la condición sea
verdadera. Es justo lo que hace falta: elegir primero, preguntar después.

#### La fruta dorada
Un temporizador, `relojDorado`. Cuando junta 8 segundos sin fruta dorada, aparece una en un lugar libre; cuando
junta 4 con la fruta en el jardín, se va. Si la cabeza la alcanza antes, son 5 puntos.

#### El cartel del final
Cuando la partida termina, el cartel depende del largo: con 15 partes o más, «EL JARDIN FLORECE»; si no, «TE
ENREDASTE». Centrado como siempre: `320 - letras * 4`.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    bool hayDorada = false;   /* true: hay una fruta dorada en el jardín */
    int gx = 0;               /* la fruta dorada: columna y fila */
    int gy = 0;
    float relojDorado = 0;    /* cuánto pasó desde que apareció (o desde que se fue) */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }

        if (estado == JUGANDO) {
            relojDorado += dt;
            if (!hayDorada && relojDorado >= 8) {
                do {
                    gx = SDL_rand(COLS);
                    gy = SDL_rand(FILAS);
                } while (!libre(gx, gy, cx, cy, largo));
                hayDorada = true;
                relojDorado = 0;
            }
            if (hayDorada && relojDorado >= 4) {
                hayDorada = false;
                relojDorado = 0;
            }
            if (hayDorada && cx[0] == gx && cy[0] == gy) {
                puntos += 5;
                hayDorada = false;
                relojDorado = 0;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        if (hayDorada) {
            SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
            SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
            SDL_RenderFillRect(lapiz, &dorada);
        }
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            const char *cartel = (largo >= 15) ? "EL JARDIN FLORECE" : "TE ENREDASTE";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Una función que responde una pregunta («¿esta celda está libre?») se usa en todos los juegos de grilla: para
poner enemigos, premios, piezas del Tetris o fantasmas. Y el Snake completo es tu tercer juego entero: lo vas a
poder bajar y jugar en tu compu.

### Errores habituales

**La fruta encima de una maceta.** Sin `libre`, la fruta puede caer debajo de una maceta y nadie la puede comer.

**`while` en lugar de `do … while`.** Con `while (!libre(fx, fy, …))` se pregunta por la fruta vieja antes de
elegir la nueva. El `do` elige primero.

**La fruta dorada eterna.** Si no se vuelve el reloj a 0 al aparecer, la fruta dorada desaparece apenas aparece
(el reloj ya pasaba de 4).

**Glitch: chocar macetas invisibles.** Si se chequea el choque con una lista de macetas y se dibuja otra, la
serpiente choca contra la nada.

### Micro-misión R04-N05-P1 · Las macetas

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia, la Serpiente Jardinera
carta: Obstáculos | dibujar MX[m], MY[m] marrones · si la cabeza está en una: PERDISTE
recompensa: xp 10, oro 10
```

#### Escena
—Mi jardín tiene macetas —dice la Serpiente Jardinera, y deja seis en el caminito con la punta de la cola—.
Mis serpientes las esquivan. La tuya, en cambio, ni las ve.

#### Gheco sugiere
Ya están las macetas: `MACETAS` (6) y dos arreglos con la columna (`MX`) y la fila (`MY`) de cada una. Dos
cosas:
1. **Dibujarlas**, después de la fruta:
```c
SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);   /* marrón maceta */
for (int m = 0; m < MACETAS; m++) {
    SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
    SDL_RenderFillRect(lapiz, &maceta);
}
```
2. **Chocarlas**, después de ver si se mordió:
```c
for (int m = 0; m < MACETAS; m++) {
    if (cx[0] == MX[m] && cy[0] == MY[m]) {
        estado = PERDISTE;
    }
}
```
Por ahora el cartel sigue diciendo «TE MORDISTE»: lo cambiamos en la última. El robot va a dejar que la
serpiente siga derecho: hay una maceta en su fila.

#### Desafío
Dibujá las macetas y hacé que la serpiente pierda si la cabeza choca una.

#### Pasos
1. Buscá `/* acá: dibujar las macetas, marrones */` y escribí el color y el `for` que las dibuja.
2. Buscá `/* acá: si la cabeza choca una maceta, perdiste */` y escribí el `for` del choque.
3. Tocá **Jugar**, empezá y dejá que la serpiente siga derecho. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };


/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        /* acá: si la cabeza choca una maceta, perdiste */


        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        /* acá: dibujar las macetas, marrones */
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Espacio
cuadros 300
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 1 | TE MORDISTE | R: OTRA VEZ
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };


/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }


        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Seis macetas marrones aparecen en el tablero, y la serpiente que no dobla a tiempo se da contra una y se
queda quieta. La Serpiente Jardinera aplaude con la cola: —Ahora sí ves mis macetas.

#### Imagen
- La Serpiente Jardinera, una serpiente de luz enorme verde y dorada con sombrerito de paja y una regadera colgada de la cola, deja macetas en el caminito.
- En la pantalla de la máquina, la grilla con cuadraditos marrones y la serpiente verde chocando contra uno.
- Kira esquiva macetas con las flechas, concentrada; Arcadia sonríe; Gheco, sobre la máquina, se agarra fuerte.

### Micro-misión R04-N05-P2 · Un lugar libre

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia, la Serpiente Jardinera
carta: Función y do … while | libre(x, y, …): false si hay serpiente o maceta · do { elegir al azar } while (!libre(…))
recompensa: xp 10, monedas 4
```

#### Escena
La fruta nueva aparece justo debajo de una maceta, y la serpiente no la puede comer nunca. La Serpiente
Jardinera frunce el ceño: —En mi jardín las frutas crecen en la tierra libre, no debajo de las macetas.

#### Gheco sugiere
Dos cosas:
1. **Una función que pregunta** si una celda está libre (va antes del `main`):
```c
static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {           /* ¿hay una parte de la serpiente? */
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {         /* ¿hay una maceta? */
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;                                /* no hay nada: libre */
}
```
`return` corta la función en el momento: apenas encuentra algo, contesta `false`.
2. **Probar hasta que salga una libre**, al poner la fruta nueva:
```c
do {
    fx = SDL_rand(COLS);
    fy = SDL_rand(FILAS);
} while (!libre(fx, fy, cx, cy, largo));
```
`do { … } while (…)` hace el bloque una vez y lo repite **mientras** la celda no esté libre.

#### Desafío
Hacé que la fruta nueva aparezca siempre en una celda libre, sin serpiente ni maceta.

#### Pasos
1. Buscá `/* acá: una función que dice si una celda está libre (sin serpiente ni maceta) */` (antes del `main`) y escribí la función `libre`.
2. Buscá `/* acá: elegir lugares al azar hasta encontrar uno libre */` y borrá las dos líneas de abajo.
3. En su lugar, escribí el `do … while` de la sugerencia.
4. Tocá **Jugar** y comé la primera fruta: la nueva tiene que verse. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

/* acá: una función que dice si una celda está libre (sin serpiente ni maceta) */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }


        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            /* acá: elegir lugares al azar hasta encontrar uno libre */
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Espacio
cuadros 160
```

#### Estado
```
buscar #ff465a
```

#### Salida esperada
```
── Estado ──
buscar #ff465a: x 440, y 100, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }


        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La fruta nueva aparece en tierra libre, a la vista. La Serpiente Jardinera asiente despacio. —Así crecen
las frutas en mi jardín —dice, y riega una flor que se enciende.

#### Imagen
- En la pantalla de la máquina, la fruta roja en una celda libre, lejos de las macetas marrones.
- La Serpiente Jardinera, la serpiente de luz verde y dorada con sombrerito de paja, riega una flor de vidrio que se enciende.
- Kira y Arcadia sonríen; Gheco, en la palma de Kira, huele la flor.

### Micro-misión R04-N05-P3 · La fruta dorada

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia, la Serpiente Jardinera
carta: Temporizador | relojDorado += dt · a los 8 s aparece en un lugar libre · a los 4 s se va · comerla: 5 puntos
recompensa: xp 10, monedas 4
```

#### Escena
La Serpiente Jardinera sacude la cola y cae una fruta de oro que brilla entre las flores. —Mis frutas de oro
no esperan a nadie —dice—. Aparecen un ratito, y si no llegás, se van.

#### Gheco sugiere
Ya están `hayDorada`, la celda `gx`, `gy` y el reloj `relojDorado`. En cada cuadro, mientras se juega:
```c
if (estado == JUGANDO) {
    relojDorado += dt;
    if (!hayDorada && relojDorado >= 8) {          /* 8 segundos sin dorada: aparece */
        do {
            gx = SDL_rand(COLS);
            gy = SDL_rand(FILAS);
        } while (!libre(gx, gy, cx, cy, largo));
        hayDorada = true;
        relojDorado = 0;
    }
    if (hayDorada && relojDorado >= 4) {           /* 4 segundos con dorada: se va */
        hayDorada = false;
        relojDorado = 0;
    }
    if (hayDorada && cx[0] == gx && cy[0] == gy) { /* ¡la alcanzaste! */
        puntos += 5;
        hayDorada = false;
        relojDorado = 0;
    }
}
```
Y dibujarla dorada, después de la fruta roja:
```c
if (hayDorada) {
    SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
    SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
    SDL_RenderFillRect(lapiz, &dorada);
}
```
El robot va a empezar, doblar para arriba (ahí no hay macetas) y esperar 9 segundos.

#### Desafío
Hacé que cada 8 segundos aparezca una fruta dorada en un lugar libre, que dure 4 y valga 5 puntos.

#### Pasos
1. Buscá `/* acá: la fruta dorada: aparece cada 8 segundos, dura 4 y vale 5 puntos */` y escribí el `if (estado == JUGANDO)` de la sugerencia.
2. Buscá `/* acá: dibujar la fruta dorada, si hay */` y escribí el `if (hayDorada)` que la dibuja.
3. Tocá **Jugar** y esperá: a los 8 segundos tiene que aparecer. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    bool hayDorada = false;   /* true: hay una fruta dorada en el jardín */
    int gx = 0;               /* la fruta dorada: columna y fila */
    int gy = 0;
    float relojDorado = 0;    /* cuánto pasó desde que apareció (o desde que se fue) */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }

        /* acá: la fruta dorada: aparece cada 8 segundos, dura 4 y vale 5 puntos */

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        /* acá: dibujar la fruta dorada, si hay */
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Espacio
cuadros 2
tecla Arriba
cuadros 520
```

#### Estado
```
buscar #ffc828
```

#### Salida esperada
```
── Estado ──
buscar #ffc828: x 440, y 100, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    bool hayDorada = false;   /* true: hay una fruta dorada en el jardín */
    int gx = 0;               /* la fruta dorada: columna y fila */
    int gy = 0;
    float relojDorado = 0;    /* cuánto pasó desde que apareció (o desde que se fue) */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }

        if (estado == JUGANDO) {
            relojDorado += dt;
            if (!hayDorada && relojDorado >= 8) {
                do {
                    gx = SDL_rand(COLS);
                    gy = SDL_rand(FILAS);
                } while (!libre(gx, gy, cx, cy, largo));
                hayDorada = true;
                relojDorado = 0;
            }
            if (hayDorada && relojDorado >= 4) {
                hayDorada = false;
                relojDorado = 0;
            }
            if (hayDorada && cx[0] == gx && cy[0] == gy) {
                puntos += 5;
                hayDorada = false;
                relojDorado = 0;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        if (hayDorada) {
            SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
            SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
            SDL_RenderFillRect(lapiz, &dorada);
        }
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Una fruta dorada se enciende en un rincón del tablero. Kira dobla, dobla otra vez… y la alcanza justo antes
de que se apague. **+5**. La Serpiente Jardinera silba de admiración.

#### Imagen
- En la pantalla de la máquina, una fruta dorada brillante en un rincón de la grilla y la serpiente verde yendo a buscarla.
- La Serpiente Jardinera sacude la cola y cae una fruta de oro entre las flores de vidrio.
- Kira juega a toda velocidad; Arcadia aplaude; Gheco atrapa en el aire una chispa dorada.

### Micro-misión R04-N05-P4 · El jardín florece

```meta
lugar: El Jardín de la Serpiente
personajes: Kira, Gheco, Arcadia, la Serpiente Jardinera
carta: Cartel centrado | al perder: cartel = largo >= 15 ? "EL JARDIN FLORECE" : "TE ENREDASTE" · x = 320 - SDL_strlen(cartel) * 4
recompensa: xp 20, monedas 5
item: Escama de Luz
```

#### Escena
—Llegá a quince anillos —dice la Serpiente Jardinera— y, cuando termine la partida, que la máquina lo diga
bien grande, en el medio: que mi jardín floreció. Y si no llegás, que diga la verdad: que te enredaste.

#### Gheco sugiere
En lugar del cartel de antes («TE MORDISTE», corrido a ojo), uno centrado que depende del largo:
```c
if (estado == PERDISTE) {
    const char *cartel = (largo >= 15) ? "EL JARDIN FLORECE" : "TE ENREDASTE";
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
}
```
- Con 15 partes o más, ganaste el jardín aunque después te hayas enredado.
- Cada letra mide 8 píxeles: para centrar un texto de `n` letras, empieza en `320 - n * 4` (como los carteles
  del Campeón y del Muro).

El robot va a dejar que la serpiente choque una maceta enseguida.

#### Desafío
Cambiá el cartel del final por uno centrado: EL JARDIN FLORECE con 15 partes o más, TE ENREDASTE si no.

#### Pasos
1. Buscá `/* acá: el cartel del final, centrado: con 15 partes o más, el jardín florece */` y borrá el `if` de abajo.
2. En su lugar, escribí el `if` de la sugerencia.
3. Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    bool hayDorada = false;   /* true: hay una fruta dorada en el jardín */
    int gx = 0;               /* la fruta dorada: columna y fila */
    int gy = 0;
    float relojDorado = 0;    /* cuánto pasó desde que apareció (o desde que se fue) */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }

        if (estado == JUGANDO) {
            relojDorado += dt;
            if (!hayDorada && relojDorado >= 8) {
                do {
                    gx = SDL_rand(COLS);
                    gy = SDL_rand(FILAS);
                } while (!libre(gx, gy, cx, cy, largo));
                hayDorada = true;
                relojDorado = 0;
            }
            if (hayDorada && relojDorado >= 4) {
                hayDorada = false;
                relojDorado = 0;
            }
            if (hayDorada && cx[0] == gx && cy[0] == gy) {
                puntos += 5;
                hayDorada = false;
                relojDorado = 0;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        if (hayDorada) {
            SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
            SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
            SDL_RenderFillRect(lapiz, &dorada);
        }
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        /* acá: el cartel del final, centrado: con 15 partes o más, el jardín florece */
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
tecla Espacio
cuadros 300
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 1 | TE ENREDASTE | R: OTRA VEZ
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 20    /* cada celda de la grilla mide 20 × 20 píxeles */
#define COLS 32     /* 640 / 20: celdas de ancho */
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, PERDISTE };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    int dx = 1;    /* hacia dónde va: 1 derecha, -1 izquierda, 0 quieta de costado */
    int dy = 0;    /* 1 abajo, -1 arriba */
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    int puntos = 0;
    enum Estado estado = MENU;
    bool hayDorada = false;   /* true: hay una fruta dorada en el jardín */
    int gx = 0;               /* la fruta dorada: columna y fila */
    int gy = 0;
    float relojDorado = 0;    /* cuánto pasó desde que apareció (o desde que se fue) */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= paso) {
            reloj -= paso;
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            cx[0] += dx;
            cy[0] += dy;
        }
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;

        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }

        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }

        if (estado == JUGANDO) {
            relojDorado += dt;
            if (!hayDorada && relojDorado >= 8) {
                do {
                    gx = SDL_rand(COLS);
                    gy = SDL_rand(FILAS);
                } while (!libre(gx, gy, cx, cy, largo));
                hayDorada = true;
                relojDorado = 0;
            }
            if (hayDorada && relojDorado >= 4) {
                hayDorada = false;
                relojDorado = 0;
            }
            if (hayDorada && cx[0] == gx && cy[0] == gy) {
                puntos += 5;
                hayDorada = false;
                relojDorado = 0;
            }
        }

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            puntos++;
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            paso = SDL_max(0.06f, paso * 0.9f);
            pitido(parlante, 660, 0.06f);
        }

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        if (hayDorada) {
            SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
            SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
            SDL_RenderFillRect(lapiz, &dorada);
        }
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            const char *cartel = (largo >= 15) ? "EL JARDIN FLORECE" : "TE ENREDASTE";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Quince anillos. Dieciséis. La serpiente de Kira se enreda por fin y la pantalla dice, en amarillo y en el
medio, **EL JARDIN FLORECE**. Todas las flores de vidrio se encienden a la vez. La Serpiente Jardinera se ríe
y riega a Kira, que también se ríe, empapada.

En la pantalla aparece **otro pedazo del mapa del Vidriero**: una torre altísima hecha de bloques de colores
que caen del cielo. {mentor} la mira y se pone seria. —La Torre que no para —dice—. Esa es difícil.

La Serpiente Jardinera se saca una escama que brilla como un vitral y se la da a Kira: la **Escama de Luz**.
—Para que mi jardín te acompañe —dice.

#### Imagen
- La Serpiente Jardinera, la serpiente de luz verde y dorada con sombrerito de paja, riega a Kira riéndose, con todas las flores de vidrio encendidas.
- En la pantalla de la máquina, un pedazo de mapa antiguo con una torre altísima de bloques de colores.
- Kira, empapada y feliz, sostiene una escama que brilla como un vitral; Arcadia mira el mapa, seria; Gheco abraza la máquina.
