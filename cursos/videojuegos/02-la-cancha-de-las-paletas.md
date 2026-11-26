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
