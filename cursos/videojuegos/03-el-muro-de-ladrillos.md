# RAMA R03 · El Muro de Ladrillos: Arkanoid

```meta
tipo: tronco
posicion: 3
```

## R03-N01 · La paleta y la pelota

```meta
tipo: tema
criatura: fantasma_fotograma
padre: R02-N07
precio: 10
temas: juegos.fisica
usa: juegos.entrada, juegos.colisiones, juegos.bucle
```

### Crónica

El pedazo de mapa que dejó el Campeón Invicto lleva a una plaza que Kira nunca había visto. En el medio hay un
paredón altísimo de ladrillos de vidrio, todos apagados, y al pie, una máquina de juegos con la pantalla negra.
—El Muro de Ladrillos —dice {mentor}, y pasa la mano por la madera—. Acá no hay rival del otro lado: hay una
pared. Tu paleta abajo, una pelota y todo un muro para romper. Pero primero, lo primero: que la paleta se
mueva y la pelota rebote. Gheco se trepa a la máquina y, en la pantalla, algo se mueve a los saltos: un
**Fantasma del Fotograma**, que va rápido o lento según el humor de la compu.

### Objetivos

Armar la base del Arkanoid con lo que ya sabés del Pong: una **paleta abajo** que se mueve con las flechas
(sin salirse de la pantalla), una **pelota** que rebota en las **dos paredes y en el techo**, la paleta que la
**devuelve hacia arriba** y la pelota que **espera arriba de la paleta** hasta que apretás el espacio.

### Antes de empezar

Toda la rama R02 (el Pong): la velocidad `vx` y `vy`, el rebote dando vuelta un signo y la función `toca`.
De R01: el teclado (N02) y el delta time (N04).

### Explicación

#### Qué es el Arkanoid
Una paleta abajo, una pelota y una pared de ladrillos arriba. La pelota rompe cada ladrillo que toca y rebota.
Si se te cae por abajo, perdés una vida. Ganás cuando no queda ningún ladrillo. Es el Pong de un solo jugador:
en vez de un rival, una pared. En este nodo armamos la paleta y la pelota; en el que sigue, los ladrillos.

#### Lo mismo que el Pong, de costado
En el Pong las paletas estaban a los costados y se movían para arriba y para abajo. Acá la paleta está
**abajo** y se mueve para la **izquierda** y la **derecha**: se cambia `y` por `x`, y la W y la S por las flechas
`SDL_SCANCODE_LEFT` y `SDL_SCANCODE_RIGHT`. Para que no se salga, `SDL_clamp` la deja entre 0 y `640 - paleta.w`.

#### Tres paredes, no cuatro
La pelota rebota en la pared de la **izquierda** y en la de la **derecha** (dando vuelta `vx`) y en el **techo**
(dando vuelta `vy`). Abajo no hay pared: si la pelota pasa el borde de abajo (`pelota.y > 480`), se cayó.

#### La paleta devuelve
Si la pelota **viene bajando** (`vy > 0`) y toca la paleta, se la pone justo arriba de la paleta y se le da la
vuelta a `vy`, para que suba. Preguntar `vy > 0` evita que la paleta la devuelva dos veces seguidas (lo mismo
que con las paletas del Pong).

#### La pelota pegada
Al empezar (y cada vez que se cae), la pelota espera **arriba de la paleta** y viaja con ella. Una variable
`bool pegada` dice si está esperando. Mientras está pegada, en cada cuadro se la pone en el medio de la paleta;
cuando apretás el **espacio**, se despega y sale hacia arriba.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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

La paleta que se mueve con un tope, la pelota con velocidad y los rebotes en las paredes son la base de un montón
de juegos. Y la pelota que espera al jugador es una idea de todos los juegos: el juego no arranca solo, espera
a que estés listo.

### Errores habituales

**Mover la paleta sin `dt`.** `paleta.x -= 5;` va más rápido en una compu rápida y más lento en una lenta: es
el Fantasma del Fotograma. Siempre `400 * dt`.

**Olvidar el tope.** Sin `SDL_clamp`, la paleta se va de la pantalla y no vuelve más.

**Rebotar en el piso.** Si se pone un rebote abajo, la pelota nunca se cae y el juego no tiene gracia: abajo
no hay pared.

**Devolverla aunque suba.** Sin el `vy > 0`, si la pelota sigue tocando la paleta en el cuadro siguiente, se da
vuelta otra vez y se queda temblando en la paleta.

### Micro-misión R03-N01-P1 · La paleta de abajo

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Mover de costado | flechas: paleta.x ∓ 400 * dt · SDL_clamp(paleta.x, 0, 640 - paleta.w)
recompensa: xp 10, oro 10
```

#### Escena
La máquina se enciende con un zumbido. Abajo de la pantalla aparece una rayita celeste: la paleta. Kira
aprieta las flechas, pero la rayita no se mueve. —Está dormida —dice {mentor}—. Despertala.

#### Gheco sugiere
La paleta es un rectángulo, `paleta`, abajo de todo. Como en el Pong, se lee el teclado con
`SDL_GetKeyboardState`, pero ahora la paleta se mueve **de costado** (cambia su `x`):
```c
if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;    /* flecha izquierda */
if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;   /* flecha derecha */
paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);      /* que no se salga */
```
- Restar a `x` la lleva a la izquierda; sumar, a la derecha.
- `400 * dt` son 400 píxeles por segundo, en cualquier compu (el delta time).
- `SDL_clamp(valor, mínimo, máximo)` deja el valor adentro de los límites: el borde izquierdo de la paleta
  no baja de 0 y no pasa de `640 - paleta.w`, para que no se salga por la derecha.

El robot va a mantener apretada la flecha izquierda medio segundo.

#### Desafío
Hacé que la paleta se mueva con las flechas izquierda y derecha, sin salirse de la pantalla.

#### Pasos
1. Buscá el comentario `/* acá: mover la paleta con las flechas, sin que se salga de la pantalla */`.
2. Debajo, escribí las dos líneas con `SDL_SCANCODE_LEFT` y `SDL_SCANCODE_RIGHT` de la sugerencia.
3. Agregá la línea con `SDL_clamp` para el tope.
4. Tocá **Jugar**, hacé clic en el juego y probá las flechas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
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

        const bool *teclas = SDL_GetKeyboardState(NULL);
        /* acá: mover la paleta con las flechas, sin que se salga de la pantalla */

        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */


        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
apretar Izquierda
cuadros 30
soltar Izquierda
cuadros 2
```

#### Estado
```
buscar #00e5ff
```

#### Salida esperada
```
── Estado ──
buscar #00e5ff: x 83, y 440, ancho 80, alto 12
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
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

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */


        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
La rayita celeste se desliza de un lado al otro y se frena justo en el borde, sin caerse. El Fantasma
del Fotograma intenta hacerla saltar, pero con el `dt` la paleta va siempre a la misma velocidad.

#### Imagen
- La máquina del Muro de Ladrillos encendida, con una paleta celeste abajo de la pantalla y una flecha de movimiento.
- Kira aprieta las flechas, concentrada; Arcadia mira por encima de su hombro.
- Un fantasma translúcido que parpadea entre dos posiciones se desvanece al costado de la pantalla; Gheco lo señala.

### Micro-misión R03-N01-P2 · Tres paredes

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Rebotar en tres lados | costados: vx = -vx · techo: vy = -vy · abajo no hay pared
recompensa: xp 10, monedas 4
```

#### Escena
La pelota amarilla sale disparada… y se va por arriba de la pantalla, como si no hubiera techo. Gheco
la busca detrás de la máquina. —En esta máquina hay tres paredes —explica {mentor}—: los dos costados y
el techo. Abajo no: abajo está tu paleta.

#### Gheco sugiere
La pelota ya se mueve sola con `vx` y `vy`. Falta que rebote. Igual que en el Pong, rebotar es poner la
pelota justo en el borde y dar vuelta un signo:
```c
if (pelota.x < 0) {                    /* pared izquierda */
    pelota.x = 0;
    vx = -vx;
}
if (pelota.x + pelota.w > 640) {       /* pared derecha */
    pelota.x = 640 - pelota.w;
    vx = -vx;
}
if (pelota.y < 0) {                    /* techo */
    pelota.y = 0;
    vy = -vy;
}
```
- En los **costados** cambia la dirección de costado: `vx`.
- En el **techo** cambia la dirección de arriba abajo: `vy`.
- Para la pared derecha se mira el borde derecho de la pelota, `pelota.x + pelota.w`.

#### Desafío
Hacé que la pelota rebote en la pared izquierda, en la derecha y en el techo.

#### Pasos
1. Buscá el comentario `/* acá: rebotar en la pared izquierda, en la derecha y en el techo */`.
2. Debajo, escribí los tres `if` de la sugerencia.
3. Tocá **Jugar** y mirá cómo rebota arriba. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
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

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        /* acá: rebotar en la pared izquierda, en la derecha y en el techo */


        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
cuadros 70
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 491, y 51, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
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

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }


        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
La pelota pega en el techo con un brillo y vuelve a bajar. Gheco sale de atrás de la máquina, todavía
buscándola. —Ahora sí tiene paredes —se ríe Kira.

#### Imagen
- La pantalla de la máquina con la pelota amarilla rebotando en el techo, con una línea punteada de su recorrido.
- Kira señala el rebote; Arcadia asiente con los brazos cruzados.
- Gheco se asoma por detrás de la máquina, buscando la pelota.

### Micro-misión R03-N01-P3 · La paleta devuelve

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Devolver hacia arriba | si toca(pelota, paleta) y vy > 0: arriba de la paleta y vy = -vy
recompensa: xp 10, monedas 4
```

#### Escena
La pelota rebota en el techo, baja… y atraviesa la paleta como si fuera de aire. Vuelve a aparecer en el
medio, como si nada. —Tu paleta todavía no sabe pegarle —dice {mentor}.

#### Gheco sugiere
Para saber si la pelota toca la paleta está la función `toca` (la de los dos rectángulos, de R01-N05).
Si la pelota **viene bajando** (`vy > 0`) y la toca:
```c
if (toca(pelota, paleta) && vy > 0) {
    pelota.y = paleta.y - pelota.h;   /* justo arriba de la paleta */
    vy = -vy;                         /* y para arriba */
}
```
- Se la pone arriba de la paleta para que no quede metida adentro.
- `vy > 0` hace que solo la devuelva cuando baja: si en el cuadro siguiente sigue tocándola, ya va
  subiendo y no se da vuelta otra vez.

El robot va a llevar la paleta hacia la derecha, para ponerla donde cae la pelota.

#### Desafío
Hacé que la paleta devuelva la pelota hacia arriba cuando la toca al bajar.

#### Pasos
1. Buscá el comentario `/* acá: si la pelota baja y toca la paleta, vuelve a subir */`.
2. Debajo, escribí el `if` con `toca(pelota, paleta) && vy > 0` de la sugerencia.
3. Tocá **Jugar** y poné la paleta debajo de la pelota. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
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

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        /* acá: si la pelota baja y toca la paleta, vuelve a subir */

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
apretar Derecha
cuadros 40
soltar Derecha
cuadros 120
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 541, y 353, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
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

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
*¡Toc!* La pelota pega en la paleta y vuelve a subir. Kira la persigue de un lado al otro. —¡La tengo!
—grita, y {mentor} sonríe: así empieza cada partida en el Muro.

#### Imagen
- La pelota amarilla rebota hacia arriba desde la paleta celeste, con una chispa.
- Kira mueve la paleta con decisión; Arcadia festeja con un puño.
- Gheco, sentado arriba de la máquina, sigue la pelota con la cabeza.

### Micro-misión R03-N01-P4 · La pelota espera

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Pelota pegada | bool pegada · si pegada: arriba de la paleta · espacio: pegada = false
recompensa: xp 10, monedas 4
```

#### Escena
Cada vez que la pelota se cae, vuelve a salir sola desde el medio, y Kira no llega nunca. —En esta
máquina la pelota te espera —dice {mentor}—. Se queda arriba de tu paleta hasta que vos digas.

#### Gheco sugiere
Ya está la variable `bool pegada`, que arranca en `true`. Se usa en tres lugares:
1. **Al mover la pelota:** si está pegada, se la pone en el medio de la paleta; si no, se mueve sola:
```c
if (pegada) {
    pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;   /* el medio de la paleta */
    pelota.y = paleta.y - pelota.h;                      /* apoyada arriba */
} else {
    pelota.x += vx * dt;
    pelota.y += vy * dt;
}
```
2. **Con el espacio**, en los eventos (como en R01-N02, una sola vez por apretada):
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
    pegada = false;
    vx = 150;
    vy = -300;    /* sale hacia arriba */
}
```
3. **Cuando se cae**, en lugar de volver al medio: `pegada = true;`.

#### Desafío
Hacé que la pelota espere arriba de la paleta y salga recién cuando se aprieta el espacio.

#### Pasos
1. Buscá `/* acá: si está pegada, la pelota viaja arriba de la paleta; si no, se mueve sola */`, borrá las dos líneas de abajo y escribí el `if (pegada) { … } else { … }`.
2. Buscá `/* acá: con el espacio, la pelota sale hacia arriba */` (en los eventos) y escribí el `if` con `SDLK_SPACE`.
3. Buscá `/* acá: vuelve a quedar pegada a la paleta */`, borrá las tres líneas de abajo y escribí `pegada = true;`.
4. Tocá **Jugar**: la pelota espera. Apretá el espacio para sacar. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con el espacio, la pelota sale hacia arriba */
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        /* acá: si está pegada, la pelota viaja arriba de la paleta; si no, se mueve sola */
        pelota.x += vx * dt;
        pelota.y += vy * dt;

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            /* acá: vuelve a quedar pegada a la paleta */
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
apretar Izquierda
cuadros 20
soltar Izquierda
cuadros 2
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 186, y 430, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
La pelota se queda quieta arriba de la paleta y la acompaña de un lado al otro. Kira elige el lugar,
aprieta el espacio y la pelota sale disparada. En el paredón, un ladrillo de vidrio parpadea, como si
se despertara.

#### Imagen
- La pelota amarilla quieta, apoyada en el medio de la paleta celeste, con un brillo que late.
- Kira, con el dedo sobre la barra espaciadora, elige el momento; Arcadia espera, divertida.
- Al fondo, el paredón de ladrillos de vidrio apagados; un ladrillo se enciende. Gheco lo mira asombrado.

## R03-N02 · Una fila de ladrillos

```meta
tipo: tema
criatura: atraviesaparedes
padre: R03-N01
precio: 10
temas: col.registros, col.arrays
usa: juegos.colisiones, prog.bucles
```

### Crónica

La pelota ya va y viene, pero arriba no hay nada que romper. {mentor} abre una tapa de la máquina: adentro hay
una caja con diez ladrillos de vidrio rosado, todos iguales, esperando su lugar. —Diez ladrillos son diez cosas
con lo mismo adentro —dice—: un lugar en la pantalla y si siguen enteros. No vamos a escribir diez variables.
Mientras tanto, una criatura gomosa se mete en la pared como si fuera de gelatina: el **Atraviesaparedes**.

### Objetivos

Guardar los ladrillos en un **arreglo de `struct`**: cada ladrillo con su caja y si está vivo. Armar una fila de
diez con un `for`, que la pelota **rompa** el ladrillo que toca y rebote, **sumar puntos** y romper **uno solo
por golpe** con `break`.

### Antes de empezar

R03-N01 (la paleta y la pelota). Del curso de C: los arreglos, el `for` y los `struct`. De R01: el texto en
pantalla (N07).

### Explicación

#### Un `struct`: varias cosas juntas
Cada ladrillo tiene dos datos: **dónde está** (un rectángulo) y **si sigue entero**. Un `struct` los junta en un
tipo nuevo:
```c
typedef struct {
    SDL_FRect caja;   /* dónde está y cuánto mide */
    bool vivo;        /* true: entero · false: roto */
} Ladrillo;
```
Desde ahí, `Ladrillo` es un tipo como `int` o `float`. Para llegar a un dato de adentro se usa el punto:
`pared[3].vivo`, `pared[3].caja.x`.

#### Un arreglo de ladrillos
`Ladrillo pared[COLUMNAS];` son diez ladrillos seguidos, del `pared[0]` al `pared[9]`. `COLUMNAS` es un
`#define`: un nombre para el número 10, así si mañana querés doce, lo cambiás en un solo lugar. Con `= { 0 }`
todo arranca en cero, así que ninguno está vivo hasta que los armemos.

#### Armar la fila con un `for`
El ladrillo número `c` va en `x = 22 + c * 60`: el primero en 22, el segundo en 82, el tercero en 142… Miden 56
de ancho, así que entre uno y otro quedan 4 píxeles de junta. `(SDL_FRect){ x, y, ancho, alto }` arma un
rectángulo en una sola línea.

#### Romper y rebotar
En cada cuadro, un `for` pregunta por cada ladrillo: ¿está vivo y la pelota lo toca? Si sí, se rompe
(`vivo = false`) y la pelota rebota (`vy = -vy`). Los rotos no se dibujan ni chocan más.

#### Uno solo por golpe: `break`
`break` corta el `for` en el momento. Si la pelota pega justo en la junta, entre dos ladrillos, sin `break`
rompería los dos y daría vuelta `vy` **dos veces**: quedaría para el mismo lado y seguiría de largo, metiéndose
en la pared (es el Atraviesaparedes).

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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

Un arreglo de `struct` es la forma de guardar **muchas cosas iguales** en un juego: los ladrillos, los
enemigos, los disparos, las gemas. Los vas a usar en todos los juegos que siguen.

### Errores habituales

**Pasarse del arreglo.** Con `c <= COLUMNAS` el `for` llega a `pared[10]`, que no existe: el programa escribe
donde no debe. El último es `pared[COLUMNAS - 1]`; por eso va `c < COLUMNAS`.

**Chocar con los rotos.** Si se olvida preguntar `pared[i].vivo`, la pelota sigue rebotando en ladrillos que
ya no se ven.

**Atraviesaparedes: rebotar dos veces.** Sin `break`, si la pelota toca dos ladrillos a la vez, da vuelta `vy`
dos veces y sigue de largo por adentro de la pared.

**Olvidar el punto.** `pared.vivo` no existe: hay que decir cuál, `pared[i].vivo`.

### Micro-misión R03-N02-P1 · Diez ladrillos en fila

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Armar con un for | pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 } · pared[c].vivo = true
recompensa: xp 10, oro 10
```

#### Escena
{mentor} saca los diez ladrillos de vidrio rosado y los deja en el piso, desordenados. —Cada uno tiene su
lugar arriba, en fila —dice—. Uno al lado del otro, con una juntita. Vos decile a la máquina dónde va
cada uno.

#### Gheco sugiere
Ya está el tipo `Ladrillo` (un `struct` con `caja` y `vivo`) y el arreglo `pared` con diez, todos en
cero. También ya está el código que **dibuja** los que estén vivos. Falta armarlos con un `for`:
```c
for (int c = 0; c < COLUMNAS; c++) {
    pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
    pared[c].vivo = true;
}
```
- `c` va de 0 a 9: es el número de ladrillo.
- `22 + c * 60` es su `x`: cada uno, 60 píxeles más a la derecha que el anterior.
- `(SDL_FRect){ x, y, ancho, alto }` arma el rectángulo de una vez: `y` 80, 56 de ancho y 20 de alto.
- `pared[c].vivo = true;` lo deja entero.

#### Desafío
Armá la fila de diez ladrillos con un for, al principio del programa.

#### Pasos
1. Buscá el comentario `/* acá: armar la fila: diez ladrillos, uno al lado del otro */` (antes del bucle del juego).
2. Debajo, escribí el `for` de la sugerencia.
3. Tocá **Jugar**: arriba tiene que aparecer la fila rosada. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    /* acá: armar la fila: diez ladrillos, uno al lado del otro */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
buscar #ff3c64
```

#### Salida esperada
```
── Estado ──
buscar #ff3c64: x 22, y 80, ancho 596, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
Diez ladrillos rosados se encienden en fila arriba de la pantalla, parejitos, con su junta oscura.
En el paredón de la plaza, una hilera entera de vidrio se ilumina.

#### Imagen
- La pantalla de la máquina con una fila de diez ladrillos rosados brillantes, parejos, con juntas oscuras.
- Arcadia acomoda un ladrillo de vidrio rosado de verdad en su lugar; Kira cuenta con los dedos.
- Gheco, sentado arriba de la máquina, sostiene un ladrillo de vidrio chiquito entre las manos.

### Micro-misión R03-N02-P2 · El ladrillo se rompe

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Romper y rebotar | si vivo y toca: vivo = false · vy = -vy
recompensa: xp 10, monedas 4
```

#### Escena
Kira saca y la pelota sube… y pasa a través de la fila como si los ladrillos fueran dibujados. —Están,
pero no estorban —dice {mentor}—. Que la pelota los sienta.

#### Gheco sugiere
Ya está el `for` que recorre los ladrillos y pregunta, para cada uno, si está vivo y la pelota lo toca:
```c
if (pared[i].vivo && toca(pelota, pared[i].caja)) {
```
Adentro falta lo que pasa cuando lo toca:
```c
pared[i].vivo = false;   /* se rompe: no se dibuja ni choca más */
vy = -vy;                /* y la pelota rebota */
```
El robot va a sacar enseguida con el espacio y a esperar a que la pelota llegue a la fila.

#### Desafío
Hacé que el ladrillo que toca la pelota se rompa y que la pelota rebote.

#### Pasos
1. Buscá el comentario `/* acá: el ladrillo se rompe y la pelota rebota */` (adentro del `if` de los ladrillos).
2. Debajo, escribí `pared[i].vivo = false;` y `vy = -vy;`.
3. Tocá **Jugar**, sacá con el espacio y mirá la fila. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                /* acá: el ladrillo se rompe y la pelota rebota */
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
cuadros 80
```

#### Estado
```
pixel 470 90
```

#### Salida esperada
```
── Estado ──
pixel 470 90: #140c28
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
*¡Crac!* Un ladrillo rosado desaparece y la pelota vuelve a bajar. Kira la devuelve y rompe otro. El
Atraviesaparedes, que estaba metido en la fila, sale despedido con cara de ofendido.

#### Imagen
- La pelota amarilla rompe un ladrillo rosado de la fila, que estalla en pedacitos de luz.
- Kira festeja; Arcadia se tapa los oídos sonriendo.
- Una criatura gomosa y translúcida sale despedida de la fila de ladrillos; Gheco se agacha para esquivarla.

### Micro-misión R03-N02-P3 · Diez puntos por ladrillo

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Sumar puntos | puntos += 10 · SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos)
recompensa: xp 10, monedas 4
```

#### Escena
Kira rompe tres ladrillos seguidos y se da vuelta, orgullosa. —¿Cuántos puntos hice? —Ni idea —dice
{mentor}—. La máquina no lleva la cuenta.

#### Gheco sugiere
Ya está la variable `int puntos = 0;`. Dos cosas:
1. Cuando se rompe un ladrillo, adentro del mismo `if`: `puntos += 10;` (es `puntos = puntos + 10;`).
2. Mostrarlo arriba a la izquierda, después de dibujar la pelota:
```c
SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);   /* blanco */
SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
```
`%d` es el lugar donde va el número (lo viste en R01-N07).

#### Desafío
Sumá diez puntos por cada ladrillo roto y mostrá el puntaje arriba a la izquierda.

#### Pasos
1. Buscá `/* acá: diez puntos por ladrillo */` y escribí `puntos += 10;`.
2. Buscá `/* acá: el puntaje arriba a la izquierda */` y escribí las dos líneas de la sugerencia.
3. Tocá **Jugar**, rompé un ladrillo y mirá el puntaje. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                /* acá: diez puntos por ladrillo */
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        /* acá: el puntaje arriba a la izquierda */
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
cuadros 80
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
Arriba a la izquierda se enciende **PUNTOS 10**. Kira rompe otro: **20**. Gheco anota en el aire con la
cola, como un árbitro.

#### Imagen
- La pantalla con el puntaje blanco arriba a la izquierda y la fila rosada con un hueco.
- Kira señala el puntaje, contenta; Arcadia aplaude.
- Gheco hace la cuenta con los dedos arriba de la máquina.

### Micro-misión R03-N02-P4 · Uno solo por golpe

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Cortar el for | break: rompe un ladrillo por golpe y no rebota dos veces
recompensa: xp 10, monedas 4
```

#### Escena
Kira saca desde un poquito más a la derecha. La pelota pega justo en la junta entre dos ladrillos, rompe
los dos… y sigue de largo hacia arriba, como si nada. —Ese es el Atraviesaparedes —dice {mentor}—: dio la
vuelta dos veces y quedó como estaba.

#### Gheco sugiere
Si la pelota toca **dos** ladrillos en el mismo cuadro, el `for` rompe el primero (`vy = -vy`, ahora
baja) y después el segundo (`vy = -vy` otra vez: ¡vuelve a subir!). Dos vueltas son ninguna: la pelota
sigue para el mismo lado, metiéndose en la pared.

La solución es romper **uno solo por golpe**: apenas se rompe uno, se corta el `for` con `break`:
```c
if (pared[i].vivo && toca(pelota, pared[i].caja)) {
    pared[i].vivo = false;
    vy = -vy;
    puntos += 10;
    break;   /* listo: no mira los demás */
}
```
`break` sale del `for` en el momento, sin mirar los ladrillos que faltan. El robot va a sacar desde un
lugar donde la pelota pega en la junta.

#### Desafío
Hacé que la pelota rompa un solo ladrillo por golpe, cortando el for con break.

#### Pasos
1. Buscá `/* acá: uno solo por golpe: salir del for */` (al final del `if` de los ladrillos).
2. Debajo, escribí `break;`.
3. Tocá **Jugar** y probá sacar desde distintos lugares. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                /* acá: uno solo por golpe: salir del for */
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
apretar Derecha
cuadros 3
soltar Derecha
tecla Espacio
cuadros 90
```

#### Estado
```
pixel 470 90
pixel 530 90
```

#### Salida esperada
```
── Estado ──
pixel 470 90: #140c28
pixel 530 90: #ff3c64
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
La pelota pega en la junta, rompe uno solo y vuelve a bajar, obediente. El Atraviesaparedes rebota contra
la fila y ya no puede entrar. —Una cosa por vez —dice {mentor}—. Así se rompe un muro.

#### Imagen
- La pelota amarilla pega en la junta entre dos ladrillos rosados: uno se rompe y el otro queda entero.
- Una criatura gomosa y translúcida rebota contra la fila de ladrillos, enojada.
- Kira choca los cinco con Arcadia; Gheco levanta un dedo: uno solo.

## R03-N03 · La pared entera

```meta
tipo: tema
criatura: glitch
padre: R03-N02
precio: 10
temas: col.matrices
usa: col.registros, col.arrays, prog.bucles
```

### Crónica

Una fila sola se rompe en un minuto. {mentor} señala el paredón de la plaza: cinco hileras de vidrio de
colores, una arriba de la otra, y la de abajo, gris, de metal. —Así era el Muro de verdad —dice—. Rosa,
naranja, verde, violeta y metal. Y cuanto más arriba, más difícil llegar, así que más puntos. Sobre la
pantalla, un **glitch** pinta todos los ladrillos del mismo color y se ríe.

### Objetivos

Pasar de una fila a una **pared de cinco filas** con dos `for` (uno adentro del otro), pintar **cada fila de su
color** con un arreglo de colores, dar **más puntos** a las filas de arriba y hacer la fila de abajo **de metal**:
necesita dos golpes.

### Antes de empezar

R03-N02 (un arreglo de `struct`, armar con `for`, romper y `break`). Del curso de C: los `for` anidados.

### Explicación

#### Dos `for`, uno adentro del otro
Para recorrer filas y columnas se pone un `for` adentro de otro. El de afuera elige la fila (`f`, de 0 a 4) y,
para cada fila, el de adentro recorre las columnas (`c`, de 0 a 9). El cuerpo se repite 5 × 10 = 50 veces.

#### Una pared en un arreglo largo
Los 50 ladrillos van en un solo arreglo, `pared[FILAS * COLUMNAS]`, fila por fila: primero los 10 de la fila
0, después los 10 de la fila 1… El ladrillo de la fila `f` y la columna `c` es el número `f * COLUMNAS + c`. Por
ejemplo, fila 2, columna 3: `2 * 10 + 3 = 23`. Así, chocar y dibujar sigue siendo **un solo `for`** (y el
`break` sigue funcionando).

#### Cada fila, más abajo
La `y` de cada fila es `60 + f * 24`: 20 de alto del ladrillo y 4 de junta. Cada ladrillo guarda también su
`fila`, porque después la vamos a necesitar para su color y sus puntos.

#### Un arreglo de colores
`SDL_Color` es un `struct` de SDL con `r`, `g`, `b` y `a`. Un arreglo con un color por fila, y al dibujar, el
ladrillo usa `colores[pared[i].fila]`.

#### Los ladrillos de metal
Un dato más en el `struct`: `golpes`, cuántos le faltan para romperse. Los de la fila de abajo arrancan con 2 y
los demás con 1. En cada golpe se le resta uno, y se rompe recién cuando llega a 0.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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

Recorrer filas y columnas con dos `for` es la base de todo lo que es una **grilla**: el tablero del Tetris, el
laberinto del Pac-Man, los mapas de baldosas de un juego de plataformas.

### Errores habituales

**Mezclar filas y columnas.** `c * COLUMNAS + f` da números repetidos y ladrillos encimados. Es la fila por el
ancho, más la columna: `f * COLUMNAS + c`.

**Glitch: todos del mismo color.** Si `SDL_SetRenderDrawColor` va antes del `for`, todos salen del último color
elegido. Cada ladrillo elige el suyo adentro del `for`.

**Romper el metal de una.** Si se deja `vivo = false` sin mirar los `golpes`, el metal se rompe como los demás.

**Recorrer solo diez.** Si un `for` quedó con `i < COLUMNAS`, solo mira la fila de arriba: la pelota atraviesa
las otras cuatro.

### Micro-misión R03-N03-P1 · Cinco filas

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Grilla con dos for | i = f * COLUMNAS + c · y = 60 + f * 24 · pared[i].fila = f
recompensa: xp 10, oro 10
```

#### Escena
{mentor} trae una escalera y la apoya en el paredón. —Cinco hileras de diez —dice—. No las vamos a
escribir de a una: una vuelta por fila, y en cada fila, una vuelta por ladrillo.

#### Gheco sugiere
El arreglo ya tiene lugar para 50 ladrillos (`FILAS * COLUMNAS`). Cambiá el `for` de la fila por dos,
uno adentro del otro:
```c
for (int f = 0; f < FILAS; f++) {            /* cada fila */
    for (int c = 0; c < COLUMNAS; c++) {     /* cada ladrillo de esa fila */
        int i = f * COLUMNAS + c;            /* su número en el arreglo */
        pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
        pared[i].vivo = true;
        pared[i].fila = f;
    }
}
```
- `i = f * COLUMNAS + c`: la fila 0 usa del 0 al 9, la fila 1 del 10 al 19, y así.
- `60 + f * 24`: cada fila, 24 píxeles más abajo (20 del ladrillo y 4 de junta).
- Cada uno guarda su `fila`, que vamos a usar para el color.

#### Desafío
Armá la pared de cinco filas de diez ladrillos con dos for.

#### Pasos
1. Buscá `/* acá: armar la pared: cinco filas de diez, con dos for */` y borrá el `for` de abajo (el de una sola fila).
2. En su lugar, escribí los dos `for` de la sugerencia.
3. Tocá **Jugar**: tienen que aparecer cinco filas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    /* acá: armar la pared: cinco filas de diez, con dos for */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
buscar #ff3c64
```

#### Salida esperada
```
── Estado ──
buscar #ff3c64: x 22, y 60, ancho 596, alto 116
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
Cinco filas rosadas se encienden una debajo de la otra. En la plaza, el paredón entero tiembla y se
ilumina de arriba abajo. —Ahora sí es un muro —dice {mentor}.

#### Imagen
- La pantalla de la máquina con una pared de cinco filas de ladrillos rosados, todas iguales.
- Arcadia, subida a una escalera, encaja ladrillos de vidrio en el paredón de la plaza; Kira le alcanza uno.
- Gheco, en la palma de Kira, cuenta las filas con la cola.

### Micro-misión R03-N03-P2 · Un color por fila

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: Colores por fila | SDL_Color color = colores[pared[i].fila] · SetRenderDrawColor con color.r, .g, .b
recompensa: xp 10, monedas 4
```

#### Escena
La pared entera es rosada. Un glitch salta de ladrillo en ladrillo, pintándolos todos igual. —Así no se
sabe cuál es cuál —dice {mentor}—. Cada fila tenía su color.

#### Gheco sugiere
Ya está el arreglo `colores`, con un `SDL_Color` por fila (rosa, naranja, verde, violeta y metal).
`SDL_Color` es un `struct` de SDL con cuatro números: `r`, `g`, `b` y `a`.

Al dibujar, antes de pintar cada ladrillo vivo, elegí el color de **su** fila:
```c
SDL_Color color = colores[pared[i].fila];
SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
```
Va adentro del `for`, porque cada ladrillo tiene que elegir el suyo.

#### Desafío
Pintá cada ladrillo con el color de su fila.

#### Pasos
1. Buscá `/* acá: pintarlo con el color de su fila */` (adentro del `for` que dibuja).
2. Debajo, escribí las dos líneas de la sugerencia.
3. Tocá **Jugar** y mirá los colores. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                /* acá: pintarlo con el color de su fila */
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
buscar #50dc64
```

#### Salida esperada
```
── Estado ──
buscar #50dc64: x 22, y 108, ancho 596, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
Rosa, naranja, verde, violeta y gris metal: la pared se enciende como un arcoíris. El glitch intenta
pintarla de nuevo y se le acaba la pintura. Se deshace en píxeles.

#### Imagen
- La pantalla con la pared de cinco filas: rosa, naranja, verde, violeta y gris metal.
- Un glitch pixelado con un pincel se deshace en píxeles al costado de la pantalla.
- Kira sonríe; Arcadia mira el paredón de la plaza, que se ilumina de colores; Gheco aplaude.

### Micro-misión R03-N03-P3 · Más arriba, más puntos

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Puntos por fila | puntos += 10 * (FILAS - pared[i].fila)
recompensa: xp 10, monedas 4
```

#### Escena
—Romper uno de abajo y uno de arriba vale lo mismo —protesta Kira—. ¡Y los de arriba son mucho más
difíciles! {mentor} asiente. —Tenés razón. Cuanto más arriba, más puntos.

#### Gheco sugiere
Cada ladrillo sabe su `fila`: 0 es la de arriba y 4 la de abajo. Si se hace `FILAS - fila`, la de arriba
da 5 y la de abajo da 1. Por 10:
```c
puntos += 10 * (FILAS - pared[i].fila);
```
| Fila | Color | Puntos |
|---|---|---|
| 0 | rosa | 50 |
| 1 | naranja | 40 |
| 2 | verde | 30 |
| 3 | violeta | 20 |
| 4 | metal | 10 |

El robot va a sacar dos veces por el mismo lugar: la primera rompe uno de abajo y la segunda, el de
arriba de ese.

#### Desafío
Hacé que cada ladrillo dé más puntos cuanto más arriba esté su fila.

#### Pasos
1. Buscá `/* acá: más puntos cuanto más arriba esté la fila */` y borrá la línea `puntos += 10;`.
2. En su lugar, escribí `puntos += 10 * (FILAS - pared[i].fila);`.
3. Tocá **Jugar**, rompé un ladrillo de abajo y otro más arriba. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                /* acá: más puntos cuanto más arriba esté la fila */
                puntos += 10;
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
cuadros 200
tecla Espacio
cuadros 90
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 30
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
El de metal da 10 y el violeta de arriba, 20. Kira ya está calculando cómo meter la pelota hasta la
fila rosa. —Cincuenta cada uno —dice, con los ojos brillando.

#### Imagen
- La pantalla con la pared de colores y un hueco que sube por dos filas; el puntaje blanco arriba.
- Kira apunta hacia la fila rosa de arriba con el dedo, decidida.
- Arcadia sonríe; Gheco, sobre la máquina, levanta cinco dedos.

### Micro-misión R03-N03-P4 · La fila de metal

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Dos golpes | golpes = 2 en la fila de abajo · golpes-- · si llega a 0: vivo = false
recompensa: xp 10, monedas 4
```

#### Escena
{mentor} golpea con los nudillos la fila de abajo del paredón: suena a lata. —Estos son de metal —dice—.
Con un golpe se abollan; con dos, se rompen.

#### Gheco sugiere
El `struct` ya tiene `golpes`: cuántos golpes le faltan a cada ladrillo. Dos cosas:
1. **Al armar la pared**, después de los dos `for`: los de la fila de abajo arrancan con 2 y el resto con 1.
```c
for (int i = 0; i < FILAS * COLUMNAS; i++) {
    pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
}
```
`condición ? a : b` vale `a` si la condición es verdadera y `b` si no (lo usaste en el Pong).
2. **Al chocar**, en lugar de romperlo directo, se le resta un golpe y se rompe si ya no le quedan:
```c
pared[i].golpes--;
if (pared[i].golpes == 0) {
    pared[i].vivo = false;
}
```
La pelota rebota igual, se rompa o no.

#### Desafío
Hacé que los ladrillos de la fila de abajo necesiten dos golpes para romperse.

#### Pasos
1. Buscá `/* acá: la fila de abajo es de metal: necesita dos golpes */` (antes del bucle) y escribí el `for` que reparte los golpes.
2. Buscá `/* acá: un golpe menos; se rompe cuando no le quedan */` y borrá la línea `pared[i].vivo = false;` de abajo.
3. En su lugar, escribí `pared[i].golpes--;` y el `if` de la sugerencia.
4. Tocá **Jugar** y pegale a uno de metal. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    /* acá: la fila de abajo es de metal: necesita dos golpes */
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                /* acá: un golpe menos; se rompe cuando no le quedan */
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
cuadros 80
```

#### Estado
```
pixel 470 166
```

#### Salida esperada
```
── Estado ──
pixel 470 166: #b4b4c8
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
*¡Clonc!* La pelota pega en el metal y rebota, pero el ladrillo sigue ahí. Al segundo golpe, se rompe con
un ruido de lata. Gheco se tapa los oídos. —Ahora el muro se defiende —dice {mentor}, contenta.

#### Imagen
- La pelota amarilla rebota en un ladrillo gris de metal de la fila de abajo, que queda entero, con una chispa.
- Arcadia golpea con los nudillos la fila de metal del paredón de la plaza; Kira escucha.
- Gheco, sobre la máquina, se tapa los oídos.

## R03-N04 · Rebote según dónde pega

```meta
tipo: tema
criatura: atraviesaparedes
padre: R03-N03
precio: 10
usa: juegos.colisiones, juegos.fisica, juegos.entrada
```

### Crónica

Kira juega diez minutos y se da cuenta de algo: la pelota hace siempre el mismo dibujo. Sube, rompe, baja, y
otra vez por el mismo lado. —Así el muro se rompe solo de un costado —dice {mentor}—. En la máquina de verdad,
vos elegías para dónde salía la pelota según dónde le pegabas con la paleta. Y cuidado con los costados de los
ladrillos: ahí se esconde el **Atraviesaparedes**.

### Objetivos

Que la pelota salga **para un lado o para el otro según dónde pega en la paleta**, que rebote bien cuando pega
en el **costado** de un ladrillo, que se **apure** un poco con cada ladrillo (sin pasarse de un tope) y que la
paleta también se mueva con el **mouse**.

### Antes de empezar

R03-N03 (la pared). Del Pong: el ángulo según dónde pega (R02-N03). De R01: el mouse (N03).

### Explicación

#### El ángulo de la paleta
Igual que en el Pong, la distancia entre el **centro de la pelota** y el **centro de la paleta** decide para
dónde sale: si pega a la izquierda del centro, la distancia es negativa y sale hacia la izquierda; si pega a la
derecha, sale hacia la derecha; en el medio, casi derecho para arriba. Multiplicada por 6, la pelota sale con
un `vx` de entre -270 y 270.

#### ¿Por dónde entró?
Hasta ahora, al tocar un ladrillo siempre se daba vuelta `vy`. Pero si la pelota pega en el **costado** de un
ladrillo, lo que tiene que cambiar es `vx`. ¿Cómo saberlo? Mirando **dónde estaba la pelota un cuadro antes**,
antes de moverse (se guarda en `previa`):
- Si **ya estaba a la altura del ladrillo** (su borde de abajo más abajo que el techo del ladrillo y su borde de
  arriba más arriba que el piso del ladrillo), no pudo haber entrado ni por arriba ni por abajo: entró por un
  **costado**. Se da vuelta `vx`.
- Si no, entró por arriba o por abajo: se da vuelta `vy`.

Es como mirar la foto del cuadro anterior para saber de dónde vino.

#### Más rápido, con un tope
Con cada ladrillo, `vy` se multiplica por 1,03 (un 3 % más rápido). `SDL_clamp` la deja entre -480 y 480: más
rápida que eso, la pelota avanzaría en un cuadro más que el alto de un ladrillo y lo atravesaría (otra vez el
Atraviesaparedes, como en el Pong).

#### La paleta con el mouse
Cuando el mouse se mueve llega un evento `SDL_EVENT_MOUSE_MOTION`, con la posición en `evento.motion.x` y
`evento.motion.y`. Se pone la paleta centrada en el mouse: `evento.motion.x - paleta.w / 2`. El `SDL_clamp` que
ya estaba la sigue frenando en los bordes.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_MOTION) {
                paleta.x = evento.motion.x - paleta.w / 2;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        SDL_FRect previa = pelota;
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                vy = SDL_clamp(vy * 1.03f, -480, 480);
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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

Elegir la dirección con la paleta es lo que hace que el Arkanoid sea un juego de puntería y no de suerte. Y
saber **de qué lado** chocaron dos cosas es lo que vas a usar para caminar sobre plataformas sin atravesarlas.

### Errores habituales

**Restar al revés.** `paleta - pelota` en lugar de `pelota - paleta` hace que, al pegar a la izquierda, salga
hacia la derecha.

**Atraviesaparedes: siempre `vy`.** Si pega en el costado y se da vuelta `vy`, la pelota se mete en el ladrillo
y sigue de largo rompiendo los de al lado.

**Sin tope.** Si se multiplica la velocidad sin `SDL_clamp`, después de muchos ladrillos la pelota va tan
rápido que atraviesa la paleta.

**El mouse sin centrar.** `paleta.x = evento.motion.x;` deja el mouse en la punta izquierda de la paleta, no en
el medio.

### Micro-misión R03-N04-P1 · El ángulo de la paleta

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Salir según dónde pega | vx = ((centro de la pelota) - (centro de la paleta)) * 6
recompensa: xp 10, oro 10
```

#### Escena
—Pegale con la punta —le dice {mentor} a Kira—. En esta máquina, si le pegás con la punta izquierda, la
pelota sale para la izquierda. Por ahora la paleta es una tabla lisa: devuelve todo igual.

#### Gheco sugiere
Cuando la paleta devuelve la pelota, además de dar vuelta `vy`, el `vx` depende de **dónde pegó**:
```c
vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
```
- `pelota.x + pelota.w / 2` es el centro de la pelota; `paleta.x + paleta.w / 2`, el de la paleta.
- La resta da negativo si pegó a la izquierda del centro (sale para la izquierda) y positivo si pegó a la
  derecha. En el medio, cerca de 0: sale casi derecho.
- Por 6, para que salga con ganas: va de -270 a 270.

El robot va a sacar y a correr la paleta hacia la derecha para recibir la pelota cuando baja.

#### Desafío
Hacé que la pelota salga para un lado o para el otro según dónde pega en la paleta.

#### Pasos
1. Buscá `/* acá: el costado depende de dónde pegó en la paleta */` (adentro del `if` de la paleta).
2. Debajo, escribí la línea de `vx` de la sugerencia.
3. Tocá **Jugar** y probá pegarle con las puntas y con el medio. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            /* acá: el costado depende de dónde pegó en la paleta */
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
apretar Derecha
cuadros 42
soltar Derecha
cuadros 100
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 479, y 221, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
Kira le pega con la punta izquierda y la pelota sale en diagonal, directo a un rincón del muro que nadie
había tocado. —¡Puntería! —grita Gheco desde la máquina.

#### Imagen
- La pelota amarilla sale en diagonal desde la punta izquierda de la paleta celeste, con una línea punteada.
- Kira, concentrada, mueve la paleta para pegarle con la punta; Arcadia mira con una sonrisa pícara.
- Gheco sigue la diagonal con el dedo, sentado arriba de la máquina.

### Micro-misión R03-N04-P2 · El golpe de costado

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: ¿Por dónde entró? | previa = pelota antes de moverse · si ya estaba a la altura del ladrillo: vx = -vx · si no: vy = -vy
recompensa: xp 10, monedas 4
```

#### Escena
La pelota pega en el costado de un ladrillo verde… y en vez de rebotar hacia el costado, se mete adentro de
la pared y rompe tres de un saque. Una criatura gomosa se ríe desde adentro del muro: el Atraviesaparedes.

#### Gheco sugiere
Si la pelota entra por el **costado** de un ladrillo, lo que tiene que cambiar es `vx`, no `vy`. Para
saber por dónde entró, se mira dónde estaba **un cuadro antes**. Dos cosas:
1. **Antes de mover la pelota**, guardar dónde estaba:
```c
SDL_FRect previa = pelota;   /* una copia: la pelota de antes */
```
2. **Al chocar con un ladrillo**, en lugar de dar vuelta siempre `vy`:
```c
SDL_FRect caja = pared[i].caja;
bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
if (aLaAltura) {
    vx = -vx;   /* ya estaba a su altura: entró por un costado */
} else {
    vy = -vy;   /* venía de arriba o de abajo */
}
```
- `previa.y + previa.h > caja.y`: el borde de abajo de la pelota estaba más abajo que el techo del ladrillo.
- `previa.y < caja.y + caja.h`: el borde de arriba estaba más arriba que el piso del ladrillo.
- Si pasan las dos, la pelota ya estaba **a la altura** del ladrillo antes de tocarlo: solo pudo llegar de
  costado.

El robot va a sacar desde un lugar donde la pelota pega de costado en un ladrillo.

#### Desafío
Hacé que la pelota rebote hacia el costado cuando pega en el costado de un ladrillo.

#### Pasos
1. Buscá `/* acá: guardar dónde estaba la pelota antes de moverse */` y escribí `SDL_FRect previa = pelota;`.
2. Buscá `/* acá: si antes de moverse ya estaba a la altura del ladrillo, entró por un costado */` y borrá la línea `vy = -vy;` de abajo.
3. En su lugar, escribí las líneas de `caja` y `aLaAltura`, y el `if` de la sugerencia.
4. Tocá **Jugar** y mirá cómo rebota en los costados. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        /* acá: guardar dónde estaba la pelota antes de moverse */
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                /* acá: si antes de moverse ya estaba a la altura del ladrillo, entró por un costado */
                vy = -vy;
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
apretar Derecha
cuadros 30
soltar Derecha
tecla Espacio
cuadros 300
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 87, y 66, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        SDL_FRect previa = pelota;
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
La pelota pega en el costado del ladrillo verde y sale rebotada hacia el costado, como tiene que ser. El
Atraviesaparedes queda afuera de la pared, aplastado contra el vidrio, con cara de no entender nada.

#### Imagen
- La pelota amarilla rebota hacia el costado al pegar en el borde lateral de un ladrillo verde, con una flecha.
- Una criatura gomosa y translúcida queda aplastada contra la pared de ladrillos, desde afuera.
- Kira y Arcadia se ríen; Gheco, sentado arriba de la máquina, señala el rebote.

### Micro-misión R03-N04-P3 · Cada vez más rápido

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco, Arcadia
carta: Apurar con tope | vy = SDL_clamp(vy * 1.03f, -480, 480)
recompensa: xp 10, monedas 4
```

#### Escena
Con media pared rota, el juego se pone aburrido: la pelota va siempre igual de lenta. —El Muro original se
apuraba —recuerda {mentor}—. Cada ladrillo que rompías, la pelota volvía con más bronca.

#### Gheco sugiere
Cada vez que se rompe (o se golpea) un ladrillo, la pelota va un 3 % más rápido de arriba abajo:
```c
vy = SDL_clamp(vy * 1.03f, -480, 480);
```
- `vy * 1.03f` es `vy` más un 3 %. La `f` dice que es un `float`.
- `SDL_clamp` la frena en 480 para arriba o para abajo: más rápido que eso, en un cuadro avanzaría más
  que el alto de un ladrillo y lo podría atravesar (lo viste en el Pong, R02-N03).

Va justo después del rebote en el ladrillo.

#### Desafío
Hacé que la pelota se apure un 3 % con cada ladrillo, sin pasarse de 480.

#### Pasos
1. Buscá `/* acá: cada ladrillo roto, la pelota un poco más rápida (con un tope) */`.
2. Debajo, escribí la línea con `SDL_clamp` de la sugerencia.
3. Tocá **Jugar** y rompé varios ladrillos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        SDL_FRect previa = pelota;
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                /* acá: cada ladrillo roto, la pelota un poco más rápida (con un tope) */
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
apretar Derecha
cuadros 42
soltar Derecha
cuadros 100
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 447, y 204, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        SDL_FRect previa = pelota;
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                vy = SDL_clamp(vy * 1.03f, -480, 480);
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
La pelota vuelve cada vez con más ganas. Kira ya no se ríe: juega con la lengua afuera, concentrada. —Así
era —dice {mentor}—. Al final, la pelota parecía una chispa.

#### Imagen
- La pelota amarilla con una estela larga, cada vez más rápida, entre la paleta y la pared de colores.
- Kira juega muy concentrada, con la lengua afuera; Arcadia la mira con orgullo.
- Gheco, arriba de la máquina, mueve la cabeza de un lado al otro cada vez más rápido.

### Micro-misión R03-N04-P4 · La paleta con el mouse

```meta
lugar: El Muro de Ladrillos
personajes: Kira, Gheco
carta: Seguir al mouse | SDL_EVENT_MOUSE_MOTION: paleta.x = evento.motion.x - paleta.w / 2
recompensa: xp 10, monedas 4
```

#### Escena
Un chico del barrio se acerca a la máquina y agarra… el mouse que está al costado del tablero. Lo mueve y no
pasa nada. —Las máquinas viejas del Muro tenían una perilla —dice {mentor}—. Esto es lo más parecido.

#### Gheco sugiere
Cuando se mueve el mouse llega un evento `SDL_EVENT_MOUSE_MOTION` (lo viste en R01-N03), con la posición
en `evento.motion.x` y `evento.motion.y`. En el `while` de los eventos:
```c
if (evento.type == SDL_EVENT_MOUSE_MOTION) {
    paleta.x = evento.motion.x - paleta.w / 2;   /* el mouse, en el medio de la paleta */
}
```
Restar la mitad del ancho deja el mouse en el **medio** de la paleta y no en la punta. No hace falta
frenarla en los bordes: el `SDL_clamp` de después ya lo hace en cada cuadro.

El robot va a llevar el mouse a la izquierda de la ventana.

#### Desafío
Hacé que la paleta siga al mouse, centrada en él.

#### Pasos
1. Buscá `/* acá: la paleta sigue al mouse */` (en el `while` de los eventos).
2. Debajo, escribí el `if` con `SDL_EVENT_MOUSE_MOTION` de la sugerencia.
3. Tocá **Jugar** y mové el mouse adentro del juego. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: la paleta sigue al mouse */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        SDL_FRect previa = pelota;
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                vy = SDL_clamp(vy * 1.03f, -480, 480);
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
mouse 120 300
cuadros 3
```

#### Estado
```
buscar #00e5ff
```

#### Salida esperada
```
── Estado ──
buscar #00e5ff: x 80, y 440, ancho 80, alto 12
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    int puntos = 0;

    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_MOTION) {
                paleta.x = evento.motion.x - paleta.w / 2;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);

        SDL_FRect previa = pelota;
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }

        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
        }

        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                vy = SDL_clamp(vy * 1.03f, -480, 480);
                puntos += 10 * (FILAS - pared[i].fila);
                break;
            }
        }

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            pegada = true;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
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
El chico mueve el mouse y la paleta lo sigue como una sombra. Rompe un ladrillo verde y grita. Detrás de él
ya hay otros dos esperando para probar.

#### Imagen
- Un chico del barrio con abrigo cerrado mueve un mouse al costado de la máquina, con cara de asombro.
- En la pantalla, la paleta celeste sigue al mouse; Kira le explica algo al chico.
- Gheco, sentado arriba de la máquina, levanta el pulgar.
