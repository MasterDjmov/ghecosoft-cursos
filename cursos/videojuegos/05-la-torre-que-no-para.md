# RAMA R05 · La Torre que no para: Tetris

```meta
tipo: tronco
posicion: 5
```

## R05-N01 · El pozo y la pieza

```meta
tipo: tema
criatura: fantasma_fotograma
padre: R04-N05
precio: 10
temas: col.matrices
usa: juegos.bucle, juegos.entrada, prog.bucles
```

### Crónica

El quinto pedazo de mapa lleva al borde de la ciudad, donde una torre altísima se pierde entre las nubes. No tiene
puerta: tiene una máquina en la base, con la pantalla angosta y alta como un pozo. Desde arriba, muy de vez en
cuando, cae un bloque de colores y se acomoda en la torre con un *clonc*. —La Torre que no para —dice {mentor}—.
El Vidriero la hizo para jugar a apilar. Hace años que está trabada: los bloques caen solos, sin nadie que los
acomode. Si la torre se llena sin orden, se tapa. Y en la pantalla, una pieza cae una vez a toda velocidad y otra
vez despacito: el **Fantasma del Fotograma** anda por acá.

### Objetivos

Dibujar el **pozo** del Tetris recorriendo una **matriz** con dos `for`, guardar la **pieza** que cae en una cajita
de 4 × 4, hacerla **bajar de a una fila** con un reloj y moverla a los costados con las **flechas**.

### Antes de empezar

Toda la escalera hasta acá. De R04: la grilla, el reloj que hace avanzar «cada tanto» (N01). De R03: la pared en
un arreglo (N03).

### Explicación

#### Qué es el Tetris
Caen piezas hechas de cuatro bloques, una por vez. Mientras caen, las movés a los costados y las girás para que
encajen. Cuando una fila del pozo queda llena de punta a punta, se borra y todo lo de arriba baja. Si la pila llega
hasta arriba, perdiste.

#### El pozo: una matriz
En el Snake la grilla era solo un dibujo. Acá cada casilla tiene que **acordarse** de si está ocupada, porque las
piezas se apilan. Para eso hay una **matriz**: un arreglo de dos dimensiones, como una tabla con filas y columnas.
`int tablero[FILAS][COLS]` tiene 20 filas de 10 casillas. `tablero[f][c]` es la casilla de la fila `f` y la columna
`c`, y vale 0 si está vacía. Para recorrerla toda hacen falta dos `for`, uno adentro del otro: el de afuera elige
la fila; el de adentro, cada casilla de esa fila.

#### La pieza: una matriz chiquita
La pieza que cae también es una matriz, de 4 × 4: un **1** donde hay un bloque y un **0** donde no. Esta tiene forma
de **T**. `px` y `py` dicen en qué columna y fila del pozo está la esquina de arriba a la izquierda de su cajita.
El bloque de la cajita `(f, c)` cae en la casilla `(py + f, px + c)` del pozo.

#### De casilla a píxeles
Como en el Snake: se multiplica por `CELDA`. Pero el pozo no empieza en el borde de la ventana sino en el medio, en
`OX` (200 píxeles): la columna `c` empieza en `OX + c * CELDA`. A cada cuadrado se le saca un píxel
(`CELDA - 1`) para que se vean las rayitas entre las casillas.

#### Bajar de a una fila
El mismo reloj del Snake: se le suma `dt` en cada cuadro y, cuando junta `caida` segundos (medio segundo), la pieza
baja una fila y al reloj se le resta lo que gastó.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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

Las matrices están en todos los juegos de tablero: el ta-te-tí, el buscaminas, el ajedrez, el laberinto del
Pac-Man y los mapas de los juegos de plataformas, que se arman casilla por casilla.

### Errores habituales

**Dar vuelta fila y columna.** `tablero[f][c]`: primero la fila (la `y`), después la columna (la `x`). Al dibujar es
al revés: la `x` sale de la columna (`OX + c * CELDA`) y la `y` de la fila (`f * CELDA`).

**Olvidarse de `OX`.** Sin sumarlo, el pozo queda pegado al borde izquierdo de la ventana.

**Usar `<=` en el `for`.** La última fila es la 19, no la 20: `f < FILAS`. Con `<=` se lee una fila que no existe.

**Bajar en cada cuadro.** Sin el reloj, la pieza cruza el pozo en un tercio de segundo: es el Fantasma del
Fotograma.

### Micro-misión R05-N01-P1 · El pozo de la torre

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Matriz | for f hasta FILAS · for c hasta COLS · celda en (OX + c * CELDA, f * CELDA) · vacía: casi negra
recompensa: xp 10, oro 10
```

#### Escena
{mentor} limpia la pantalla de la máquina con la manga: está toda negra. —Ahí había un pozo —dice—, diez
casillas de ancho y veinte de alto. Cada casilla se acordaba de si tenía un bloque o no.

#### Gheco sugiere
El pozo es la matriz `tablero`: 20 filas (`FILAS`) de 10 casillas (`COLS`). Dos `for`, uno adentro del otro,
pasan por todas. Para cada una, un cuadrado:
```c
for (int f = 0; f < FILAS; f++) {          /* cada fila… */
    for (int c = 0; c < COLS; c++) {       /* …y cada casilla de esa fila */
        SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
        if (tablero[f][c] == 0) {
            SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
        } else {
            SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
        }
        SDL_RenderFillRect(lapiz, &celda);
    }
}
```
- `OX + c * CELDA`: el pozo empieza en el píxel 200, y cada columna está 24 píxeles más a la derecha.
- `CELDA - 1`: un píxel menos, para que se vean las rayitas entre casillas.
- Por ahora todas están vacías: el `else` va a servir cuando se apilen piezas.

#### Desafío
Dibujá el pozo: un cuadrado por cada casilla de la matriz, casi negro si está vacía.

#### Pasos
1. Buscá el comentario `/* acá: dibujar el pozo: una celda por cada casilla del tablero */`.
2. Debajo, escribí los dos `for` de la sugerencia, con el `if` del color y el cuadrado.
3. Tocá **Jugar**: tiene que verse el pozo en el medio. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
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


        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        /* acá: dibujar el pozo: una celda por cada casilla del tablero */
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
buscar #1c1c2c
```

#### Salida esperada
```
── Estado ──
buscar #1c1c2c: x 200, y 0, ancho 239, alto 479
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
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


        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
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
En el medio de la pantalla aparece el pozo: doscientas casillas oscuras, parejitas, como las ventanas de un
edificio de noche. Gheco las cuenta con la cola y se rinde en la treinta y siete.

#### Imagen
- La pantalla angosta y alta de la máquina, con un pozo de casillas oscuras en el medio.
- Arcadia limpia la pantalla con la manga; Kira mira la torre altísima que se pierde entre las nubes.
- Gheco, sentado arriba de la máquina, cuenta las casillas con la cola, mareado.

### Micro-misión R05-N01-P2 · Una pieza en su cajita

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Pieza | for f hasta 4 · for c hasta 4 · si pieza[f][c] == 1: bloque en (OX + (px + c) * CELDA, (py + f) * CELDA)
recompensa: xp 10, monedas 4
```

#### Escena
Un bloque cae desde lo alto de la torre y rebota en el techo de la máquina: *clonc*. Kira lo levanta: son
cuatro cubitos pegados en forma de T. —Cada pieza tiene cuatro —dice {mentor}—. La máquina la guarda en una
cajita de cuatro por cuatro: un uno donde hay cubito, un cero donde no.

#### Gheco sugiere
La pieza es la matriz `pieza[4][4]`. Para dibujarla, otra vez dos `for`, pero de 4 × 4, y un cuadrado solo
donde hay un 1:
```c
SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
for (int f = 0; f < 4; f++) {
    for (int c = 0; c < 4; c++) {
        if (pieza[f][c] == 1) {
            SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
            SDL_RenderFillRect(lapiz, &bloque);
        }
    }
}
```
El bloque `(f, c)` de la cajita va en la columna `px + c` y la fila `py + f` del pozo: la cajita está en la
columna 3 y la fila 0.

#### Desafío
Dibujá la pieza: un cuadrado violeta por cada 1 de su cajita de 4 × 4.

#### Pasos
1. Buscá `/* acá: dibujar la pieza: un cuadrado por cada 1 de la cajita */`.
2. Debajo, escribí el color y los dos `for` de la sugerencia.
3. Tocá **Jugar**: arriba del pozo tiene que verse la T. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
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


        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        /* acá: dibujar la pieza: un cuadrado por cada 1 de la cajita */
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
buscar #aa50ff
```

#### Salida esperada
```
── Estado ──
buscar #aa50ff: x 272, y 24, ancho 71, alto 47
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
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


        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
Arriba del pozo aparece una T violeta, quietita, esperando. Kira compara con la pieza de verdad que tiene en
la mano: es igual. —Cuatro cubitos —dice—, y la cajita es el molde.

#### Imagen
- La pantalla de la máquina con el pozo oscuro y una pieza violeta en forma de T arriba de todo.
- Kira sostiene en la mano una pieza de cuatro cubitos violetas en forma de T, comparándola con la pantalla.
- Arcadia señala la pantalla; Gheco se esconde detrás de la pieza de Kira, curioso.

### Micro-misión R05-N01-P3 · Una fila cada medio segundo

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Reloj | reloj += dt · si reloj >= caida: reloj -= caida y py++ (baja una fila)
recompensa: xp 10, monedas 4
```

#### Escena
La T está quieta arriba del pozo. Desde lo alto de la torre se oye un *clonc*, después otro, cada vez más
seguido y después más lento. —El Fantasma del Fotograma —dice {mentor}—. Las piezas tienen que caer siempre
al mismo ritmo: una fila cada medio segundo, en cualquier máquina.

#### Gheco sugiere
Ya están `reloj` (el tiempo juntado) y `caida` (medio segundo). Es el reloj del Snake, pero la pieza baja en
lugar de avanzar:
```c
reloj += dt;              /* junta el tiempo que pasó */
if (reloj >= caida) {     /* ¿ya juntó medio segundo? */
    reloj -= caida;       /* lo gasta */
    py++;                 /* y la cajita baja una fila */
}
```
Como la `y` de la pieza se calcula con `py`, al sumarle 1 todo el dibujo baja una casilla. Por ahora sigue de
largo por el fondo: en el nodo que viene aprende a pararse.

#### Desafío
Hacé que la pieza baje una fila cada medio segundo, con un reloj que junta el tiempo.

#### Pasos
1. Buscá `/* acá: juntar el tiempo y, cada «caida» segundos, bajar una fila */`.
2. Debajo, escribí las líneas del reloj de la sugerencia.
3. Tocá **Jugar**: la T tiene que bajar a saltitos parejos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
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

        /* acá: juntar el tiempo y, cada «caida» segundos, bajar una fila */

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 100
```

#### Estado
```
pixel 300 100
```

#### Salida esperada
```
── Estado ──
pixel 300 100: #aa50ff
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
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
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La T baja: *tic*, una fila, *tic*, otra, siempre igual. El Fantasma del Fotograma sopla para apurarla, pero
el reloj no se deja, y se va flotando torre arriba, enojado.

#### Imagen
- La pantalla de la máquina con la pieza violeta en T a mitad del pozo, con rayitas de movimiento hacia abajo.
- Un fantasma redondo y translúcido, borroso, se aleja flotando torre arriba, enojado.
- Kira lleva el ritmo con la mano; Arcadia sonríe; Gheco, sobre la máquina, mueve la cabeza al compás.

### Micro-misión R05-N01-P4 · A los costados

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Flechas | izquierda: px-- · derecha: px++ (una columna por apretada)
recompensa: xp 10, monedas 4
```

#### Escena
La T cae siempre por el mismo lugar, derechito. Kira aprieta las flechas, pero la pieza ni se entera.
—Mientras cae, la movés —dice {mentor}—. Una columna por apretada: ni más ni menos.

#### Gheco sugiere
Mover la pieza es cambiar `px`, la columna de su cajita. Va en los eventos, para que sea una columna por
apretada (no mientras la tecla está apretada):
```c
if (evento.type == SDL_EVENT_KEY_DOWN) {
    if (evento.key.key == SDLK_LEFT) {
        px--;           /* una columna a la izquierda */
    }
    if (evento.key.key == SDLK_RIGHT) {
        px++;           /* una columna a la derecha */
    }
}
```
Por ahora se puede salir del pozo: en el nodo que viene la frenan las paredes. El robot va a apretar la
flecha de la izquierda.

#### Desafío
Hacé que las flechas de los costados muevan la pieza una columna.

#### Pasos
1. Buscá `/* acá: las flechas de los costados mueven la pieza una columna */` (en el `while` de los eventos).
2. Debajo, escribí el `if` con las dos flechas de la sugerencia.
3. Tocá **Jugar**, hacé clic en el juego y mové la T. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: las flechas de los costados mueven la pieza una columna */
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 2
```

#### Estado
```
pixel 253 30
```

#### Salida esperada
```
── Estado ──
pixel 253 30: #aa50ff
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
Kira aprieta la flecha y la T se corre una casilla, obediente; otra vez, y otra. Desde la torre se oye un
*clonc* más contento que los anteriores. Gheco aplaude con la cola.

#### Imagen
- La pantalla de la máquina con la pieza violeta en T corrida hacia un costado del pozo, con una flecha.
- Kira aprieta las flechas, concentrada; Arcadia mira la torre, donde cae un bloque de colores.
- Gheco aplaude con la cola, sentado arriba de la máquina.

## R05-N02 · Chocar y quedarse

```meta
tipo: tema
criatura: atraviesaparedes
padre: R05-N01
precio: 10
temas: prog.funciones
usa: col.matrices, juegos.colisiones, prog.bucles
```

### Crónica

La T baja, Kira la corre a un costado… y la pieza sigue de largo, atraviesa la pared del pozo y se pierde fuera de
la pantalla. La siguiente atraviesa el piso. Desde la máquina asoma, como si fuera de gelatina, el
**Atraviesaparedes**: se ríe mientras pasa de un lado al otro del vidrio. —Una pieza tiene que chocar —dice
{mentor}—: con las paredes, con el piso y con las que ya están. Y cuando no puede bajar más, se queda.

### Objetivos

Escribir una **función** que pregunta si la pieza **cabe** en un lugar (sin salirse del pozo ni pisar otro bloque),
usarla para que las paredes y el piso la frenen, **fijar** la pieza en el pozo cuando ya no puede bajar y sacar
otra arriba, para que las piezas **se apilen**.

### Antes de empezar

El nodo anterior. De R04: la función `libre` del jefe, que preguntaba si una celda estaba libre (N05). Del curso de
C: las funciones que devuelven `bool` y las matrices como parámetro.

### Explicación

#### Preguntar antes de mover
En el Pong o el Arkanoid, la pelota se movía y **después** se veía si chocaba. En el Tetris es al revés: antes de
mover la pieza se pregunta **si va a caber** en el lugar nuevo. Si cabe, se mueve; si no, se queda donde está. Así
nunca queda metida adentro de nada.

#### La función `cabe`
`cabe(pieza, tablero, px, py)` recorre los 16 lugares de la cajita y, por cada bloque (cada 1), calcula en qué
casilla del pozo caería: columna `x = px + c` y fila `y = py + f`. Contesta `false` apenas encuentra un bloque que:
- se sale por un costado (`x < 0` o `x >= COLS`);
- se sale por abajo (`y >= FILAS`);
- o cae en una casilla ocupada (`tablero[y][x] != 0`).

Si revisa los cuatro bloques y ninguno molesta, contesta `true`. Es como la `libre` del Snake, pero para cuatro
bloques a la vez.

#### Una matriz como parámetro
`int tablero[FILAS][COLS]` en los paréntesis de la función le dice que recibe la matriz entera. Como con los
arreglos, no se copia: la función mira el mismo tablero del `main`.

#### Fijar la pieza
Cuando la pieza **no cabe una fila más abajo**, llegó: se copia al pozo. Cada bloque de la cajita pone un 1 en
su casilla del tablero, y desde ese momento el pozo lo dibuja (celeste). Después sale otra pieza arriba, en la
columna 3 y la fila 0.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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

«Preguntar antes de mover» es la forma más segura de hacer chocar cosas en una grilla: el Pac-Man contra las paredes
del laberinto y el personaje de un juego de tablero contra los obstáculos se hacen igual.

### Errores habituales

**Mover y después preguntar.** Si primero se hace `px--` y después se mira, la pieza ya quedó adentro de la pared.

**Preguntar por el lugar de ahora.** Para bajar hay que preguntar por `py + 1`, no por `py`: el lugar donde
**va a estar**.

**Revisar los ceros.** La cajita tiene ceros que se pueden salir del pozo sin problema: solo importan los bloques.
Por eso todo va adentro de `if (pieza[f][c] == 1)`.

**Atraviesaparedes: el `return true` adentro del `for`.** Si contesta `true` después de mirar el primer bloque, los
otros tres pueden estar adentro de la pared. El `true` va al final, cuando ya revisó todos.

### Micro-misión R05-N02-P1 · Las paredes del pozo

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Función cabe | si x < 0 o x >= COLS: return false · flecha: moverse solo si cabe(…, px ± 1, py)
recompensa: xp 10, oro 10
```

#### Escena
Kira corre la T a la izquierda, otra vez, y otra… y la pieza atraviesa la pared del pozo como si fuera de aire.
El Atraviesaparedes se asoma del otro lado y le saca la lengua.

#### Gheco sugiere
Ya está la función `cabe`: recorre los bloques de la cajita y calcula la casilla `x`, `y` de cada uno. Dos
cosas:
1. **Que conteste `false` si un bloque se sale por un costado:**
```c
if (x < 0 || x >= COLS) {
    return false;
}
```
2. **Que las flechas pregunten antes de mover**, por la columna de al lado:
```c
if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
    px--;
}
if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
    px++;
}
```
Si la pieza no cabe una columna más allá, la flecha no hace nada. El robot va a apretar la flecha de la
izquierda cinco veces.

#### Desafío
Hacé que las paredes del pozo frenen la pieza: moverse solo si cabe en la columna de al lado.

#### Pasos
1. Buscá `/* acá: no cabe si el bloque se sale por un costado */` (en la función `cabe`) y escribí el `if` de la sugerencia.
2. Buscá `/* acá: moverse solo si la pieza cabe en la columna de al lado */` y cambiá los dos `if` de las flechas por los de la sugerencia.
3. Tocá **Jugar** y llevá la T contra una pared. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                /* acá: no cabe si el bloque se sale por un costado */
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                /* acá: moverse solo si la pieza cabe en la columna de al lado */
                if (evento.key.key == SDLK_LEFT) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
tecla Izquierda
tecla Izquierda
tecla Izquierda
tecla Izquierda
cuadros 2
```

#### Estado
```
buscar #aa50ff
```

#### Salida esperada
```
── Estado ──
buscar #aa50ff: x 200, y 24, ancho 71, alto 47
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La T llega a la pared y se frena en seco. Kira aprieta la flecha diez veces más: nada, ni un píxel. El
Atraviesaparedes empuja desde afuera, pero no puede entrar.

#### Imagen
- La pantalla de la máquina con la pieza violeta en T pegada a la pared izquierda del pozo.
- Una criatura de gelatina translúcida empuja el vidrio de la pantalla desde afuera, sin poder pasar.
- Kira aprieta la flecha muchas veces; Arcadia se ríe; Gheco empuja la pared del pozo con las dos patas.

### Micro-misión R05-N02-P2 · El piso

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Bajar si cabe | si y >= FILAS: return false · bajar solo si cabe(…, px, py + 1)
recompensa: xp 10, monedas 4
```

#### Escena
La T baja, baja… y sigue de largo por el fondo del pozo, como si no tuviera piso. El Atraviesaparedes aparece
debajo de la máquina con la pieza en la mano.

#### Gheco sugiere
Igual que las paredes, pero para abajo. Dos cosas:
1. **En `cabe`, que un bloque tampoco se salga por abajo:**
```c
if (y >= FILAS) {
    return false;
}
```
2. **Bajar solo si cabe una fila más abajo** (en el reloj, en lugar del `py++` solo):
```c
if (cabe(pieza, tablero, px, py + 1)) {
    py++;
}
```
La última fila es la 19: un bloque en la fila 20 ya se salió. El robot va a esperar 12 segundos, más de lo
que tarda en llegar al fondo.

#### Desafío
Hacé que la pieza se frene en el fondo del pozo: bajar solo si cabe una fila más abajo.

#### Pasos
1. Buscá `/* acá: ni si se sale por abajo */` (en la función `cabe`) y escribí el `if` de la sugerencia.
2. Buscá `/* acá: bajar solo si la pieza cabe una fila más abajo */` y borrá el `py++;` de abajo.
3. En su lugar, escribí el `if` de la sugerencia.
4. Tocá **Jugar** y dejá que la T llegue al fondo. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                /* acá: ni si se sale por abajo */
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            /* acá: bajar solo si la pieza cabe una fila más abajo */
            py++;
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 720
```

#### Estado
```
buscar #aa50ff
```

#### Salida esperada
```
── Estado ──
buscar #aa50ff: x 272, y 432, ancho 71, alto 47
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La T llega al fondo y se queda ahí, apoyada, como una pieza de verdad sobre una mesa. El Atraviesaparedes
golpea el piso del pozo desde abajo: *toc, toc*. No pasa.

#### Imagen
- La pantalla de la máquina con la pieza violeta en T apoyada en el fondo del pozo.
- Debajo de la máquina, una criatura de gelatina translúcida golpea el piso con el puño, sin poder pasar.
- Kira se agacha a mirar; Arcadia sonríe; Gheco se sienta arriba de la máquina, tranquilo.

### Micro-misión R05-N02-P3 · Se queda y sale otra

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Fijar | si no cabe(…, px, py + 1): cada bloque pone un 1 en tablero[py + f][px + c] · otra pieza en px = 3, py = 0
recompensa: xp 10, monedas 4
```

#### Escena
La T llegó al fondo y ahí se quedó… para siempre. No sale ninguna otra. —Cuando una pieza ya no puede bajar,
se vuelve parte de la torre —dice {mentor}—. Y arriba aparece la siguiente.

#### Gheco sugiere
Después de bajar (o de intentarlo), se pregunta si todavía puede bajar otra fila. Si no puede, llegó:
```c
if (!cabe(pieza, tablero, px, py + 1)) {
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                tablero[py + f][px + c] = 1;   /* el bloque pasa a ser del pozo */
            }
        }
    }
    px = 3;    /* y sale otra pieza arriba */
    py = 0;
}
```
- `!` da vuelta la respuesta: «si **no** cabe».
- Cada bloque pone un 1 en su casilla del pozo; el pozo dibuja los 1 en celeste.
- Volver la cajita a la columna 3 y la fila 0 es sacar una pieza nueva (por ahora, siempre la T).

#### Desafío
Hacé que la pieza se quede en el pozo cuando ya no puede bajar, y que salga otra arriba.

#### Pasos
1. Buscá `/* acá: si ya no puede bajar, se queda en el pozo y sale otra arriba */` (en el reloj).
2. Debajo, escribí el `if` de la sugerencia, con los dos `for` que copian la pieza al tablero.
3. Tocá **Jugar** y esperá a que llegue al fondo. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            /* acá: si ya no puede bajar, se queda en el pozo y sale otra arriba */
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 600
```

#### Estado
```
buscar #00dcff
```

#### Salida esperada
```
── Estado ──
buscar #00dcff: x 272, y 432, ancho 71, alto 47
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La T toca el fondo, se pone celeste y se queda. Arriba ya asoma otra T violeta, lista para bajar. Desde lo alto
de la torre se oye un *clonc* contento: un piso más.

#### Imagen
- La pantalla de la máquina con una pieza celeste en el fondo del pozo y una violeta nueva arriba.
- Desde lo alto de la torre cae un bloque de colores que se acomoda con chispitas.
- Kira festeja con el puño; Arcadia mira la torre; Gheco imita la forma de T con el cuerpo.

### Micro-misión R05-N02-P4 · Una arriba de la otra

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Apilar | en cabe: si tablero[y][x] != 0: return false (la casilla ya está ocupada)
recompensa: xp 10, monedas 4
```

#### Escena
La segunda T baja… y se mete adentro de la primera, como si fuera un fantasma. Las dos quedan encimadas en el
fondo. El Atraviesaparedes, desde adentro del pozo, se frota las manos.

#### Gheco sugiere
A `cabe` le falta la última pregunta: si la casilla ya tiene un bloque. Va después de la del piso, cuando ya
se sabe que `x` e `y` están adentro del pozo:
```c
if (tablero[y][x] != 0) {
    return false;
}
```
¿Por qué después? Porque si `y` fuera 20, `tablero[20]` no existe. Primero se mira que esté adentro y recién
después se mira la casilla.

Como las flechas, la caída y el fijar usan `cabe`, con esto ya chocan todas. El robot va a esperar a que caigan
dos piezas.

#### Desafío
Hacé que la pieza no pueda meterse en una casilla ocupada, para que las piezas se apilen.

#### Pasos
1. Buscá `/* acá: ni si pisa un bloque que ya está en el pozo */` (en la función `cabe`).
2. Debajo, escribí el `if` de la sugerencia.
3. Tocá **Jugar** y esperá dos piezas: la segunda tiene que quedar arriba. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                /* acá: ni si pisa un bloque que ya está en el pozo */
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 1100
```

#### Estado
```
pixel 282 394
```

#### Salida esperada
```
── Estado ──
pixel 282 394: #00dcff
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La segunda T baja y se apoya **arriba** de la primera, encajada. Después una tercera, y una cuarta. El
Atraviesaparedes se queda atrapado entre dos piezas, se escurre como gelatina y se va.

#### Imagen
- La pantalla de la máquina con varias piezas en T apiladas en el fondo del pozo, una arriba de la otra.
- Una criatura de gelatina translúcida se escurre entre dos bloques y huye.
- Kira, Arcadia y Gheco miran la pila crecer, contentos.

## R05-N03 · Girar y las siete piezas

```meta
tipo: tema
criatura: glitch
padre: R05-N02
precio: 10
temas: col.matrices
usa: prog.funciones, prog.matematica-azar, prog.bucles
```

### Crónica

Las T se apilan, una arriba de la otra, y enseguida queda una torrecita torcida, llena de huecos. —Así no encaja
nada —dice {mentor}—. En la Torre de verdad caen siete piezas distintas, y cada una se puede girar. Por la pantalla
pasa un parpadeo: un gatito pixelado se mete entre las piezas y las deja medio corridas. Es el **Glitch**.

### Objetivos

**Girar** la pieza un cuarto de vuelta armando otra matriz, girarla solo si **cabe**, sacar **una de las siete
piezas al azar** de una tabla y dibujar cada una (y lo que queda en el pozo) **con su color**.

### Antes de empezar

El nodo anterior. De R04: elegir al azar con `SDL_rand` (N03). De R03: los colores de cada fila de la pared (N03).

### Explicación

#### Girar una matriz
Girar la pieza es girar su cajita de 4 × 4 un cuarto de vuelta, como las agujas del reloj. La fila de arriba pasa a
ser la columna de la derecha; la columna de la izquierda pasa a ser la fila de arriba. En cuentas: el lugar
`(f, c)` de la pieza girada sale del lugar `(3 - c, f)` de la de antes. Se arma en **otra** cajita, `girada`,
porque si se escribiera encima de la misma se pisarían los números que todavía no se leyeron. Al final se copia de
vuelta.

#### Girar solo si cabe
Al lado de una pared, la pieza girada puede quedar medio afuera. Se gira, se pregunta con `cabe` y, si no cabe, se
gira **tres veces más**: cuatro cuartos de vuelta son una vuelta entera, y queda como estaba.

#### Las siete piezas: una tabla de matrices
`PIEZAS[7][4][4]` son siete cajitas de 4 × 4, una por pieza: la I (el palo), la O (el cuadrado), la T, la S, la Z,
la J y la L. `tipo` dice cuál es la que cae (del 0 al 6). Para sacar una nueva, se elige `tipo = SDL_rand(7)` y se
copia su cajita en `pieza`, casilla por casilla.

#### Los colores en una tabla
`COLORES[8][3]` tiene el rojo, el verde y el azul de cada color. El 0 es el de la casilla vacía, y del 1 al 7, el
de cada pieza: la pieza `tipo` usa el color `tipo + 1`. Así, cuando una pieza se queda en el pozo, guarda
`tipo + 1` en sus casillas, y el pozo se dibuja con un solo renglón: el color de la casilla `t` es
`COLORES[t]`.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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

Girar matrices sirve para girar mapas, imágenes y tableros. Y guardar los datos en tablas (las piezas, los colores)
en lugar de llenar el código de `if` hace que sumar una pieza nueva sea agregar un renglón.

### Errores habituales

**Girar en la misma cajita.** Si se hace `pieza[f][c] = pieza[3 - c][f]` sin `girada`, se pisan los números que
todavía no se leyeron y la pieza queda rota: es el Glitch.

**Girar sin preguntar.** Al lado de la pared, la pieza girada queda con un bloque afuera del pozo.

**`tipo` en lugar de `tipo + 1`.** El color 0 es el de vacía: si la I guarda `tipo` (0), se vuelve invisible al
quedarse en el pozo.

**`SDL_rand(6)`.** Da del 0 al 5: la L no sale nunca. Para siete piezas, `SDL_rand(7)`.

### Micro-misión R05-N03-P1 · Un cuarto de vuelta

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Girar | girada[f][c] = pieza[3 - c][f] (en otra cajita) · después copiar girada en pieza
recompensa: xp 10, oro 10
```

#### Escena
Kira aprieta la flecha de arriba: la T debería girar, pero se queda igual. —Girar es lo que hace interesante a
la Torre —dice {mentor}—. La cajita entera da un cuarto de vuelta, como las agujas del reloj.

#### Gheco sugiere
La flecha de arriba ya llama a `girar(pieza)`, pero la función está vacía. Adentro, la pieza girada se arma
en **otra** cajita y después se copia de vuelta:
```c
int girada[4][4];
for (int f = 0; f < 4; f++) {
    for (int c = 0; c < 4; c++) {
        girada[f][c] = pieza[3 - c][f];   /* la fila de arriba pasa a la columna de la derecha */
    }
}
for (int f = 0; f < 4; f++) {
    for (int c = 0; c < 4; c++) {
        pieza[f][c] = girada[f][c];       /* se copia de vuelta */
    }
}
```
¿Por qué otra cajita? Si se escribiera en la misma, al llegar a un lugar ya se habría pisado el número que
había que leer. El robot va a apretar la flecha de arriba.

#### Desafío
Hacé que la flecha de arriba gire la pieza un cuarto de vuelta.

#### Pasos
1. Buscá `/* acá: armar la pieza girada en otra cajita y copiarla de vuelta */` (en la función `girar`).
2. Debajo, escribí `girada` y los dos pares de `for` de la sugerencia.
3. Tocá **Jugar** y apretá la flecha de arriba. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    /* acá: armar la pieza girada en otra cajita y copiarla de vuelta */
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
tecla Arriba
cuadros 2
```

#### Estado
```
buscar #aa50ff
```

#### Salida esperada
```
── Estado ──
buscar #aa50ff: x 296, y 0, ancho 47, alto 71
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
Kira aprieta la flecha y la T gira: ahora apunta para la izquierda. Otra vez: para arriba. Cuatro veces, y
vuelve a ser la de siempre. Gheco gira sobre sí mismo para imitarla y se marea.

#### Imagen
- La pantalla de la máquina con la pieza violeta en T girada un cuarto de vuelta, con una flecha curva.
- Kira aprieta la flecha de arriba; Arcadia gira las manos para mostrar el cuarto de vuelta.
- Gheco gira sobre sí mismo arriba de la máquina, mareado.

### Micro-misión R05-N03-P2 · Girar sin salirse

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Deshacer | girar · si no cabe: girar tres veces más (cuatro cuartos = una vuelta entera)
recompensa: xp 10, monedas 4
```

#### Escena
Kira lleva la T contra la pared derecha y la gira dos veces: un bloque queda **afuera** del pozo, flotando en
la nada. —Girar también tiene que respetar las paredes —dice {mentor}.

#### Gheco sugiere
Después de girar, se pregunta si la pieza cabe ahí. Si no cabe, se la deja como estaba. ¿Cómo? Girándola tres
veces más: cuatro cuartos de vuelta son una vuelta entera.
```c
girar(pieza);
if (!cabe(pieza, tablero, px, py)) {
    girar(pieza);      /* dos cuartos… */
    girar(pieza);      /* tres… */
    girar(pieza);      /* cuatro: una vuelta entera, como estaba */
}
```
El robot va a llevar la T contra la pared derecha y la va a girar dos veces.

#### Desafío
Hacé que la pieza gire solo si girada cabe en el pozo.

#### Pasos
1. Buscá `/* acá: si girada no cabe, girarla tres veces más para que vuelva como estaba */` (abajo del `girar(pieza);` de la flecha de arriba).
2. Debajo, escribí el `if` de la sugerencia.
3. Tocá **Jugar**, llevá la T contra una pared y girala. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    /* acá: si girada no cabe, girarla tres veces más para que vuelva como estaba */
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
tecla Derecha
tecla Derecha
tecla Derecha
tecla Derecha
tecla Arriba
tecla Arriba
cuadros 2
```

#### Estado
```
buscar #aa50ff
```

#### Salida esperada
```
── Estado ──
buscar #aa50ff: x 392, y 0, ancho 47, alto 71
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
Contra la pared, la T intenta girar… y no gira: se queda como estaba, con todos sus bloques adentro. Kira la
aleja un paso de la pared y ahí sí, gira tranquila.

#### Imagen
- La pantalla de la máquina con la pieza violeta pegada a la pared derecha del pozo, sin salirse.
- Kira aprieta la flecha de arriba, pensativa; Arcadia asiente.
- Gheco, con las patas contra la pared del pozo, la empuja para que la pieza no salga.

### Micro-misión R05-N03-P3 · Siete piezas

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: Al azar | tipo = SDL_rand(7) · copiar PIEZAS[tipo] en pieza · color COLORES[tipo + 1]
recompensa: xp 10, monedas 4
```

#### Escena
Desde lo alto de la torre caen piezas de todas las formas: un palo largo, un cuadrado, unas como escalones,
unas como ganchos. Pero en la pantalla sale siempre la T. El Glitch se ríe, sentado arriba del pozo.

#### Gheco sugiere
Ya están las tablas `PIEZAS` (las siete cajitas) y `COLORES` (un color por pieza), y `tipo` (qué pieza es).
Dos cosas:
1. **La pieza nueva, al azar** (donde sale otra arriba):
```c
tipo = SDL_rand(7);                          /* del 0 al 6 */
for (int f = 0; f < 4; f++) {
    for (int c = 0; c < 4; c++) {
        pieza[f][c] = PIEZAS[tipo][f][c];    /* se copia su cajita */
    }
}
```
2. **Su color**, en lugar del violeta fijo:
```c
SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
```
`COLORES[tipo + 1]` es una fila de la tabla: `[0]` el rojo, `[1]` el verde, `[2]` el azul. El robot va a
esperar a que salga la segunda pieza.

#### Desafío
Hacé que cada pieza nueva sea una de las siete al azar, dibujada con su color.

#### Pasos
1. Buscá `/* acá: la pieza nueva, una de las siete al azar */` y escribí el `tipo = SDL_rand(7);` y los dos `for` de la sugerencia.
2. Buscá `/* acá: el color de la pieza que cae, según su tipo */` y cambiá el color violeta por el de la sugerencia.
3. Tocá **Jugar** y esperá varias piezas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                /* acá: la pieza nueva, una de las siete al azar */
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        /* acá: el color de la pieza que cae, según su tipo */
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 600
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 296, y 96, ancho 47, alto 47
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La segunda pieza no es una T: es otra, de otro color. La tercera, otra más. El Glitch intenta corrérselas,
pero cada pieza sale entera, con su forma y su color.

#### Imagen
- La pantalla de la máquina con piezas de varias formas y colores: un palo celeste, un cuadrado amarillo, una ese verde.
- Un gatito pixelado que parpadea mira, sorprendido, sentado arriba de la máquina.
- Kira y Arcadia sonríen; Gheco sostiene en la mano una pieza de colores de verdad.

### Micro-misión R05-N03-P4 · Cada una con su color

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Pozo de colores | al fijar: tablero[…] = tipo + 1 · al dibujar: color COLORES[tablero[f][c]]
recompensa: xp 10, monedas 4
```

#### Escena
Las piezas bajan de colores, pero apenas tocan el fondo se vuelven todas celestes, como si se despintaran.
—En la Torre cada bloque se queda con su color —dice {mentor}—. Si no, no se sabe qué pieza era cuál.

#### Gheco sugiere
El pozo tiene que guardar **el color** y no solo un 1. Dos cosas:
1. **Al fijar**, en lugar de `1`:
```c
tablero[py + f][px + c] = tipo + 1;   /* del 1 al 7: el color de esta pieza */
```
2. **Al dibujar el pozo**, en lugar del `if` con dos colores:
```c
int t = tablero[f][c];
SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
```
Como `COLORES[0]` es el casi negro de las vacías, un solo renglón sirve para todas las casillas. El robot va
a esperar a que se quede la primera T.

#### Desafío
Hacé que cada bloque se quede en el pozo con el color de su pieza.

#### Pasos
1. Buscá `/* acá: guardar en el pozo el color de la pieza (tipo + 1) en lugar de un 1 */` y cambiá el `1` por `tipo + 1`.
2. Buscá `/* acá: cada casilla con su color, sacado de la tabla COLORES */` y borrá el `if` de abajo.
3. En su lugar, escribí las dos líneas de la sugerencia.
4. Tocá **Jugar** y dejá que se apilen piezas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            /* acá: guardar en el pozo el color de la pieza (tipo + 1) en lugar de un 1 */
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                /* acá: cada casilla con su color, sacado de la tabla COLORES */
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
cuadros 600
```

#### Estado
```
pixel 306 466
```

#### Salida esperada
```
── Estado ──
pixel 306 466: #aa50ff
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
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
La T toca el fondo y se queda violeta; arriba, un palo celeste, y al lado un cuadrado amarillo. La torrecita
parece un vitral. Desde lo alto de la Torre de verdad cae un bloque de cada color.

#### Imagen
- La pantalla de la máquina con el fondo del pozo lleno de bloques de muchos colores, como un vitral.
- Desde lo alto de la torre caen bloques de colores, brillando.
- Kira y Arcadia miran admiradas; Gheco apoya la cara contra la pantalla.

## R05-N04 · Líneas completas

```meta
tipo: tema
criatura: fuga_texturas
padre: R05-N03
precio: 10
temas: col.matrices
usa: prog.funciones, prog.bucles, prog.cadenas
```

### Crónica

En el fondo del pozo aparece una fila de bloques grises con un solo hueco: escombros que dejó la Torre. Las
piezas se apilan arriba, el pozo se va llenando y nada se borra nunca. —El secreto de la Torre —dice {mentor}— es
que una fila llena de punta a punta **desaparece**, y todo lo de arriba baja. Si no, se tapa enseguida. Entre los
bloques grises, algo se infla como un globo: la **Fuga de Texturas**, que junta todo lo que nadie borra.

### Objetivos

Hacer **caer de golpe** la pieza con el espacio, escribir una función que **borra las filas llenas** y baja lo que
hay arriba, y llevar la cuenta de las **líneas** y los **puntos** (más puntos si se borran varias juntas).

### Antes de empezar

El nodo anterior. De R03: contar los ladrillos que quedan (N05). De R02: el marcador (N02).

### Explicación

#### Caer de golpe
Con el espacio, la pieza baja **mientras** quepa una fila más abajo: un `while` que repite `py++` hasta que ya no
puede. Después se pone el reloj en `caida`, así en el cuadro siguiente el reloj ve que no puede bajar y la deja en
el pozo.

#### ¿Está llena esta fila?
Para saberlo, se cuentan sus casillas ocupadas. Si son `COLS` (10), está llena de punta a punta.

#### Borrar una fila: bajar todo lo de arriba
No se «borra» nada: cada fila, desde la llena para arriba, **copia la de arriba suyo**. La llena queda pisada por la
que tenía encima, esa por la de más arriba, y así hasta la fila 0, que queda vacía.

#### Revisar la misma fila otra vez
Se revisa de abajo para arriba (`f--`). Pero después de bajar todo, en la fila `f` quedó lo que estaba arriba, ¡y
también puede estar llena! Por eso, al borrar, se hace `f++`: como el `for` le resta 1, la vuelta siguiente vuelve a
mirar la misma fila.

#### Una función que devuelve un número
`borrarLineas` hace todo eso y **devuelve** cuántas filas borró (`return borradas;`). Con ese número se suman las
líneas y los puntos. Borrar varias juntas vale más: la tabla `PREMIO` dice cuánto por 1, 2, 3 o 4 filas.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
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

Bajar los datos de un arreglo para tapar un hueco se usa para sacar algo de una lista: un enemigo que muere, un
disparo que salió de la pantalla, un mensaje viejo del chat. Y devolver un número desde una función sirve para
contar cualquier cosa que la función hizo.

### Errores habituales

**Revisar de arriba para abajo.** Al bajar las filas, la que se revisa después ya cambió y se saltea.

**Olvidarse del `f++`.** Si dos filas seguidas están llenas, se borra una sola: la de arriba bajó y nadie la volvió a
mirar.

**`g >= 0` en el `for` que copia.** La fila 0 no tiene ninguna arriba: `tablero[-1]` no existe. Por eso va
`g > 0`, y la fila 0 se vacía aparte.

**Fuga de Texturas: no borrar nada.** Si la función cuenta las filas llenas pero no las borra, el pozo se llena en un
minuto y suma puntos sin parar.

### Micro-misión R05-N04-P1 · Caer de golpe

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Caída rápida | espacio: while (cabe(…, px, py + 1)) py++ · reloj = caida
recompensa: xp 10, oro 10
```

#### Escena
Las piezas bajan despacito, medio segundo por fila, y Kira ya sabe dónde las quiere poner. —En la Torre se
podía soltar la pieza —dice {mentor}— y caía de golpe, hasta donde llegara.

#### Gheco sugiere
Con el espacio, la pieza baja **mientras** quepa una fila más abajo:
```c
if (evento.key.key == SDLK_SPACE) {
    while (cabe(pieza, tablero, px, py + 1)) {
        py++;            /* una fila más… y otra… hasta que no cabe */
    }
    reloj = caida;       /* así se queda en el pozo en el cuadro que viene */
}
```
- `while` repite mientras la condición sea verdadera: puede bajar 0 filas o 17.
- Con el reloj lleno, en el cuadro siguiente la pieza ve que no puede bajar y se queda.

El robot va a apretar el espacio apenas empieza: la T tiene que caer al fondo, con la pata en el hueco de los
escombros.

#### Desafío
Hacé que con el espacio la pieza caiga de golpe hasta donde llegue.

#### Pasos
1. Buscá `/* acá: con el espacio, la pieza cae de golpe hasta donde llegue */` (en los eventos).
2. Debajo, escribí el `if` del espacio, con el `while`, de la sugerencia.
3. Tocá **Jugar**, hacé clic en el juego y apretá el espacio. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                /* acá: con el espacio, la pieza cae de golpe hasta donde llegue */
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
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
cuadros 3
```

#### Estado
```
pixel 306 466
```

#### Salida esperada
```
── Estado ──
pixel 306 466: #aa50ff
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
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
Kira aprieta el espacio y la T cae como una piedra: *¡clonc!*, con la pata justo en el hueco de los escombros.
Gheco, del susto, salta a los brazos de Arcadia.

#### Imagen
- La pantalla de la máquina con la pieza violeta en T cayendo de golpe al fondo del pozo, con rayas de velocidad.
- En el fondo del pozo, una fila de bloques grises con un hueco donde encaja la pata de la T.
- Gheco salta del susto a los brazos de Arcadia; Kira se ríe.

### Micro-misión R05-N04-P2 · La fila llena desaparece

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: fuga_texturas
carta: Borrar | contar ocupadas · si son COLS: cada fila g copia la g - 1 · fila 0 vacía · f++ para revisarla otra vez
recompensa: xp 10, monedas 4
```

#### Escena
La pata de la T tapó el hueco: la fila de abajo quedó llena de punta a punta. Pero no pasa nada. La Fuga de
Texturas se infla, contenta, entre los bloques grises. —Una fila llena se tiene que ir —dice {mentor}.

#### Gheco sugiere
La función `borrarLineas` ya se llama cada vez que una pieza se queda, pero está vacía. Adentro, revisá cada
fila **de abajo para arriba**:
```c
for (int f = FILAS - 1; f >= 0; f--) {
    int ocupadas = 0;
    for (int c = 0; c < COLS; c++) {
        if (tablero[f][c] != 0) {
            ocupadas++;
        }
    }
    if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
        for (int g = f; g > 0; g--) {       /* cada fila copia la de arriba */
            for (int c = 0; c < COLS; c++) {
                tablero[g][c] = tablero[g - 1][c];
            }
        }
        for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
            tablero[0][c] = 0;
        }
        borradas++;
        f++;                                /* revisar otra vez la misma fila */
    }
}
```
La fila llena queda pisada por la que tenía arriba, y todo baja una. El `f++` hace que la vuelta siguiente
mire otra vez la misma fila, por si lo que bajó también está lleno.

#### Desafío
Hacé que las filas llenas se borren y todo lo de arriba baje una fila.

#### Pasos
1. Buscá `/* acá: revisar cada fila de abajo para arriba; si está llena, bajar todo lo de arriba */` (en la función `borrarLineas`).
2. Debajo, escribí el `for` grande de la sugerencia.
3. Tocá **Jugar**, apretá el espacio y mirá la fila de escombros. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    /* acá: revisar cada fila de abajo para arriba; si está llena, bajar todo lo de arriba */
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
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
cuadros 3
```

#### Estado
```
pixel 210 466
```

#### Salida esperada
```
── Estado ──
pixel 210 466: #1c1c2c
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
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
La T tapa el hueco y la fila entera se borra: los escombros grises desaparecen y la T baja una fila. La Fuga de
Texturas se desinfla con un silbido, como un globo pinchado, y se va volando.

#### Imagen
- La pantalla de la máquina con una fila del fondo brillando y desapareciendo, y los bloques de arriba bajando.
- Una criatura como una nube que se desinfla con un silbido, volando lejos.
- Kira festeja con los brazos en alto; Arcadia aplaude; Gheco salta en el aire.

### Micro-misión R05-N04-P3 · Cuántas líneas

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Contar | lineas += borradas (lo que devolvió borrarLineas) · texto LINEAS %d
recompensa: xp 10, monedas 4
```

#### Escena
Las filas se borran, pero nadie lleva la cuenta. —La Torre se acuerda de cada fila que le sacaron —dice
{mentor}—. Contalas, que después las vamos a necesitar.

#### Gheco sugiere
`borrarLineas` **devuelve** cuántas filas borró, y eso se guarda en `borradas`. Ya está `lineas` en 0. Dos
cosas:
1. **Sumarlas**, abajo de `int borradas = borrarLineas(tablero);`:
```c
lineas += borradas;
```
2. **Mostrarlas** a la izquierda del pozo (el color blanco ya está puesto):
```c
SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
```
El robot va a apretar el espacio para que la T borre la fila de escombros.

#### Desafío
Contá las filas borradas y mostralas a la izquierda del pozo.

#### Pasos
1. Buscá `/* acá: sumar las filas borradas a las líneas */` y escribí `lineas += borradas;`.
2. Buscá `/* acá: mostrar las líneas a la izquierda del pozo */` y escribí el texto de la sugerencia.
3. Tocá **Jugar** y borrá la fila de escombros. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                /* acá: sumar las filas borradas a las líneas */
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        /* acá: mostrar las líneas a la izquierda del pozo */
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
cuadros 3
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: LINEAS 1
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
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
A la izquierda del pozo aparece **LINEAS 1**. Gheco lo anota con la cola en el vidrio empañado de la máquina,
por las dudas.

#### Imagen
- La pantalla de la máquina con el pozo y un contador blanco a la izquierda (sin letras legibles).
- Gheco dibuja una rayita con la cola en el vidrio empañado de la máquina.
- Kira y Arcadia sonríen.

### Micro-misión R05-N04-P4 · Más juntas, más puntos

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Premio | puntos += PREMIO[borradas] (0, 100, 300, 500, 800) · texto PUNTOS %d
recompensa: xp 10, monedas 4
```

#### Escena
—En la Torre —dice {mentor}— borrar una fila vale poco, y borrar cuatro de una vez vale muchísimo. Los
jugadores buenos esperan el palo largo para borrar cuatro juntas.

#### Gheco sugiere
Ya está la tabla `PREMIO`: cuántos puntos vale borrar 0, 1, 2, 3 o 4 filas juntas, y `puntos` en 0.
```c
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };
```
Dos cosas:
1. **Sumar el premio**, abajo de las líneas:
```c
puntos += PREMIO[borradas];   /* borradas es 0, 1, 2, 3 o 4 */
```
2. **Mostrarlos**, abajo de las líneas:
```c
SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
```
Borrar dos juntas (300) vale más que dos por separado (200): ahí está la gracia.

#### Desafío
Sumá los puntos con la tabla PREMIO y mostralos abajo de las líneas.

#### Pasos
1. Buscá `/* acá: más puntos si se borran varias juntas */` y escribí `puntos += PREMIO[borradas];`.
2. Buscá `/* acá: mostrar los puntos abajo de las líneas */` y escribí el texto de la sugerencia.
3. Tocá **Jugar** y borrá la fila de escombros. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                /* acá: más puntos si se borran varias juntas */
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        /* acá: mostrar los puntos abajo de las líneas */
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
cuadros 3
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: LINEAS 1 | PUNTOS 100
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
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
**PUNTOS 100**. Kira ya está mirando el pozo con otros ojos: deja un hueco largo a la derecha, esperando el
palo celeste. Arcadia sonríe: —Ya pensás como la Torre.

#### Imagen
- La pantalla de la máquina con el pozo, las piezas apiladas dejando un hueco largo a la derecha y dos contadores blancos (sin letras legibles).
- Kira mira el pozo, estratega, con la mano en el mentón; Arcadia sonríe.
- Gheco sostiene un palo de bloques celestes de verdad, listo para tirarlo.

## R05-N05 · Menú, fin y revancha

```meta
tipo: tema
criatura: bucle_eterno
padre: R05-N04
precio: 10
temas: juegos.estados
usa: juegos.sonido, prog.funciones, juegos.bucle
```

### Crónica

Kira juega y juega, y la pila llega hasta arriba de todo… y la máquina se queda colgada: la pieza nueva aparece
encima de las otras y nada se mueve. Ni una tecla responde. —El **Bucle Eterno** —dice {mentor}, y le da un
golpecito a la máquina—. Un juego tiene que saber cuándo empieza, cuándo se terminó y cómo se vuelve a empezar.
Como el Pong y el Snake: un menú, el fin y la revancha.

### Objetivos

Ordenar la Torre con **estados** (menú, jugando, perdiste) como en el Snake, darse cuenta de que **se tapó** cuando la
pieza nueva ya no cabe, volver a jugar con la **R** y sumarle **sonido**.

### Antes de empezar

El nodo anterior. De R04: el `enum`, el menú y la revancha (N04). De R01: el pitido (N09).

### Explicación

#### Los estados, otra vez
El mismo `enum` del Snake: `MENU`, `JUGANDO` y `PERDISTE`. Cada parte del juego mira el estado: el reloj solo junta
tiempo jugando, las teclas de la pieza solo andan jugando, y cada estado dibuja su cartel. En el menú se empieza
con el **Enter** (el espacio ya hace caer la pieza).

#### ¿Cuándo se pierde?
En el Tetris no hay vidas: se pierde cuando la torre llega hasta arriba. ¿Cómo se sabe? Justo después de sacar una
pieza nueva, se pregunta si **cabe** donde aparece. Si no cabe, es que ya hay bloques ahí: la torre se tapó.

#### Volver a empezar
La función `armar` deja el pozo como al principio: todas las casillas en 0 y la fila de escombros abajo. Es la
misma que se usa al arrancar, así la revancha queda **igual** que la primera partida. Con la R se arma el pozo, se
ponen las líneas y los puntos en 0 y se vuelve a jugar.

#### El sonido
El `pitido` de R01: uno grave y cortito cada vez que una pieza se queda (*toc*) y uno agudo, más largo, cuando se
borra alguna fila.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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

Todo juego tiene estados: el menú, la partida, la pausa, el fin. Y una función que deja todo «como al principio» es
la manera segura de armar la revancha: si se usa la misma para arrancar, no se olvida nada.

### Errores habituales

**Empezar con el espacio.** El espacio hace caer la pieza: si también empieza, la primera pieza cae de golpe apenas
se arranca. Por eso el menú usa el Enter.

**Preguntar si se perdió antes de sacar la pieza.** Hay que preguntar por la pieza **nueva**, en el lugar donde
aparece, recién sacada.

**La revancha que no vacía el pozo.** Si la R solo cambia el estado, la pieza nueva sigue sin caber y se vuelve a
perder en el acto.

**Bucle Eterno: el juego que sigue sin cartel.** Si no se cambia el estado al perder, la pieza nueva se queda
encimada y el juego parece colgado.

### Micro-misión R05-N05-P1 · El menú de la Torre

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Estados | MENU: el reloj no corre, cartel LA TORRE · Enter: JUGANDO · las teclas de la pieza, solo JUGANDO
recompensa: xp 10, oro 10
```

#### Escena
La máquina se prende y la pieza ya está cayendo, sin aviso. —Primero el nombre bien grande —dice {mentor}—,
y que nada se mueva hasta que el jugador diga «empiezo».

#### Gheco sugiere
Ya están el `enum` (`MENU`, `JUGANDO`, `PERDISTE`), `estado` en `MENU` y las teclas de la pieza solo andan
jugando. Tres cosas:
1. **El Enter empieza**, en los eventos:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
    estado = JUGANDO;
}
```
2. **El reloj corre solo jugando**, en lugar del `reloj += dt;` solo:
```c
if (estado == JUGANDO) {
    reloj += dt;
}
```
3. **El cartel del menú**, al final del dibujo:
```c
if (estado == MENU) {
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_SetRenderScale(lapiz, 4, 4);          /* letras cuatro veces más grandes */
    SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
    SDL_SetRenderScale(lapiz, 1, 1);
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
    SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
}
```
El robot va a esperar un segundo en el menú y después apretar el Enter.

#### Desafío
Hacé el menú: la pieza quieta y el cartel hasta que se apriete el Enter.

#### Pasos
1. Buscá `/* acá: en el menú, el Enter empieza la partida */` y escribí el `if` del Enter.
2. Buscá `/* acá: el reloj corre solo mientras se juega */`, borrá el `reloj += dt;` de abajo y escribí el `if` de la sugerencia.
3. Buscá `/* acá: el menú: el nombre grande y cómo se empieza */` y escribí el `if (estado == MENU)` del cartel.
4. Tocá **Jugar**, mirá el menú y apretá el Enter. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            /* acá: en el menú, el Enter empieza la partida */
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* acá: el reloj corre solo mientras se juega */
        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        /* acá: el menú: el nombre grande y cómo se empieza */
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
cuadros 60
tecla Enter
cuadros 30
```

#### Estado
```
buscar #aa50ff
```

#### Salida esperada
```
── Estado ──
buscar #aa50ff: x 272, y 48, ancho 71, alto 47
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
La pantalla se prende con **LA TORRE** en letras amarillas enormes, y la pieza espera, quieta. Kira aprieta el
Enter: el cartel se va y la T empieza a bajar. Gheco aplaude como en el cine.

#### Imagen
- La pantalla de la máquina con un cartel amarillo enorme sobre el pozo (sin letras legibles) y la pieza quieta arriba.
- Kira apoya el dedo sobre un botón grande de la máquina; Arcadia sonríe.
- Gheco aplaude, sentado arriba de la máquina, como en el cine.

### Micro-misión R05-N05-P2 · La torre se tapó

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
criatura: bucle_eterno
carta: Fin | al sacar la pieza nueva: si no cabe(…, px, py): PERDISTE · cartel SE TAPO LA TORRE
recompensa: xp 10, monedas 4
```

#### Escena
Kira deja caer pieza tras pieza sin borrar nada, y la pila llega hasta arriba. La pieza nueva aparece encima
de las otras y todo se cuelga. El Bucle Eterno da vueltas y vueltas alrededor de la máquina.

#### Gheco sugiere
Se pierde cuando la pieza nueva ya no cabe donde aparece. Dos cosas:
1. **Preguntar**, justo después de sacarla (después de `px = 3;` y `py = 0;`):
```c
if (!cabe(pieza, tablero, px, py)) {
    estado = PERDISTE;
}
```
2. **El cartel**, al final del dibujo:
```c
if (estado == PERDISTE) {
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
}
```
Como el reloj solo corre jugando, al perder la pieza se queda quieta. El robot va a empezar y soltar piezas
de golpe, sin moverlas, hasta llenar el pozo.

#### Desafío
Hacé que se pierda cuando la pieza nueva ya no cabe, con el cartel SE TAPO LA TORRE.

#### Pasos
1. Buscá `/* acá: si la pieza nueva ya no cabe, la torre se tapó: perdiste */` y escribí el `if` de la sugerencia.
2. Buscá `/* acá: el cartel de perdiste, amarillo, sobre el pozo */` y escribí el `if` del cartel.
3. Tocá **Jugar**, empezá y soltá piezas con el espacio hasta llenar el pozo. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                /* acá: si la pieza nueva ya no cabe, la torre se tapó: perdiste */
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        /* acá: el cartel de perdiste, amarillo, sobre el pozo */
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 2
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: LINEAS 1 | PUNTOS 100 | SE TAPO LA TORRE
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
La pila llega arriba de todo y la máquina dice, en amarillo, **SE TAPO LA TORRE**. La pieza se queda quieta.
El Bucle Eterno se frena de golpe, mareado, y se va caminando en zigzag.

#### Imagen
- La pantalla de la máquina con el pozo lleno de bloques de colores hasta arriba y un cartel amarillo (sin letras legibles).
- Una criatura que es un aro de luz girando se frena, mareada, y se va caminando en zigzag.
- Kira se rasca la cabeza; Arcadia sonríe; Gheco se tapa los ojos.

### Micro-misión R05-N05-P3 · Otra vez

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Revancha | R en PERDISTE: armar(tablero) · lineas = 0 · puntos = 0 · px = 3, py = 0 · JUGANDO
recompensa: xp 10, monedas 4
```

#### Escena
La torre se tapó y ahí se quedó. Kira aprieta todas las teclas: nada. —Una revancha —pide—. —La función
`armar` deja el pozo como al principio —dice {mentor}—: la misma que se usa al prender la máquina.

#### Gheco sugiere
Después de perder, la R deja todo como al principio y se vuelve a jugar:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
    armar(tablero);     /* el pozo vacío, con los escombros */
    lineas = 0;
    puntos = 0;
    px = 3;             /* la pieza, arriba */
    py = 0;
    estado = JUGANDO;
}
```
Y avisarlo, abajo del cartel:
```c
if (estado == PERDISTE) {
    SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
}
```
`armar` es la misma función que arma el pozo al principio del `main`: así la revancha arranca igual.

#### Desafío
Hacé que con la R, después de perder, el pozo quede como al principio y se vuelva a jugar.

#### Pasos
1. Buscá `/* acá: después de perder, la R deja todo como al principio y se vuelve a jugar */` y escribí el `if` de la R.
2. Buscá `/* acá: avisar que con la R se juega otra vez */` y escribí el `if` del aviso.
3. Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            /* acá: después de perder, la R deja todo como al principio y se vuelve a jugar */
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        /* acá: avisar que con la R se juega otra vez */
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 2
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla R
cuadros 3
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: LINEAS 0 | PUNTOS 0
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
Kira aprieta la R y el pozo se vacía de golpe, con un *fsss*, como si alguien hubiera barrido la torre. La
fila de escombros vuelve a su lugar, y arriba asoma la pieza siguiente. —Ahora sí —dice Kira.

#### Imagen
- La pantalla de la máquina con el pozo vacío otra vez, la fila de escombros grises abajo y una pieza nueva arriba.
- Kira, decidida, se arremanga el brazal; Arcadia le guiña un ojo.
- Gheco barre con la cola unos bloquecitos que quedaron sobre la máquina.

### Micro-misión R05-N05-P4 · Toc y tin

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia
carta: Sonido | al quedarse: pitido(parlante, 220, 0.05f) · si borradas > 0: pitido(parlante, 880, 0.15f)
recompensa: xp 10, monedas 4
```

#### Escena
La Torre de Kira anda entera, pero muda. Desde lo alto de la Torre de verdad, en cambio, cada bloque suena
al acomodarse: *toc*. Y cuando se va una fila entera, *tiiin*.

#### Gheco sugiere
Ya están el parlante y la función `pitido` (la de R01). Dos sonidos, donde una pieza se queda en el pozo:
```c
pitido(parlante, 220, 0.05f);         /* toc: grave y cortito */
int borradas = borrarLineas(tablero);
if (borradas > 0) {
    pitido(parlante, 880, 0.15f);     /* tin: agudo y más largo */
}
```
El primero va **antes** de `int borradas = …` y el segundo, **después**. El robot va a empezar y soltar la
primera pieza: tiene que sonar el toc y, como borra la fila de escombros, también el tin.

#### Desafío
Hacé que suene un toc cuando una pieza se queda y un tin cuando se borra alguna fila.

#### Pasos
1. Buscá `/* acá: un toc grave cada vez que una pieza se queda */` y escribí el primer `pitido`.
2. Buscá `/* acá: y uno agudo si borró alguna fila */` y escribí el `if` con el segundo `pitido`.
3. Tocá **Jugar**, empezá y soltá la primera pieza. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                /* acá: un toc grave cada vez que una pieza se queda */
                int borradas = borrarLineas(tablero);
                /* acá: y uno agudo si borró alguna fila */
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 2
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

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
*Toc… tiiin*. La primera fila se va con un sonido que hace sonreír a Arcadia. —Así sonaba la Torre cuando el
Vidriero jugaba —dice, bajito.

#### Imagen
- La pantalla de la máquina con una fila brillando al borrarse y notas musicales saliendo del parlante.
- Arcadia sonríe con nostalgia, con los auriculares gamer al cuello; Kira juega concentrada.
- Gheco baila con las notas musicales arriba de la máquina.

## R05-N06 · Jefe: La Torre que no para

```meta
tipo: jefe
criatura: glitch
padre: R05-N05
precio: 10
insignia: Sello de la Torre que no para
insignia_descripcion: Detuviste a la Torre que no para: un Tetris entero, con el pozo en una matriz, las siete piezas que giran, las líneas que se borran, la pieza siguiente, los escombros que empujan, la caída que se acelera, el menú, la revancha y el sonido.
temas: juegos.estados
usa: col.matrices, prog.funciones, prog.matematica-azar, juegos.bucle
```

### Crónica

Cuando Kira borra la décima fila, la máquina tiembla. Los bloques de la torre de verdad empiezan a moverse solos,
se despegan de las paredes y se acomodan en una figura enorme: un gigante hecho de bloques de colores, con dos
ventanas encendidas por ojos y una pieza girando arriba, como un sombrero. Bosteza con un ruido de piedras. —Hace
treinta años que apilo sin parar —dice, con voz cansada—. No sé frenar. Nadie me enseñó. Si me ganás, a lo mejor
puedo dormir. Es **la Torre que no para**, y no va a esperar a nadie: empuja escombros desde abajo y se apura cada
vez más.

### Objetivos

Terminar el Tetris completo contra la Torre: mostrar la **pieza siguiente**, aguantar los **escombros** que la Torre
empuja desde abajo cada 10 segundos, una **caída que se acelera** con el nivel y un **cartel final centrado** que dice
si la Torre se detuvo.

### Antes de empezar

Toda la rama R05. De R03: el muro que bajaba con un temporizador (N07). De R04: el cartel centrado del jefe (N05).

### Explicación

#### La pieza siguiente
Los jugadores buenos miran qué viene. Se guarda `siguiente`, elegida al azar desde el principio. Cuando sale una
pieza nueva, **es la que estaba esperando** (`tipo = siguiente`) y recién ahí se elige otra para después. Se
dibuja a la derecha del pozo, con su cajita de la tabla `PIEZAS`.

#### Los escombros desde abajo
Un temporizador, `relojTorre`, como el muro de R03. Cada 10 segundos, todo el pozo **sube** una fila (cada fila
copia la de abajo, al revés que al borrar) y la de abajo se llena de escombros grises con un hueco al azar. Si la
pieza que cae puede, sube también, para no quedar adentro.

#### Cada vez más rápido
Otro temporizador, `relojNivel`. Cada 20 segundos sube el nivel y la caída se multiplica por 0,8: medio segundo
pasa a ser 0,4, después 0,32… Con `SDL_max(0.1f, …)` nunca baja de una décima, para que se pueda jugar.

#### El cartel del final
Con 10 líneas o más, «LA TORRE SE DETIENE»; si no, «LA TORRE TE TAPO». Centrado como siempre: `320 - letras * 4`.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        if (estado == JUGANDO) {
            relojNivel += dt;
        }
        if (relojNivel >= 20) {
            relojNivel -= 20;
            nivel++;
            caida = SDL_max(0.1f, caida * 0.8f);
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            const char *cartel = (lineas >= 10) ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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

«Lo que viene después» se usa en todos los juegos que se planifican (la próxima pieza, la próxima oleada, la
próxima carta). Y el Tetris completo es tu cuarto juego entero: lo vas a poder bajar y jugar en tu compu.

### Errores habituales

**Elegir la siguiente antes de usarla.** Si se hace `siguiente = SDL_rand(7)` antes de `tipo = siguiente`, la pieza que
se mostraba nunca sale: sale otra.

**Subir las filas de arriba para abajo.** Para subir, cada fila copia la de **abajo**, empezando por la fila 0. Si se
empieza por abajo, se copia la misma fila de escombros en todo el pozo.

**La caída que llega a 0.** Sin `SDL_max`, después de muchos niveles la pieza cae en un solo cuadro y no se puede
jugar.

**Glitch: dibujar la siguiente con el color de la que cae.** Hay que usar `COLORES[siguiente + 1]`, no `tipo + 1`.

### Micro-misión R05-N06-P1 · La que viene

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia, la Torre que no para
carta: Siguiente | al sacar: tipo = siguiente · siguiente = SDL_rand(7) · dibujarla a la derecha en (470 + c * CELDA, 60 + f * CELDA)
recompensa: xp 10, oro 10
```

#### Escena
—Te voy a dar una ventaja —dice la Torre, y una de sus ventanas se enciende a un costado del pozo—. Vas a
ver la pieza que viene. Yo siempre la sé. Si vos también la sabés, quizás me alcances.

#### Gheco sugiere
Ya está `siguiente`, elegida al azar al principio. Dos cosas:
1. **La pieza nueva es la que esperaba**, en lugar de `tipo = SDL_rand(7);`:
```c
tipo = siguiente;          /* sale la que se estaba mostrando */
siguiente = SDL_rand(7);   /* y se elige otra para después */
```
2. **Dibujarla** a la derecha del pozo, con su cajita de la tabla:
```c
SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
for (int f = 0; f < 4; f++) {
    for (int c = 0; c < 4; c++) {
        if (PIEZAS[siguiente][f][c] == 1) {
            SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
            SDL_RenderFillRect(lapiz, &bloque);
        }
    }
}
SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
```
El orden importa: primero se usa la que esperaba, después se elige otra.

#### Desafío
Mostrá la pieza siguiente a la derecha del pozo, y hacé que sea la que sale después.

#### Pasos
1. Buscá `/* acá: la pieza nueva es la que estaba esperando, y se elige otra para después */`, borrá el `tipo = SDL_rand(7);` de abajo y escribí las dos líneas de la sugerencia.
2. Buscá `/* acá: mostrar la pieza siguiente a la derecha del pozo */` y escribí el texto, el color y los dos `for` de la sugerencia.
3. Tocá **Jugar** y empezá: a la derecha tiene que verse la que viene. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                /* acá: la pieza nueva es la que estaba esperando, y se elige otra para después */
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        /* acá: mostrar la pieza siguiente a la derecha del pozo */
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 3
```

#### Estado
```
pixel 500 90
```

#### Salida esperada
```
── Estado ──
pixel 500 90: #ffdc00
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
A la derecha del pozo aparece un cuadrado amarillo: la que viene. Cuando la T se queda, sale justo el
cuadrado, y a la derecha aparece otra. Kira ya no juega a ciegas. La Torre bosteza: —Bien. Ahora en serio.

#### Imagen
- La Torre que no para: un gigante hecho de bloques de colores, con dos ventanas encendidas por ojos y una pieza girando arriba como sombrero, enciende una ventana a un costado.
- En la pantalla de la máquina, el pozo y, a la derecha, una cajita con un cuadrado amarillo.
- Kira mira la cajita de la derecha, atenta; Arcadia mira a la Torre; Gheco, sobre la máquina, señala la cajita.

### Micro-misión R05-N06-P2 · Los escombros de la Torre

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia, la Torre que no para
carta: Temporizador | relojTorre += dt · a los 10 s: cada fila copia la de abajo · abajo escombros con hueco = SDL_rand(COLS) · py--
recompensa: xp 10, monedas 4
```

#### Escena
La Torre golpea el piso con un pie de bloques y desde abajo del pozo sube una fila gris, empujando todo para
arriba. —Yo no paro —dice—. Mientras vos acomodás, yo apilo desde abajo.

#### Gheco sugiere
Ya está `relojTorre`. Cada 10 segundos (jugando), todo el pozo sube una fila y abajo aparecen escombros con un
hueco al azar:
```c
if (estado == JUGANDO) {
    relojTorre += dt;
}
if (relojTorre >= 10) {
    relojTorre -= 10;
    for (int f = 0; f < FILAS - 1; f++) {      /* cada fila copia la de abajo */
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = tablero[f + 1][c];
        }
    }
    int hueco = SDL_rand(COLS);                 /* escombros con un hueco al azar */
    for (int c = 0; c < COLS; c++) {
        tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
    }
    if (py > 0) {
        py--;                                   /* la pieza también sube */
    }
}
```
`(c == hueco) ? 0 : 8` es un `if` en una línea: 0 (vacía) en el hueco, 8 (escombros) en las demás. El robot va
a empezar y esperar 10 segundos: la primera pieza borra los escombros del principio, así que los grises
tienen que ser los nuevos.

#### Desafío
Hacé que cada 10 segundos todo suba una fila y abajo aparezcan escombros con un hueco al azar.

#### Pasos
1. Buscá `/* acá: cada 10 segundos, la Torre empuja una fila de escombros desde abajo */`.
2. Debajo, escribí los dos `if` de la sugerencia: el que junta el tiempo y el que empuja los escombros.
3. Tocá **Jugar**, empezá y esperá 10 segundos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        /* acá: cada 10 segundos, la Torre empuja una fila de escombros desde abajo */
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 620
```

#### Estado
```
buscar #6e6e78
```

#### Salida esperada
```
── Estado ──
buscar #6e6e78: x 200, y 456, ancho 239, alto 23
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
Cada diez segundos, el pozo sube con un *grrr* de piedras y abajo aparece una fila gris con un hueco. Kira mete
la pieza justo en el hueco y la fila se borra. La Torre gruñe, sorprendida: —Nadie me había devuelto los
escombros.

#### Imagen
- La Torre que no para, el gigante de bloques de colores, golpea el piso con un pie y hace subir una fila de bloques grises.
- En la pantalla de la máquina, el pozo con una fila gris nueva abajo, con un hueco, empujando todo para arriba.
- Kira juega rápido, decidida; Arcadia se agarra de la máquina que tiembla; Gheco se sujeta de los auriculares de Arcadia.

### Micro-misión R05-N06-P3 · Cada vez más rápido

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia, la Torre que no para
carta: Nivel | relojNivel += dt · a los 20 s: nivel++ · caida = SDL_max(0.1f, caida * 0.8f) · texto NIVEL %d
recompensa: xp 10, monedas 4
```

#### Escena
La pieza en sombrero de la Torre gira cada vez más rápido. —Y cada rato —dice— me apuro un poquito. Nunca
dejo de apurarme. Por eso me llaman así.

#### Gheco sugiere
Ya están `relojNivel` y `nivel` (en 1). Cada 20 segundos (jugando), sube el nivel y la caída se acorta:
```c
if (estado == JUGANDO) {
    relojNivel += dt;
}
if (relojNivel >= 20) {
    relojNivel -= 20;
    nivel++;
    caida = SDL_max(0.1f, caida * 0.8f);   /* un 20 % más rápido, pero nunca menos de 0,1 s */
}
```
Y mostrar el nivel, abajo de los puntos:
```c
SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
```
`SDL_max` devuelve el más grande de los dos: si `caida * 0.8f` quedara muy chiquito, se queda en 0,1. El robot
va a empezar y esperar 20 segundos.

#### Desafío
Hacé que cada 20 segundos suba el nivel y la pieza caiga más rápido, y mostrá el nivel.

#### Pasos
1. Buscá `/* acá: cada 20 segundos, la Torre se apura: sube el nivel y la pieza cae más rápido */` y escribí los dos `if` de la sugerencia.
2. Buscá `/* acá: mostrar el nivel abajo de los puntos */` y escribí el texto de la sugerencia.
3. Tocá **Jugar**, empezá y esperá 20 segundos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        /* acá: cada 20 segundos, la Torre se apura: sube el nivel y la pieza cae más rápido */
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        /* acá: mostrar el nivel abajo de los puntos */
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 1220
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: LINEAS 1 | PUNTOS 100 | NIVEL 2 | SIGUIENTE
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        if (estado == JUGANDO) {
            relojNivel += dt;
        }
        if (relojNivel >= 20) {
            relojNivel -= 20;
            nivel++;
            caida = SDL_max(0.1f, caida * 0.8f);
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
**NIVEL 2**, y las piezas bajan más ligero. **NIVEL 3**, más todavía. Kira ya no piensa: mira la siguiente,
gira, suelta. Las ventanas de la Torre parpadean, como si se le cerraran los ojos.

#### Imagen
- La Torre que no para, el gigante de bloques de colores, con la pieza en sombrero girando muy rápido y las ventanas parpadeando de sueño.
- En la pantalla de la máquina, piezas cayendo rápido con rayas de velocidad.
- Kira juega a toda velocidad, con los dedos en las flechas; Arcadia la alienta; Gheco gira como la pieza del sombrero.

### Micro-misión R05-N06-P4 · La Torre se detiene

```meta
lugar: La Torre que no para
personajes: Kira, Gheco, Arcadia, la Torre que no para
carta: Cartel centrado | al perder: cartel = lineas >= 10 ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO" · x = 320 - SDL_strlen(cartel) * 4
recompensa: xp 20, monedas 5
item: Pieza Dorada
```

#### Escena
—Borrá diez filas —dice la Torre, con los ojos casi cerrados— y, cuando termine la partida, que la máquina lo
diga en el medio, bien claro: que la Torre se detuvo. Y si no llegás, que diga la verdad: que te tapé.

#### Gheco sugiere
En lugar del cartel de antes («SE TAPO LA TORRE», corrido a ojo), uno centrado que depende de las líneas:
```c
if (estado == PERDISTE) {
    const char *cartel = (lineas >= 10) ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO";
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
}
```
- Con 10 líneas o más, le ganaste a la Torre aunque después te haya tapado.
- Cada letra mide 8 píxeles: un texto de `n` letras, centrado, empieza en `320 - n * 4` (como los carteles
  del Campeón, del Muro y de la Serpiente).

El robot va a empezar y soltar piezas de golpe hasta llenar el pozo.

#### Desafío
Cambiá el cartel del final por uno centrado: LA TORRE SE DETIENE con 10 líneas o más, LA TORRE TE TAPO si no.

#### Pasos
1. Buscá `/* acá: el cartel del final, centrado: con 10 líneas o más, la Torre se detiene */` y borrá el `if` de abajo.
2. En su lugar, escribí el `if` de la sugerencia.
3. Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        if (estado == JUGANDO) {
            relojNivel += dt;
        }
        if (relojNivel >= 20) {
            relojNivel -= 20;
            nivel++;
            caida = SDL_max(0.1f, caida * 0.8f);
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        /* acá: el cartel del final, centrado: con 10 líneas o más, la Torre se detiene */
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
tecla Enter
cuadros 2
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
tecla Espacio
cuadros 3
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: LINEAS 1 | PUNTOS 100 | NIVEL 1 | SIGUIENTE | LA TORRE TE TAPO | R: OTRA VEZ
```

#### Solución
```c
#include <SDL3/SDL.h>

#define CELDA 24    /* cada celda del pozo mide 24 × 24 píxeles */
#define COLS 10     /* el pozo tiene 10 columnas… */
#define FILAS 20    /* …y 20 filas: 10 × 24 = 240 de ancho y 20 × 24 = 480 de alto */
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                if (x < 0 || x >= COLS) {
                    return false;
                }
                if (y >= FILAS) {
                    return false;
                }
                if (tablero[y][x] != 0) {
                    return false;
                }
            }
        }
    }
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */
    int pieza[4][4] = {                 /* la pieza que cae, en una cajita de 4 × 4: 1 es un bloque */
        { 0, 0, 0, 0 },
        { 1, 1, 1, 0 },
        { 0, 1, 0, 0 },
        { 0, 0, 0, 0 },
    };
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    int siguiente = SDL_rand(7);   /* la que viene después */
    int px = 3;   /* dónde está la cajita en el pozo: columna y fila de su esquina de arriba a la izquierda */
    int py = 0;
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    int lineas = 0;         /* cuántas filas se borraron */
    int puntos = 0;
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            reloj += dt;
        }
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        if (estado == JUGANDO) {
            relojNivel += dt;
        }
        if (relojNivel >= 20) {
            relojNivel -= 20;
            nivel++;
            caida = SDL_max(0.1f, caida * 0.8f);
        }
        if (reloj >= caida) {
            reloj -= caida;
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                pitido(parlante, 220, 0.05f);
                int borradas = borrarLineas(tablero);
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                lineas += borradas;
                puntos += PREMIO[borradas];
                tipo = siguiente;
                siguiente = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                px = 3;
                py = 0;
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLS; c++) {
                SDL_FRect celda = { OX + c * CELDA, f * CELDA, CELDA - 1, CELDA - 1 };
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                SDL_RenderFillRect(lapiz, &celda);
            }
        }
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        if (estado == PERDISTE) {
            const char *cartel = (lineas >= 10) ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
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
Diez filas. Once. Doce. La pila de Kira llega por fin hasta arriba y la pantalla dice, en amarillo y en el
medio, **LA TORRE SE DETIENE**. La Torre que no para deja de moverse. Por primera vez en treinta años, se sienta
despacio, apoya la cabeza de bloques en las nubes y ronca: *grrr… clonc… grrr*.

Antes de dormirse del todo, de su sombrero cae una pieza que brilla como el oro. Kira la ataja: la **Pieza
Dorada**, una T que pesa como una pluma.

En la pantalla aparece **otro pedazo del mapa del Vidriero**: una pista larga en las afueras, con biplanos de
madera y nubes pintadas. {mentor} sonríe: —La Pista de los Biplanos. Ahí sí que se vuela.

#### Imagen
- La Torre que no para, el gigante de bloques de colores, sentado y dormido con la cabeza apoyada en las nubes, roncando.
- En la pantalla de la máquina, un pedazo de mapa antiguo con una pista larga y biplanos de madera.
- Kira sostiene una pieza en forma de T que brilla como el oro; Arcadia mira el mapa, sonriente; Gheco abraza la pieza dorada.
