# RAMA R02 · La Cancha de las Paletas: Pong

```meta
tipo: tronco
posicion: 2
```

## R02-N01 · La cancha y las dos paletas

```meta
tipo: tema
criatura: atraviesaparedes
padre: R01-N10
precio: 10
temas: juegos.fisica
usa: juegos.entrada, juegos.colisiones, juegos.bucle
```

### Crónica

Las puertas del Banco de Pruebas quedan atrás. La calle de neón está oscura, salvo un cartel que parpadea al
ritmo de un *tic… tic…* que se escucha desde lejos. Adentro, un salón con el piso pintado como una cancha, y
en el medio, la máquina más vieja de Ciudad Arcadia. —Acá empezó todo —dice {mentor}, y le saca el polvo con
la manga—. El primer juego que se hizo popular en el mundo fue este: dos paletas y una pelota. Si la
encendemos, la ciudad entera se va a enterar.

### Objetivos

Armar la cancha de Pong con lo que ya sabés: la red del medio con un `for`, **dos jugadores en el mismo
teclado**, una pelota con **velocidad** (`vx`, `vy`) que **rebota** en las paredes y las **paletas que la
devuelven**. Al final, se juega de a dos.

### Antes de empezar

Todo R01: el teclado (N02), el delta time (N04) y las colisiones (N05). Del curso de C: `for`, `if` y funciones.

### Explicación

#### Qué es el Pong
Dos paletas, una a cada lado, y una pelota que va y viene. Cada jugador mueve la suya hacia arriba y hacia
abajo para devolver la pelota. Si se le pasa, el otro hace un punto. En este nodo armamos la cancha y el
rebote; en el siguiente, los puntos.

#### La velocidad de la pelota
Hasta ahora las cosas se movían cuando se apretaba una tecla. La pelota se mueve sola, siempre, con una
**velocidad** guardada en dos variables:
```c
float vx = 200;   /* píxeles por segundo de costado: + derecha, - izquierda */
float vy = 90;    /* píxeles por segundo de arriba abajo: + baja, - sube */
```
Y en cada cuadro avanza lo que le toca en el tiempo que pasó (el delta time de R01-N04):
```c
pelota.x += vx * dt;
pelota.y += vy * dt;
```

#### Rebotar es dar vuelta un signo
Cuando la pelota pega arriba o abajo, sigue de costado igual, pero cambia de dirección vertical: `vy = -vy;`.
Cuando pega en una paleta, cambia la dirección de costado: `vx = -vx;`. Siempre, antes, se la pone justo en el
borde, para que no quede adentro de la pared (ni de la paleta).

#### Dos jugadores, un teclado
`SDL_GetKeyboardState` tiene una casilla por tecla, así que puede haber varias apretadas a la vez: el jugador 1
usa la W y la S, el jugador 2 las flechas, y los dos juegan juntos.

#### No pegarle dos veces
Si la pelota toca la paleta y en el cuadro siguiente todavía la está tocando, daría la vuelta otra vez y se
quedaría trabada. Por eso se pregunta también hacia dónde va: la paleta izquierda solo la devuelve si viene
hacia la izquierda (`vx < 0`).

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 230, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 150, 12, 12 };
    float vx = -200;  /* arranca yendo hacia el jugador 1 */
    float vy = 90;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        /* la paleta del jugador 2 la devuelve */
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }
        /* la paleta del jugador 1 la devuelve */
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }

        /* si sale por un costado, vuelve al medio */
        if (pelota.x < -12 || pelota.x > 640) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

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

La velocidad con dos partes y el rebote dando vuelta un signo están en casi todos los juegos: la pelota del
Arkanoid, los rebotes de un plataformas, las naves que van y vienen. El Pong es el lugar más simple para
aprenderlo bien.

### Errores habituales

**Dar vuelta el signo sin acomodar la pelota.** Si solo se hace `vy = -vy;` y la pelota quedó un poquito
afuera, en el cuadro siguiente sigue afuera y se da vuelta otra vez: tiembla pegada a la pared.

**Mirar el borde equivocado.** Abajo, lo que choca es el borde de abajo de la pelota: `pelota.y + pelota.h`,
no `pelota.y`. Con `pelota.y > 480` la pelota se mete entera antes de rebotar.

**Atraviesaparedes: rebotar sin mirar la dirección.** Sin el `vx < 0`, la pelota puede quedar adentro de la
paleta dando vueltas de un lado a otro, como enganchada.

**Moverla sin delta time.** `pelota.x += 3;` anda, pero en una compu más rápida la pelota vuela. Con
`vx * dt`, va igual en todas.

### Micro-misión R02-N01-P1 · La red del medio

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Dibujar con un for | for (int y = 0; y < 480; y += 40) · una raya cada 40 píxeles
recompensa: xp 10, oro 10
```

#### Escena
La Cancha de las Paletas es un salón enorme con el piso pintado como una cancha de tenis, pero de neón.
En el medio, la máquina más vieja de la ciudad: dos paletas y nada más. —Le falta la red —dice {mentor}—.
Sin la red, nadie sabe de qué lado juega.

#### Gheco sugiere
La red son rayitas una debajo de la otra: un rectángulo de 4 de ancho y 20 de alto, después un hueco de
20, otra raya… Escribir doce rectángulos a mano es mucho. Un `for` lo hace solo:
```c
for (int y = 0; y < 480; y += 40) {
    SDL_FRect raya = { 318, (float)y, 4, 20 };
    SDL_RenderFillRect(lapiz, &raya);
}
```
- `y` arranca en 0 y salta de a 40 (`y += 40`): 0, 40, 80… hasta 440. Cada vuelta dibuja una raya.
- 40 = 20 de raya + 20 de hueco.
- `318` es la `x`: el medio de la pantalla es 320, y la raya mide 4, así que empieza 2 antes.
- `(float)y` convierte el número entero `y` en el `float` que pide `SDL_FRect`.

Antes del `for`, elegí el color de la red: `SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);` (un violeta
apagado, para que no distraiga). Va antes de las paletas, así queda debajo.

#### Desafío
Dibujá la red del medio: rayas de 4 × 20, una cada 40 píxeles, en x = 318, de color (90, 80, 130).

#### Pasos
1. Buscá el comentario `/* acá: la red del medio, con un for */`.
2. Debajo, elegí el color: `SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);`.
3. Escribí el `for (int y = 0; y < 480; y += 40) {` con el rectángulo `{ 318, (float)y, 4, 20 }` y su `SDL_RenderFillRect` adentro.
4. Cerrá la llave del `for` con `}`, tocá **Jugar** para verla y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        /* acá: la red del medio, con un for */

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
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
pixel 320 10
pixel 320 30
pixel 320 450
```

#### Salida esperada
```
── Estado ──
pixel 320 10: #5a5082
pixel 320 30: #140c28
pixel 320 450: #5a5082
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        /* acá: la red del medio, con un for */
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
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
Las rayas aparecen de arriba abajo, una por una, como si alguien las pintara con tiza. La máquina vieja
suelta un *bip* grave. —Ahora sí es una cancha —dice {mentor}.

#### Imagen
- El salón de la Cancha de las Paletas: un piso enorme pintado como una cancha de neón, con una máquina vieja en el medio.
- En la pantalla de la máquina, dos paletas (una cian y una rosa) y una red de rayitas violetas en el medio.
- Kira se agacha a mirar la pantalla; Arcadia sonríe con los brazos en jarra; Gheco camina por la red como por un puente.

### Micro-misión R02-N01-P2 · Dos jugadores, un teclado

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Dos jugadores | W y S para uno · las flechas para el otro · el mismo SDL_GetKeyboardState
recompensa: xp 10, monedas 4
```

#### Escena
—El Pong de verdad se juega de a dos, en la misma máquina —dice {mentor}, y se para del lado rosa—. Vos con
la W y la S. Yo, con las flechas. Pero mi paleta no se mueve…

#### Gheco sugiere
La paleta del jugador 1 ya se mueve con el **estado** del teclado (lo viste en R01-N02), a 300 píxeles por
segundo con delta time (R01-N04):
```c
if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
```
Para el jugador 2 es lo mismo, cambiando dos cosas: las teclas (`SDL_SCANCODE_UP` y `SDL_SCANCODE_DOWN`) y
la paleta (`der` en lugar de `izq`). El mismo array `teclas` sirve para los dos: tiene una casilla por tecla,
así que los dos jugadores pueden apretar a la vez.

`SDL_clamp` la deja adentro de la pantalla: `480 - der.h` es lo más abajo que puede estar su borde de arriba.
El robot va a mantener apretada la flecha Arriba un ratito.

#### Desafío
Hacé que la paleta rosa (der) suba con la flecha Arriba y baje con la flecha Abajo, sin salirse de la pantalla.

#### Pasos
1. Buscá el comentario `/* acá: el jugador 2, con las flechas Arriba y Abajo */`.
2. Debajo, `if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;`.
3. Después, `if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;`.
4. Y `der.y = SDL_clamp(der.y, 0, 480 - der.h);`. Tocá **Jugar**, probá las dos paletas a la vez y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        /* acá: el jugador 2, con las flechas Arriba y Abajo */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
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
apretar Arriba
cuadros 20
soltar Arriba
cuadros 3
```

#### Estado
```
buscar #ff3ca0
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 98, ancho 12, alto 80
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        /* acá: el jugador 2, con las flechas Arriba y Abajo */
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
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
Las dos paletas suben y bajan al mismo tiempo. {mentor} se ríe: —¡Hacía años que nadie me ganaba de este
lado! Gheco corre de una punta a la otra sin saber a quién alentar.

#### Imagen
- La máquina vieja de la Cancha con dos lugares para jugar, uno a cada lado.
- Kira con dos dedos sobre las teclas de un lado; Arcadia, del otro, con las flechas, muy concentrada.
- En la pantalla, la paleta cian y la paleta rosa a distintas alturas; Gheco corre entre las dos, indeciso.

### Micro-misión R02-N01-P3 · La pelota que rebota

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: El rebote | si toca el borde: ponerla en el borde y vy = -vy
recompensa: xp 10, monedas 4
```

#### Escena
{mentor} pone una ficha y aparece la pelota amarilla. Cruza la cancha en diagonal… y se va por abajo, para
siempre. —Así no se puede jugar —suspira—. Las paredes de arriba y de abajo tienen que devolverla.

#### Gheco sugiere
La pelota tiene una **velocidad** con dos partes: `vx` (cuánto se mueve de costado por segundo) y `vy`
(cuánto se mueve hacia abajo por segundo). Si `vy` es positiva, baja; si es negativa, sube.

**Rebotar** es darle la vuelta a `vy`: `vy = -vy;`. Si bajaba a 150, ahora sube a 150.

Se rebota cuando se pasa del borde:
```c
if (pelota.y < 0) {
    pelota.y = 0;     /* la vuelvo a poner justo en el borde */
    vy = -vy;
}
```
Para el borde de abajo, lo que se mira es el borde de abajo de la pelota: `pelota.y + pelota.h > 480`. Y se
la deja en `480 - pelota.h`.

¿Por qué ponerla de nuevo en el borde? Si quedó un poquito afuera y solo se da vuelta `vy`, en el cuadro
siguiente puede seguir afuera y volver a darse vuelta: queda temblando pegada a la pared. (El
Atraviesaparedes vive de eso.)

#### Desafío
Hacé que la pelota rebote en el borde de arriba y en el de abajo.

#### Pasos
1. Buscá el comentario `/* acá: que rebote arriba y abajo */`.
2. Escribí el `if (pelota.y < 0) {` con `pelota.y = 0;` y `vy = -vy;` adentro, y cerralo.
3. Escribí el `if (pelota.y + pelota.h > 480) {` con `pelota.y = 480 - pelota.h;` y `vy = -vy;` adentro, y cerralo.
4. Tocá **Jugar** para verla rebotar y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 120;   /* píxeles por segundo, hacia la derecha */
    float vy = 150;   /* píxeles por segundo, hacia abajo */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        /* acá: que rebote arriba y abajo */

        /* si sale por un costado, vuelve al medio */
        if (pelota.x < -12 || pelota.x > 640) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

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
cuadros 120
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 557, y 399, ancho 12, alto 12
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 120;   /* píxeles por segundo, hacia la derecha */
    float vy = 150;   /* píxeles por segundo, hacia abajo */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        /* acá: que rebote arriba y abajo */
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        /* si sale por un costado, vuelve al medio */
        if (pelota.x < -12 || pelota.x > 640) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

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
La pelota baja, pega en el borde con un brillo y vuelve a subir. Rebota, rebota, rebota. Gheco la sigue con
la cabeza hasta marearse. —Eso —dice {mentor}—. Ahora ya es casi un juego.

#### Imagen
- La pantalla grande de la Cancha: la pelota amarilla con su recorrido en zigzag, rebotando arriba y abajo con un destello en cada borde.
- Kira festeja; Arcadia aplaude.
- Gheco, mareado, sigue la pelota con la cabeza y los ojos en espiral.

### Micro-misión R02-N01-P4 · Pegarle con la paleta

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Devolver la pelota | if (toca(pelota, izq) && vx < 0) · pegarla a la paleta · vx = -vx
recompensa: xp 10, monedas 4
```

#### Escena
La pelota viene derecho a la paleta cian… y la atraviesa como si fuera humo. Desde la pared, un
Atraviesaparedes se ríe con la boca llena de ladrillos. —La paleta rosa ya la devuelve —dice {mentor}—. A la
tuya le falta lo mismo.

#### Gheco sugiere
La función `toca(a, b)` (la de R01-N05) dice si dos rectángulos se pisan. La paleta del jugador 2 ya
devuelve la pelota así:
```c
if (toca(pelota, der) && vx > 0) {
    pelota.x = der.x - pelota.w;   /* la pego al frente de la paleta */
    vx = -vx;                      /* y la mando para el otro lado */
}
```
- `vx > 0` quiere decir «viene hacia la derecha», hacia esa paleta. Así no rebota dos veces si en el cuadro
  siguiente todavía la toca.
- Pegarla al frente es lo mismo que hiciste con los bordes: que no quede adentro.

Para el jugador 1 es al revés: la pelota viene hacia la izquierda (`vx < 0`), y el frente de la paleta
izquierda es su borde derecho: `izq.x + izq.w`.

#### Desafío
Hacé que la paleta cian (izq) también devuelva la pelota.

#### Pasos
1. Buscá el comentario `/* acá: que la paleta del jugador 1 también la devuelva */`.
2. Escribí `if (toca(pelota, izq) && vx < 0) {`.
3. Adentro, `pelota.x = izq.x + izq.w;` y `vx = -vx;`, y cerrá la llave.
4. Tocá **Jugar** y jugá un rato con alguien (W y S contra las flechas). Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 230, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 150, 12, 12 };
    float vx = -200;  /* arranca yendo hacia el jugador 1 */
    float vy = 90;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        /* la paleta del jugador 2 la devuelve */
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }
        /* acá: que la paleta del jugador 1 también la devuelva */

        /* si sale por un costado, vuelve al medio */
        if (pelota.x < -12 || pelota.x > 640) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

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
cuadros 120
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 154, y 332, ancho 12, alto 12
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 230, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 150, 12, 12 };
    float vx = -200;  /* arranca yendo hacia el jugador 1 */
    float vy = 90;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        /* la paleta del jugador 2 la devuelve */
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }
        /* acá: que la paleta del jugador 1 también la devuelva */
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }

        /* si sale por un costado, vuelve al medio */
        if (pelota.x < -12 || pelota.x > 640) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }

        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

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
*¡Toc!* La pelota pega en la paleta cian y vuelve. *¡Toc!* La rosa la devuelve. El Atraviesaparedes se
queda sin lugar por donde meterse y se escurre por una rendija del piso. Las luces del salón se encienden
de a una. {mentor} sonríe: —Ya se puede jugar. Lo que falta es saber quién va ganando.

#### Imagen
- La máquina de la Cancha encendida: la pelota amarilla rebota contra la paleta cian con una chispa.
- Un Atraviesaparedes se escurre por una rendija del piso, enojado.
- Kira juega contra Arcadia, las dos riéndose; Gheco hace de árbitro sentado sobre la máquina.

## R02-N02 · Los puntos

```meta
tipo: tema
criatura: glitch
padre: R02-N01
precio: 10
usa: juegos.colisiones, juegos.bucle, juegos.entrada
```

### Crónica

Kira y {mentor} juegan diez minutos sin parar. La pelota va, viene, se escapa por un costado, vuelve al
medio… y nadie sabe quién va ganando. —Así no es un partido —dice {mentor}, cruzada de brazos—. Es pelotear.
Gheco, sentado arriba de la máquina, levanta una mano por cada pelota que se escapa, pero ya se le acabaron
los dedos. Sobre la pantalla parpadea un **glitch**: dos números que se pisan y no dicen nada.

### Objetivos

Que el Pong lleve la cuenta: sumar un punto cuando la pelota se escapa por un costado, sacar desde el medio
hacia el otro lado, mostrar el marcador grande arriba y dar un segundo de respiro antes de cada saque.

### Antes de empezar

R02-N01 (la cancha, las paletas y el rebote). De R01: el texto en pantalla y la escala (N07) y el delta
time (N04).

### Explicación

#### ¿Cuándo es punto?
Cuando la pelota sale **entera** por un costado. Por la izquierda, sale cuando su borde derecho pasa el 0:
`pelota.x + pelota.w < 0`. Por la derecha, cuando su borde izquierdo pasa el ancho de la ventana:
`pelota.x > 640`. Si se escapa por la izquierda, al jugador 1 se le pasó: el punto es para el jugador 2.

#### Dos contadores
Cada jugador tiene su variable entera, que arranca en 0:
```c
int puntosIzq = 0;
int puntosDer = 0;
```
`puntosDer++;` le suma uno (es lo mismo que `puntosDer = puntosDer + 1;`).

#### Un aviso: «hubo punto»
Pase lo que pase, después de un punto se hace lo mismo: la pelota vuelve al medio. Para no escribirlo dos
veces, se usa una variable `bool punto` que arranca en `false`, se pone en `true` en cualquiera de los dos
casos y, al final, un solo `if (punto)` acomoda la pelota.

#### El saque
Si la pelota vuelve al medio con la misma velocidad, sale siempre para el mismo lado. Dándole la vuelta a
`vx` (`vx = -vx;`), cada saque va hacia el otro jugador.

#### El marcador grande
`SDL_SetRenderScale(lapiz, 4, 4)` hace que todo lo que se dibuje después salga 4 veces más grande, también
las coordenadas: `(60, 5)` cae en `(240, 20)` de la pantalla. Después hay que volver a `1, 1`, porque si no
el cuadro siguiente se dibuja todo gigante.

#### Un respiro
Una variable `espera` con los segundos que faltan para sacar. Mientras sea mayor que 0, se le resta `dt` y la
pelota no se mueve. Al hacer un punto se la pone en 1: un segundo de pausa para que los dos se acomoden.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;   /* segundos que faltan para sacar */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = -vx;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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

Contar puntos, volver a sacar y esperar un ratito antes de seguir es lo que hace que un juego tenga
partidas: lo mismo pasa con las vidas del Arkanoid, las líneas del Tetris o los niveles de las naves.

### Errores habituales

**Mirar el borde equivocado.** Con `pelota.x < 0` el punto se cuenta cuando la pelota todavía está a medias
en la pantalla. Para que salga entera, el borde derecho: `pelota.x + pelota.w < 0`.

**Glitch: el punto que se cuenta cien veces.** Si la pelota no vuelve al medio en el mismo cuadro, en el
cuadro siguiente sigue afuera y suma otro punto, y otro… El `if (punto)` la saca de ahí enseguida.

**Olvidar volver la escala a 1.** Todo lo que se dibuja después (y el cuadro siguiente) sale cuatro veces más
grande y corrido.

**Restar la espera sin `dt`.** `espera -= 1;` se termina en un solo cuadro. El tiempo se descuenta en
segundos: `espera -= dt;`.

### Micro-misión R02-N02-P1 · ¿Quién hizo el punto?

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Contar el punto | se fue por la izquierda: puntosDer++ · por la derecha: puntosIzq++
recompensa: xp 10, oro 10
```

#### Escena
—Primero, la cuenta —dice {mentor}—. Si la pelota se le escapa a Kira por la izquierda, el punto es
mío. Si se me escapa a mí por la derecha, es de ella. La máquina ya ve cuándo se escapa: le falta
sumar.

#### Gheco sugiere
Ya están los dos `if` que ven si la pelota se fue por un costado, y las dos variables del marcador,
`puntosIzq` y `puntosDer`, que arrancan en 0. Falta sumar:
- Si se fue **por la izquierda** (`pelota.x + pelota.w < 0`), se le pasó al jugador 1: punto para el
  jugador 2, `puntosDer++;`.
- Si se fue **por la derecha** (`pelota.x > 640`), punto para el jugador 1: `puntosIzq++;`.

`++` le suma uno a la variable: `puntosDer++;` es lo mismo que `puntosDer = puntosDer + 1;`. El
marcador de arriba ya muestra las dos variables, así que se va a ver solo.

El robot no va a mover las paletas: la pelota se le va a escapar al jugador 2.

#### Desafío
Sumá el punto al jugador que corresponde cada vez que la pelota se escapa por un costado.

#### Pasos
1. Buscá el comentario `/* acá: un punto para el jugador 2 */` (adentro del `if` de la izquierda) y escribí debajo `puntosDer++;`.
2. Buscá `/* acá: un punto para el jugador 1 */` (adentro del `if` de la derecha) y escribí `puntosIzq++;`.
3. Tocá **Jugar** y dejá pasar la pelota: el número de arriba tiene que cambiar. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            /* acá: un punto para el jugador 2 */
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            /* acá: un punto para el jugador 1 */
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 280, 20, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 352, 20, "%d", puntosDer);
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
textos
```

#### Salida esperada
```
── Estado ──
textos: 1 | 0
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 280, 20, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 352, 20, "%d", puntosDer);
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
La pelota se escapa por la derecha y arriba aparece un **1** del lado de Kira. {mentor} resopla:
—Uno a cero. No te agrandes.

#### Imagen
- La máquina de la Cancha con el marcador encendido arriba: un 1 de un lado y un 0 del otro.
- Kira festeja con el puño; Arcadia, del otro lado, resopla con los brazos cruzados.
- Gheco, sentado arriba de la máquina, levanta un dedo como un árbitro.

### Micro-misión R02-N02-P2 · El saque

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Sacar hacia el otro lado | al volver al medio: vx = -vx
recompensa: xp 10, monedas 4
```

#### Escena
Después del punto, la pelota vuelve al medio… y sale otra vez hacia {mentor}, que ni la ve venir.
—¡Eso es trampa! —se queja—. El saque tiene que ir para el otro lado.

#### Gheco sugiere
Después de un punto, el `if (punto)` vuelve a poner la pelota en el medio. Pero `vx` sigue igual:
si iba hacia la derecha, sale otra vez hacia la derecha.

Para que el saque salga **para el otro lado**, se le da la vuelta a `vx`, como en un rebote:
```c
vx = -vx;
```
Si valía 300 (hacia la derecha), pasa a valer -300 (hacia la izquierda).

#### Desafío
Hacé que después de cada punto la pelota salga desde el medio hacia el otro lado.

#### Pasos
1. Buscá el comentario `/* acá: que el saque salga para el otro lado */` adentro del `if (punto)`.
2. Debajo, escribí `vx = -vx;`.
3. Tocá **Jugar** y mirá qué pasa después del primer punto. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            /* acá: que el saque salga para el otro lado */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 280, 20, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 352, 20, "%d", puntosDer);
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
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 135, y 305, ancho 12, alto 12
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = -vx;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 280, 20, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 352, 20, "%d", puntosDer);
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
Ahora el saque cruza la cancha hacia el que no hizo el punto. {mentor} lo devuelve con un golpe
seco. —Así sí. Parejo.

#### Imagen
- La pelota amarilla sale del centro de la cancha hacia la paleta rosa, con una estela.
- Arcadia, lista, con la mano sobre los controles; Kira sonríe del otro lado.
- Gheco señala con la cola hacia dónde va la pelota.

### Micro-misión R02-N02-P3 · El marcador grande

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Texto grande | SDL_SetRenderScale(lapiz, 4, 4) · dibujar · volver a 1, 1
recompensa: xp 10, monedas 4
```

#### Escena
Los números del marcador son tan chiquitos que Gheco tiene que subirse a la pantalla para leerlos.
—En una cancha, el marcador se ve desde la puerta —dice {mentor}.

#### Gheco sugiere
Las letras de `SDL_RenderDebugText` miden 8 × 8 píxeles. Para agrandarlas, se agranda **todo lo que
se dibuja después** con la escala (lo viste en R01-N07):
```c
SDL_SetRenderScale(lapiz, 4, 4);   /* todo 4 veces más grande */
SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
SDL_SetRenderScale(lapiz, 1, 1);   /* y de vuelta a lo normal */
```
Con la escala, las coordenadas también se multiplican por 4: `(60, 5)` cae en `(240, 20)` de la
pantalla, y `(88, 5)` en `(352, 20)`. Por eso se escriben más chicas.

#### Desafío
Dibujá el marcador cuatro veces más grande, a los dos lados de la red.

#### Pasos
1. Buscá el comentario `/* acá: el marcador cuatro veces más grande */` y borrá las dos líneas de abajo (las de 280 y 352).
2. En su lugar, escribí `SDL_SetRenderScale(lapiz, 4, 4);`.
3. Dibujá los dos números en `(60, 5)` y `(88, 5)` con `SDL_RenderDebugTextFormat`, como estaban.
4. Al final, `SDL_SetRenderScale(lapiz, 1, 1);`. Tocá **Jugar** y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = -vx;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        /* acá: el marcador cuatro veces más grande */
        SDL_RenderDebugTextFormat(lapiz, 280, 20, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 352, 20, "%d", puntosDer);
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
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 240, y 20, ancho 140, alto 28
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = -vx;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
Dos números enormes se encienden arriba de la red. Desde la puerta del salón, alguien aplaude: la
Cancha ya tiene marcador de verdad.

#### Imagen
- La pantalla de la máquina con dos números blancos enormes arriba, a cada lado de la red.
- Kira, de lejos, señala el marcador; Arcadia asiente.
- Gheco, que estaba subido a la pantalla, se baja de un salto.

### Micro-misión R02-N02-P4 · Un respiro antes del saque

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Esperar | espera = 1 al hacer un punto · si espera > 0: espera -= dt y la pelota quieta
recompensa: xp 10, monedas 4
```

#### Escena
Apenas hay un punto, la pelota ya está saliendo otra vez. {mentor} no llega ni a acomodar la paleta.
—Un segundito, por favor —pide—. Las máquinas viejas siempre daban un respiro.

#### Gheco sugiere
Se agrega una variable `espera`: los **segundos que faltan** para sacar. Ya está creada y arranca en 0.

1. Cuando hay un punto, adentro del `if (punto)`: `espera = 1;` (un segundo).
2. Donde se mueve la pelota, solo se la mueve si no hay que esperar:
```c
if (espera > 0) {
    espera -= dt;   /* va bajando, en segundos */
} else {
    pelota.x += vx * dt;
    pelota.y += vy * dt;
}
```
Mientras `espera` sea mayor que 0, la pelota se queda quieta en el medio. Cuando llega a 0, vuelve a
moverse sola.

#### Desafío
Hacé que después de cada punto la pelota espere un segundo en el medio antes de salir.

#### Pasos
1. Buscá `/* acá: un segundo de respiro antes del saque */` (en el `if (punto)`) y escribí `espera = 1;`.
2. Buscá `/* acá: si hay que esperar, descontar el tiempo y no mover la pelota */`.
3. Envolvé las dos líneas que mueven la pelota con el `if (espera > 0) { espera -= dt; } else { … }` de la sugerencia.
4. Tocá **Jugar**, dejá pasar una pelota y mirá el respiro. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;   /* segundos que faltan para sacar */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        /* acá: si hay que esperar, descontar el tiempo y no mover la pelota */
        pelota.x += vx * dt;
        pelota.y += vy * dt;
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = -vx;
            /* acá: un segundo de respiro antes del saque */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
cuadros 90
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 314, y 234, ancho 12, alto 12
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;   /* segundos que faltan para sacar */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = -vx;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
Punto, un segundo de silencio, y el saque. {mentor} acomoda la paleta con calma y sonríe. —Ahora sí
parece un partido. —El glitch del marcador se ordena: dos números claros que ya no se pisan.

#### Imagen
- La pelota amarilla quieta en el centro de la cancha, con un brillo que late, esperando el saque.
- Arcadia acomoda la paleta tranquila; Kira estira los dedos.
- Un glitch chiquito se desarma en píxeles al lado del marcador; Gheco lo mira irse.

## R02-N03 · La pelota que acelera

```meta
tipo: tema
criatura: atraviesaparedes
padre: R02-N02
precio: 10
temas: juegos.fisica
usa: juegos.colisiones, juegos.bucle
```

### Crónica

Los partidos ya tienen marcador, pero son eternos: la pelota va y viene siempre igual de lenta y siempre
derecho, como un péndulo. Gheco bosteza. —En la Cancha de verdad, cada golpe la apuraba un poco —cuenta
{mentor}—. Y el campeón sabía pegarle con la punta de la paleta para mandarla en diagonal. —En la pared,
un **Atraviesaparedes** se frota las manos: si la pelota va demasiado rápido, él sabe cómo hacerla pasar
a través de la paleta.

### Objetivos

Que la pelota se acelere con cada golpe (multiplicando su velocidad), que tenga un tope para que nunca
atraviese la paleta, y que salga para arriba o para abajo según dónde pegó en la paleta.

### Antes de empezar

R02-N02 (los puntos y el saque). De R01: el delta time (N04) y las colisiones (N05).

### Explicación

#### Acelerar es multiplicar
Para que cada golpe la apure un 10 %, al devolverla se multiplica la velocidad por `1.1`:
```c
vx = -vx * 1.1f;   /* dar la vuelta y un 10 % más */
```
300 pasa a 330, después a 363, después a 399… La `f` de `1.1f` dice que es un `float`, como `vx`.

#### Un tope
Si nunca para de crecer, llega un momento en que la pelota avanza más de 12 píxeles por cuadro: en un cuadro
está antes de la paleta y en el siguiente, del otro lado, **sin haberla tocado nunca**. Ese es el truco del
Atraviesaparedes. Con un tope de 600 píxeles por segundo avanza unos 10 por cuadro, menos que el ancho de la
paleta. `SDL_clamp(valor, mínimo, máximo)` lo deja adentro:
```c
vx = SDL_clamp(vx, -600, 600);
```
El mínimo es -600 porque la pelota también puede ir hacia la izquierda (velocidad negativa).

#### Pegarle con la punta
Se mide **cuánto se corrió la pelota del medio de la paleta**: el centro de la pelota menos el centro de la
paleta.
```c
float diferencia = (pelota.y + pelota.h / 2) - (der.y + der.h / 2);
```
Si pegó en el medio, da 0 y la pelota sale derecho. Si pegó abajo, da positivo (sale para abajo); si pegó
arriba, negativo (sale para arriba). Multiplicado por 5, es la nueva `vy`: cuanto más en la punta, más
inclinada sale.

#### El saque vuelve a empezar
Después de un punto, la pelota vuelve al medio con la velocidad del principio (300) y derecho (`vy = 0`). Eso
ya está escrito en el `if (punto)`: `(vx > 0) ? -300 : 300` quiere decir «si iba para la derecha, -300; si
no, 300».

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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

Que un juego se ponga más difícil de a poco es lo que lo hace entretenido: la pelota del Arkanoid, las
piezas del Tetris y las naves enemigas también se aceleran. Y el tope es la regla de oro para que lo rápido
no atraviese lo que tiene que chocar.

### Errores habituales

**Multiplicar por 10 en lugar de 1.1.** `vx * 10` la vuelve diez veces más rápida de un golpe. Un 10 % más
es `vx * 1.1f`.

**Atraviesaparedes: sin tope.** Después de muchos golpes la pelota va tan rápido que salta la paleta de un
cuadro al otro y es punto aunque la paleta estaba ahí.

**Tope solo para un lado.** `SDL_clamp(vx, 0, 600)` deja en 0 cualquier velocidad hacia la izquierda: la
pelota se queda quieta. El mínimo tiene que ser -600.

**Restar al revés.** `(der.y + der.h / 2) - (pelota.y + …)` da el signo contrario: la pelota que pega abajo
sale para arriba.

### Micro-misión R02-N03-P1 · Cada golpe, más rápido

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Acelerar | al devolverla: vx = -vx * 1.1f
recompensa: xp 10, oro 10
```

#### Escena
—Primero, que se apure —dice {mentor}—. Cada vez que una paleta la devuelve, un poquito más rápido.
Así el partido empieza tranquilo y termina a los gritos.

#### Gheco sugiere
Cuando una paleta devuelve la pelota, hoy se le da la vuelta a `vx`: `vx = -vx;`. Para que además vaya
**un 10 % más rápido**, se multiplica por `1.1`:
```c
vx = -vx * 1.1f;
```
Si venía a 300 hacia la derecha, vuelve a 330 hacia la izquierda. La `f` dice que `1.1` es un
`float`, como `vx`.

Hay que cambiarlo en las **dos** paletas: en la de la izquierda y en la de la derecha.

#### Desafío
Hacé que cada vez que una paleta devuelve la pelota, la pelota salga un 10 % más rápido.

#### Pasos
1. Buscá el comentario `/* acá: devolverla un 10 % más rápido */` (en la paleta izquierda).
2. Cambiá la línea de abajo, `vx = -vx;`, por `vx = -vx * 1.1f;`.
3. Hacé lo mismo en la paleta derecha (es la otra línea `vx = -vx;` que está adentro de `toca(pelota, der)`).
4. Tocá **Jugar** y mirá cómo se apura. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            /* acá: devolverla un 10 % más rápido */
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
cuadros 90
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 411, y 234, ancho 12, alto 12
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
Golpe, golpe, golpe: cada uno más rápido que el anterior. Gheco ya no bosteza; ahora mueve la cabeza
de un lado al otro, cada vez más ligero.

#### Imagen
- La pelota amarilla con una estela cada vez más larga, rebotando entre la paleta cian y la rosa.
- Kira y Arcadia juegan concentradas, inclinadas sobre los controles.
- Gheco, sobre la máquina, mueve la cabeza de un lado al otro, cada vez más rápido.

### Micro-misión R02-N03-P2 · Con un tope

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: El tope | vx = SDL_clamp(vx, -600, 600) · menos que el ancho de la paleta por cuadro
recompensa: xp 10, monedas 4
```

#### Escena
La pelota ya va tan rápido que, de golpe, pasa **a través** de la paleta de {mentor} sin tocarla. En
la pared, el Atraviesaparedes aplaude. —¡Eso no vale! —grita {mentor}—. La tocó. Bueno… no la tocó.
La saltó.

#### Gheco sugiere
Cada cuadro la pelota avanza `vx * dt`. Si va demasiado rápido, en un cuadro está **antes** de la
paleta y en el siguiente ya está **del otro lado**: nunca se pisaron, así que `toca` nunca da `true`.

La paleta mide 12 de ancho. A 600 píxeles por segundo, la pelota avanza unos 10 por cuadro: nunca la
puede saltar. Por eso, después de acelerarla, se le pone un **tope**:
```c
vx = SDL_clamp(vx, -600, 600);
```
`SDL_clamp` deja el número entre -600 y 600 (negativo es hacia la izquierda). Va en las **dos**
paletas, justo después de `vx = -vx * 1.1f;`.

El robot va a dejar que la pelota rebote muchas veces, hasta que llegue al tope.

#### Desafío
Ponele un tope de 600 píxeles por segundo a la velocidad de la pelota, en las dos paletas.

#### Pasos
1. Buscá `/* acá: que no pase del tope */` (en la paleta izquierda) y escribí debajo `vx = SDL_clamp(vx, -600, 600);`.
2. En la paleta derecha, después de `vx = -vx * 1.1f;`, escribí la misma línea.
3. Tocá **Jugar** y dejá que rebote mucho rato. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            /* acá: que no pase del tope */
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
cuadros 700
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 137, y 234, ancho 12, alto 12
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
Por más rápido que vaya, la pelota siempre choca con la paleta. El Atraviesaparedes empuja, empuja… y
se da la cabeza contra el borde. Se va refunfuñando por una rendija.

#### Imagen
- La pelota amarilla muy rápida, con una estela larga, chocando contra la paleta rosa con una chispa.
- Un Atraviesaparedes, criatura gomosa y translúcida, se golpea la cabeza contra el borde de la pantalla, enojado.
- Arcadia festeja haber devuelto la pelota; Kira se ríe; Gheco se tapa los ojos.

### Micro-misión R02-N03-P3 · Pegarle con la punta

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: El ángulo | vy = (centro de la pelota - centro de la paleta) * 5
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora, el secreto del campeón —dice {mentor}, y baja la voz—. Si le pegás con la punta de abajo, la
pelota sale para abajo. Con la de arriba, para arriba. En el medio, derecho. Probalo con mi paleta.

#### Gheco sugiere
Para saber dónde pegó, se compara el **centro de la pelota** con el **centro de la paleta**:
- el centro de la pelota (en altura) es `pelota.y + pelota.h / 2`;
- el centro de la paleta derecha es `der.y + der.h / 2`.

La resta dice cuánto se corrió del medio: 0 si pegó justo en el medio, positivo si pegó más abajo,
negativo si pegó más arriba. Multiplicada por 5 es la nueva velocidad hacia abajo:
```c
vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
```
Si pegó 30 píxeles abajo del medio, sale a 150 hacia abajo. En esta micro-misión, solo la paleta
derecha.

#### Desafío
Hacé que la pelota salga de la paleta derecha para arriba o para abajo según dónde pegó.

#### Pasos
1. Buscá el comentario `/* acá: que salga para arriba o para abajo según dónde pegó */` adentro de `toca(pelota, der)`.
2. Debajo, escribí `vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;`.
3. Tocá **Jugar** y pegale con la punta de la paleta rosa (las flechas). Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            /* acá: que salga para arriba o para abajo según dónde pegó */
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
cuadros 90
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 411, y 318, ancho 12, alto 12
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
La pelota pega en la punta de la paleta rosa y sale en diagonal, rebota en el techo y cruza la cancha.
Kira silba. —Eso sí que no lo vi venir.

#### Imagen
- La pelota amarilla sale en diagonal desde la punta de la paleta rosa, con una línea de recorrido que rebota en el borde de arriba.
- Arcadia, con una sonrisa pícara, acaba de mover la paleta; Kira abre grandes los ojos.
- Gheco sigue la diagonal con el dedo.

### Micro-misión R02-N03-P4 · Las dos paletas

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: El ángulo en las dos | el mismo cálculo con izq.y + izq.h / 2
recompensa: xp 10, monedas 4
```

#### Escena
—¡Ahora yo también! —pide Kira—. Si {mentor} puede pegarle con la punta, la paleta cian también tiene
que poder.

#### Gheco sugiere
Es la misma cuenta que en la paleta derecha, pero con la paleta izquierda:
```c
vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
```
Va adentro de `toca(pelota, izq)`, después del tope.

El robot va a bajar la paleta cian con la S para que la pelota le pegue cerca de la punta de arriba.

#### Desafío
Hacé que la paleta izquierda también mande la pelota para arriba o para abajo según dónde pegó.

#### Pasos
1. Buscá el comentario `/* acá: que salga para arriba o para abajo según dónde pegó */` adentro de `toca(pelota, izq)`.
2. Debajo, escribí `vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;`.
3. Tocá **Jugar** y jugá un partido con las dos puntas. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            /* acá: que salga para arriba o para abajo según dónde pegó */
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
apretar S
cuadros 42
soltar S
cuadros 80
```

#### Estado
```
buscar #ffdc00
textos
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 180, y 468, ancho 12, alto 12
textos: 0 | 0
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx * 1.1f;
            vx = SDL_clamp(vx, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
Diagonales, rebotes en el techo, golpes con la punta: ahora el partido es de verdad. {mentor} se ríe a
carcajadas. —¡Así jugaba el campeón! —dice. Y se queda callada, mirando la máquina más vieja, como si
se acordara de algo.

#### Imagen
- La pantalla de la Cancha con el recorrido de la pelota en zigzag, rebotando en las dos paletas y en los bordes.
- Kira y Arcadia juegan riéndose a carcajadas.
- Gheco, de árbitro, señala una diagonal con los dos brazos.

## R02-N04 · La máquina juega

```meta
tipo: tema
criatura: glitch
padre: R02-N03
precio: 10
temas: juegos.ia
usa: juegos.colisiones, juegos.entrada, juegos.bucle
```

### Crónica

Es tarde. {mentor} se va a revisar las luces del salón y Kira se queda sola frente a la máquina, con la
paleta rosa quieta del otro lado. —Si nadie juega de ese lado, no hay partido —dice Gheco. Entonces Kira
tiene una idea: ¿y si la paleta rosa se moviera sola? Una máquina que juega. Las de antes lo hacían: mirabas
la pantalla y del otro lado no había nadie, y aun así te devolvían la pelota. Un **glitch** se ríe en la
pantalla: él sabe cómo hacer temblar a una paleta que piensa demasiado.

### Objetivos

Programar una paleta que juega sola (una inteligencia artificial muy simple): que mire dónde está la pelota y
se acerque, con una velocidad máxima para que se le pueda ganar, que no tiemble cuando ya llegó, que vuelva al
medio mientras la pelota se aleja y que se pueda elegir entre jugar contra la máquina o de a dos.

### Antes de empezar

R02-N03 (la pelota que acelera). De R01: el teclado (N02) y el delta time (N04).

### Explicación

#### Una máquina que juega no adivina
La «inteligencia» de la paleta es una regla chiquita, repetida en cada cuadro:
1. **¿A dónde tengo que ir?** Al lugar de la pelota (el **objetivo**).
2. **¿Qué tan lejos estoy?** El objetivo menos el centro de la paleta: la **distancia**.
3. **Me acerco un poquito**: si la distancia es negativa (el objetivo está más arriba), subo; si es positiva,
   bajo.

#### Que se le pueda ganar
Si la paleta fuera directo al objetivo (`der.y = objetivo`), nunca erraría: aburridísimo. Por eso se mueve como
mucho **240 píxeles por segundo** (`240 * dt` por cuadro), menos que la pelota cuando se acelera. Si la pelota va
muy rápido o en diagonal, no llega.

#### Que no tiemble
Si ya está casi en el lugar, un paso de más la pasa, y en el cuadro siguiente vuelve, y se pasa para el otro
lado: tiembla. La solución es una **zona muerta**: si está a menos de 10 píxeles, no se mueve.
`SDL_fabsf(distancia)` es la distancia sin el signo (el valor absoluto: -7 da 7).

#### Jugar como alguien
Un buen jugador no persigue la pelota cuando se aleja: vuelve al medio y espera. Si `vx > 0`, la pelota viene
hacia la paleta derecha: el objetivo es la pelota. Si no, el objetivo es el medio de la cancha (240).

#### Uno o dos jugadores
Una variable `bool contraLaMaquina` decide quién mueve la paleta derecha: la máquina o las flechas. Con un
evento de teclado (de un toque, como en R01-N02) se cambia: la tecla 1 o la 2.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_1) {
                contraLaMaquina = true;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_2) {
                contraLaMaquina = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = 240;
            if (vx > 0) {
                objetivo = pelota.y + pelota.h / 2;
            }
            float distancia = objetivo - (der.y + der.h / 2);
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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

Los enemigos de casi todos los juegos funcionan así: miran algo (dónde estás vos), deciden a dónde ir y se
acercan con una velocidad máxima. Los fantasmas del laberinto, las naves enemigas y los robots de los
plataformas son variaciones de esta misma regla.

### Errores habituales

**Teletransportar la paleta.** `der.y = pelota.y;` hace una paleta perfecta que nunca pierde. Moverla de a
`240 * dt` es lo que la hace humana.

**Glitch: la paleta que tiembla.** Sin la zona muerta, cuando ya llegó se pasa un poquito para un lado y para
el otro, cuadro a cuadro.

**Comparar la pelota con el borde de la paleta.** `pelota.y < der.y` compara con el borde de arriba: la paleta
termina recibiendo con la punta. Se compara con el centro: `der.y + der.h / 2`.

**Olvidar `SDL_fabsf`.** `if (distancia < 10)` es verdadero para cualquier distancia negativa (la pelota está
arriba): la paleta nunca sube.

### Micro-misión R02-N04-P1 · La paleta que sigue

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Acercarse | distancia = objetivo - centro · si < 0, subir · si > 0, bajar (240 * dt)
recompensa: xp 10, oro 10
```

#### Escena
—Empecemos por lo más simple —dice Kira—. La paleta rosa mira dónde está la pelota y va para ahí.
Gheco se sienta arriba de la paleta, listo para el viaje.

#### Gheco sugiere
Ya está calculada la **distancia**: dónde está la pelota (el `objetivo`) menos el centro de la paleta.
- Si la distancia es **negativa**, la pelota está más arriba: la paleta sube, `der.y -= 240 * dt;`.
- Si es **positiva**, está más abajo: la paleta baja, `der.y += 240 * dt;`.

```c
if (distancia < 0) der.y -= 240 * dt;
if (distancia > 0) der.y += 240 * dt;
```
240 píxeles por segundo es la velocidad máxima de la máquina: más lenta que la pelota rápida, para
que se le pueda ganar.

#### Desafío
Hacé que la paleta derecha se acerque sola a la pelota, a 240 píxeles por segundo.

#### Pasos
1. Buscá el comentario `/* acá: acercar la paleta al objetivo */`.
2. Debajo, escribí `if (distancia < 0) der.y -= 240 * dt;`.
3. En la línea siguiente, `if (distancia > 0) der.y += 240 * dt;`.
4. Tocá **Jugar**: ahora jugás vos solo con la W y la S contra la máquina. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = pelota.y + pelota.h / 2;
            float distancia = objetivo - (der.y + der.h / 2);
            /* acá: acercar la paleta al objetivo */
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
cuadros 40
```

#### Estado
```
buscar #ff3ca0
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 199, ancho 12, alto 80
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = pelota.y + pelota.h / 2;
            float distancia = objetivo - (der.y + der.h / 2);
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
La paleta rosa se mueve sola y le devuelve la pelota a Kira. Gheco, sentado encima, se agarra fuerte.
—¡Está viva! —grita—. Bueno… está mirando.

#### Imagen
- La paleta rosa moviéndose sola en la pantalla, con una flecha de movimiento hacia la pelota amarilla.
- Kira juega sola, asombrada, con los dedos en la W y la S.
- Gheco, diminuto, sentado sobre el borde de la máquina del lado rosa, agarrado fuerte.

### Micro-misión R02-N04-P2 · Que no tiemble

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: Zona muerta | si SDL_fabsf(distancia) < 10, distancia = 0
recompensa: xp 10, monedas 4
```

#### Escena
La paleta rosa llega a la altura de la pelota… y se pone a temblar: arriba, abajo, arriba, abajo, como
si tuviera frío. En la pantalla, un glitch se ríe con cada temblor.

#### Gheco sugiere
Cuando la paleta ya está casi en el lugar, un paso de más la pasa. En el cuadro siguiente vuelve, se
pasa para el otro lado… y así: tiembla.

La solución es una **zona muerta**: si está a menos de 10 píxeles, la distancia se toma como 0 y la
paleta no se mueve.
```c
if (SDL_fabsf(distancia) < 10) {
    distancia = 0;
}
```
`SDL_fabsf` da el número sin signo (el **valor absoluto**): `SDL_fabsf(-7)` es 7. Así sirve para los
dos lados.

#### Desafío
Hacé que la paleta de la máquina no se mueva cuando está a menos de 10 píxeles de su objetivo.

#### Pasos
1. Buscá el comentario `/* acá: si está cerca (a menos de 10 píxeles), no moverse */`.
2. Escribí `if (SDL_fabsf(distancia) < 10) {`, adentro `distancia = 0;` y cerrá la llave.
3. Tocá **Jugar** y mirá la paleta cuando llega: ya no tiembla. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = pelota.y + pelota.h / 2;
            float distancia = objetivo - (der.y + der.h / 2);
            /* acá: si está cerca (a menos de 10 píxeles), no moverse */
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
cuadros 40
```

#### Estado
```
buscar #ff3ca0
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 190, ancho 12, alto 80
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = pelota.y + pelota.h / 2;
            float distancia = objetivo - (der.y + der.h / 2);
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
La paleta llega, frena y espera, quieta y tranquila. El glitch se queda sin temblor del que reírse y
se apaga con un chasquido.

#### Imagen
- La paleta rosa quieta, alineada con la pelota amarilla, con un halo tranquilo.
- Un glitch pixelado se apaga con chispas al costado de la pantalla.
- Kira sonríe; Gheco aplaude sentado arriba de la máquina.

### Micro-misión R02-N04-P3 · Volver al medio

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Jugar como alguien | si vx > 0 el objetivo es la pelota · si no, el medio (240)
recompensa: xp 10, monedas 4
```

#### Escena
La paleta rosa persigue la pelota incluso cuando se va para el otro lado, y después no llega a volver.
—Un buen jugador no persigue: espera en el medio —dice {mentor}, que volvió con una linterna.

#### Gheco sugiere
La pelota **viene** hacia la paleta derecha cuando `vx > 0` (va hacia la derecha). Solo en ese caso
vale la pena seguirla. Si se aleja, lo mejor es volver al **medio de la cancha**, que está en 240.
```c
float objetivo = 240;
if (vx > 0) {
    objetivo = pelota.y + pelota.h / 2;
}
```
Es decir: el objetivo es el medio, salvo que la pelota venga.

#### Desafío
Hacé que la máquina siga la pelota solo cuando viene hacia ella y, si no, vuelva al medio (240).

#### Pasos
1. Buscá el comentario `/* acá: seguir la pelota solo cuando viene; si no, volver al medio (240) */`.
2. Cambiá la línea de abajo por `float objetivo = 240;`.
3. Debajo, escribí `if (vx > 0) {`, adentro `objetivo = pelota.y + pelota.h / 2;` y cerrá la llave.
4. Tocá **Jugar** y mirá qué hace la paleta rosa cuando la pelota se aleja. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            /* acá: seguir la pelota solo cuando viene; si no, volver al medio (240) */
            float objetivo = pelota.y + pelota.h / 2;
            float distancia = objetivo - (der.y + der.h / 2);
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
cuadros 120
```

#### Estado
```
buscar #ff3ca0
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 190, ancho 12, alto 80
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
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
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = 240;
            if (vx > 0) {
                objetivo = pelota.y + pelota.h / 2;
            }
            float distancia = objetivo - (der.y + der.h / 2);
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
Ahora la paleta rosa devuelve, vuelve al medio y espera, como un jugador de verdad. {mentor} la mira con
la linterna en la mano. —Así jugaba él —murmura—. El campeón.

#### Imagen
- La paleta rosa en el medio de su lado, esperando, mientras la pelota amarilla se aleja hacia la paleta cian.
- Arcadia, con una linterna en la mano, mira la pantalla muy seria.
- Kira juega concentrada; Gheco mira a Arcadia con curiosidad.

### Micro-misión R02-N04-P4 · Uno o dos jugadores

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Elegir | evento de la tecla 1: contraLaMaquina = true · tecla 2: false
recompensa: xp 10, monedas 4
```

#### Escena
—¿Y si mañana viene alguien a jugar de a dos? —pregunta Kira—. Tiene que poder elegir. {mentor} le
señala dos botones viejos en el tablero de la máquina: uno con un muñequito y otro con dos.

#### Gheco sugiere
La variable `contraLaMaquina` ya decide quién mueve la paleta derecha: si es `true`, la máquina; si es
`false`, las flechas. Abajo de la pantalla ya se ve el modo.

Falta cambiarla con el teclado, con un **evento** (un toque, como en R01-N02), adentro del
`while (SDL_PollEvent(&evento))`:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_1) {
    contraLaMaquina = true;
}
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_2) {
    contraLaMaquina = false;
}
```
El robot va a apretar el 2 y después la flecha de arriba.

#### Desafío
Hacé que con la tecla 1 se juegue contra la máquina y con la 2, de a dos (la paleta derecha con las flechas).

#### Pasos
1. Buscá el comentario `/* acá: con la tecla 1, contra la máquina; con la 2, de a dos */`.
2. Escribí el `if` de la tecla 1, con `contraLaMaquina = true;` adentro.
3. Escribí el `if` de la tecla 2, con `contraLaMaquina = false;` adentro.
4. Tocá **Jugar**, probá las dos teclas y mirá el cartelito de abajo. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con la tecla 1, contra la máquina; con la 2, de a dos */
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = 240;
            if (vx > 0) {
                objetivo = pelota.y + pelota.h / 2;
            }
            float distancia = objetivo - (der.y + der.h / 2);
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
cuadros 2
tecla 2
apretar Arriba
cuadros 30
soltar Arriba
cuadros 2
```

#### Estado
```
buscar #ff3ca0
textos
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 21, ancho 12, alto 80
textos: 0 | 0 | 2 JUGADORES
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
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_1) {
                contraLaMaquina = true;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_2) {
                contraLaMaquina = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            float objetivo = 240;
            if (vx > 0) {
                objetivo = pelota.y + pelota.h / 2;
            }
            float distancia = objetivo - (der.y + der.h / 2);
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
        } else {
            if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        }
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }
        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = SDL_clamp(-vx * 1.1f, -600, 600);
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
Con el 1, la máquina juega sola; con el 2, {mentor} agarra las flechas. —Uno contra uno o contra la
máquina —dice—. Como en los buenos tiempos. —Y mira de reojo la máquina más vieja del salón, tapada con
una lona, en el fondo.

#### Imagen
- El tablero de la máquina de la Cancha con dos botones viejos: uno con un muñequito y otro con dos.
- Kira aprieta uno de los botones; Arcadia ya tiene las manos en las flechas.
- Al fondo del salón, una máquina grande tapada con una lona; Gheco la mira con sospecha.

## R02-N05 · Menú, partido y fin

```meta
tipo: tema
criatura: bucle_eterno
padre: R02-N04
precio: 10
temas: juegos.estados
usa: juegos.entrada, juegos.bucle
```

### Crónica

A la mañana siguiente llega gente nueva a la Cancha: chicos del barrio que vieron las luces encendidas. Se
paran frente a la máquina y no saben qué hacer: la pelota ya está corriendo, no hay cartel de bienvenida, y
el partido no termina nunca. —Un juego de verdad tiene un principio y un final —dice {mentor}—. Un menú para
elegir, el partido, y alguien que gana. Si no, es un **Bucle Eterno**. —Y en el borde de la pantalla, la
serpiente de luz se muerde la cola, contenta.

### Objetivos

Ordenar el juego en **estados** (momentos): el menú, el partido y el fin. Empezar con la barra espaciadora,
terminar cuando alguien llega a 5, jugar la revancha con la R y volver al menú con ESC.

### Antes de empezar

R02-N04 (la máquina juega). De R01: el evento de una tecla (N02) y el jefe «Junta las gemas» (N10), que ya
tenía un fin y una revancha.

### Explicación

#### Los momentos de un juego
Casi todos los juegos pasan por los mismos momentos: un **menú** donde se elige, el **partido** y el **fin**
con el resultado. A cada uno se le dice **estado**. En cada cuadro el juego pregunta en qué estado está y
hace lo que corresponde: en el menú no se mueve nada, en el partido se mueve todo, en el fin se muestra quién
ganó.

#### Ponerles nombre: `enum`
Se podría usar un número (0 el menú, 1 el partido, 2 el fin), pero es fácil confundirse. Un `enum` le pone
nombre a esos números:
```c
enum Estado { MENU, JUGANDO, FIN };   /* MENU vale 0, JUGANDO 1, FIN 2 */
enum Estado estado = MENU;
```
Después se pregunta `if (estado == JUGANDO)`, que se lee solo.

#### Pasar de un estado a otro
Cada cambio tiene su motivo, y casi siempre es un evento:
- en el **menú**, la barra espaciadora → **jugando**;
- **jugando**, alguien llega a 5 → **fin**;
- en el **fin**, la R → el marcador a 0 y otra vez al **menú**;
- **jugando**, ESC → **menú** (para cambiar entre uno y dos jugadores).

Siempre se pregunta en qué estado está **y** qué tecla se apretó: la R solo hace algo en el fin; el espacio,
solo en el menú.

#### Todo lo que se mueve, adentro de `if (estado == JUGANDO)`
Las paletas, la pelota y los puntos se actualizan solo mientras se juega. Por eso en el menú y en el fin
queda todo quieto, aunque el bucle siga dando vueltas.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) {
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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

Todos los juegos de la escalera tienen estados: el Arkanoid (menú, jugando, nivel superado, fin), el Tetris,
las naves… Y muchos programas que no son juegos también: un cajero automático o un formulario de varios
pasos son estados con sus cambios.

### Errores habituales

**Bucle Eterno: un juego sin fin.** Sin el estado `FIN`, el partido sigue para siempre y nadie gana.

**No preguntar el estado antes de la tecla.** Si la R reinicia sin preguntar `estado == FIN`, en medio del
partido cualquier R borra el marcador.

**Cambiar de estado y seguir moviendo.** Si la actualización no está adentro de `if (estado == JUGANDO)`, la
pelota sigue corriendo detrás del menú.

**Comparar con `=` en lugar de `==`.** `if (estado = FIN)` no pregunta: cambia el estado a `FIN` y siempre es
verdadero.

### Micro-misión R02-N05-P1 · El menú

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Empezar | en el menú, evento de la barra espaciadora: estado = JUGANDO
recompensa: xp 10, oro 10
```

#### Escena
Los chicos del barrio miran el cartel **PONG** que ahora brilla en la pantalla. —¿Y ahora? —pregunta
uno. Kira aprieta la barra espaciadora… y no pasa nada. El menú no deja empezar.

#### Gheco sugiere
El juego ya arranca en el estado `MENU` y muestra el cartel. Falta la salida: cuando se aprieta la
barra espaciadora **estando en el menú**, el estado pasa a `JUGANDO`.

Va adentro del `if (evento.type == SDL_EVENT_KEY_DOWN …)`, donde ya está guardada la tecla en la
variable `tecla`:
```c
if (estado == MENU && tecla == SDLK_SPACE) {
    estado = JUGANDO;
}
```
`&&` quiere decir «y»: las dos cosas tienen que ser ciertas.

#### Desafío
Hacé que en el menú, con la barra espaciadora, empiece el partido.

#### Pasos
1. Buscá el comentario `/* acá: en el menú, con la barra espaciadora empieza el partido */`.
2. Escribí `if (estado == MENU && tecla == SDLK_SPACE) {`.
3. Adentro, `estado = JUGANDO;`, y cerrá la llave.
4. Tocá **Jugar**, hacé clic en el juego y apretá la barra espaciadora. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                /* acá: en el menú, con la barra espaciadora empieza el partido */
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
cuadros 5
tecla Espacio
cuadros 30
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: 0 | 0
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
Espacio, y la pelota sale. Los chicos gritan. Uno ya está pidiendo el turno.

#### Imagen
- La pantalla de la Cancha con un cartel enorme amarillo de bloques de luz arriba y dos renglones blancos abajo (sin texto legible).
- Un grupo de chicos del barrio, con abrigos cerrados, rodea la máquina mirando con curiosidad.
- Kira aprieta la barra espaciadora; Gheco, sobre la máquina, levanta los brazos.

### Micro-misión R02-N05-P2 · Gana el que llega a 5

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
criatura: bucle_eterno
carta: El fin | después de un punto: si alguno llegó a 5, estado = FIN
recompensa: xp 10, monedas 4
```

#### Escena
Los chicos juegan y juegan: 8 a 6, 12 a 9, 20 a 18… —¿Cuándo termina? —pregunta uno, cansado. En la
pantalla, el Bucle Eterno da vueltas y vueltas, feliz.

#### Gheco sugiere
El partido tiene que terminar cuando alguno llega a **5 puntos**. Lo mejor es preguntarlo justo después
de un punto, adentro del `if (punto)`:
```c
if (puntosIzq == 5 || puntosDer == 5) {
    estado = FIN;
}
```
`||` quiere decir «o»: alcanza con que uno de los dos llegue. En el estado `FIN` la pantalla ya
muestra quién ganó.

El robot va a jugar un partido de a dos sin mover las paletas, hasta que alguien llegue a 5.

#### Desafío
Hacé que el partido termine cuando alguno de los dos llega a 5 puntos.

#### Pasos
1. Buscá el comentario `/* acá: si alguien llegó a 5, se terminó el partido */` (adentro del `if (punto)`).
2. Escribí `if (puntosIzq == 5 || puntosDer == 5) {`.
3. Adentro, `estado = FIN;`, y cerrá la llave.
4. Tocá **Jugar** y jugá hasta 5. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                /* acá: si alguien llegó a 5, se terminó el partido */
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
cuadros 2
tecla 2
tecla Espacio
cuadros 1500
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: 0 | 5 | GANA EL JUGADOR 2 | R: REVANCHA
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
5 a 3. La pantalla se queda quieta y aparece el cartel del ganador. El Bucle Eterno se suelta la cola,
confundido: el juego terminó, y él no sabe dar vueltas sin fin.

#### Imagen
- La pantalla de la Cancha quieta, con el marcador grande arriba y un cartel amarillo de ganador en el medio (sin texto legible).
- Una serpiente de luz violeta, el Bucle Eterno, suelta su cola confundida en el borde de la pantalla.
- Los chicos festejan; Kira aplaude; Gheco levanta la mano de un ganador imaginario.

### Micro-misión R02-N05-P3 · Revancha

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: La revancha | en el fin, la R: puntos a 0 y estado = MENU
recompensa: xp 10, monedas 4
```

#### Escena
—¡Revancha! —pide el que perdió. Pero la pantalla se quedó congelada en el fin y no hay forma de
volver a empezar sin apagar la máquina.

#### Gheco sugiere
En el estado `FIN`, la R tiene que dejar todo listo para otro partido: el marcador en 0 y de vuelta al
menú (así se puede elegir otra vez uno o dos jugadores).
```c
if (estado == FIN && tecla == SDLK_R) {
    puntosIzq = 0;
    puntosDer = 0;
    estado = MENU;
}
```
Va con los demás eventos de teclado. La pelota no hace falta acomodarla: después del último punto ya
quedó en el medio.

#### Desafío
Hacé que en el fin, con la R, el marcador vuelva a 0 y se vuelva al menú.

#### Pasos
1. Buscá el comentario `/* acá: en el fin, con la R el marcador vuelve a 0 y se vuelve al menú */`.
2. Escribí `if (estado == FIN && tecla == SDLK_R) {`.
3. Adentro, `puntosIzq = 0;`, `puntosDer = 0;` y `estado = MENU;`. Cerrá la llave.
4. Tocá **Jugar**, terminá un partido y apretá la R. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
                /* acá: en el fin, con la R el marcador vuelve a 0 y se vuelve al menú */
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
cuadros 2
tecla 2
tecla Espacio
cuadros 1500
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
textos: PONG | ESPACIO: JUGAR | 2 JUGADORES | 1 O 2 PARA CAMBIAR
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
R, y el cartel de **PONG** vuelve a brillar. Los chicos hacen fila para la revancha. {mentor} sonríe
desde la puerta: hacía años que no había fila en la Cancha.

#### Imagen
- Una fila de chicos del barrio, con abrigos cerrados, esperando turno frente a la máquina de la Cancha.
- En la pantalla, otra vez el cartel amarillo enorme del menú.
- Arcadia, desde la puerta, sonríe; Kira y Gheco ordenan la fila.

### Micro-misión R02-N05-P4 · Volver al menú

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Salir al menú | jugando, ESC: estado = MENU
recompensa: xp 10, monedas 4
```

#### Escena
A mitad de un partido, una chica quiere cambiar a jugar contra la máquina. Pero el 1 y el 2 solo
funcionan en el menú, y al menú no se puede volver.

#### Gheco sugiere
En la Clase 0, ESC cerraba el juego. Acá, **jugando**, ESC vuelve al **menú**, como en casi todos los
juegos:
```c
if (estado == JUGANDO && tecla == SDLK_ESCAPE) {
    estado = MENU;
}
```
El marcador no se borra: si vuelve a apretar espacio, sigue el mismo partido.

#### Desafío
Hacé que jugando, con ESC, se vuelva al menú.

#### Pasos
1. Buscá el comentario `/* acá: jugando, con ESC se vuelve al menú */`.
2. Escribí `if (estado == JUGANDO && tecla == SDLK_ESCAPE) {`.
3. Adentro, `estado = MENU;`, y cerrá la llave.
4. Tocá **Jugar**: empezá, apretá ESC, cambiá con el 1 o el 2 y seguí. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                /* acá: jugando, con ESC se vuelve al menú */
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
cuadros 5
tecla Espacio
cuadros 30
tecla Escape
cuadros 5
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PONG | ESPACIO: JUGAR | 1 JUGADOR: CONTRA LA MAQUINA | 1 O 2 PARA CAMBIAR
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) {
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
Menú, partido, fin, revancha y vuelta al menú: la máquina de la Cancha ya es un juego completo. Los
chicos no se quieren ir. El Bucle Eterno, sin vueltas que dar, se escurre por debajo de la máquina.

#### Imagen
- La máquina de la Cancha encendida a pleno, con chicos jugando y otros mirando alrededor.
- Una serpiente de luz violeta se escurre por debajo del gabinete.
- Kira y Arcadia chocan los cinco; Gheco, arriba de la máquina, saluda a los chicos.

## R02-N06 · Sonido y pausa

```meta
tipo: tema
criatura: fuga_texturas
padre: R02-N05
precio: 10
temas: juegos.sonido
usa: juegos.estados, juegos.entrada
```

### Crónica

La Cancha está llena, pero algo falta. {mentor} cierra los ojos y escucha: las paletas golpean en silencio,
los puntos pasan sin que nadie se entere. —Las máquinas de antes hacían *toc* —dice—. Un toc agudo en cada
golpe y un *bum* grave en cada punto. Con los ojos cerrados sabías cómo iba el partido. —Y además, cuando
llaman a cenar, hay que poder parar sin perder. En el estante del fondo, una niebla de imágenes repetidas se
agita: la **Fuga de Texturas** también se come los sonidos que nadie libera.

### Objetivos

Que la Cancha suene: un pitido corto y agudo en cada golpe de paleta y uno grave y largo en cada punto.
Además, una pausa con la P y un botón de silencio con la M.

### Antes de empezar

R02-N05 (menú, partido y fin). De R01: el sonido (N09), con la función `pitido`.

### Explicación

#### El parlante y el pitido
Es lo mismo que en R01-N09: se abre el parlante una vez al principio y la función `pitido` arma una onda y
se la manda. El número de vueltas por segundo (la **frecuencia**) decide si suena agudo o grave: 440 es un
*la*, agudo y corto para el golpe; 220 es la misma nota una octava más grave, para el punto.

#### ¿Dónde va cada sonido?
Exactamente donde pasa la cosa: el toc, adentro de los `if (toca(...))` de las paletas; el bum, adentro del
`if (punto)`. Así suena en el mismo cuadro en que se ve.

#### La pausa
Una variable `bool pausado`. La P le da la vuelta: `pausado = !pausado;` (`!` es «lo contrario»: si era
`true` pasa a `false`, y al revés). Mientras esté en pausa, no se actualiza nada: se agrega a la condición
que envuelve todo lo que se mueve, `if (estado == JUGANDO && !pausado)`. El dibujo sigue, así se ve la
cancha quieta con el cartel.

#### Silencio
Otra variable que se da vuelta con una tecla: `mudo`. Esta vez es **global** (afuera de `main`, con
`static`), porque la usa la función `pitido`: si está en silencio, `return;` sale de la función sin hacer
nada.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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

El sonido dice cosas sin que haya que mirar: un golpe, un punto, un peligro. Y la pausa y el silencio son
dos cosas que cualquier jugador espera encontrar; se van a repetir en cada juego de la escalera.

### Errores habituales

**Fuga de Texturas: no liberar la onda.** `pitido` pide memoria con `SDL_malloc` en cada sonido. Si falta el
`SDL_free`, cada golpe se queda con un pedazo de memoria y la máquina se ahoga de a poco.

**Sonar en cada cuadro.** Si el pitido va afuera del `if (toca(...))`, suena 60 veces por segundo y se
amontona en el parlante.

**Pausar con `estado`.** Si la P cambia el estado a otro y la R o el ESC también, se pierde dónde estaba el
partido. Una variable aparte, `pausado`, es más simple.

**Olvidar `!pausado` en la condición.** El cartel dice PAUSA, pero la pelota sigue corriendo.

### Micro-misión R02-N06-P1 · El toc de la paleta

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Sonar al golpear | pitido(parlante, 440, 0.05f) adentro de cada toca(...)
recompensa: xp 10, oro 10
```

#### Escena
—El toc primero —dice {mentor}—. Cortito y agudo, en cada golpe. Como una pelotita de ping-pong.

#### Gheco sugiere
El parlante y la función `pitido` ya están (son los de R01-N09). Falta llamarla **justo cuando una
paleta devuelve la pelota**, adentro de cada `if (toca(...))`:
```c
pitido(parlante, 440, 0.05f);   /* agudo (440) y cortito (5 centésimas de segundo) */
```
En las **dos** paletas: la izquierda y la derecha.

#### Desafío
Hacé que suene un pitido corto y agudo (440, 0.05 segundos) cada vez que una paleta devuelve la pelota.

#### Pasos
1. Buscá el comentario `/* acá: el toc de la paleta */` (adentro de la paleta izquierda) y escribí `pitido(parlante, 440, 0.05f);`.
2. Escribí la misma línea al final del `if (toca(pelota, der) && vx > 0)`.
3. Tocá **Jugar** (con el sonido de la compu prendido) y escuchá los golpes. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
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

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                /* acá: el toc de la paleta */
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
cuadros 2
tecla Espacio
cuadros 120
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

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
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

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
*Toc… toc… toc.* Los chicos del barrio se quedan callados para escuchar. Uno cierra los ojos y sigue el
partido de oído.

#### Imagen
- La máquina de la Cancha con anillos de sonido cian saliendo del borde de la pantalla en cada golpe.
- Un chico del barrio con los ojos cerrados, escuchando; Kira juega.
- Gheco mueve la cabeza al ritmo del toc, con los auriculares gigantes puestos.

### Micro-misión R02-N06-P2 · El bum del punto

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Sonar al hacer un punto | pitido(parlante, 220, 0.3f) adentro del if (punto)
recompensa: xp 10, monedas 4
```

#### Escena
—Y el punto, que se note —pide {mentor}—. Más grave y más largo. Que hasta los de la puerta sepan que
alguien hizo un punto.

#### Gheco sugiere
El punto se nota con otro pitido, **más grave** (220 vueltas por segundo, la mitad que el toc) y **más
largo** (0.3 segundos). Va al principio del `if (punto)`:
```c
pitido(parlante, 220, 0.3f);
```

El robot va a jugar de a dos y va a subir la paleta rosa para que la pelota pase sin tocar ninguna
paleta: solo va a sonar el punto.

#### Desafío
Hacé que suene un pitido grave y largo (220, 0.3 segundos) cada vez que alguien hace un punto.

#### Pasos
1. Buscá el comentario `/* acá: el punto suena más grave y más largo */` (adentro del `if (punto)`).
2. Debajo, escribí `pitido(parlante, 220, 0.3f);`.
3. Tocá **Jugar**, dejá pasar una pelota y escuchá. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
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

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                /* acá: el punto suena más grave y más largo */
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
cuadros 2
tecla 2
tecla Espacio
apretar Arriba
cuadros 40
soltar Arriba
cuadros 40
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

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
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

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
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
*Bum.* Desde la puerta, alguien grita «¡punto!» sin haber visto la pantalla. {mentor} sonríe: así
sonaba la Cancha cuando estaba llena.

#### Imagen
- Un anillo de sonido grande, violeta y grave, saliendo de la máquina de la Cancha.
- En la puerta del salón, un chico grita con las manos alrededor de la boca.
- Arcadia sonríe con los ojos cerrados; Gheco, sobre la máquina, se tapa los oídos.

### Micro-misión R02-N06-P3 · Pausa

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Pausar | P: pausado = !pausado · si está en pausa, no se mueve nada
recompensa: xp 10, monedas 4
```

#### Escena
—¡A cenar! —grita alguien desde la puerta. El chico que va ganando no puede soltar los controles: si se
va, pierde. —Una pausa —dice Kira—. Las máquinas tienen que poder esperar.

#### Gheco sugiere
La variable `pausado` ya existe y arranca en `false`. Hacen falta tres cosas:
1. Jugando, la **P** le da la vuelta: `pausado = !pausado;` (`!` es «lo contrario»).
2. Lo que se mueve, solo si **no** está en pausa: la condición grande pasa a ser
   `if (estado == JUGANDO && !pausado) {`.
3. Un cartel que diga PAUSA:
```c
if (estado == JUGANDO && pausado) {
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
    SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
}
```
El robot va a apretar la P en medio del partido.

#### Desafío
Hacé que jugando, con la P, el partido se pause (nada se mueve y aparece el cartel PAUSA) y se despause.

#### Pasos
1. Buscá `/* acá: jugando, la P pausa y despausa */` y escribí `if (estado == JUGANDO && tecla == SDLK_P) { pausado = !pausado; }`.
2. Buscá `/* acá: no mover nada mientras está en pausa */` y cambiá la línea de abajo por `if (estado == JUGANDO && !pausado) {`.
3. Buscá `/* acá: el cartel de la pausa */` y escribí el `if` del cartel de la sugerencia.
4. Tocá **Jugar**, apretá la P dos veces y mirá. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
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

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                /* acá: jugando, la P pausa y despausa */
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* acá: no mover nada mientras está en pausa */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        /* acá: el cartel de la pausa */
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
cuadros 2
tecla Espacio
cuadros 20
tecla P
cuadros 30
```

#### Estado
```
buscar #ffdc00
textos
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 421, y 234, ancho 12, alto 12
textos: 0 | 0 | PAUSA
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
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

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
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
P, y la cancha se congela con un cartel de PAUSA. El chico se va a cenar tranquilo. —Vuelvo en diez
minutos —avisa—. No me toquen la paleta.

#### Imagen
- La pantalla de la Cancha congelada, con la pelota quieta en el aire y un cartel blanco en el medio (sin texto legible).
- Un chico del barrio se aleja hacia la puerta, mirando para atrás.
- Gheco hace guardia sentado sobre la paleta cian, de brazos cruzados.

### Micro-misión R02-N06-P4 · Silencio

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
criatura: fuga_texturas
carta: Silenciar | M: mudo = !mudo · en pitido: if (mudo) return;
recompensa: xp 10, monedas 4
```

#### Escena
Es de noche y {mentor} quiere seguir probando la máquina sin despertar a los vecinos de la Cancha. —Un
botón de silencio —pide—. Que se pueda jugar callado.

#### Gheco sugiere
La variable `mudo` ya existe, pero esta vez es **global**: está arriba de todo, afuera de `main`, con
`static`. Así la puede ver la función `pitido`.
1. Al principio de `pitido`, si está en silencio, se sale sin hacer nada:
```c
if (mudo) {
    return;
}
```
2. Con la **M**, en cualquier estado: `if (tecla == SDLK_M) { mudo = !mudo; }`.
3. Un aviso abajo, a la derecha, cuando está en silencio: `if (mudo)` con
   `SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");`.

El robot va a apretar la M antes de jugar: no tiene que sonar nada.

#### Desafío
Hacé que con la M la máquina se quede en silencio (ningún pitido) y vuelva a sonar, con un aviso en pantalla.

#### Pasos
1. Buscá `/* acá: si está en silencio, salir sin sonar */` (en `pitido`) y escribí el `if (mudo) { return; }`.
2. Buscá `/* acá: la M prende y apaga el sonido */` y escribí `if (tecla == SDLK_M) { mudo = !mudo; }`.
3. Buscá `/* acá: avisar que está en silencio */` y escribí el `if (mudo)` con el color y el texto «SIN SONIDO».
4. Tocá **Jugar**, apretá la M y escuchá. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    /* acá: si está en silencio, salir sin sonar */
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                /* acá: la M prende y apaga el sonido */
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        /* acá: avisar que está en silencio */
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
cuadros 2
tecla M
tecla Espacio
cuadros 120
```

#### Estado
```
sonido
textos
```

#### Salida esperada
```
── Estado ──
sonido: no
textos: 0 | 0 | SIN SONIDO
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
M, y la Cancha juega en silencio, con el cartelito en una esquina. En el estante del fondo, la Fuga de
Texturas busca sonidos olvidados que comerse… y no encuentra ninguno: cada pitido libera su memoria.
Se deshace en el aire.

#### Imagen
- La máquina de la Cancha jugando en silencio, con un cartelito violeta en la esquina de la pantalla (sin texto legible).
- En un estante del fondo, una niebla de imágenes repetidas (la Fuga de Texturas) se deshace en el aire.
- Arcadia juega tranquila; Kira, a su lado, se lleva un dedo a la boca; Gheco duerme acurrucado sobre la máquina.

## R02-N07 · Jefe: El Campeón Invicto

```meta
tipo: jefe
criatura: glitch
padre: R02-N06
precio: 10
insignia: Sello de la Cancha de las Paletas
insignia_descripcion: Despertaste al Campeón Invicto: un Pong entero, con menú, dos jugadores o contra la máquina, aceleración, sonido, pausa y un fin con revancha.
temas: juegos.ia
usa: juegos.estados, juegos.colisiones, juegos.sonido, prog.matematica-azar
```

### Crónica

Cuando los chicos se van, {mentor} camina hasta el fondo del salón y saca la lona de la máquina más vieja.
Es enorme, de madera oscura, con dos paletas gastadas y una placa de bronce sin letras. —El **Campeón
Invicto** —dice—. El Vidriero le enseñó a jugar solo, y nadie le ganó nunca. Ni yo. Cuando él se fue, se
apagó.

La máquina tose, parpadea y se enciende a medias: la paleta de la máquina tiembla, el saque sale siempre
igual, no sabe si jugar fácil o difícil. Un glitch viejo le corre por la pantalla. —Le falta lo último que le
enseñaste a la Cancha —dice {mentor}—. Y algo más: un campeón de verdad se pone serio cuando le hacés
puntos.

### Objetivos

Terminar el Pong completo, con el Campeón Invicto del otro lado: una máquina que se apura cuantos más puntos le
hacés, un saque con una inclinación al azar, la dificultad para elegir en el menú y un cartel del campeón al
terminar.

### Antes de empezar

Toda la rama R02. De R01: el azar con `SDL_rand` y centrar un texto (N07 y N10).

### Explicación

#### Un rival que se pone serio
La máquina ya sabe jugar (R02-N04). Para que sea un campeón, su **rapidez** cambia con el partido: arranca en
una base y suma 40 por cada punto que le hiciste.
```c
float rapidez = base + 40 * puntosIzq;
```
Con 0 puntos va a 200; con 3, a 320. Cuanto mejor jugás, más difícil se pone.

#### El saque al azar
Si el saque sale siempre derecho, se aprende de memoria. `SDL_rand(241)` da un número entero entre 0 y 240 (lo
usaste en R01-N10 para las gemas). Restándole 120 queda entre -120 y 120: a veces sube, a veces baja, a veces
casi derecho.

#### Fácil o difícil
Una variable `bool dificil` que se elige en el menú con dos teclas (F y D). La rapidez de base sale de ahí:
`dificil ? 280 : 200` («si es difícil, 280; si no, 200»).

#### El cartel del final, centrado
Las letras miden 8 de ancho. Un texto de `n` letras mide `n * 8`; para centrarlo en una pantalla de 640, se
empieza en `320 - n * 4`. `SDL_strlen(cartel)` cuenta las letras.

#### El juego completo
Juntando toda la rama: la cancha y la red, dos jugadores o contra la máquina, el rebote y la aceleración con
tope, el ángulo según dónde pega, el marcador grande, el respiro antes del saque, el menú, el fin a 5, la
revancha, el sonido, la pausa y el silencio.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    bool dificil = false;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_F) dificil = false;
                if (estado == MENU && tecla == SDLK_D) dificil = true;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = dificil ? 280 : 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = SDL_rand(241) - 120;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
            SDL_RenderDebugText(lapiz, 236, 340, dificil ? "DIFICIL (F O D)" : "FACIL (F O D)");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            const char *cartel = puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2";
            if (contraLaMaquina) {
                cartel = puntosIzq == 5 ? "LE GANASTE AL CAMPEON" : "EL CAMPEON SIGUE INVICTO";
            }
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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

Un rival que se adapta a cómo jugás es la base de la dificultad de casi todos los juegos. Y el Pong completo es
tu primer juego entero con todo lo que tiene un juego de verdad: lo vas a poder bajar y jugar en tu compu.

### Errores habituales

**Sumar la rapidez en cada cuadro.** `rapidez += 40;` dentro del bucle la hace crecer sin parar. Se calcula
de nuevo en cada cuadro a partir de los puntos: `base + 40 * puntosIzq`.

**`SDL_rand(120)` para los dos lados.** Da entre 0 y 119: el saque siempre baja. Para que también suba, se
resta la mitad: `SDL_rand(241) - 120`.

**Centrar sin restar.** `320 + n * 4` corre el texto a la derecha; se empieza a la izquierda del centro.

**Glitch: el saque que se repite.** Si el azar se pide una sola vez al principio y se guarda, todos los saques
salen iguales. Se pide de nuevo en cada saque.

### Micro-misión R02-N07-P1 · El campeón se pone serio

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Rapidez que crece | rapidez = base + 40 * puntosIzq
recompensa: xp 10, oro 10
```

#### Escena
La paleta del Campeón se mueve siempre igual, sin ganas. —Un campeón se pone serio cuando le hacés
puntos —dice {mentor}—. Cada punto tuyo, un poco más rápido.

#### Gheco sugiere
La paleta de la máquina se mueve `rapidez * dt` por cuadro, y hoy la rapidez es siempre 240. Ya hay
una variable `base` que vale 200: la rapidez del principio.

Para que suba 40 por cada punto que le hace el jugador 1:
```c
float rapidez = base + 40 * puntosIzq;
```
Con 0 puntos, 200; con 1, 240; con 2, 280… Se calcula de nuevo en cada cuadro, así siempre va con el
marcador.

#### Desafío
Hacé que la rapidez de la máquina sea la base (200) más 40 por cada punto que le hizo el jugador 1.

#### Pasos
1. Buscá el comentario `/* acá: cuantos más puntos le hacés, más rápido se mueve (40 más por punto) */`.
2. Cambiá la línea de abajo, `float rapidez = 240;`, por `float rapidez = base + 40 * puntosIzq;`.
3. Tocá **Jugar**, hacele un punto al Campeón y mirá cómo se apura. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = 200;
                /* acá: cuantos más puntos le hacés, más rápido se mueve (40 más por punto) */
                float rapidez = 240;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
cuadros 2
tecla Espacio
cuadros 30
```

#### Estado
```
buscar #ff3ca0
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 125, ancho 12, alto 80
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
Le hacés un punto y la paleta del Campeón se tensa; otro, y ya se mueve como un rayo. {mentor} se
muerde los labios. —Así era. Exactamente así.

#### Imagen
- La máquina del Campeón Invicto: enorme, de madera oscura, con una placa de bronce lisa; en la pantalla, la paleta rosa con líneas de velocidad.
- Kira, concentrada, juega contra la máquina; Arcadia mira detrás de ella, nerviosa.
- Gheco, sobre la máquina, se agarra de la placa de bronce.

### Micro-misión R02-N07-P2 · El saque al azar

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Azar | vy = SDL_rand(241) - 120 en cada saque
recompensa: xp 10, monedas 4
```

#### Escena
Kira descubre el truco: el saque del Campeón sale siempre derecho, al mismo lugar. Pone la paleta ahí y
gana el punto. —Así no vale —se ríe {mentor}—. Un saque tiene que sorprender.

#### Gheco sugiere
Después de cada punto la pelota sale con `vy = 0`: siempre derecho. Con el azar (lo usaste en R01-N10
para las gemas) sale distinto cada vez:
- `SDL_rand(241)` da un número entero entre 0 y 240;
- restándole 120, queda entre -120 (para arriba) y 120 (para abajo).
```c
vy = SDL_rand(241) - 120;
```
El robot va a jugar de a dos y va a dejar pasar una pelota para ver el saque.

#### Desafío
Hacé que en cada saque la pelota salga con una inclinación al azar, entre -120 y 120.

#### Pasos
1. Buscá el comentario `/* acá: el saque sale con una inclinación al azar, entre -120 y 120 */` (adentro del `if (punto)`).
2. Cambiá la línea de abajo, `vy = 0;`, por `vy = SDL_rand(241) - 120;`.
3. Tocá **Jugar** y mirá varios saques. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                /* acá: el saque sale con una inclinación al azar, entre -120 y 120 */
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
cuadros 2
tecla 2
tecla Espacio
apretar Arriba
cuadros 40
soltar Arriba
cuadros 110
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 171, y 208, ancho 12, alto 12
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = SDL_rand(241) - 120;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
El saque sale para arriba, después para abajo, después casi derecho. Kira ya no sabe dónde poner la
paleta. —Ahora sí —dice {mentor}—. Ahora es un campeón.

#### Imagen
- La pantalla del Campeón con tres recorridos posibles de la pelota saliendo del centro: uno hacia arriba, uno derecho y uno hacia abajo, como abanico.
- Kira duda con la paleta en el aire; Arcadia se ríe.
- Gheco hace un gesto de «no sé» con los brazos.

### Micro-misión R02-N07-P3 · Fácil o difícil

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
carta: Dificultad | en el menú F o D: dificil = false o true · base = dificil ? 280 : 200
recompensa: xp 10, monedas 4
```

#### Escena
Al día siguiente vuelven los chicos del barrio, y los más chiquitos pierden 5 a 0 contra el Campeón.
—Que se pueda elegir —pide Kira—. Fácil para empezar, difícil para los que se animan.

#### Gheco sugiere
La variable `dificil` ya existe (arranca en `false`). Faltan tres cosas:
1. En el menú, con la **F**, fácil; con la **D**, difícil (con los otros eventos del menú):
```c
if (estado == MENU && tecla == SDLK_F) dificil = false;
if (estado == MENU && tecla == SDLK_D) dificil = true;
```
2. La base sale de ahí: `float base = dificil ? 280 : 200;` («si es difícil, 280; si no, 200»).
3. En el menú ya se ve qué dificultad está elegida.

El robot va a apretar la D en el menú y después jugar.

#### Desafío
Hacé que en el menú se elija la dificultad (F fácil, D difícil) y que en difícil la máquina arranque a 280 en lugar de 200.

#### Pasos
1. Buscá `/* acá: en el menú, F para fácil y D para difícil */` y escribí los dos `if` de la sugerencia.
2. Buscá `/* acá: la rapidez de base según la dificultad: 280 si es difícil, 200 si es fácil */`.
3. Cambiá la línea de abajo, `float base = 200;`, por `float base = dificil ? 280 : 200;`.
4. Tocá **Jugar**, probá las dos dificultades y mirá el menú. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    bool dificil = false;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                /* acá: en el menú, F para fácil y D para difícil */
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                /* acá: la rapidez de base según la dificultad: 280 si es difícil, 200 si es fácil */
                float base = 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = SDL_rand(241) - 120;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
cuadros 2
tecla D
cuadros 2
tecla Espacio
cuadros 40
```

#### Estado
```
buscar #ff3ca0
```

#### Salida esperada
```
── Estado ──
buscar #ff3ca0: x 608, y 191, ancho 12, alto 80
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    bool dificil = false;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_F) dificil = false;
                if (estado == MENU && tecla == SDLK_D) dificil = true;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = dificil ? 280 : 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = SDL_rand(241) - 120;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
            SDL_RenderDebugText(lapiz, 236, 340, dificil ? "DIFICIL (F O D)" : "FACIL (F O D)");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
Los chiquitos juegan en fácil y le hacen un punto al Campeón: festejan como si fuera una final. Los
grandes eligen difícil y se quedan callados, concentrados.

#### Imagen
- Chicos del barrio, con abrigos cerrados, frente a la máquina del Campeón: los más chicos festejan un punto.
- En la pantalla, el menú con un renglón nuevo resaltado (sin texto legible).
- Kira explica algo a un chico chiquito; Gheco, a su lado, le levanta el pulgar.

### Micro-misión R02-N07-P4 · El cartel del campeón

```meta
lugar: La Cancha de las Paletas
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: El final | contra la máquina: «LE GANASTE AL CAMPEON» o «EL CAMPEON SIGUE INVICTO», centrado
recompensa: xp 20, monedas 5
item: Paleta del Campeón
```

#### Escena
Llega la hora: Kira contra el Campeón Invicto, en difícil, a 5 puntos. Todo el barrio mira. Pero al
terminar, la máquina dice lo mismo que una Cancha cualquiera: «gana el jugador». —Un campeón se despide
con su propio cartel —dice {mentor}.

#### Gheco sugiere
Cuando se juega **contra la máquina**, el final tiene que hablar del Campeón:
```c
const char *cartel = puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2";
if (contraLaMaquina) {
    cartel = puntosIzq == 5 ? "LE GANASTE AL CAMPEON" : "EL CAMPEON SIGUE INVICTO";
}
SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
```
- `const char *cartel` guarda un texto; se elige primero el de dos jugadores y, si es contra la
  máquina, se cambia.
- Para **centrarlo**: cada letra mide 8, así que el texto mide `SDL_strlen(cartel) * 8`; empieza la
  mitad antes del centro: `320 - SDL_strlen(cartel) * 4.0f`. (Las letras van sin tilde: la letra
  chiquita de SDL no las tiene.)

El robot va a jugar contra la máquina hasta el final.

#### Desafío
Hacé que al terminar contra la máquina aparezca, centrado, «LE GANASTE AL CAMPEON» o «EL CAMPEON SIGUE INVICTO».

#### Pasos
1. Buscá el comentario `/* acá: contra la máquina, el cartel del campeón, centrado */` y borrá la línea de abajo.
2. Escribí `const char *cartel = …` con los dos textos de dos jugadores.
3. Escribí el `if (contraLaMaquina) { … }` que cambia el cartel.
4. Dibujalo centrado con `SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);`. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    bool dificil = false;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_F) dificil = false;
                if (estado == MENU && tecla == SDLK_D) dificil = true;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = dificil ? 280 : 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = SDL_rand(241) - 120;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
            SDL_RenderDebugText(lapiz, 236, 340, dificil ? "DIFICIL (F O D)" : "FACIL (F O D)");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            /* acá: contra la máquina, el cartel del campeón, centrado */
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
cuadros 2
tecla Espacio
cuadros 3000
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: 0 | 5 | EL CAMPEON SIGUE INVICTO | R: REVANCHA
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool mudo = false;   /* true: la máquina no suena */

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    if (mudo) {
        return;
    }
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El Campeon Invicto", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    bool dificil = false;
    enum Estado estado = MENU;
    bool pausado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                if (estado == MENU && tecla == SDLK_F) dificil = false;
                if (estado == MENU && tecla == SDLK_D) dificil = true;
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (estado == JUGANDO && !pausado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                float base = dificil ? 280 : 200;
                float rapidez = base + 40 * puntosIzq;
                if (distancia < -10) der.y -= rapidez * dt;
                if (distancia > 10) der.y += rapidez * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
            der.y = SDL_clamp(der.y, 0, 480 - der.h);

            if (espera > 0) {
                espera -= dt;
            } else {
                pelota.x += vx * dt;
                pelota.y += vy * dt;
            }
            if (pelota.y < 0) {
                pelota.y = 0;
                vy = -vy;
            }
            if (pelota.y + pelota.h > 480) {
                pelota.y = 480 - pelota.h;
                vy = -vy;
            }
            if (toca(pelota, izq) && vx < 0) {
                pelota.x = izq.x + izq.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                pitido(parlante, 440, 0.05f);
            }

            bool punto = false;
            if (pelota.x + pelota.w < 0) {
                puntosDer++;
                punto = true;
            }
            if (pelota.x > 640) {
                puntosIzq++;
                punto = true;
            }
            if (punto) {
                pitido(parlante, 220, 0.3f);
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = SDL_rand(241) - 120;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
            SDL_RenderDebugText(lapiz, 236, 340, dificil ? "DIFICIL (F O D)" : "FACIL (F O D)");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            const char *cartel = puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2";
            if (contraLaMaquina) {
                cartel = puntosIzq == 5 ? "LE GANASTE AL CAMPEON" : "EL CAMPEON SIGUE INVICTO";
            }
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
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
Cinco a cuatro. La pantalla del Campeón se queda quieta y, por primera vez en treinta años, dice **LE
GANASTE AL CAMPEON**. El salón entero grita. La máquina zumba, la placa de bronce se calienta y en la
pantalla aparece un dibujo nuevo: **otro pedazo del mapa del Vidriero**. Este muestra un muro de
ladrillos de colores, altísimo.

{mentor} se seca los ojos con la manga. Del costado de la máquina se abre una tapita y cae una paleta
vieja, de madera, gastada en la punta: la **Paleta del Campeón**. —Te la ganaste —dice—. El Muro de
Ladrillos nos espera.

#### Imagen
- La máquina del Campeón Invicto encendida a pleno, con luces en los costados; en la pantalla, un pedazo de mapa antiguo con un muro altísimo de ladrillos de colores.
- Una paleta vieja de madera, gastada en la punta, cae de una tapita al costado de la máquina.
- Kira con los brazos en alto; Arcadia se seca los ojos con la manga; Gheco abraza la placa de bronce; detrás, los chicos del barrio festejan.
