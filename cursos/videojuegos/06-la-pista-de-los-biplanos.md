# RAMA R06 · La Pista de los Biplanos: naves

```meta
tipo: tronco
posicion: 6
```

## R06-N01 · El biplano y el cielo

```meta
tipo: tema
criatura: fantasma_fotograma
padre: R05-N06
precio: 10
temas: juegos.fisica
usa: juegos.entrada, col.arrays, juegos.bucle
```

### Crónica

El sexto pedazo de mapa lleva a las afueras de Ciudad Arcadia: una pista larga de pasto, un hangar de madera y,
colgados del techo, biplanos de juguete con las alas de tela. En el medio del hangar hay una máquina alta con un
volante de avión en lugar de botones. —La Pista de los Biplanos —dice {mentor}, y sopla el polvo del volante—. Acá
se vuela: vos manejás el avión, y el cielo pasa por debajo. En la pantalla, unas nubes se mueven a saltitos, unas
veces rápido y otras lento: el **Fantasma del Fotograma** se metió en el cielo.

### Objetivos

Mover el **biplano** con las flechas mantenidas (en las cuatro direcciones), que **no se salga** de la ventana, y
hacer que el **cielo se mueva**: nubes en un arreglo que bajan y, cuando salen por abajo, vuelven a aparecer
arriba en otro lugar.

### Antes de empezar

Toda la escalera hasta acá. De R02: las paletas con las teclas mantenidas y `SDL_clamp` (N01). De R01: el delta
time (N04).

### Explicación

#### Qué es un juego de naves
Un avión que vuela hacia arriba de la pantalla, dispara y esquiva a los enemigos que bajan. En realidad el avión
casi no avanza: lo que se mueve es **el cielo**, que pasa hacia abajo, y eso hace parecer que el avión vuela.

#### Moverse en cuatro direcciones
Como las paletas del Pong, pero con las cuatro flechas: `SDL_GetKeyboardState` dice qué teclas están apretadas
**ahora**, y cada una mueve el avión `velocidad * dt` píxeles. Si se aprietan dos (arriba y a la derecha), se
mueve en diagonal.

#### No salirse
`SDL_clamp(valor, mínimo, máximo)` deja el valor adentro de los límites: la `x` entre 0 y `640 - avion.w`, la `y`
entre 0 y `480 - avion.h`.

#### El cielo que pasa
Las nubes están en dos arreglos, `nx` y `ny`. En cada cuadro, todas bajan `80 * dt`. Cuando una pasa el borde de
abajo, se la sube arriba de todo (un poquito afuera, en -30) y se le da otra `x` al azar: así el cielo no se
termina nunca, con las mismas seis nubes.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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

El fondo que se mueve es la base de todos los juegos que avanzan: naves, autitos de carrera, corredores sin fin.
Reusar las mismas nubes en lugar de crear nuevas es un truco que vas a usar con balas, enemigos y partículas.

### Errores habituales

**Mover con los eventos.** `SDL_EVENT_KEY_DOWN` llega una vez por apretada: el avión saltaría y se quedaría quieto.
Para moverse mientras la tecla está apretada, `SDL_GetKeyboardState`.

**Olvidarse del `dt`.** Sin multiplicar por `dt`, el avión vuela distinto en cada compu: es el Fantasma del
Fotograma.

**Volver la nube a 0.** Si vuelve en `y = 0`, aparece de golpe, entera, arriba de la pantalla. En -30 entra de a poco.

**Clamp con `640`.** La `x` es la esquina izquierda del avión: el máximo es `640 - avion.w`, si no, se sale el ala.

### Micro-misión R06-N01-P1 · Despegar

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Flechas mantenidas | teclas = SDL_GetKeyboardState(NULL) · si teclas[SDL_SCANCODE_LEFT]: avion.x -= velocidad * dt (y las otras tres)
recompensa: xp 10, oro 10
```

#### Escena
{mentor} enciende la máquina: en la pantalla hay un cielo azul y un biplano amarillo, quieto en el medio, con
la hélice girando. Kira agarra el volante y lo mueve para todos lados. El avión ni se entera.

#### Gheco sugiere
Mientras una flecha está apretada, el avión se mueve `velocidad * dt` píxeles para ese lado. Como las paletas:
```c
const bool *teclas = SDL_GetKeyboardState(NULL);   /* qué teclas están apretadas ahora */
if (teclas[SDL_SCANCODE_LEFT]) {
    avion.x -= velocidad * dt;
}
if (teclas[SDL_SCANCODE_RIGHT]) {
    avion.x += velocidad * dt;
}
if (teclas[SDL_SCANCODE_UP]) {
    avion.y -= velocidad * dt;     /* para arriba, la y baja */
}
if (teclas[SDL_SCANCODE_DOWN]) {
    avion.y += velocidad * dt;
}
```
Son cuatro `if` separados (no `else`): así, con dos flechas a la vez, va en diagonal. El robot va a mantener
apretada la flecha de la izquierda medio segundo.

#### Desafío
Hacé que las cuatro flechas, mientras están apretadas, muevan el biplano.

#### Pasos
1. Buscá `/* acá: las flechas, mientras están apretadas, mueven el biplano */`.
2. Debajo, escribí `teclas` y los cuatro `if` de la sugerencia.
3. Tocá **Jugar**, hacé clic en el juego y volá con las flechas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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

        /* acá: las flechas, mientras están apretadas, mueven el biplano */

        for (int n = 0; n < NUBES; n++) {
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
buscar #ffc83c
```

#### Salida esperada
```
── Estado ──
buscar #ffc83c: x 152, y 400, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }

        for (int n = 0; n < NUBES; n++) {
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
El biplano se inclina y vuela a la izquierda, después arriba, después en diagonal. Kira se ríe: el volante de
la máquina se mueve solo con sus flechas. Gheco, colgado de un biplano de juguete del techo, hace *brrrr*.

#### Imagen
- La pantalla de la máquina con un cielo azul y un biplano amarillo volando en diagonal, con rayitas de movimiento.
- Kira maneja un volante de avión enorme en la máquina, feliz; Arcadia sopla el polvo del volante.
- Gheco cuelga de un biplano de juguete con alas de tela, colgado del techo del hangar, haciendo brrrr.

### Micro-misión R06-N01-P2 · Sin salirse del cielo

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Tope | avion.x = SDL_clamp(avion.x, 0, 640 - avion.w) · avion.y = SDL_clamp(avion.y, 0, 480 - avion.h)
recompensa: xp 10, monedas 4
```

#### Escena
Kira vuela a la izquierda… y el biplano se va de la pantalla y no vuelve. —El cielo de la máquina tiene bordes
—dice {mentor}—. El avión no se puede ir.

#### Gheco sugiere
`SDL_clamp(valor, mínimo, máximo)` deja el valor entre los dos límites. Después de mover:
```c
avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);   /* ni más a la izquierda que 0, ni más a la derecha que 600 */
avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);
```
La `x` es la esquina izquierda del avión: para que el ala derecha no se salga, el máximo es `640 - avion.w`.
El robot va a mantener la flecha de la izquierda dos segundos.

#### Desafío
Hacé que el biplano no se salga de la ventana por ningún borde.

#### Pasos
1. Buscá `/* acá: que el biplano no se salga de la ventana */`.
2. Debajo, escribí los dos `SDL_clamp` de la sugerencia.
3. Tocá **Jugar** y llevá el avión contra un borde. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        /* acá: que el biplano no se salga de la ventana */

        for (int n = 0; n < NUBES; n++) {
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 120
soltar Izquierda
cuadros 2
```

#### Estado
```
buscar #ffc83c
```

#### Salida esperada
```
── Estado ──
buscar #ffc83c: x 0, y 400, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
El biplano llega al borde y se queda ahí, apoyado en el aire, como contra un vidrio. Kira lo pasea por los
cuatro costados: no se escapa por ninguno.

#### Imagen
- La pantalla de la máquina con el biplano amarillo pegado al borde izquierdo del cielo, sin salirse.
- Kira gira el volante hasta el tope; Arcadia asiente.
- Gheco, colgado del techo, se balancea de un biplano de juguete a otro.

### Micro-misión R06-N01-P3 · El cielo pasa

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Fondo | para cada nube n: ny[n] += 80 * dt
recompensa: xp 10, monedas 4
```

#### Escena
El biplano vuela, pero las nubes están clavadas en el cielo, como pintadas: parece que el avión no avanza.
Las nubes de la pantalla de al lado, en cambio, saltan rápido y lento. —El Fantasma del Fotograma —dice
{mentor}—. Las nubes tienen que bajar, siempre igual, con el `dt`.

#### Gheco sugiere
Ya está el `for` que pasa por las seis nubes. Adentro, que cada una baje:
```c
ny[n] += 80 * dt;     /* 80 píxeles por segundo, hacia abajo */
```
El avión casi no se mueve, pero las nubes pasan por debajo: eso hace parecer que vuela hacia arriba. El robot
va a esperar un segundo.

#### Desafío
Hacé que las nubes bajen 80 píxeles por segundo, para que parezca que el biplano vuela.

#### Pasos
1. Buscá `/* acá: cada nube baja, así parece que el biplano avanza */` (adentro del `for` de las nubes).
2. Debajo, escribí la línea de la sugerencia.
3. Tocá **Jugar**: las nubes tienen que pasar. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            /* acá: cada nube baja, así parece que el biplano avanza */
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
buscar #c8dcff
```

#### Salida esperada
```
── Estado ──
buscar #c8dcff: x 60, y 120, ancho 560, alto 360
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Las nubes empiezan a pasar, parejitas, y de golpe el biplano parece volar de verdad. El Fantasma del Fotograma
trata de apurar una nube, pero el `dt` no lo deja, y se va volando, ofendido.

#### Imagen
- La pantalla de la máquina con el biplano amarillo y nubes blancas pasando hacia abajo, con rayitas de velocidad.
- Un fantasma redondo y translúcido, borroso, se aleja volando entre las nubes de la pantalla, ofendido.
- Kira maneja sonriendo; Arcadia mira por la puerta del hangar la pista de pasto; Gheco siente el viento en la cara.

### Micro-misión R06-N01-P4 · Un cielo sin fin

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Volver arriba | si ny[n] > 480: ny[n] = -30 · nx[n] = SDL_rand(560)
recompensa: xp 10, monedas 4
```

#### Escena
Las nubes pasan… y se terminan. Al rato el cielo queda vacío, azul y aburrido. —No hacen falta más nubes
—dice {mentor}—. Las que salen por abajo, que vuelvan a entrar por arriba.

#### Gheco sugiere
Adentro del mismo `for`, después de bajarla:
```c
if (ny[n] > 480) {          /* ¿ya salió por abajo? */
    ny[n] = -30;            /* vuelve arriba, un poquito afuera */
    nx[n] = SDL_rand(560);  /* en otro lugar, para que no se note */
}
```
- En -30 la nube (que mide 30 de alto) queda justo arriba del borde y entra de a poco.
- `SDL_rand(560)` da un número del 0 al 559: la nube mide 80, así que nunca se sale por la derecha.

El robot va a esperar cinco segundos.

#### Desafío
Hacé que la nube que sale por abajo vuelva a entrar por arriba, en otro lugar.

#### Pasos
1. Buscá `/* acá: si una nube sale por abajo, vuelve a aparecer arriba, en otro lugar */`.
2. Debajo, escribí el `if` de la sugerencia.
3. Tocá **Jugar** y esperá: el cielo no se tiene que vaciar. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            /* acá: si una nube sale por abajo, vuelve a aparecer arriba, en otro lugar */
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
buscar #c8dcff
```

#### Salida esperada
```
── Estado ──
buscar #c8dcff: x 39, y 16, ancho 438, alto 461
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Las nubes que se van por abajo vuelven a asomar por arriba, cada vez en otro lugar. El cielo no se termina
nunca. Gheco se queda mirando, hipnotizado, y cuenta: son solo seis.

#### Imagen
- La pantalla de la máquina con nubes entrando por arriba y saliendo por abajo, con flechas curvas que las unen.
- Kira vuela tranquila; Arcadia sonríe, con los brazos cruzados.
- Gheco cuenta seis nubes con los dedos, hipnotizado, arriba de la máquina.

## R06-N02 · Las balas

```meta
tipo: tema
criatura: fuga_texturas
padre: R06-N01
precio: 10
temas: col.registros
usa: col.arrays, juegos.entrada, prog.bucles
```

### Crónica

Kira vuela por el cielo de la máquina, pero en el panel hay un botón rojo que dice, en letras gastadas, algo que
nadie se acuerda. Lo aprieta: nada. —Los biplanos de la máquina disparaban burbujas de luz —dice {mentor}—. Pero
no infinitas: la máquina tenía lugar para cinco. Si cada disparo fuera una burbuja nueva, la memoria se llenaría.
Desde atrás del panel, algo se infla como un globo: la **Fuga de Texturas**, que vive de lo que nadie libera.

### Objetivos

Guardar las balas en un **arreglo de structs** (cada una con su `x`, su `y` y si está **viva**), disparar buscando
una **libre**, hacerlas subir, **apagarlas** cuando salen de la pantalla para poder reusarlas y mostrar cuántas
quedan en el cargador.

### Antes de empezar

El nodo anterior. De R03: el arreglo de `struct Ladrillo` con su `viva` (N02) y el `break` (N02).

### Explicación

#### Muchas cosas iguales: un arreglo de structs
Una bala tiene tres datos: `x`, `y` y `viva` (si está volando). Se juntan en un `struct Bala`, como los ladrillos del
Arkanoid, y se arma un arreglo de cinco: `struct Bala balas[BALAS]`. Con `= { 0 }` todas empiezan en cero: guardadas,
sin volar.

#### Disparar: buscar una libre
No se crea una bala nueva: se busca en el arreglo una que **no** esté viva (`!balas[i].viva`), se la pone en la punta
del biplano y se la marca viva. El `break` corta el `for` apenas encuentra una: si no, con una apretada saldrían las
cinco juntas. Si están todas volando, no sale nada.

#### Volar y apagarse
En cada cuadro, cada bala viva sube `500 * dt`. Cuando pasa el borde de arriba, se marca `viva = false`: vuelve al
cargador, lista para otro disparo. Es la misma idea que las nubes que vuelven arriba: **reusar** en lugar de crear.

#### El cargador
Un cuadradito naranja abajo a la izquierda por cada bala libre. Se ve cómo se gastan al disparar y cómo vuelven
cuando salen de la pantalla.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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

Un arreglo de structs con un `viva` (lo que se llama una «pileta» de objetos) se usa para todo lo que aparece y
desaparece muchas veces: balas, enemigos, explosiones, chispas, monedas. Es rápido y la memoria no crece nunca.

### Errores habituales

**Olvidarse del `break`.** Con una apretada se disparan todas las balas libres juntas, encimadas.

**Mover las balas muertas.** Si se mueve sin mirar `viva`, las guardadas también suben y, al dispararlas, aparecen
lejos.

**Fuga de Texturas: no apagarlas.** Si la bala que sale de la pantalla sigue viva, después de cinco disparos el
cargador queda vacío para siempre: las balas siguen «volando» afuera, donde nadie las ve.

**`balas[i] = 0`.** Un struct no se pone en cero así: se cambia el campo, `balas[i].viva = false`.

### Micro-misión R06-N02-P1 · Fuego

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Disparar | espacio: for i hasta BALAS · si !balas[i].viva: x = avion.x + 18, y = avion.y - 10, viva = true · break
recompensa: xp 10, oro 10
```

#### Escena
Kira aprieta el espacio y el botón rojo del panel se enciende, pero del biplano no sale nada. —Hay cinco
burbujas guardadas —dice {mentor}—. Al disparar, buscás una que esté libre y la soltás.

#### Gheco sugiere
Ya está el arreglo `balas` (cinco `struct Bala`, todas guardadas). Con el espacio, se busca la primera libre:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
    for (int i = 0; i < BALAS; i++) {
        if (!balas[i].viva) {               /* ¿está guardada? */
            balas[i].x = avion.x + 18;      /* en la punta del biplano */
            balas[i].y = avion.y - 10;
            balas[i].viva = true;           /* ¡a volar! */
            break;                          /* una sola por apretada */
        }
    }
}
```
`balas[i].x` es el campo `x` de la bala número `i`. Las balas vivas ya se dibujan. El robot va a apretar el
espacio.

#### Desafío
Hacé que con el espacio salga una bala libre desde la punta del biplano.

#### Pasos
1. Buscá `/* acá: con el espacio, buscar una bala libre y dispararla desde el biplano */` (en los eventos).
2. Debajo, escribí el `if` del espacio con el `for` de la sugerencia.
3. Tocá **Jugar**, hacé clic en el juego y apretá el espacio. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con el espacio, buscar una bala libre y dispararla desde el biplano */
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 2
```

#### Estado
```
buscar #ffff78
```

#### Salida esperada
```
── Estado ──
buscar #ffff78: x 318, y 390, ancho 4, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Kira aprieta el espacio y en la punta del biplano aparece una burbuja de luz amarilla. Se queda ahí, flotando,
esperando. —Ya salió —dice Arcadia—. Ahora tiene que volar.

#### Imagen
- La pantalla de la máquina con el biplano amarillo y una burbuja de luz amarilla en la punta.
- Kira aprieta un botón rojo grande del panel de la máquina; Arcadia señala la pantalla.
- Gheco, sobre la máquina, se tapa las orejas esperando un estruendo.

### Micro-misión R06-N02-P2 · Para arriba

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Volar | para cada bala viva: balas[i].y -= 500 * dt
recompensa: xp 10, monedas 4
```

#### Escena
Las burbujas salen del biplano y se quedan flotando, quietas, donde salieron. —Una burbuja de luz es rápida
—dice {mentor}—. Mucho más que el avión.

#### Gheco sugiere
Ya está el `for` que pasa por las balas y el `if` que mira solo las vivas. Adentro, que suban:
```c
balas[i].y -= 500 * dt;   /* 500 píxeles por segundo, hacia arriba */
```
Solo las vivas se mueven: las guardadas esperan en el cargador. El robot va a disparar y esperar medio
segundo.

#### Desafío
Hacé que las balas vivas suban 500 píxeles por segundo.

#### Pasos
1. Buscá `/* acá: la bala sube rápido */` (adentro del `if (balas[i].viva)`).
2. Debajo, escribí la línea de la sugerencia.
3. Tocá **Jugar** y dispará. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                /* acá: la bala sube rápido */
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 30
```

#### Estado
```
buscar #ffff78
```

#### Salida esperada
```
── Estado ──
buscar #ffff78: x 318, y 135, ancho 4, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
*¡Fiuuu!* La burbuja sale disparada hacia arriba y se pierde en el cielo. Kira dispara otra, y otra. Gheco
trata de seguirlas con la vista y se marea.

#### Imagen
- La pantalla de la máquina con el biplano amarillo disparando burbujas de luz que suben rápido, con estelas.
- Kira dispara con el botón rojo, entusiasmada; Arcadia sonríe.
- Gheco sigue las burbujas con la vista y se marea, sentado arriba de la máquina.

### Micro-misión R06-N02-P3 · El cargador no se vacía

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
criatura: fuga_texturas
carta: Reusar | si balas[i].y < -10: balas[i].viva = false (vuelve a estar libre)
recompensa: xp 10, monedas 4
```

#### Escena
Kira dispara cinco veces… y la sexta, nada. Ni la séptima. Las cinco burbujas se fueron por arriba, pero la
máquina cree que siguen volando. La Fuga de Texturas se infla, feliz, detrás del panel.

#### Gheco sugiere
Cuando una bala sale por arriba, hay que **guardarla** otra vez, así queda libre para otro disparo. Adentro del
mismo `if`, después de moverla:
```c
if (balas[i].y < -10) {     /* la bala mide 10: ya salió entera */
    balas[i].viva = false;   /* vuelve al cargador */
}
```
El robot va a disparar cinco veces, esperar a que salgan, y disparar una sexta.

#### Desafío
Hacé que la bala que sale por arriba se apague y quede libre para otro disparo.

#### Pasos
1. Buscá `/* acá: si salió por arriba, se apaga y queda libre para otro disparo */`.
2. Debajo, escribí el `if` de la sugerencia.
3. Tocá **Jugar** y dispará muchas veces. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                /* acá: si salió por arriba, se apaga y queda libre para otro disparo */
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 60
tecla Espacio
cuadros 60
tecla Espacio
cuadros 60
tecla Espacio
cuadros 60
tecla Espacio
cuadros 60
tecla Espacio
cuadros 2
```

#### Estado
```
buscar #ffff78
```

#### Salida esperada
```
── Estado ──
buscar #ffff78: x 318, y 365, ancho 4, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Las burbujas que salen por arriba vuelven al cargador, y Kira puede disparar todo lo que quiera. La Fuga de
Texturas se desinfla con un silbido y se va volando por la puerta del hangar.

#### Imagen
- La pantalla de la máquina con el biplano disparando una fila larga de burbujas de luz que nunca se acaban.
- Una criatura como una nube que se desinfla con un silbido sale volando por la puerta del hangar.
- Kira dispara sin parar; Arcadia aplaude; Gheco persigue la nube desinflada.

### Micro-misión R06-N02-P4 · El cargador

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Contar libres | for i hasta BALAS · si !balas[i].viva: un cuadradito naranja en (10 + i * 12, 456)
recompensa: xp 10, monedas 4
```

#### Escena
—Los pilotos de la máquina sabían cuántas burbujas les quedaban —dice {mentor}—. Abajo, en un costado,
había una fila de lucecitas: una por cada burbuja guardada.

#### Gheco sugiere
Un cuadradito naranja por cada bala **libre**, abajo a la izquierda:
```c
SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
for (int i = 0; i < BALAS; i++) {
    if (!balas[i].viva) {                           /* guardada: se muestra */
        SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
        SDL_RenderFillRect(lapiz, &libre);
    }
}
```
`10 + i * 12`: cada lucecita, 12 píxeles más a la derecha que la anterior. Al disparar se apaga una; cuando la
bala sale de la pantalla, vuelve. El robot va a disparar una vez.

#### Desafío
Mostrá abajo a la izquierda un cuadradito naranja por cada bala libre.

#### Pasos
1. Buscá `/* acá: el cargador: un cuadradito naranja abajo por cada bala libre */`.
2. Debajo, escribí el color y el `for` de la sugerencia.
3. Tocá **Jugar** y dispará: mirá cómo se apagan y vuelven. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        /* acá: el cargador: un cuadradito naranja abajo por cada bala libre */
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 2
```

#### Estado
```
buscar #ffa03c
```

#### Salida esperada
```
── Estado ──
buscar #ffa03c: x 22, y 456, ancho 44, alto 14
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Abajo a la izquierda aparecen cinco lucecitas naranjas. Kira dispara dos: quedan tres. Las burbujas salen por
arriba y, *plin, plin*, las lucecitas vuelven. —Cinco que van y vuelven —dice Kira—. Nunca se terminan.

#### Imagen
- La pantalla de la máquina con el biplano y, abajo a la izquierda, una fila de lucecitas naranjas.
- Kira cuenta las lucecitas con el dedo; Arcadia asiente.
- Gheco sostiene una lucecita naranja de verdad, como una linterna, arriba de la máquina.

## R06-N03 · Los enemigos

```meta
tipo: tema
criatura: atraviesaparedes
padre: R06-N02
precio: 10
temas: juegos.colisiones
usa: col.registros, col.arrays, prog.matematica-azar
```

### Crónica

El biplano dispara burbujas a un cielo vacío. —Falta a qué apuntarle —dice {mentor}, y abre un cajón lleno de
globos rojos de juguete, desinflados—. En la máquina bajaban globos, uno por segundo, y había que reventarlos antes
de que se escaparan. Nadie se lastima: son globos. Pero en la pantalla las burbujas atraviesan los globos sin
reventarlos, y desde adentro del vidrio se ríe el **Atraviesaparedes**.

### Objetivos

Hacer **aparecer** un enemigo por segundo con un temporizador, en una pileta de structs como las balas, que **bajen**
y se apaguen al salir, que las **balas los revienten** (dos `for`, uno adentro del otro, y la colisión de
rectángulos) y mostrar los **puntos**.

### Antes de empezar

El nodo anterior. De R01: la colisión entre rectángulos (N06). De R03: el temporizador (N07).

### Explicación

#### Los enemigos: otra pileta
Igual que las balas: un `struct Enemigo` con `x`, `y` y `vivo`, y un arreglo de ocho. Un temporizador,
`relojEnemigo`, junta el tiempo y cada un segundo busca un enemigo libre y lo pone arriba de todo, en una `x` al
azar. Si los ocho están en el cielo, ese segundo no sale ninguno.

#### Bajar y escaparse
Cada enemigo vivo baja `120 * dt`. Si pasa el borde de abajo, se apaga: se escapó y queda libre para salir otra vez.

#### Cada bala contra cada enemigo
Para saber si alguna bala tocó algún enemigo hay que probar **todas las parejas**: un `for` por las balas y, adentro,
otro por los enemigos. Con 5 balas y 8 enemigos son 40 preguntas por cuadro, y la compu las hace en un instante. Para
cada pareja se arman las dos cajitas y se pregunta con `SDL_HasRectIntersectionFloat`, pero solo si **los dos están
vivos** (si no, una bala guardada podría reventar un globo).

#### Reventar
Si se tocan, los dos se apagan (vuelven a sus piletas) y se suman 10 puntos.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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

«Cada uno contra cada uno» con dos `for` es la manera más simple de chocar dos grupos de cosas: disparos contra
enemigos, el jugador contra las monedas, los fantasmas contra el Pac-Man.

### Errores habituales

**No mirar si están vivos.** Una bala guardada (con su `x` e `y` viejas) puede «reventar» un globo que pasa por
ahí: es el Atraviesaparedes al revés.

**Apagar solo la bala.** Si el enemigo no se apaga, la bala siguiente lo vuelve a reventar y suma puntos sin parar.

**El `break` al soltar el enemigo.** Sin él, en un segundo salen los ocho juntos, encimados.

**Atraviesaparedes: balas muy rápidas.** Si la bala avanzara más que lo que mide el globo en un solo cuadro, podría
saltarlo sin tocarlo. A 500 por segundo avanza 8 píxeles por cuadro y el globo mide 30: no pasa.

### Micro-misión R06-N03-P1 · Globos a la vista

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Temporizador | relojEnemigo += dt · a 1 s: buscar un enemigo libre · x = SDL_rand(600), y = 0, vivo = true · break
recompensa: xp 10, oro 10
```

#### Escena
{mentor} infla un globo rojo y lo suelta: sube hasta el techo del hangar. En la pantalla, en cambio, el cielo
sigue vacío. —En la máquina salía uno por segundo —dice—, cada vez en otro lugar.

#### Gheco sugiere
Ya están el arreglo `enemigos` (ocho, guardados) y `relojEnemigo`. Cada un segundo, buscar uno libre y
soltarlo arriba, en una `x` al azar:
```c
relojEnemigo += dt;
if (relojEnemigo >= 1) {
    relojEnemigo -= 1;
    for (int e = 0; e < ENEMIGOS; e++) {
        if (!enemigos[e].vivo) {
            enemigos[e].x = SDL_rand(600);    /* el globo mide 40: de 0 a 599 */
            enemigos[e].y = 0;                /* arriba de todo */
            enemigos[e].vivo = true;
            break;                            /* uno solo por segundo */
        }
    }
}
```
Es lo mismo que disparar una bala, pero lo dispara el reloj. Los vivos ya se dibujan. El robot va a esperar
un segundo y un poquito.

#### Desafío
Hacé que cada un segundo salga un enemigo arriba, en una x al azar.

#### Pasos
1. Buscá `/* acá: cada un segundo, sale un enemigo arriba, en una x al azar */`.
2. Debajo, escribí el temporizador con el `for` que busca uno libre.
3. Tocá **Jugar** y esperá: tienen que ir apareciendo globos arriba. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        /* acá: cada un segundo, sale un enemigo arriba, en una x al azar */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
buscar #dc3c3c
```

#### Salida esperada
```
── Estado ──
buscar #dc3c3c: x 204, y 0, ancho 40, alto 30
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Arriba de la pantalla aparece un globo rojo, después otro, y otro, cada uno en un lugar distinto. Se quedan
ahí, colgados del borde. Gheco infla un globo de verdad y casi sale volando con él.

#### Imagen
- La pantalla de la máquina con el biplano amarillo abajo y varios globos rojos arriba, en distintos lugares.
- Arcadia infla un globo rojo de juguete; Kira mira la pantalla.
- Gheco, agarrado de un globo rojo, se eleva un poquito sobre la máquina, asustado y feliz.

### Micro-misión R06-N03-P2 · Bajan y se escapan

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Bajar | enemigos[e].y += 120 * dt · si y > 480: vivo = false
recompensa: xp 10, monedas 4
```

#### Escena
Los globos se amontonan arriba, quietos, hasta que salen los ocho y no sale ninguno más. —Tienen que bajar
—dice {mentor}—, despacito. Y si llegan abajo, se escapan.

#### Gheco sugiere
Ya está el `for` que mira los enemigos vivos. Adentro, que bajen y, si salen por abajo, se apaguen:
```c
enemigos[e].y += 120 * dt;       /* 120 píxeles por segundo */
if (enemigos[e].y > 480) {       /* ¿se escapó por abajo? */
    enemigos[e].vivo = false;    /* vuelve a la pileta */
}
```
Al apagarse, el reloj lo puede volver a soltar arriba. El robot va a esperar tres segundos.

#### Desafío
Hacé que los enemigos bajen 120 píxeles por segundo y se apaguen al salir por abajo.

#### Pasos
1. Buscá `/* acá: el enemigo baja y, si sale por abajo, se apaga */`.
2. Debajo, escribí las líneas de la sugerencia.
3. Tocá **Jugar** y mirá bajar los globos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                /* acá: el enemigo baja y, si sale por abajo, se apaga */
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 180
```

#### Estado
```
buscar #dc3c3c
```

#### Salida esperada
```
── Estado ──
buscar #dc3c3c: x 133, y 6, ancho 169, alto 271
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Los globos bajan despacito, como hojas, y los que llegan abajo se escapan por el borde. Arriba siempre sale otro.
Kira ya tiene el dedo en el botón rojo.

#### Imagen
- La pantalla de la máquina con globos rojos bajando despacio hacia el biplano amarillo, con rayitas de movimiento.
- Kira, con el dedo listo sobre el botón rojo del panel; Arcadia sonríe.
- Gheco mira bajar un globo de verdad que se le escapó a Arcadia en el hangar.

### Micro-misión R06-N03-P3 · ¡Pum!

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Colisión | for cada bala · for cada enemigo · si los dos vivos y SDL_HasRectIntersectionFloat: apagar los dos · puntos += 10
recompensa: xp 10, monedas 4
```

#### Escena
Kira apunta, dispara… y la burbuja atraviesa el globo como si fuera de humo. Otra, y otra. Dentro del vidrio de
la pantalla, el Atraviesaparedes se ríe con la boca llena de burbujas.

#### Gheco sugiere
Cada bala contra cada enemigo: dos `for`, uno adentro del otro. Para cada pareja, las dos cajitas y la pregunta:
```c
for (int i = 0; i < BALAS; i++) {
    for (int e = 0; e < ENEMIGOS; e++) {
        SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
        SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
        if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
            balas[i].viva = false;     /* la burbuja se gasta */
            enemigos[e].vivo = false;  /* y el globo revienta */
            puntos += 10;
        }
    }
}
```
Solo cuenta si **los dos** están vivos. El robot va a llevar el biplano debajo del primer globo y disparar.

#### Desafío
Hacé que una bala que toca un enemigo apague a los dos y sume 10 puntos.

#### Pasos
1. Buscá `/* acá: si una bala toca un enemigo, los dos se apagan y suman 10 puntos */`.
2. Debajo, escribí los dos `for` con la colisión de la sugerencia.
3. Tocá **Jugar**, apuntá a un globo y dispará. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        /* acá: si una bala toca un enemigo, los dos se apagan y suman 10 puntos */

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 45
tecla Espacio
cuadros 45
```

#### Estado
```
buscar #dc3c3c
```

#### Salida esperada
```
── Estado ──
buscar #dc3c3c: no está
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
*¡Pum!* La burbuja toca el globo y los dos desaparecen en una lluvia de chispitas. Kira revienta otro, y otro.
El Atraviesaparedes se queda sin lugar por donde pasar y se escurre fuera del vidrio.

#### Imagen
- La pantalla de la máquina con una burbuja de luz reventando un globo rojo en una lluvia de chispitas.
- Una criatura de gelatina translúcida se escurre fuera del vidrio de la pantalla, derrotada.
- Kira festeja con el puño; Arcadia aplaude; Gheco se tapa las orejas por el ¡pum!

### Micro-misión R06-N03-P4 · Los puntos

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Marcador | SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos)
recompensa: xp 10, monedas 4
```

#### Escena
Los globos revientan uno tras otro, pero la máquina no cuenta nada. —Diez puntos por globo —dice {mentor}—.
Y que se vea arriba, a la izquierda, como en todas las máquinas.

#### Gheco sugiere
Los puntos ya se suman al reventar. Falta mostrarlos, al final del dibujo:
```c
SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
```
`%d` se reemplaza por el número de `puntos`. El robot va a esperar un ratito.

#### Desafío
Mostrá los puntos arriba a la izquierda.

#### Pasos
1. Buscá `/* acá: mostrar los puntos arriba a la izquierda */`.
2. Debajo, escribí el color y el texto de la sugerencia.
3. Tocá **Jugar** y reventá globos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        /* acá: mostrar los puntos arriba a la izquierda */
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
cuadros 10
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

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Arriba a la izquierda aparece **PUNTOS 0**, y con cada globo sube de a diez. Kira ya va por cien. Gheco anota
el récord con la cola en el polvo de la máquina.

#### Imagen
- La pantalla de la máquina con globos rojos, el biplano y un marcador blanco arriba a la izquierda (sin letras legibles).
- Kira juega concentrada; Arcadia mira el marcador, contenta.
- Gheco escribe con la cola en el polvo de la máquina.

## R06-N04 · Oleadas

```meta
tipo: tema
criatura: glitch
padre: R06-N03
precio: 10
temas: juegos.ia
usa: col.registros, prog.matematica-azar, juegos.bucle
```

### Crónica

Kira revienta globos sin parar, y se aburre: todos bajan derecho, de a uno, siempre igual. —En la máquina venían
en **oleadas** —dice {mentor}—: cinco, un respiro, cinco más rápidos. Y bailaban de costado. Y los más pícaros
tiraban burbujitas de agua. En la pantalla, un globo parpadea y aparece corrido, medio adentro de otro: un gatito
pixelado se ríe en un rincón. Es el **Glitch**.

### Objetivos

Hacer que los enemigos se muevan en **zigzag** con el seno, que vengan en **oleadas** de cinco con un respiro entre
una y otra, que cada oleada sea **más rápida** y que los enemigos **tiren** (otra pileta de balas, que bajan).

### Antes de empezar

El nodo anterior. De R01: el pitido con el seno (N09). De R02: la pelota que acelera (N03).

### Explicación

#### El zigzag: el seno
`SDL_sinf(número)` da un valor entre -1 y 1 que sube y baja, una y otra vez, a medida que el número crece: es una ola.
Si a la `x` del enemigo se le suma `SDL_sinf(y / 40) * 120 * dt`, mientras baja va de un lado al otro, suave. El `40`
dice qué tan largas son las curvas, y el `120`, qué tan anchas.

#### Oleadas
`salidos` cuenta cuántos enemigos de la oleada ya salieron. Mientras sean menos de cinco, corre el reloj de los
enemigos; cuando salieron los cinco, corre el `descanso`. A los tres segundos de respiro, `salidos` vuelve a 0 y
`oleada` sube: empieza la siguiente.

#### Cada vez más rápido
La velocidad depende de la oleada: `100 + 40 * oleada`. En la primera son 140 píxeles por segundo; en la segunda,
180; en la tercera, 220.

#### Los enemigos tiran
Los tiros son **balas**: el mismo `struct Bala`, en otra pileta, `tiros`. Cada segundo y medio, el primer enemigo vivo
suelta un tiro desde abajo suyo. Los tiros bajan y se apagan al salir. (Que le peguen al biplano es el nodo que
viene.)

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
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

Las oleadas (con su respiro y su dificultad que sube) son la forma de armar el ritmo de casi todos los juegos de
acción. Y el seno sirve para todo lo que va y viene: enemigos que flotan, plataformas que suben y bajan, una moneda
que brilla.

### Errores habituales

**El seno en grados.** `SDL_sinf` usa radianes: con `SDL_sinf(y)` sola, el enemigo tiembla rapidísimo. Dividiendo por
40, la curva se estira.

**Olvidarse de contar.** Sin `salidos++`, la oleada nunca termina.

**Volver `descanso` a 0 al empezar.** Si no, la segunda oleada termina el respiro en un instante.

**Glitch: dos `break` confundidos.** El de adentro corta la búsqueda de un tiro libre; el de afuera hace que tire **un
solo** enemigo. Sin el de afuera, tiran todos juntos.

### Micro-misión R06-N04-P1 · Zigzag

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: Seno | enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt
recompensa: xp 10, oro 10
```

#### Escena
Los globos bajan derecho como plomadas. —Los globos de verdad bailan con el viento —dice {mentor}, y sopla uno
que se va de costado, de acá para allá.

#### Gheco sugiere
`SDL_sinf` da un número que sube y baja entre -1 y 1, como una ola. Abajo de la línea que lo hace bajar:
```c
enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
```
- Mientras el globo baja, `y / 40` crece y el seno va y viene: el globo se corre a un lado y al otro.
- `* 120` es qué tan rápido se corre de costado; `* dt`, para que sea igual en todas las compus.

El robot va a esperar dos segundos.

#### Desafío
Hacé que los enemigos se muevan de costado, de un lado a otro, mientras bajan.

#### Pasos
1. Buscá `/* acá: y se mueve de costado, de un lado a otro, como un zigzag */`.
2. Debajo, escribí la línea con `SDL_sinf` de la sugerencia.
3. Tocá **Jugar** y mirá bailar los globos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                /* acá: y se mueve de costado, de un lado a otro, como un zigzag */
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
cuadros 120
```

#### Estado
```
buscar #dc3c3c
```

#### Salida esperada
```
── Estado ──
buscar #dc3c3c: x 133, y 4, ancho 191, alto 150
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
Los globos bajan bailando, de un lado al otro, como hojas en el viento. Ahora apuntar cuesta. El Glitch intenta
hacerlos parpadear, pero el seno es parejo y no lo deja.

#### Imagen
- La pantalla de la máquina con globos rojos bajando en zigzag, con líneas curvas de movimiento.
- Un gatito pixelado que parpadea mira enojado desde un rincón de la pantalla.
- Arcadia sopla un globo de verdad que se va de costado; Kira lo sigue con la vista; Gheco lo persigue.

### Micro-misión R06-N04-P2 · Cinco y un respiro

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Oleadas | si salidos < POR_OLEADA: relojEnemigo += dt · si no: descanso += dt, a los 3 s: salidos = 0, oleada++ · al soltar uno: salidos++
recompensa: xp 10, monedas 4
```

#### Escena
Los globos salen sin parar, uno por segundo, para siempre. —Así nadie respira —dice {mentor}—. En la máquina
venían de a cinco. Después, un ratito de calma. Y otra oleada.

#### Gheco sugiere
Ya están `oleada` (en 1), `salidos` y `descanso`. Tres cosas:
1. **El reloj corre solo si faltan salir**, en lugar de `relojEnemigo += dt;`:
```c
if (salidos < POR_OLEADA) {
    relojEnemigo += dt;
} else {
    descanso += dt;                /* ya salieron los cinco: respiro */
    if (descanso >= 3) {
        descanso = 0;
        salidos = 0;
        oleada++;                  /* ¡la que sigue! */
    }
}
```
2. **Contar** cada enemigo que sale, antes del `break`: `salidos++;`
3. **Mostrar la oleada**, abajo de los puntos:
```c
SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
```
El robot va a esperar nueve segundos: cinco globos, el respiro y la oleada 2.

#### Desafío
Hacé que los enemigos vengan de a cinco, con 3 segundos de respiro entre oleadas, y mostrá la oleada.

#### Pasos
1. Buscá `/* acá: mientras falten enemigos de esta oleada, corre el reloj; si no, un respiro de 3 segundos y la oleada siguiente */`, borrá el `relojEnemigo += dt;` de abajo y escribí el `if` de la sugerencia.
2. Buscá `/* acá: contar el que salió */` y escribí `salidos++;`.
3. Buscá `/* acá: mostrar la oleada abajo de los puntos */` y escribí el texto.
4. Tocá **Jugar** y esperá el respiro. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        /* acá: mientras falten enemigos de esta oleada, corre el reloj; si no, un respiro de 3 segundos y la oleada siguiente */
        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    /* acá: contar el que salió */
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        /* acá: mostrar la oleada abajo de los puntos */
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
cuadros 540
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0 | OLEADA 2
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += 120 * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
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
Cinco globos… calma… y arriba a la izquierda, **OLEADA 2**. Kira aprovecha el respiro para estirar los dedos.
Gheco se toma un sorbito de la gaseosa de la Boletería.

#### Imagen
- La pantalla de la máquina con el cielo vacío entre dos oleadas y un cartelito blanco arriba (sin letras legibles).
- Kira estira los dedos, sonriendo; Arcadia le pasa una gaseosa.
- Gheco toma un sorbito de una botellita de gaseosa, arriba de la máquina.

### Micro-misión R06-N04-P3 · Más rápidos

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Dificultad | enemigos[e].y += (100 + 40 * oleada) * dt
recompensa: xp 10, monedas 4
```

#### Escena
La segunda oleada baja igual de lenta que la primera. —Cada oleada era más brava —dice {mentor}—. Si no, a la
décima uno se duerme.

#### Gheco sugiere
En lugar de `120`, una velocidad que crece con la oleada:
```c
enemigos[e].y += (100 + 40 * oleada) * dt;
```
| oleada | velocidad |
|---|---|
| 1 | 140 |
| 2 | 180 |
| 3 | 220 |

Los paréntesis hacen que primero se calcule la velocidad y después se multiplique por `dt`. El robot va a
esperar dos segundos.

#### Desafío
Hacé que cada oleada baje más rápido: 100 + 40 por la oleada.

#### Pasos
1. Buscá `/* acá: cada oleada baja más rápido */` y borrá la línea de abajo.
2. En su lugar, escribí la línea de la sugerencia.
3. Tocá **Jugar** y aguantá varias oleadas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                /* acá: cada oleada baja más rápido */
                enemigos[e].y += 120 * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
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
buscar #dc3c3c
```

#### Salida esperada
```
── Estado ──
buscar #dc3c3c: x 133, y 5, ancho 175, alto 170
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }


        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
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
La tercera oleada baja como lluvia. Kira dispara rápido, mueve el biplano, vuelve a disparar. Arcadia silba: —Ya
parecés piloto de verdad.

#### Imagen
- La pantalla de la máquina con una oleada de globos rojos bajando rápido, con rayas de velocidad.
- Kira juega a toda velocidad; Arcadia silba admirada.
- Gheco se pone unas antiparras de piloto más grandes que él, arriba de la máquina.

### Micro-misión R06-N04-P4 · Burbujitas de agua

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Tiros | relojTiro += dt · a 1,5 s: el primer enemigo vivo suelta un tiro libre · cada tiro: y += 250 * dt, si y > 480: viva = false
recompensa: xp 10, monedas 4
```

#### Escena
—Los globos más pícaros tiraban burbujitas de agua para abajo —dice {mentor}—. Si te mojaban, perdías una vida.
Primero, que tiren.

#### Gheco sugiere
Los tiros son balas: ya está la pileta `tiros` (el mismo `struct Bala`) y `relojTiro`. Dos cosas:
1. **Tirar y mover**, antes de dibujar:
```c
relojTiro += dt;
if (relojTiro >= 1.5f) {
    relojTiro -= 1.5f;
    for (int e = 0; e < ENEMIGOS; e++) {
        if (enemigos[e].vivo) {                     /* el primer enemigo vivo… */
            for (int t = 0; t < TIROS; t++) {
                if (!tiros[t].viva) {               /* …usa un tiro libre */
                    tiros[t].x = enemigos[e].x + 18;
                    tiros[t].y = enemigos[e].y + 30;
                    tiros[t].viva = true;
                    break;
                }
            }
            break;                                  /* tira uno solo */
        }
    }
}
for (int t = 0; t < TIROS; t++) {
    if (tiros[t].viva) {
        tiros[t].y += 250 * dt;                     /* bajan */
        if (tiros[t].y > 480) {
            tiros[t].viva = false;
        }
    }
}
```
2. **Dibujarlos**, rojo anaranjado:
```c
SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
for (int t = 0; t < TIROS; t++) {
    if (tiros[t].viva) {
        SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
        SDL_RenderFillRect(lapiz, &tiro);
    }
}
```
El robot va a esperar dos segundos.

#### Desafío
Hacé que cada segundo y medio el primer enemigo vivo tire, y que los tiros bajen y se apaguen al salir.

#### Pasos
1. Buscá `/* acá: cada segundo y medio, el primer enemigo vivo tira; los tiros bajan y se apagan al salir */` y escribí el temporizador y el `for` que los mueve.
2. Buscá `/* acá: dibujar los tiros de los enemigos, rojo anaranjado */` y escribí el color y el `for` que los dibuja.
3. Tocá **Jugar** y esquivá las burbujitas. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        /* acá: cada segundo y medio, el primer enemigo vivo tira; los tiros bajan y se apagan al salir */

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        /* acá: dibujar los tiros de los enemigos, rojo anaranjado */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
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
buscar #ff5a28
```

#### Salida esperada
```
── Estado ──
buscar #ff5a28: x 267, y 236, ancho 4, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
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
Los globos empiezan a tirar burbujitas de agua que caen como gotas. Por ahora atraviesan el biplano sin
mojarlo. —Por ahora —dice {mentor}, y le guiña un ojo a Kira.

#### Imagen
- La pantalla de la máquina con globos rojos tirando gotitas anaranjadas hacia abajo, cerca del biplano.
- Arcadia le guiña un ojo a Kira; Kira esquiva concentrada.
- Gheco abre un paraguitas diminuto arriba de la máquina.

## R06-N05 · Vidas, menú y revancha

```meta
tipo: tema
criatura: bucle_eterno
padre: R06-N04
precio: 10
temas: juegos.estados
usa: juegos.colisiones, col.registros, juegos.bucle
```

### Crónica

Las burbujitas de agua atraviesan el biplano sin mojarlo, y los globos que chocan contra el ala pasan de largo.
Kira juega y juega, y la partida no termina nunca: ni empieza, en realidad, porque los globos ya bajan apenas se
prende la máquina. —El **Bucle Eterno** —dice {mentor}—. Un juego tiene que saber cuándo empieza, cuándo te
mojaron, cuándo se terminó y cómo se vuelve a empezar.

### Objetivos

Ordenar el juego con **estados** (menú, jugando, perdiste) congelando el tiempo fuera de la partida, darle al biplano
**tres vidas** que se pierden al chocar un globo o un tiro, unos segundos de **parpadeo** sin que lo mojen después de
cada golpe, y la **revancha** con la R.

### Antes de empezar

El nodo anterior. De R05: el menú con Enter y la revancha (N05). De R03: las vidas (N05).

### Explicación

#### Congelar el tiempo
En este juego casi todo se mueve con `dt`: el biplano, las nubes, los globos, los relojes. Un truco: si no se está
jugando, se pone `dt = 0`. Todo lo que se multiplica por `dt` se queda quieto, y todos los relojes se frenan. Con una
sola línea, el menú y el fin congelan el juego entero.

#### Un golpe
Cada globo y cada tiro vivo se prueba contra la cajita del biplano. Si lo toca, se apaga y se anota que hubo un
`golpe`. Después, **una sola vez** por cuadro: si hubo golpe, una vida menos (aunque lo hayan tocado dos cosas a la
vez). Sin vidas, el juego termina.

#### Unos segundos de respiro
Después de un golpe, `invulnerable` vale 2 y va bajando con `dt`. Mientras sea mayor que 0, los golpes no cuentan (las
cosas que lo tocan se rompen igual). Para que se note, el biplano **parpadea**: `(int)(invulnerable * 10) % 2` vale 0 y
1 alternados cada décimo de segundo, y solo se dibuja cuando vale 0.

#### La revancha
Con la R se apagan las tres piletas (balas, enemigos y tiros), el biplano vuelve a su lugar, y los puntos, las vidas,
la oleada y los relojes vuelven a empezar.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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

Congelar el tiempo con `dt = 0` sirve para la pausa de cualquier juego. Y el parpadeo de invulnerabilidad está en casi
todos los juegos de acción: es la manera de avisar «te salvaste por un ratito».

### Errores habituales

**Restar una vida por cada cosa que toca.** Si un globo y un tiro lo tocan en el mismo cuadro, se irían dos vidas
juntas. Por eso primero se junta en `golpe` y después se resta una sola.

**Olvidarse de `invulnerable = 2`.** Un globo grande toca el biplano varios cuadros seguidos: sin el respiro, se van
las tres vidas en un instante.

**La revancha que no apaga las piletas.** Los globos de la partida anterior siguen ahí y mojan al biplano apenas
arranca.

**Bucle Eterno: el juego que no termina.** Si al llegar a 0 vidas no se cambia el estado, las vidas siguen bajando:
-1, -2, -3…

### Micro-misión R06-N05-P1 · Antes de despegar

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Estados | si estado != JUGANDO: dt = 0 · Enter en el MENU: JUGANDO · cartel LOS BIPLANOS
recompensa: xp 10, oro 10
```

#### Escena
La máquina se prende y los globos ya están bajando, sin aviso. —Primero el nombre bien grande —dice {mentor}—,
y que nada se mueva hasta que el piloto diga «despego».

#### Gheco sugiere
Ya están el `enum` (`MENU`, `JUGANDO`, `PERDISTE`) y `estado` en `MENU`; el espacio dispara solo jugando. Tres
cosas:
1. **Congelar el tiempo**, justo después de calcular `dt`:
```c
if (estado != JUGANDO) {
    dt = 0;       /* todo lo que se mueve con dt se queda quieto */
}
```
2. **El Enter despega**, en los eventos:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
    estado = JUGANDO;
}
```
3. **El cartel del menú**, al final del dibujo:
```c
if (estado == MENU) {
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_SetRenderScale(lapiz, 4, 4);
    SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
    SDL_SetRenderScale(lapiz, 1, 1);
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
    SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
}
```
El robot va a esperar un segundo en el menú y después apretar el Enter: el primer globo tiene que salir recién un segundo después de despegar.

#### Desafío
Hacé el menú: el juego quieto y el cartel hasta que se apriete el Enter.

#### Pasos
1. Buscá `/* acá: si no se está jugando, el tiempo no pasa: todo queda quieto */` y escribí el `if` del `dt = 0`.
2. Buscá `/* acá: en el menú, el Enter empieza la partida */` y escribí el `if` del Enter.
3. Buscá `/* acá: el menú: el nombre grande y cómo se empieza */` y escribí el `if (estado == MENU)` del cartel.
4. Tocá **Jugar**, mirá el menú y apretá el Enter. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: en el menú, el Enter empieza la partida */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        /* acá: si no se está jugando, el tiempo no pasa: todo queda quieto */

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        /* acá: el menú: el nombre grande y cómo se empieza */
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
tecla Enter
cuadros 30
```

#### Estado
```
buscar #dc3c3c
```

#### Salida esperada
```
── Estado ──
buscar #dc3c3c: no está
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
La pantalla se prende con **LOS BIPLANOS** en letras amarillas, y todo espera, quieto, hasta las nubes. Kira
aprieta el Enter: las nubes empiezan a pasar y el primer globo asoma arriba.

#### Imagen
- La pantalla de la máquina con un cartel amarillo enorme sobre el cielo quieto (sin letras legibles).
- Kira se pone unas antiparras de piloto, lista; Arcadia sonríe.
- Gheco hace la cuenta regresiva con los dedos arriba de la máquina.

### Micro-misión R06-N05-P2 · Tres vidas

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
criatura: bucle_eterno
carta: Golpe | enemigo o tiro vivo que toca el avión: se apaga, golpe = true · si golpe: vidas--, invulnerable = 2 · sin vidas: PERDISTE
recompensa: xp 10, monedas 4
```

#### Escena
Un globo choca contra el ala del biplano y pasa de largo, como si nada. Las burbujitas de agua lo atraviesan.
El Bucle Eterno da vueltas alrededor de la máquina: el juego no termina nunca.

#### Gheco sugiere
Ya están `vidas` (3), `invulnerable` y `golpe`. Tres cosas:
1. **¿Algo tocó el biplano?** Cada enemigo y cada tiro vivo contra la cajita del avión:
```c
for (int e = 0; e < ENEMIGOS; e++) {
    SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
    if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
        enemigos[e].vivo = false;
        golpe = true;
    }
}
for (int t = 0; t < TIROS; t++) {
    SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
    if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
        tiros[t].viva = false;
        golpe = true;
    }
}
```
2. **Una vida menos** (una sola, aunque lo toquen dos cosas):
```c
if (golpe) {
    vidas--;
    invulnerable = 2;      /* lo usamos en la que viene */
    if (vidas <= 0) {
        estado = PERDISTE;
    }
}
```
3. **Las vidas y el cartel**, abajo de la oleada:
```c
SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
if (estado == PERDISTE) {
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
}
```
El robot va a despegar y poner el biplano debajo del primer globo.

#### Desafío
Hacé que chocar un globo o un tiro cueste una vida, y que sin vidas se termine el vuelo.

#### Pasos
1. Buscá `/* acá: si un enemigo o un tiro toca el biplano, se apaga y es un golpe */` y escribí los dos `for`.
2. Buscá `/* acá: un golpe es una vida menos; sin vidas, se terminó */` y escribí el `if (golpe)`.
3. Buscá `/* acá: las vidas arriba a la derecha y el cartel del final */` y escribí el texto y el cartel.
4. Tocá **Jugar** y dejate mojar. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        /* acá: si un enemigo o un tiro toca el biplano, se apaga y es un golpe */
        /* acá: un golpe es una vida menos; sin vidas, se terminó */

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        /* acá: las vidas arriba a la derecha y el cartel del final */
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
cuadros 300
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0 | OLEADA 1 | VIDAS 2
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
Un globo choca contra el ala: *¡plaf!*, revienta y arriba a la derecha queda **VIDAS 2**. Kira se seca la cara
como si la hubieran mojado de verdad. El Bucle Eterno se frena, mareado, y se va.

#### Imagen
- La pantalla de la máquina con un globo rojo reventando contra el ala del biplano amarillo, en una salpicadura de agua.
- Una criatura que es un aro de luz girando se frena, mareada, y se va caminando en zigzag.
- Kira se seca la cara riéndose; Arcadia le alcanza un pañuelo; Gheco, empapado, se sacude como un perrito.

### Micro-misión R06-N05-P3 · Un ratito a salvo

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Invulnerable | invulnerable -= dt · si invulnerable > 0: golpe = false · dibujar solo si invulnerable <= 0 o (int)(invulnerable * 10) % 2 == 0
recompensa: xp 10, monedas 4
```

#### Escena
Un globo grande toca el ala… y se van las tres vidas de golpe, una por cuadro. —Después de un golpe, el piloto
tiene un ratito a salvo —dice {mentor}—. Y el avión parpadea, para que se sepa.

#### Gheco sugiere
Dos cosas:
1. **El ratito a salvo**, entre los choques y la resta de la vida:
```c
invulnerable -= dt;
if (invulnerable > 0) {
    golpe = false;      /* este golpe no cuenta */
}
```
2. **El parpadeo**, en lugar de dibujar el cuerpo y el ala siempre:
```c
if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
    SDL_RenderFillRect(lapiz, &cuerpo);
    SDL_RenderFillRect(lapiz, &ala);
}
```
`invulnerable * 10` cuenta décimos de segundo; `% 2` da 0 y 1 alternados: un décimo se ve y otro no. El robot va
a dejar el biplano quieto debajo de los globos un buen rato.

#### Desafío
Hacé que después de un golpe el biplano tenga dos segundos sin que lo mojen, y que parpadee mientras tanto.

#### Pasos
1. Buscá `/* acá: después de un golpe, dos segundos en que nada lo moja */` y escribí las líneas de la sugerencia.
2. Buscá `/* acá: mientras dura, el biplano parpadea: se dibuja un décimo de segundo sí y otro no */` y borrá las dos líneas de abajo.
3. En su lugar, escribí el `if` del parpadeo.
4. Tocá **Jugar** y dejate mojar. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        /* acá: después de un golpe, dos segundos en que nada lo moja */
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        /* acá: mientras dura, el biplano parpadea: se dibuja un décimo de segundo sí y otro no */
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
cuadros 600
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0 | OLEADA 2 | VIDAS 1
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
El globo toca el ala, el biplano parpadea y, por dos segundos, las burbujitas lo atraviesan sin mojarlo. Kira
aprovecha para escaparse. —Como un escudo de luz —dice, y mira su brazal.

#### Imagen
- La pantalla de la máquina con el biplano amarillo parpadeando, semitransparente, entre gotitas que lo atraviesan.
- Kira mira su brazal de control, pensativa; Arcadia asiente.
- Gheco se tapa y destapa los ojos al ritmo del parpadeo, arriba de la máquina.

### Micro-misión R06-N05-P4 · Otra vez al aire

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia
carta: Revancha | R en PERDISTE: apagar balas, enemigos y tiros · avión a (300, 400) · puntos, vidas, oleada y relojes como al principio · JUGANDO
recompensa: xp 10, monedas 4
```

#### Escena
Se terminó el vuelo y ahí se quedó. Kira aprieta todas las teclas: nada. —Otra vez —pide—. —Todo como al
principio —dice {mentor}—: el cielo vacío, el avión en la pista y tres vidas.

#### Gheco sugiere
Con la R, después de perder, se apagan las tres piletas y todo vuelve a empezar:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
    for (int i = 0; i < BALAS; i++) {
        balas[i].viva = false;
    }
    for (int e = 0; e < ENEMIGOS; e++) {
        enemigos[e].vivo = false;
    }
    for (int t = 0; t < TIROS; t++) {
        tiros[t].viva = false;
    }
    avion.x = 300;
    avion.y = 400;
    puntos = 0;
    vidas = 3;
    oleada = 1;
    salidos = 0;
    descanso = 0;
    relojEnemigo = 0;
    relojTiro = 0;
    invulnerable = 0;
    estado = JUGANDO;
}
```
Y avisarlo, abajo del cartel:
```c
if (estado == PERDISTE) {
    SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
}
```

#### Desafío
Hacé que con la R, después de perder, todo vuelva a empezar.

#### Pasos
1. Buscá `/* acá: después de perder, la R deja todo como al principio */` y escribí el `if` de la R.
2. Buscá `/* acá: avisar que con la R se vuela otra vez */` y escribí el `if` del aviso.
3. Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
            /* acá: después de perder, la R deja todo como al principio */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        /* acá: avisar que con la R se vuela otra vez */
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
cuadros 1800
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
textos: PUNTOS 0 | OLEADA 1 | VIDAS 3
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
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
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
Kira aprieta la R: el cielo se vacía, el biplano vuelve a la pista y arriba dice **VIDAS 3**. —Ahora sí —dice, y
despega de nuevo.

#### Imagen
- La pantalla de la máquina con el cielo vacío, el biplano amarillo abajo en su lugar y nubes pasando.
- Kira, decidida, se acomoda el brazal; Arcadia le guiña un ojo.
- Gheco hace la señal de despegue con dos banderitas arriba de la máquina.

## R06-N06 · Jefe: La Nave Nodriza

```meta
tipo: jefe
criatura: glitch
padre: R06-N05
precio: 10
insignia: Sello de la Pista de los Biplanos
insignia_descripcion: Hiciste aterrizar a la Nave Nodriza: un juego de naves entero, con el cielo que pasa, las balas y los enemigos en piletas de structs, las oleadas, los tiros, las vidas con parpadeo, el menú, la revancha y un jefe con barra de vida.
temas: juegos.estados
usa: juegos.colisiones, col.registros, juegos.ia, juegos.bucle
```

### Crónica

Después de la quinta oleada, el hangar se oscurece: algo enorme tapa el sol en la puerta. Es un dirigible de
juguete del tamaño de una casa, hecho de retazos de tela de colores, con hélices que zumban y una canasta llena de
globos rojos colgando abajo. Tiene dos ojos de buzo redondos en la proa y una sonrisa de lona. —¡Por fin un piloto!
—dice, con voz de altoparlante—. Treinta años soltando globos sin que nadie me los reviente. Yo soy **la Nave
Nodriza**, la que lleva los globos. Si querés que aterrice, vas a tener que mojarme más de lo que yo te mojo a vos.

### Objetivos

Terminar el juego de naves contra la Nave Nodriza: que **aparezca** a los 20 segundos y vaya y venga, que las balas
le saquen **vida** (con su barra), que **tire bombas de agua** de los dos costados y un **cartel final centrado** que
diga si aterrizó o te mojó.

### Antes de empezar

Toda la rama R06. De R02: el Campeón con su rapidez (N07). De R05: el cartel centrado del jefe (N06).

### Explicación

#### Un jefe es un enemigo grande
La Nodriza es un rectángulo grande, `nodriza`, con su propia velocidad de costado, `nvx`. Cuando llega a un borde, se
da vuelta (`nvx = -nvx`), como la pelota del Pong. No aparece desde el principio: un reloj, `relojNodriza`, espera 20
segundos.

#### La vida del jefe y su barra
`nvida` empieza en 20. Cada bala viva que toca la Nodriza se apaga y le saca uno. La barra verde de arriba mide
`nvida * 10` píxeles: empieza en 200 y se achica con cada golpe. Cuando llega a 0, la Nodriza se va y ganaste: un
estado nuevo, `GANASTE`.

#### Las bombas de agua
Cada 0,8 segundos, la Nodriza suelta **dos** tiros: uno de cada costado. Se buscan dos tiros libres en la pileta con
un contador, `puestas`: el `for` se corta cuando ya puso dos (`puestas < 2` en la condición). El primero sale del
costado izquierdo y el segundo, del derecho.

#### El cartel del final
Si ganaste, «LA NODRIZA ATERRIZA»; si perdiste, «TE MOJARON». Centrado como siempre: `320 - letras * 4`.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        if (hayNodriza) {
            relojBombas += dt;
        }
        if (relojBombas >= 0.8f) {
            relojBombas -= 0.8f;
            int puestas = 0;
            for (int t = 0; t < TIROS && puestas < 2; t++) {
                if (!tiros[t].viva) {
                    tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
                    tiros[t].y = nodriza.y + nodriza.h;
                    tiros[t].viva = true;
                    puestas++;
                }
            }
        }
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE || estado == GANASTE) {
            const char *cartel = (estado == GANASTE) ? "LA NODRIZA ATERRIZA" : "TE MOJARON";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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

Un jefe con barra de vida está en casi todos los juegos de acción: es un enemigo como los demás, pero más grande, con
más vida y con sus propios ataques. Y el juego de naves completo es tu quinto juego entero: lo vas a poder bajar y
jugar en tu compu.

### Errores habituales

**La barra que no se achica.** Si el ancho es fijo (200), la barra no muestra nada. Tiene que salir de `nvida`.

**Golpear a la Nodriza antes de que aparezca.** Sin el `hayNodriza` en la condición, las balas chocan contra un
rectángulo invisible arriba de la pantalla.

**Poner las dos bombas en el mismo tiro libre.** Sin el contador `puestas`, el `for` usa todos los tiros libres
(o uno solo, con `break`).

**Glitch: que la Nodriza se trabe en el borde.** Si al tocar el borde se da vuelta pero no vuelve adentro, en el
cuadro siguiente se vuelve a dar vuelta y tiembla. Con `dt` chiquito y la vuelta inmediata, alcanza para salir.

### Micro-misión R06-N06-P1 · Algo tapa el sol

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia, la Nave Nodriza
carta: Jefe | relojNodriza += dt · a los 20 s: hayNodriza = true · si está: nodriza.x += nvx * dt · en un borde: nvx = -nvx
recompensa: xp 10, oro 10
```

#### Escena
—Cuando un piloto aguantaba veinte segundos —dice la Nave Nodriza—, yo bajaba a saludarlo. Y a mojarlo un
poquito.

#### Gheco sugiere
Ya están la cajita `nodriza`, su velocidad `nvx` y `relojNodriza`. Dos cosas:
1. **Que aparezca a los 20 segundos y vaya y venga:**
```c
relojNodriza += dt;
if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
    hayNodriza = true;
}
if (hayNodriza) {
    nodriza.x += nvx * dt;
    if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
        nvx = -nvx;          /* llegó a un borde: se da vuelta */
    }
}
```
2. **Dibujarla**, lila, antes de los tiros:
```c
if (hayNodriza) {
    SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
    SDL_RenderFillRect(lapiz, &nodriza);
}
```
El robot va a despegar, esconder el biplano en una esquina y esperar 21 segundos.

#### Desafío
Hacé que a los 20 segundos aparezca la Nodriza y vaya y venga de costado.

#### Pasos
1. Buscá `/* acá: a los 20 segundos aparece la Nodriza, y va y viene de costado */` y escribí las líneas de la sugerencia.
2. Buscá `/* acá: dibujar la Nodriza, lila */` y escribí el `if` que la dibuja.
3. Tocá **Jugar**, despegá y aguantá 20 segundos. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        /* acá: a los 20 segundos aparece la Nodriza, y va y viene de costado */
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        /* acá: dibujar la Nodriza, lila */
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
apretar Izquierda
cuadros 70
soltar Izquierda
cuadros 1200
```

#### Estado
```
buscar #aa78dc
```

#### Salida esperada
```
── Estado ──
buscar #aa78dc: x 380, y 40, ancho 200, alto 60
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
A los veinte segundos, el cielo de la pantalla se oscurece y baja un dirigible lila enorme que va de un lado al
otro, zumbando. Kira traga saliva. Gheco se esconde detrás del volante.

#### Imagen
- La Nave Nodriza: un dirigible de juguete enorme hecho de retazos de tela de colores, con hélices, dos ojos de buzo redondos en la proa, una sonrisa de lona y una canasta llena de globos rojos, en la puerta del hangar.
- En la pantalla de la máquina, un dirigible lila grande arriba y el biplano amarillo abajo.
- Kira traga saliva, decidida; Arcadia mira la Nodriza con una sonrisa; Gheco se esconde detrás del volante de la máquina.

### Micro-misión R06-N06-P2 · La barra de vida

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia, la Nave Nodriza
carta: Vida del jefe | bala viva que toca la Nodriza: se apaga · nvida-- · puntos += 5 · sin vida: GANASTE · barra de nvida * 10
recompensa: xp 10, monedas 4
```

#### Escena
Kira le dispara a la Nodriza: las burbujas la atraviesan como si fuera una nube. —Je —dice la Nodriza—. Yo
aguanto veinte burbujas. Y quiero ver cuántas me quedan.

#### Gheco sugiere
Ya está `nvida` en 20. Dos cosas:
1. **Cada bala que la toca le saca una vida:**
```c
for (int i = 0; i < BALAS; i++) {
    SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
    if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
        balas[i].viva = false;
        nvida--;
        puntos += 5;
        if (nvida <= 0) {
            hayNodriza = false;     /* ¡se va! */
            estado = GANASTE;
        }
    }
}
```
2. **La barra**, verde, arriba en el medio:
```c
if (hayNodriza) {
    SDL_FRect barra = { 220, 8, nvida * 10, 8 };   /* 200 píxeles con 20 vidas */
    SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
    SDL_RenderFillRect(lapiz, &barra);
}
```
El robot va a esconder el biplano en una esquina y esperar a la Nodriza: la barra tiene que aparecer con ella.

#### Desafío
Hacé que cada bala que toca la Nodriza le saque una vida, con su barra verde que se achica.

#### Pasos
1. Buscá `/* acá: cada bala que la toca le saca una vida; sin vidas, ganaste */` y escribí el `for` de la sugerencia.
2. Buscá `/* acá: su barra de vida, verde, arriba en el medio */` y escribí el `if` de la barra.
3. Tocá **Jugar**, esperá a la Nodriza y dispárale. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        /* acá: cada bala que la toca le saca una vida; sin vidas, ganaste */
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        /* acá: su barra de vida, verde, arriba en el medio */
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
apretar Izquierda
cuadros 70
soltar Izquierda
cuadros 1200
```

#### Estado
```
buscar #78dc78
```

#### Salida esperada
```
── Estado ──
buscar #78dc78: x 220, y 8, ancho 200, alto 8
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
Cada burbuja que la toca hace *¡plop!* y la barra verde se achica un poquito. —¡Ay, ay! —se ríe la Nodriza—.
¡Me hacés cosquillas!

#### Imagen
- La Nave Nodriza, el dirigible de retazos de tela con ojos de buzo, se ríe mojada mientras burbujas de luz le explotan en la panza.
- En la pantalla de la máquina, el dirigible lila con una barra verde arriba que se achica.
- Kira dispara sin parar; Arcadia aplaude; Gheco cuenta los ¡plop! con los dedos.

### Micro-misión R06-N06-P3 · Bombas de agua

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia, la Nave Nodriza
carta: Dos tiros | relojBombas += dt · a 0,8 s: dos tiros libres (puestas < 2): uno en nodriza.x + 20 y otro en nodriza.x + nodriza.w - 24
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora me toca a mí —dice la Nodriza, y de su canasta asoman dos regaderas, una de cada lado—. ¡Bombas de agua!

#### Gheco sugiere
Ya está `relojBombas`. Cada 0,8 segundos (mientras está la Nodriza), dos tiros: uno de cada costado. Se cuentan
con `puestas`, y el `for` se corta cuando ya puso dos:
```c
if (hayNodriza) {
    relojBombas += dt;
}
if (relojBombas >= 0.8f) {
    relojBombas -= 0.8f;
    int puestas = 0;
    for (int t = 0; t < TIROS && puestas < 2; t++) {
        if (!tiros[t].viva) {
            tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
            tiros[t].y = nodriza.y + nodriza.h;
            tiros[t].viva = true;
            puestas++;
        }
    }
}
```
- `t < TIROS && puestas < 2`: sigue mientras haya tiros por mirar **y** falte poner alguno.
- El primero (`puestas == 0`) sale del costado izquierdo; el segundo, del derecho.

Los tiros ya bajan y mojan solos. El robot va a esconder el biplano en una esquina y esperar a la Nodriza.

#### Desafío
Hacé que la Nodriza tire dos bombas de agua, una de cada costado, cada 0,8 segundos.

#### Pasos
1. Buscá `/* acá: la Nodriza tira dos bombas de agua, una de cada lado, cada 0,8 segundos */`.
2. Debajo, escribí los dos `if` de la sugerencia.
3. Tocá **Jugar**, esperá a la Nodriza y esquivá. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        /* acá: la Nodriza tira dos bombas de agua, una de cada lado, cada 0,8 segundos */
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
apretar Izquierda
cuadros 70
soltar Izquierda
cuadros 1300
```

#### Estado
```
buscar #ff5a28
```

#### Salida esperada
```
── Estado ──
buscar #ff5a28: x 361, y 121, ancho 240, alto 210
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        if (hayNodriza) {
            relojBombas += dt;
        }
        if (relojBombas >= 0.8f) {
            relojBombas -= 0.8f;
            int puestas = 0;
            for (int t = 0; t < TIROS && puestas < 2; t++) {
                if (!tiros[t].viva) {
                    tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
                    tiros[t].y = nodriza.y + nodriza.h;
                    tiros[t].viva = true;
                    puestas++;
                }
            }
        }
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
La Nodriza riega el cielo con dos chorros de burbujas de agua, uno de cada lado. Kira pasa por el medio,
esquivando, y le dispara justo debajo de la panza. —¡Bien pensado! —se ríe la Nodriza.

#### Imagen
- La Nave Nodriza, el dirigible de retazos de tela, riega el cielo con dos regaderas colgadas de su canasta, una de cada lado.
- En la pantalla de la máquina, el dirigible lila soltando gotas anaranjadas de los dos costados y el biplano pasando por el medio.
- Kira esquiva concentrada; Arcadia se cubre con la mano riéndose; Gheco abre un paraguitas.

### Micro-misión R06-N06-P4 · La Nodriza aterriza

```meta
lugar: La Pista de los Biplanos
personajes: Kira, Gheco, Arcadia, la Nave Nodriza
carta: Cartel centrado | al terminar: cartel = estado == GANASTE ? "LA NODRIZA ATERRIZA" : "TE MOJARON" · x = 320 - SDL_strlen(cartel) * 4
recompensa: xp 20, monedas 5
item: Hélice de Plata
```

#### Escena
—Si me ganás —dice la Nodriza—, que la máquina lo diga en el medio, bien claro: que aterricé. Y si me ganás yo
a vos, que diga que te mojé.

#### Gheco sugiere
En lugar del cartel de antes («FIN DEL VUELO», corrido a ojo), uno centrado para los dos finales:
```c
if (estado == PERDISTE || estado == GANASTE) {
    const char *cartel = (estado == GANASTE) ? "LA NODRIZA ATERRIZA" : "TE MOJARON";
    SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
    SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
    SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
}
```
Cada letra mide 8 píxeles: un texto de `n` letras, centrado, empieza en `320 - n * 4` (como los carteles del
Campeón, el Muro, la Serpiente y la Torre). El robot va a dejar que lo mojen hasta perder.

#### Desafío
Cambiá el cartel del final por uno centrado: LA NODRIZA ATERRIZA si ganaste, TE MOJARON si perdiste.

#### Pasos
1. Buscá `/* acá: el cartel del final, centrado: si ganaste, la Nodriza aterriza */` y borrá el `if` de abajo.
2. En su lugar, escribí el `if` de la sugerencia.
3. Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        if (hayNodriza) {
            relojBombas += dt;
        }
        if (relojBombas >= 0.8f) {
            relojBombas -= 0.8f;
            int puestas = 0;
            for (int t = 0; t < TIROS && puestas < 2; t++) {
                if (!tiros[t].viva) {
                    tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
                    tiros[t].y = nodriza.y + nodriza.h;
                    tiros[t].viva = true;
                    puestas++;
                }
            }
        }
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        /* acá: el cartel del final, centrado: si ganaste, la Nodriza aterriza */
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
tecla Enter
cuadros 1800
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS 0 | OLEADA 3 | VIDAS 0 | TE MOJARON | R: OTRA VEZ
```

#### Solución
```c
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */

enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */
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
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        if (estado != JUGANDO) {
            dt = 0;
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);

        for (int n = 0; n < NUBES; n++) {
            ny[n] += 80 * dt;
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
        }

        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                balas[i].y -= 500 * dt;
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
            }
        }

        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    salidos++;
                    break;
                }
            }
        }
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                enemigos[e].y += (100 + 40 * oleada) * dt;
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
            }
        }

        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }

        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }

        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        if (hayNodriza) {
            relojBombas += dt;
        }
        if (relojBombas >= 0.8f) {
            relojBombas -= 0.8f;
            int puestas = 0;
            for (int t = 0; t < TIROS && puestas < 2; t++) {
                if (!tiros[t].viva) {
                    tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
                    tiros[t].y = nodriza.y + nodriza.h;
                    tiros[t].viva = true;
                    puestas++;
                }
            }
        }
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE || estado == GANASTE) {
            const char *cartel = (estado == GANASTE) ? "LA NODRIZA ATERRIZA" : "TE MOJARON";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
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
La última burbuja le da justo en la panza. La barra verde se apaga y la pantalla dice, en amarillo y en el
medio, **LA NODRIZA ATERRIZA**. Afuera del hangar, la Nave Nodriza de verdad baja despacito, apoya la canasta en
el pasto de la pista y apaga las hélices, empapada y feliz. —Treinta años esperando un piloto así —dice.

De su hélice más chica se desprende una pieza que brilla como una moneda: la **Hélice de Plata**. —Para que
nunca te falte viento —dice, y se la da a Kira.

En la pantalla aparece **otro pedazo del mapa del Vidriero**: un tren viejo que entra en un túnel oscuro, con
ventanitas que brillan. {mentor} se ríe bajito: —El Tren Fantasma. No te asustes: los fantasmas de ahí son
muy educados.

#### Imagen
- La Nave Nodriza, el dirigible de retazos de tela con ojos de buzo, aterrizada en el pasto de la pista, empapada y sonriente, con las hélices quietas.
- En la pantalla de la máquina, un pedazo de mapa antiguo con un tren viejo entrando en un túnel oscuro.
- Kira sostiene una hélice chiquita que brilla como la plata; Arcadia mira el mapa, divertida; Gheco se sienta en la hélice.
