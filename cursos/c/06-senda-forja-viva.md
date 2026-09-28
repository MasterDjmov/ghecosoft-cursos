# RAMA S01 · Senda de la Forja Viva: videojuegos con SDL3

```meta
tipo: senda
posicion: 6
```

## S01-N01 · La Forja Viva: ventana y bucle de juego

```meta
tipo: tema
padre: R05-N05
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
```

### Crónica

Detrás del yunque de la Encrucijada hay una puerta de vidrio negro. Del otro lado, el metal no está quieto: las piezas se mueven solas, sesenta veces por segundo, sobre una superficie que brilla. Es la **Forja Viva**.

—Acá no se escriben programas que terminan, {heroe} —dice {mentor}—. Se escriben mundos que **siguen andando** hasta que alguien cierra la puerta.

### Objetivos

- Instalar SDL3, compilar y enlazar un programa que abre una ventana.
- Entender el **bucle de juego**: tiempo, entrada, actualizar y dibujar.
- Mover cosas con *delta time* para que la velocidad no dependa de la compu.

### Antes de empezar

Todo el camino principal, en especial structs (12), punteros (13) y el menú de consola (R04-N05).

### Explicación

#### Instalar y compilar SDL3

SDL3 es una biblioteca: hay que tenerla instalada y **enlazarla**. En Ubuntu reciente:

```bash
sudo apt install libsdl3-dev        # si tu versión no la trae, se compila: ver FullCursos/external/build-sdl3.sh
gcc -std=c11 -Wall -Wextra -o juego main.c $(pkg-config --cflags --libs sdl3) -lm
./juego
```

`pkg-config` le dice al compilador dónde están los `.h` (`-I...`) y la biblioteca (`-lSDL3`). Estos programas abren una **ventana**: se prueban en tu compu, no en la plataforma, y las misiones se entregan como `.zip` con el código.

#### Las cuatro piezas

```c
SDL_Init(SDL_INIT_VIDEO);                                   /* encender SDL */
SDL_Window *ventana = SDL_CreateWindow("Título", 800, 600, 0);
SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);   /* el que dibuja (usa la placa de video) */
...
SDL_DestroyRenderer(pincel);                                /* y todo se devuelve al final */
SDL_DestroyWindow(ventana);
SDL_Quit();
```

Cada función puede fallar: en SDL3, `SDL_Init` devuelve `false` y las otras, `NULL`; `SDL_GetError()` dice por qué.

#### El bucle de juego

El menú de consola esperaba a que eligieras. Un juego **no espera**: repite lo mismo muchas veces por segundo, toques algo o no.

```c
while (corriendo) {
    /* 1. tiempo */     dt = segundos desde el cuadro anterior
    /* 2. entrada */    while (SDL_PollEvent(&evento)) { ... }
    /* 3. actualizar */ mover cosas usando dt
    /* 4. dibujar */    SDL_RenderClear → dibujar → SDL_RenderPresent
}
```

- `SDL_PollEvent` saca de a uno los eventos pendientes (teclas, mouse, cerrar la ventana) y devuelve `false` cuando no quedan.
- Se dibuja en un lienzo oculto y `SDL_RenderPresent` lo muestra de golpe (*doble búfer*): así no se ve cómo se va pintando.

#### Delta time

Si movés `x += 4` en cada cuadro, en una compu que hace 60 cuadros por segundo va a 240 píxeles por segundo, y en una de 240 cuadros va cuatro veces más rápido. Con **delta time** la velocidad se mide en píxeles **por segundo**:

```c
Uint64 ahora = SDL_GetTicks();                     /* milisegundos desde que arrancó SDL */
float dt = (float) (ahora - antes) / 1000.0f;      /* segundos */
caja.x += velocidad * dt;
```

Los rectángulos usan coordenadas decimales: `SDL_FRect { x, y, ancho, alto }`. El `(0, 0)` está **arriba a la izquierda** y la `y` crece hacia abajo.

### Código de ejemplo

```c
/*
 * S01-N01 - La ventana y el bucle de juego.
 * Un cuadrado que rebota de lado a lado, a la misma velocidad a 60 o a 240 FPS.
 */
#include <SDL3/SDL.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("La Forja Viva", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        fprintf(stderr, "No se pudo crear la ventana: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_FRect caja = { 100.0f, 280.0f, 40.0f, 40.0f };
    float velocidad = 220.0f;                   /* pixeles por SEGUNDO */
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();

    while (corriendo) {
        /* 1. tiempo: cuantos segundos pasaron desde el cuadro anterior */
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;                          /* si la compu se trabo, no saltar */
        }

        /* 2. entrada: todos los eventos pendientes */
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                corriendo = false;
            } else if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) {
                corriendo = false;
            }
        }

        /* 3. actualizar el mundo */
        caja.x += velocidad * dt;
        if (caja.x < 0) {
            caja.x = 0;
            velocidad = -velocidad;
        } else if (caja.x + caja.w > ANCHO) {
            caja.x = ANCHO - caja.w;
            velocidad = -velocidad;
        }

        /* 4. dibujar: borrar, pintar y mostrar */
        SDL_SetRenderDrawColor(pincel, 20, 20, 30, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 240, 160, 40, 255);
        SDL_RenderFillRect(pincel, &caja);
        SDL_RenderPresent(pincel);
    }

    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

SDL es la biblioteca que usan cientos de juegos comerciales, emuladores y reproductores de video para abrir ventanas, leer teclado y joystick y dibujar en cualquier sistema operativo. El bucle de juego con delta time es la base de todos los motores: Unity, Godot y Unreal hacen exactamente esto por dentro.

### Errores habituales

**Esqueleto: no enlazar SDL.** Compilar sin `$(pkg-config --libs sdl3)`:

```
undefined reference to `SDL_Init'
```

**Slime: el `.h` que no aparece.** `fatal error: SDL3/SDL.h: No such file or directory`: SDL3 no está instalada o falta `--cflags`.

**Ogro: moverse sin `dt`.** El juego va distinto en cada compu.

**Ogro: no vaciar los eventos.** Leer un solo evento por cuadro hace que la ventana tarde en responder o que el sistema diga que "no responde".

**Troll: no destruir lo que se creó.** La ventana y el renderer se devuelven al final, en orden inverso.

### Misión S01-N01-M1 · Rebote en dos ejes

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Partiendo del ejemplo, hacé que la caja se mueva en diagonal y rebote contra los **cuatro** bordes. En cada choque, cambiá el color (por ejemplo, rotando los canales R, G y B) y mostrá en el título de la ventana cuántos choques lleva (`SDL_SetWindowTitle`).

#### Criterio de aprobación

- Rebota en los cuatro bordes sin salirse de la ventana.
- Se mueve con `dt` (velocidad en píxeles por segundo).
- Cambia de color y cuenta los choques en el título.

#### Código inicial

```c
/*
 * S01-N01 - La ventana y el bucle de juego.
 * Un cuadrado que rebota de lado a lado, a la misma velocidad a 60 o a 240 FPS.
 */
#include <SDL3/SDL.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("La Forja Viva", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        fprintf(stderr, "No se pudo crear la ventana: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_FRect caja = { 100.0f, 280.0f, 40.0f, 40.0f };
    float velocidad = 220.0f;                   /* pixeles por SEGUNDO */
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();

    while (corriendo) {
        /* 1. tiempo: cuantos segundos pasaron desde el cuadro anterior */
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;                          /* si la compu se trabo, no saltar */
        }

        /* 2. entrada: todos los eventos pendientes */
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                corriendo = false;
            } else if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) {
                corriendo = false;
            }
        }

        /* 3. actualizar el mundo */
        caja.x += velocidad * dt;
        if (caja.x < 0) {
            caja.x = 0;
            velocidad = -velocidad;
        } else if (caja.x + caja.w > ANCHO) {
            caja.x = ANCHO - caja.w;
            velocidad = -velocidad;
        }

        /* 4. dibujar: borrar, pintar y mostrar */
        SDL_SetRenderDrawColor(pincel, 20, 20, 30, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 240, 160, 40, 255);
        SDL_RenderFillRect(pincel, &caja);
        SDL_RenderPresent(pincel);
    }

    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Solución de referencia

```c
/* S01-N01 Mision 1 - Rebote en dos ejes: rebota contra los cuatro bordes y cambia de color en cada choque. */
#include <SDL3/SDL.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Rebote", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_FRect caja = { 100, 100, 40, 40 };
    float vx = 220, vy = 160;
    Uint8 r = 240, g = 160, b = 40;
    int choques = 0;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        bool choco = false;
        caja.x += vx * dt;
        caja.y += vy * dt;
        if (caja.x < 0 || caja.x + caja.w > ANCHO) {
            vx = -vx;
            caja.x = caja.x < 0 ? 0 : ANCHO - caja.w;
            choco = true;
        }
        if (caja.y < 0 || caja.y + caja.h > ALTO) {
            vy = -vy;
            caja.y = caja.y < 0 ? 0 : ALTO - caja.h;
            choco = true;
        }
        if (choco) {
            choques++;
            Uint8 tmp = r;          /* rotar los canales: un color distinto en cada choque */
            r = g;
            g = b;
            b = tmp;
            char titulo[40];
            snprintf(titulo, sizeof titulo, "Rebote - choques: %d", choques);
            SDL_SetWindowTitle(ventana, titulo);
        }
        SDL_SetRenderDrawColor(pincel, 20, 20, 30, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, r, g, b, 255);
        SDL_RenderFillRect(pincel, &caja);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Misión S01-N01-M2 · Contar los cuadros

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Medí los **cuadros por segundo**: contá cuántas veces se ejecuta el bucle y, una vez por segundo, mostralo en el título. Con la tecla `V`, prendé y apagá la sincronización vertical (`SDL_SetRenderVSync`) y observá cómo cambian los FPS. Explicá en un comentario qué pasa con y sin VSync.

#### Criterio de aprobación

- Actualiza los FPS una vez por segundo con `SDL_GetTicks`.
- La tecla V alterna el VSync.
- Explica en un comentario qué cambia con y sin VSync.

#### Solución de referencia

```c
/* S01-N01 Mision 2 - Contar los cuadros: medir los FPS y mostrarlos en el titulo una vez por segundo. */
#include <SDL3/SDL.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("FPS", 640, 480, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    bool vsync = true;
    SDL_SetRenderVSync(pincel, 1);
    int cuadros = 0;
    Uint64 inicio_segundo = SDL_GetTicks();
    bool corriendo = true;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_V) {
                vsync = !vsync;                           /* V: prender o apagar la sincronizacion */
                SDL_SetRenderVSync(pincel, vsync ? 1 : 0);
            }
        }
        cuadros++;
        Uint64 ahora = SDL_GetTicks();
        if (ahora - inicio_segundo >= 1000) {
            char titulo[64];
            snprintf(titulo, sizeof titulo, "FPS: %d (VSync %s) - V para cambiar", cuadros, vsync ? "si" : "no");
            SDL_SetWindowTitle(ventana, titulo);
            cuadros = 0;
            inicio_segundo = ahora;
        }
        Uint8 brillo = (Uint8) (ahora / 8 % 256);          /* un fondo que late */
        SDL_SetRenderDrawColor(pincel, brillo / 4, 20, 40, 255);
        SDL_RenderClear(pincel);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Encargo S01-N01-E1 · El reloj del Gremio

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, c
```

#### Consigna

El Gremio quiere un reloj en la pared: tres barras horizontales que se llenan según la hora (de 24), los minutos y los segundos. Usá `time` y `localtime` para la hora actual y mostrala también en el título como `hh:mm:ss`.

#### Criterio de aprobación

- Tres barras proporcionales a hora, minuto y segundo.
- Muestra la hora en el título.

#### Solución de referencia

```c
/* S01-N01 Encargo - El reloj del Gremio: tres barras que se llenan con la hora, los minutos y los segundos. */
#include <SDL3/SDL.h>
#include <stdio.h>
#include <time.h>

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Reloj del Gremio", 600, 220, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    bool corriendo = true;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        time_t t = time(NULL);
        struct tm *hora = localtime(&t);
        float partes[3] = { hora->tm_hour / 24.0f, hora->tm_min / 60.0f, hora->tm_sec / 60.0f };
        SDL_SetRenderDrawColor(pincel, 15, 15, 25, 255);
        SDL_RenderClear(pincel);
        for (int i = 0; i < 3; i++) {
            SDL_FRect fondo = { 30, 30 + i * 60.0f, 540, 40 };
            SDL_FRect lleno = { 30, 30 + i * 60.0f, 540 * partes[i], 40 };
            SDL_SetRenderDrawColor(pincel, 50, 50, 70, 255);
            SDL_RenderFillRect(pincel, &fondo);
            SDL_SetRenderDrawColor(pincel, (Uint8) (80 + i * 70), 180, 80, 255);
            SDL_RenderFillRect(pincel, &lleno);
        }
        char titulo[48];
        snprintf(titulo, sizeof titulo, "Reloj del Gremio - %02d:%02d:%02d", hora->tm_hour, hora->tm_min, hora->tm_sec);
        SDL_SetWindowTitle(ventana, titulo);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Cuáles son las cuatro partes de cada vuelta del bucle de juego?

Medir el tiempo, leer la entrada, actualizar el mundo y dibujar.

#### ¿Para qué sirve el delta time?

Para que las velocidades estén en unidades por segundo y el juego vaya igual en una compu rápida y en una lenta.

#### ¿Qué hace `SDL_RenderPresent`?

Muestra de golpe lo que se dibujó en el lienzo oculto (doble búfer).

#### ¿Por qué `SDL_PollEvent` va dentro de un `while`?

Porque puede haber varios eventos pendientes en un mismo cuadro y hay que procesarlos todos.

#### Si aparece `undefined reference to SDL_Init`, ¿qué falta?

Enlazar la biblioteca: agregar `$(pkg-config --libs sdl3)` (o `-lSDL3`) al comando.

### Soluciones (docente)

Senda basada en `FullCursos/06-SDL3` (01 a 06). Las entregas son archivos: se prueban compilando con SDL3 (`gcc main.c $(pkg-config --cflags --libs sdl3) -lm`).

## S01-N02 · Teclado, mouse y movimiento

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: ogro
ejecutable: no
```

### Crónica

En la Forja Viva, las piezas obedecen a quien sabe hablarles. Una tecla apretada es una orden; una tecla **mantenida**, una orden que dura.

—No confundas un golpe de martillo con sostener el martillo, {heroe} —dice {mentor}—. El que no lo distingue, o no se mueve… o no para.

### Objetivos

- Distinguir **eventos** (algo que pasa una vez) del **estado** del teclado (qué está apretado ahora).
- Mover un personaje con velocidad por segundo y la diagonal normalizada.
- Usar el mouse: posición, botones y rueda.

### Antes de empezar

La ventana y el bucle de juego (S01-N01).

### Explicación

#### Eventos o estado

| Para | Se usa | Ejemplo |
|---|---|---|
| algo que pasa **una vez** | eventos (`SDL_EVENT_KEY_DOWN`) | saltar, abrir el menú, disparar |
| algo que dura **mientras** se mantiene | el estado (`SDL_GetKeyboardState`) | caminar, acelerar |

```c
const bool *teclas = SDL_GetKeyboardState(NULL);
if (teclas[SDL_SCANCODE_W]) dy -= 1;
```

- Los **scancodes** (`SDL_SCANCODE_W`) son la **posición** física de la tecla: WASD funciona igual en un teclado francés.
- Los **keycodes** (`SDLK_ESCAPE`, en `evento.key.key`) son la **letra** que produce.
- `evento.key.repeat` es verdadero cuando el evento viene de mantener la tecla apretada.

#### La diagonal

Con `dx = 1` y `dy = 1`, el vector mide √2 ≈ 1,41: en diagonal se iría un 41 % más rápido. Se **normaliza** dividiendo por su largo:

```c
float largo = sqrtf(dx * dx + dy * dy);
if (largo > 0) { dx /= largo; dy /= largo; }
```

`sqrtf` está en `<math.h>`: se compila con `-lm`.

#### El mouse

```c
if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN && evento.button.button == SDL_BUTTON_LEFT) {
    destino_x = evento.button.x;     /* en SDL3 las coordenadas son float */
}
if (evento.type == SDL_EVENT_MOUSE_WHEEL) {
    zoom += evento.wheel.y;          /* +1 o -1 por cada paso de la rueda */
}
```

`SDL_clamp(valor, mínimo, máximo)` deja un valor dentro de un rango (para no salirse de la ventana).

### Código de ejemplo

```c
/*
 * S01-N02 - Teclado y movimiento: el estado del teclado, velocidad * dt
 * y la diagonal normalizada (para no ir mas rapido en diagonal).
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("WASD para moverte - Espacio para correr", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);

    SDL_FRect heroe = { ANCHO / 2.0f, ALTO / 2.0f, 32, 32 };
    const float VELOCIDAD = 240.0f;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            /* EVENTOS: cosas que pasan una vez (apretar Escape, cerrar la ventana) */
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }

        /* ESTADO: que teclas estan apretadas AHORA (para moverse mientras se mantienen) */
        const bool *teclas = SDL_GetKeyboardState(NULL);
        float dx = 0, dy = 0;
        if (teclas[SDL_SCANCODE_W]) dy -= 1;
        if (teclas[SDL_SCANCODE_S]) dy += 1;
        if (teclas[SDL_SCANCODE_A]) dx -= 1;
        if (teclas[SDL_SCANCODE_D]) dx += 1;
        float largo = sqrtf(dx * dx + dy * dy);
        if (largo > 0) {                         /* normalizar: la diagonal no es mas rapida */
            dx /= largo;
            dy /= largo;
        }
        float velocidad = teclas[SDL_SCANCODE_SPACE] ? VELOCIDAD * 2 : VELOCIDAD;
        heroe.x += dx * velocidad * dt;
        heroe.y += dy * velocidad * dt;
        heroe.x = SDL_clamp(heroe.x, 0, ANCHO - heroe.w);
        heroe.y = SDL_clamp(heroe.y, 0, ALTO - heroe.h);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Todo juego y toda aplicación interactiva decide cómo leer la entrada: los juegos de plataformas leen el estado para caminar y los eventos para saltar; los editores de imágenes usan el mouse arrastrado para pintar; y normalizar vectores es la misma cuenta que usan los motores de física, los drones y los robots para moverse a la velocidad correcta en cualquier dirección.

### Errores habituales

**Ogro: moverse con eventos.** Mover 5 píxeles en cada `SDL_EVENT_KEY_DOWN`: el personaje se traba y depende de la repetición del teclado. Para caminar se usa el estado.

**Ogro: la diagonal rápida.** Sumar `dx` y `dy` sin normalizar.

**Esqueleto: `sqrtf` sin `-lm`.** `undefined reference to 'sqrtf'`.

**Ogro: el temblor al llegar.** Al ir hacia un punto, si el paso es más grande que la distancia que falta, el personaje se pasa, vuelve y tiembla. Si la distancia es menor que el paso, se lo pone directo en el destino.

**Goblin: coordenadas `int`.** En SDL3 las posiciones del mouse y los `SDL_FRect` son `float`.

### Misión S01-N02-M1 · El lago de hielo

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Cambiá el movimiento del ejemplo por uno con **inercia**: las teclas empujan (aceleración de 900 píxeles/s²), un roce frena de a poco y la rapidez máxima es de 320 píxeles/s. Al chocar con un borde, el héroe rebota perdiendo la mitad de la velocidad. Tiene que sentirse como patinar.

#### Criterio de aprobación

- Guarda la velocidad entre cuadros (`vx`, `vy`).
- Aceleración, roce y velocidad máxima usan `dt`.
- Rebota en los bordes perdiendo velocidad.

#### Código inicial

```c
/*
 * S01-N02 - Teclado y movimiento: el estado del teclado, velocidad * dt
 * y la diagonal normalizada (para no ir mas rapido en diagonal).
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("WASD para moverte - Espacio para correr", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);

    SDL_FRect heroe = { ANCHO / 2.0f, ALTO / 2.0f, 32, 32 };
    const float VELOCIDAD = 240.0f;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            /* EVENTOS: cosas que pasan una vez (apretar Escape, cerrar la ventana) */
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }

        /* ESTADO: que teclas estan apretadas AHORA (para moverse mientras se mantienen) */
        const bool *teclas = SDL_GetKeyboardState(NULL);
        float dx = 0, dy = 0;
        if (teclas[SDL_SCANCODE_W]) dy -= 1;
        if (teclas[SDL_SCANCODE_S]) dy += 1;
        if (teclas[SDL_SCANCODE_A]) dx -= 1;
        if (teclas[SDL_SCANCODE_D]) dx += 1;
        float largo = sqrtf(dx * dx + dy * dy);
        if (largo > 0) {                         /* normalizar: la diagonal no es mas rapida */
            dx /= largo;
            dy /= largo;
        }
        float velocidad = teclas[SDL_SCANCODE_SPACE] ? VELOCIDAD * 2 : VELOCIDAD;
        heroe.x += dx * velocidad * dt;
        heroe.y += dy * velocidad * dt;
        heroe.x = SDL_clamp(heroe.x, 0, ANCHO - heroe.w);
        heroe.y = SDL_clamp(heroe.y, 0, ALTO - heroe.h);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Solución de referencia

```c
/*
 * S01-N02 Mision 1 - Aceleracion e inercia: el heroe acelera y frena de a poco,
 * como si patinara sobre el hielo del lago de la Forja.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Hielo: WASD", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);

    SDL_FRect heroe = { ANCHO / 2.0f, ALTO / 2.0f, 32, 32 };
    const float MAXIMA = 320.0f, ACELERACION = 900.0f, ROCE = 3.0f;
    float vx = 0, vy = 0;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            /* EVENTOS: cosas que pasan una vez (apretar Escape, cerrar la ventana) */
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }

        /* ESTADO: que teclas estan apretadas AHORA (para moverse mientras se mantienen) */
        const bool *teclas = SDL_GetKeyboardState(NULL);
        float dx = 0, dy = 0;
        if (teclas[SDL_SCANCODE_W]) dy -= 1;
        if (teclas[SDL_SCANCODE_S]) dy += 1;
        if (teclas[SDL_SCANCODE_A]) dx -= 1;
        if (teclas[SDL_SCANCODE_D]) dx += 1;
        float largo = sqrtf(dx * dx + dy * dy);
        if (largo > 0) {                         /* normalizar: la diagonal no es mas rapida */
            dx /= largo;
            dy /= largo;
        }
        vx += dx * ACELERACION * dt;             /* la tecla empuja */
        vy += dy * ACELERACION * dt;
        vx -= vx * ROCE * dt;                    /* el roce frena de a poco */
        vy -= vy * ROCE * dt;
        float rapidez = sqrtf(vx * vx + vy * vy);
        if (rapidez > MAXIMA) {
            vx = vx / rapidez * MAXIMA;
            vy = vy / rapidez * MAXIMA;
        }
        heroe.x += vx * dt;
        heroe.y += vy * dt;
        if (heroe.x <= 0 || heroe.x >= ANCHO - heroe.w) {
            vx = -vx * 0.5f;                     /* rebota perdiendo fuerza */
        }
        if (heroe.y <= 0 || heroe.y >= ALTO - heroe.h) {
            vy = -vy * 0.5f;
        }
        heroe.x = SDL_clamp(heroe.x, 0, ANCHO - heroe.w);
        heroe.y = SDL_clamp(heroe.y, 0, ALTO - heroe.h);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Misión S01-N02-M2 · Ir adonde hacés clic

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Con el botón izquierdo del mouse, marcá un destino: el héroe va hacia ahí a 300 píxeles por segundo y se detiene justo encima, sin temblar. Dibujá una línea (`SDL_RenderLine`) desde el héroe hasta el destino. La rueda del mouse cambia el tamaño del héroe entre 12 y 96 píxeles.

#### Criterio de aprobación

- Se mueve hacia el clic con velocidad por segundo.
- Llega sin pasarse ni temblar.
- La rueda cambia el tamaño dentro de los límites.

#### Solución de referencia

```c
/* S01-N02 Mision 2 - El mouse: el heroe va hacia donde hacés clic, y la rueda cambia su tamanio. */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Clic para ir - rueda para cambiar el tamanio", 800, 600, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    float x = 400, y = 300, destino_x = 400, destino_y = 300, lado = 32;
    const float VELOCIDAD = 300.0f;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_MOUSE_BUTTON_DOWN && e.button.button == SDL_BUTTON_LEFT) {
                destino_x = e.button.x;
                destino_y = e.button.y;
            } else if (e.type == SDL_EVENT_MOUSE_WHEEL) {
                lado = SDL_clamp(lado + e.wheel.y * 4, 12, 96);
            }
        }
        float dx = destino_x - x, dy = destino_y - y;
        float distancia = sqrtf(dx * dx + dy * dy);
        float paso = VELOCIDAD * dt;
        if (distancia <= paso) {                 /* llego: no pasarse ni temblar */
            x = destino_x;
            y = destino_y;
        } else {
            x += dx / distancia * paso;
            y += dy / distancia * paso;
        }
        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 240, 90, 90, 255);
        SDL_RenderLine(pincel, x, y, destino_x, destino_y);
        SDL_FRect heroe = { x - lado / 2, y - lado / 2, lado, lado };
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Encargo S01-N02-E1 · El tablero de dibujo

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, c
```

#### Consigna

Para la escuela del Gremio: un tablero para dibujar con el mouse. Mientras el botón está apretado, cada movimiento deja un punto (guardalos en un array con su color, sin pasarte de su tamaño). Las teclas `1`, `2` y `3` eligen el color y `C` borra todo.

#### Criterio de aprobación

- Pinta solo mientras el botón está apretado.
- Guarda los puntos en un array sin desbordarlo.
- Cambia de color y borra con el teclado.

#### Solución de referencia

```c
/* S01-N02 Encargo - El tablero de dibujo del Gremio: pintar con el mouse, C borra, 1-3 eligen color. */
#include <SDL3/SDL.h>
#include <stdio.h>

#define MAX_PUNTOS 5000

typedef struct {
    float x, y;
    Uint8 color;
} Punto;

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Tablero: arrastra para pintar - 1 2 3 color - C borra", 800, 600, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    static Punto puntos[MAX_PUNTOS];
    int cantidad = 0;
    Uint8 color = 0;
    const Uint8 PALETA[3][3] = { { 240, 200, 60 }, { 90, 200, 240 }, { 240, 90, 90 } };
    bool pintando = false, corriendo = true;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_MOUSE_BUTTON_DOWN) {
                pintando = true;
            } else if (e.type == SDL_EVENT_MOUSE_BUTTON_UP) {
                pintando = false;
            } else if (e.type == SDL_EVENT_MOUSE_MOTION && pintando && cantidad < MAX_PUNTOS) {
                puntos[cantidad++] = (Punto) { e.motion.x, e.motion.y, color };
            } else if (e.type == SDL_EVENT_KEY_DOWN) {
                if (e.key.key == SDLK_C) cantidad = 0;
                if (e.key.key == SDLK_1) color = 0;
                if (e.key.key == SDLK_2) color = 1;
                if (e.key.key == SDLK_3) color = 2;
            }
        }
        SDL_SetRenderDrawColor(pincel, 20, 20, 28, 255);
        SDL_RenderClear(pincel);
        for (int i = 0; i < cantidad; i++) {
            const Uint8 *c = PALETA[puntos[i].color];
            SDL_SetRenderDrawColor(pincel, c[0], c[1], c[2], 255);
            SDL_FRect p = { puntos[i].x - 3, puntos[i].y - 3, 6, 6 };
            SDL_RenderFillRect(pincel, &p);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Cuándo conviene un evento y cuándo el estado del teclado?

El evento, para acciones que pasan una vez (saltar, pausar); el estado, para lo que dura mientras se mantiene apretado (caminar).

#### ¿Por qué se normaliza el vector de movimiento?

Para que en diagonal no se mueva más rápido: el vector (1, 1) mide √2.

#### ¿Qué diferencia hay entre un scancode y un keycode?

El scancode es la posición física de la tecla; el keycode, la letra que produce según la distribución del teclado.

#### ¿Qué indica `evento.key.repeat`?

Que el evento viene de mantener la tecla apretada (repetición), no de apretarla de nuevo.

### Soluciones (docente)

Basado en `06-SDL3` (04 Teclado, 05 Mouse, 09 Movimiento, 10 DeltaTime).

## S01-N03 · Colisiones y enemigos

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: orco
ejecutable: no
```

### Crónica

En la Forja Viva las piezas chocan. Algunas son paredes que no se mueven; otras, criaturas de hierro que te siguen el rastro.

—Saber **cuándo** dos cosas se tocan es la mitad de cualquier juego, {heroe} —dice {mentor}—. La otra mitad es decidir qué pasa después.

### Objetivos

- Detectar si dos rectángulos se tocan (AABB).
- Frenar contra las paredes resolviendo **eje por eje**, para deslizarse en lugar de trabarse.
- Programar enemigos simples: perseguir y patrullar.
- Usar colores con transparencia (alfa) y muchos objetos a la vez en un array.

### Antes de empezar

Teclado, mouse y movimiento (S01-N02).

### Explicación

#### ¿Se tocan?

Dos rectángulos alineados con los ejes (*AABB*) se tocan si se superponen **en los dos ejes a la vez**:

```c
bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x &&
           a.y < b.y + b.h && a.y + a.h > b.y;
}
```

#### Eje por eje

Si se mueve en diagonal y choca, volver atrás los dos ejes deja al personaje **pegado** a la pared. Moviendo primero en `x` (y deshaciendo solo `x` si choca) y después en `y`, se **desliza** a lo largo de la pared:

```c
mover_eje(&heroe, dx * velocidad * dt, 0, paredes, n);
mover_eje(&heroe, 0, dy * velocidad * dt, paredes, n);
```

#### Enemigos simples

- **Perseguir**: el vector del enemigo al héroe, normalizado, por la velocidad del enemigo.
- **Patrullar**: ir y volver entre dos puntos, dando vuelta el sentido en cada extremo.
- **Ver**: perseguir solo si la distancia es menor que un radio.

#### Transparencia

Con `SDL_SetRenderDrawBlendMode(pincel, SDL_BLENDMODE_BLEND)`, el cuarto valor del color (**alfa**, de 0 a 255) es la opacidad: 255 es sólido y 70, un velo que deja ver lo de abajo.

#### Muchas cosas a la vez

Chispas, balas, enemigos: se guardan en un **array de structs** con un campo que dice si están activos (o cuánto les queda de vida). En cada cuadro se actualizan y se dibujan solo los activos, y los lugares libres se reutilizan. `SDL_rand(n)` da un número al azar de 0 a n − 1.

### Código de ejemplo

```c
/*
 * S01-N03 - Colisiones: rectangulos que se tocan (AABB), paredes que frenan
 * resolviendo eje por eje, y un enemigo que persigue.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

static bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Mueve en un eje; si choca una pared, vuelve atras en ese eje y devuelve true. */
static bool mover_eje(SDL_FRect *r, float dx, float dy, const SDL_FRect *paredes, int n)
{
    r->x += dx;
    r->y += dy;
    for (int i = 0; i < n; i++) {
        if (se_tocan(*r, paredes[i])) {
            r->x -= dx;
            r->y -= dy;
            return true;
        }
    }
    return false;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Colisiones - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    SDL_SetRenderDrawBlendMode(pincel, SDL_BLENDMODE_BLEND);

    SDL_FRect paredes[] = { { 0, 0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 }, { 0, 0, 20, ALTO },
                            { ANCHO - 20, 0, 20, ALTO }, { 250, 150, 300, 24 }, { 390, 300, 24, 200 } };
    const int N = (int) (sizeof paredes / sizeof paredes[0]);
    SDL_FRect heroe = { 100, 100, 30, 30 }, enemigo = { 650, 450, 28, 28 };
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool *t = SDL_GetKeyboardState(NULL);
        float dx = (float) (t[SDL_SCANCODE_D] - t[SDL_SCANCODE_A]);
        float dy = (float) (t[SDL_SCANCODE_S] - t[SDL_SCANCODE_W]);
        mover_eje(&heroe, dx * 250 * dt, 0, paredes, N);   /* eje por eje: asi se desliza contra la pared */
        mover_eje(&heroe, 0, dy * 250 * dt, paredes, N);

        float ex = heroe.x - enemigo.x, ey = heroe.y - enemigo.y;
        float d = sqrtf(ex * ex + ey * ey);
        if (d > 1) {
            mover_eje(&enemigo, ex / d * 110 * dt, 0, paredes, N);
            mover_eje(&enemigo, 0, ey / d * 110 * dt, paredes, N);
        }
        bool atrapado = se_tocan(heroe, enemigo);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 110, 110, 130, 255);
        SDL_RenderFillRects(pincel, paredes, N);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_SetRenderDrawColor(pincel, 230, 70, 60, 255);
        SDL_RenderFillRect(pincel, &enemigo);
        if (atrapado) {                                   /* un velo rojo semitransparente */
            SDL_SetRenderDrawColor(pincel, 255, 0, 0, 70);
            SDL_FRect todo = { 0, 0, ANCHO, ALTO };
            SDL_RenderFillRect(pincel, &todo);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

La detección AABB es la primera prueba de colisión de casi todos los motores de juegos y de física (antes de probar formas más complejas), y también se usa en las interfaces gráficas para saber sobre qué botón está el mouse. Los sistemas de partículas (chispas, humo, lluvia) son arrays de structs que se actualizan en cada cuadro, como en esta unidad.

### Errores habituales

**Ogro: `<=` en lugar de `<`.** Con `<=`, dos rectángulos que apenas se rozan por el borde cuentan como chocados.

**Ogro: resolver los dos ejes juntos.** El personaje queda trabado contra la pared en lugar de deslizarse.

**Ogro: el túnel.** Con un `dt` muy grande, algo rápido puede atravesar una pared fina de un cuadro al otro. Por eso se limita `dt` (`if (dt > 0.1f) dt = 0.1f;`).

**Orco: el array de partículas lleno.** Escribir una chispa nueva sin buscar un lugar libre desborda el array.

**Slime: el alfa que no se ve.** Sin `SDL_BLENDMODE_BLEND`, el alfa se ignora y todo es sólido.

### Misión S01-N03-M1 · Las chispas

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Cuando el héroe **empieza** a chocar con una pared, soltá 12 chispas desde su centro en direcciones al azar (`SDL_rand`). Guardalas en un array de hasta 200 structs (posición, velocidad y vida en segundos); cada una dura 0,6 segundos y se desvanece bajando el alfa. Reutilizá los lugares de las chispas apagadas.

#### Criterio de aprobación

- Suelta chispas solo al empezar el choque, no en cada cuadro.
- Las guarda en un array sin desbordarlo, reutilizando las apagadas.
- Se desvanecen con el alfa.

#### Código inicial

```c
/*
 * S01-N03 - Colisiones: rectangulos que se tocan (AABB), paredes que frenan
 * resolviendo eje por eje, y un enemigo que persigue.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

static bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Mueve en un eje; si choca una pared, vuelve atras en ese eje y devuelve true. */
static bool mover_eje(SDL_FRect *r, float dx, float dy, const SDL_FRect *paredes, int n)
{
    r->x += dx;
    r->y += dy;
    for (int i = 0; i < n; i++) {
        if (se_tocan(*r, paredes[i])) {
            r->x -= dx;
            r->y -= dy;
            return true;
        }
    }
    return false;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Colisiones - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    SDL_SetRenderDrawBlendMode(pincel, SDL_BLENDMODE_BLEND);

    SDL_FRect paredes[] = { { 0, 0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 }, { 0, 0, 20, ALTO },
                            { ANCHO - 20, 0, 20, ALTO }, { 250, 150, 300, 24 }, { 390, 300, 24, 200 } };
    const int N = (int) (sizeof paredes / sizeof paredes[0]);
    SDL_FRect heroe = { 100, 100, 30, 30 }, enemigo = { 650, 450, 28, 28 };
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool *t = SDL_GetKeyboardState(NULL);
        float dx = (float) (t[SDL_SCANCODE_D] - t[SDL_SCANCODE_A]);
        float dy = (float) (t[SDL_SCANCODE_S] - t[SDL_SCANCODE_W]);
        mover_eje(&heroe, dx * 250 * dt, 0, paredes, N);   /* eje por eje: asi se desliza contra la pared */
        mover_eje(&heroe, 0, dy * 250 * dt, paredes, N);

        float ex = heroe.x - enemigo.x, ey = heroe.y - enemigo.y;
        float d = sqrtf(ex * ex + ey * ey);
        if (d > 1) {
            mover_eje(&enemigo, ex / d * 110 * dt, 0, paredes, N);
            mover_eje(&enemigo, 0, ey / d * 110 * dt, paredes, N);
        }
        bool atrapado = se_tocan(heroe, enemigo);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 110, 110, 130, 255);
        SDL_RenderFillRects(pincel, paredes, N);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_SetRenderDrawColor(pincel, 230, 70, 60, 255);
        SDL_RenderFillRect(pincel, &enemigo);
        if (atrapado) {                                   /* un velo rojo semitransparente */
            SDL_SetRenderDrawColor(pincel, 255, 0, 0, 70);
            SDL_FRect todo = { 0, 0, ANCHO, ALTO };
            SDL_RenderFillRect(pincel, &todo);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Solución de referencia

```c
/*
 * S01-N03 Mision 1 - Las chispas: particulas que salen del heroe cuando choca con una pared,
 * guardadas en un array y que se desvanecen con el alfa.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600
#define MAX_CHISPAS 200

typedef struct {
    float x, y, vx, vy, vida;   /* vida en segundos: al llegar a 0 la chispa se apaga */
} Chispa;

static Chispa chispas[MAX_CHISPAS];

static void soltar_chispas(float x, float y)
{
    int soltadas = 0;
    for (int i = 0; i < MAX_CHISPAS && soltadas < 12; i++) {
        if (chispas[i].vida <= 0) {                      /* reutilizar un lugar libre */
            float angulo = (float) SDL_rand(360) * 3.14159f / 180.0f;
            float rapidez = 80.0f + (float) SDL_rand(160);
            chispas[i] = (Chispa) { x, y, cosf(angulo) * rapidez, sinf(angulo) * rapidez, 0.6f };
            soltadas++;
        }
    }
}

static bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Mueve en un eje; si choca una pared, vuelve atras en ese eje y devuelve true. */
static bool mover_eje(SDL_FRect *r, float dx, float dy, const SDL_FRect *paredes, int n)
{
    r->x += dx;
    r->y += dy;
    for (int i = 0; i < n; i++) {
        if (se_tocan(*r, paredes[i])) {
            r->x -= dx;
            r->y -= dy;
            return true;
        }
    }
    return false;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Colisiones - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    SDL_SetRenderDrawBlendMode(pincel, SDL_BLENDMODE_BLEND);

    SDL_FRect paredes[] = { { 0, 0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 }, { 0, 0, 20, ALTO },
                            { ANCHO - 20, 0, 20, ALTO }, { 250, 150, 300, 24 }, { 390, 300, 24, 200 } };
    const int N = (int) (sizeof paredes / sizeof paredes[0]);
    SDL_FRect heroe = { 100, 100, 30, 30 }, enemigo = { 650, 450, 28, 28 };
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool *t = SDL_GetKeyboardState(NULL);
        float dx = (float) (t[SDL_SCANCODE_D] - t[SDL_SCANCODE_A]);
        float dy = (float) (t[SDL_SCANCODE_S] - t[SDL_SCANCODE_W]);
        bool choco = mover_eje(&heroe, dx * 250 * dt, 0, paredes, N);
        choco = mover_eje(&heroe, 0, dy * 250 * dt, paredes, N) || choco;
        static bool chocaba = false;
        if (choco && !chocaba) {                          /* solo al empezar a chocar, no en cada cuadro */
            soltar_chispas(heroe.x + heroe.w / 2, heroe.y + heroe.h / 2);
        }
        chocaba = choco;
        for (int i = 0; i < MAX_CHISPAS; i++) {
            if (chispas[i].vida > 0) {
                chispas[i].x += chispas[i].vx * dt;
                chispas[i].y += chispas[i].vy * dt;
                chispas[i].vida -= dt;
            }
        }

        float ex = heroe.x - enemigo.x, ey = heroe.y - enemigo.y;
        float d = sqrtf(ex * ex + ey * ey);
        if (d > 1) {
            mover_eje(&enemigo, ex / d * 110 * dt, 0, paredes, N);
            mover_eje(&enemigo, 0, ey / d * 110 * dt, paredes, N);
        }
        bool atrapado = se_tocan(heroe, enemigo);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 110, 110, 130, 255);
        SDL_RenderFillRects(pincel, paredes, N);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_SetRenderDrawColor(pincel, 230, 70, 60, 255);
        SDL_RenderFillRect(pincel, &enemigo);
        for (int i = 0; i < MAX_CHISPAS; i++) {
            if (chispas[i].vida > 0) {
                SDL_SetRenderDrawColor(pincel, 255, 200, 60, (Uint8) (255 * chispas[i].vida / 0.6f));
                SDL_FRect p = { chispas[i].x, chispas[i].y, 4, 4 };
                SDL_RenderFillRect(pincel, &p);
            }
        }
        if (atrapado) {                                   /* un velo rojo semitransparente */
            SDL_SetRenderDrawColor(pincel, 255, 0, 0, 70);
            SDL_FRect todo = { 0, 0, ANCHO, ALTO };
            SDL_RenderFillRect(pincel, &todo);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Misión S01-N03-M2 · La patrulla

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Reemplazá al perseguidor por **tres guardias** en un array: cada uno patrulla entre dos puntos en `x` y solo persigue al héroe si está a menos de 180 píxeles. Si cualquiera lo toca, se muestra el velo rojo.

#### Criterio de aprobación

- Los guardias están en un array de structs.
- Patrullan entre dos puntos y persiguen solo dentro del radio.
- La colisión con cualquiera se detecta.

#### Código inicial

```c
/*
 * S01-N03 - Colisiones: rectangulos que se tocan (AABB), paredes que frenan
 * resolviendo eje por eje, y un enemigo que persigue.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

static bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Mueve en un eje; si choca una pared, vuelve atras en ese eje y devuelve true. */
static bool mover_eje(SDL_FRect *r, float dx, float dy, const SDL_FRect *paredes, int n)
{
    r->x += dx;
    r->y += dy;
    for (int i = 0; i < n; i++) {
        if (se_tocan(*r, paredes[i])) {
            r->x -= dx;
            r->y -= dy;
            return true;
        }
    }
    return false;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Colisiones - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    SDL_SetRenderDrawBlendMode(pincel, SDL_BLENDMODE_BLEND);

    SDL_FRect paredes[] = { { 0, 0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 }, { 0, 0, 20, ALTO },
                            { ANCHO - 20, 0, 20, ALTO }, { 250, 150, 300, 24 }, { 390, 300, 24, 200 } };
    const int N = (int) (sizeof paredes / sizeof paredes[0]);
    SDL_FRect heroe = { 100, 100, 30, 30 }, enemigo = { 650, 450, 28, 28 };
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool *t = SDL_GetKeyboardState(NULL);
        float dx = (float) (t[SDL_SCANCODE_D] - t[SDL_SCANCODE_A]);
        float dy = (float) (t[SDL_SCANCODE_S] - t[SDL_SCANCODE_W]);
        mover_eje(&heroe, dx * 250 * dt, 0, paredes, N);   /* eje por eje: asi se desliza contra la pared */
        mover_eje(&heroe, 0, dy * 250 * dt, paredes, N);

        float ex = heroe.x - enemigo.x, ey = heroe.y - enemigo.y;
        float d = sqrtf(ex * ex + ey * ey);
        if (d > 1) {
            mover_eje(&enemigo, ex / d * 110 * dt, 0, paredes, N);
            mover_eje(&enemigo, 0, ey / d * 110 * dt, paredes, N);
        }
        bool atrapado = se_tocan(heroe, enemigo);

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 110, 110, 130, 255);
        SDL_RenderFillRects(pincel, paredes, N);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_SetRenderDrawColor(pincel, 230, 70, 60, 255);
        SDL_RenderFillRect(pincel, &enemigo);
        if (atrapado) {                                   /* un velo rojo semitransparente */
            SDL_SetRenderDrawColor(pincel, 255, 0, 0, 70);
            SDL_FRect todo = { 0, 0, ANCHO, ALTO };
            SDL_RenderFillRect(pincel, &todo);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Solución de referencia

```c
/*
 * S01-N03 Mision 2 - La patrulla: tres guardias que van y vienen entre dos puntos
 * y solo persiguen si el heroe se acerca a menos de 180 pixeles.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600

typedef struct {
    SDL_FRect caja;
    float desde_x, hasta_x, sentido;
} Guardia;

static bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Mueve en un eje; si choca una pared, vuelve atras en ese eje y devuelve true. */
static bool mover_eje(SDL_FRect *r, float dx, float dy, const SDL_FRect *paredes, int n)
{
    r->x += dx;
    r->y += dy;
    for (int i = 0; i < n; i++) {
        if (se_tocan(*r, paredes[i])) {
            r->x -= dx;
            r->y -= dy;
            return true;
        }
    }
    return false;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Colisiones - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    SDL_SetRenderDrawBlendMode(pincel, SDL_BLENDMODE_BLEND);

    SDL_FRect paredes[] = { { 0, 0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 }, { 0, 0, 20, ALTO },
                            { ANCHO - 20, 0, 20, ALTO }, { 250, 150, 300, 24 }, { 390, 300, 24, 200 } };
    const int N = (int) (sizeof paredes / sizeof paredes[0]);
    SDL_FRect heroe = { 100, 100, 30, 30 };
    Guardia guardias[] = { { { 480, 80, 28, 28 }, 440, 720, 1 }, { { 100, 520, 28, 28 }, 60, 340, 1 }, { { 600, 380, 28, 28 }, 450, 740, -1 } };
    const int G = (int) (sizeof guardias / sizeof guardias[0]);
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool *t = SDL_GetKeyboardState(NULL);
        float dx = (float) (t[SDL_SCANCODE_D] - t[SDL_SCANCODE_A]);
        float dy = (float) (t[SDL_SCANCODE_S] - t[SDL_SCANCODE_W]);
        mover_eje(&heroe, dx * 250 * dt, 0, paredes, N);   /* eje por eje: asi se desliza contra la pared */
        mover_eje(&heroe, 0, dy * 250 * dt, paredes, N);

        bool atrapado = false;
        for (int g = 0; g < G; g++) {
            SDL_FRect *c = &guardias[g].caja;
            float ex = heroe.x - c->x, ey = heroe.y - c->y;
            float d = sqrtf(ex * ex + ey * ey);
            if (d < 180 && d > 1) {                         /* te vio: persigue */
                mover_eje(c, ex / d * 120 * dt, 0, paredes, N);
                mover_eje(c, 0, ey / d * 120 * dt, paredes, N);
            } else {                                        /* patrulla entre dos puntos */
                c->x += guardias[g].sentido * 80 * dt;
                if (c->x < guardias[g].desde_x || c->x > guardias[g].hasta_x) {
                    guardias[g].sentido = -guardias[g].sentido;
                }
            }
            atrapado = atrapado || se_tocan(heroe, *c);
        }

        SDL_SetRenderDrawColor(pincel, 25, 25, 35, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 110, 110, 130, 255);
        SDL_RenderFillRects(pincel, paredes, N);
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_SetRenderDrawColor(pincel, 230, 70, 60, 255);
        for (int g = 0; g < G; g++) {
            SDL_RenderFillRect(pincel, &guardias[g].caja);
        }
        if (atrapado) {                                   /* un velo rojo semitransparente */
            SDL_SetRenderDrawColor(pincel, 255, 0, 0, 70);
            SDL_FRect todo = { 0, 0, ANCHO, ALTO };
            SDL_RenderFillRect(pincel, &todo);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Encargo S01-N03-E1 · Los botones del Gremio

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, c
```

#### Consigna

Dibujá tres botones (Comprar, Vender, Salir) con su texto (`SDL_RenderDebugText`). Se iluminan cuando el mouse pasa por encima (la misma prueba de "punto dentro de un rectángulo"), cuentan los clics en el título, y Salir cierra el programa.

#### Criterio de aprobación

- Detecta si el mouse está sobre cada botón.
- Cuenta los clics y los muestra.
- Salir termina el programa.

#### Solución de referencia

```c
/* S01-N03 Encargo - Los botones del Gremio: se iluminan con el mouse y cuentan clics. */
#include <SDL3/SDL.h>
#include <stdio.h>

typedef struct {
    SDL_FRect caja;
    const char *nombre;
    int clics;
} Boton;

static bool adentro(SDL_FRect r, float x, float y)
{
    return x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Botones del Gremio", 640, 240, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    Boton botones[] = { { { 40, 80, 160, 70 }, "Comprar", 0 }, { { 240, 80, 160, 70 }, "Vender", 0 }, { { 440, 80, 160, 70 }, "Salir", 0 } };
    bool corriendo = true;
    float mx = -1, my = -1;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_MOUSE_MOTION) {
                mx = e.motion.x;
                my = e.motion.y;
            } else if (e.type == SDL_EVENT_MOUSE_BUTTON_DOWN) {
                for (int i = 0; i < 3; i++) {
                    if (adentro(botones[i].caja, e.button.x, e.button.y)) {
                        botones[i].clics++;
                        if (i == 2) {
                            corriendo = false;
                        }
                    }
                }
                char titulo[80];
                snprintf(titulo, sizeof titulo, "Comprar: %d  Vender: %d", botones[0].clics, botones[1].clics);
                SDL_SetWindowTitle(ventana, titulo);
            }
        }
        SDL_SetRenderDrawColor(pincel, 20, 22, 30, 255);
        SDL_RenderClear(pincel);
        for (int i = 0; i < 3; i++) {
            bool encima = adentro(botones[i].caja, mx, my);
            SDL_SetRenderDrawColor(pincel, encima ? 90 : 55, encima ? 170 : 90, encima ? 230 : 130, 255);
            SDL_RenderFillRect(pincel, &botones[i].caja);
            SDL_SetRenderDrawColor(pincel, 230, 230, 240, 255);
            SDL_RenderRect(pincel, &botones[i].caja);
            SDL_RenderDebugText(pincel, botones[i].caja.x + 16, botones[i].caja.y + 30, botones[i].nombre);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Qué condición cumplen dos rectángulos que se tocan?

Se superponen en `x` y en `y` a la vez: cada uno empieza antes de que termine el otro, en los dos ejes.

#### ¿Por qué conviene resolver las colisiones eje por eje?

Para que el personaje se deslice a lo largo de la pared en lugar de quedar trabado.

#### ¿Qué es el alfa y qué hay que activar para que funcione?

Es la opacidad del color; hay que activar `SDL_BLENDMODE_BLEND`.

#### ¿Cómo se agregan partículas sin desbordar el array?

Buscando un lugar libre (una partícula apagada) y, si no hay, no agregando.

### Soluciones (docente)

Basado en `06-SDL3` (07 Rectángulos, 08 Color, 11 JugadorEnemigo, 12 Colisiones).

## S01-N04 · Jefe de la Forja Viva: la Salamandra del Horno

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
ejecutable: no
insignia: Domador de la Salamandra
insignia_descripcion: Venciste a la Salamandra del Horno: hiciste un videojuego completo en C con SDL3.
```

### Crónica

En el corazón de la Forja Viva vive la **Salamandra del Horno**: rápida, incansable, y te sigue a donde vayas. Entre las paredes brillan monedas de fuego frío. Si las juntás todas antes de que te alcance, la Salamandra se duerme.

—Ya tenés todo, {heroe} —dice {mentor}—: el bucle, el teclado, los choques y un enemigo. Ahora juntalo en un juego que alguien quiera jugar dos veces.

### Objetivos

- Escribir un videojuego completo con estados (jugando, ganaste, perdiste).
- Separar los **datos** del juego (niveles) del código que los usa.
- Terminar un proyecto: que se pueda ganar, perder y volver a jugar.

### Antes de empezar

Toda la Senda de la Forja Viva.

### Explicación

#### El proyecto

El punto de partida es *Junta las monedas* (el código de ejemplo, de `FullCursos/06-SDL3/13-Proyecto`): WASD para moverse, paredes, monedas y un enemigo que persigue. Todo en un solo archivo.

#### Estados del juego

Un `enum` con los estados (`JUGANDO`, `GANASTE`, `PERDISTE`) decide qué se actualiza: cuando terminó, el mundo se congela pero la ventana sigue respondiendo.

#### Datos, no código

Para tener varios niveles no se copian tres veces las paredes: cada nivel se guarda como **datos** en un array de structs (sus paredes y sus gemas, con su cantidad) y el mismo código juega cualquiera. Agregar un nivel es agregar una fila: la misma idea que las tablas de acciones del camino principal.

#### Texto en pantalla

`SDL_RenderDebugText(pincel, x, y, "texto")` escribe con una letra simple incorporada en SDL3 (sin tildes ni eñes): alcanza para marcadores y mensajes. Para letras lindas hace falta otra biblioteca (SDL_ttf).

### Código de ejemplo

```c
#include <SDL3/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

/*
 * Proyecto de cierre de la etapa 06 (SDL3 en C, un solo archivo).
 *
 * "Junta las monedas": mueve al jugador con WASD por un cuarto con paredes,
 * junta las 6 monedas y evita al enemigo que te persigue.
 *   - ganas si juntas todas las monedas
 *   - perdes si el enemigo te toca
 *
 * Integra: game loop + dt, teclado por estado, colisiones AABB (jugador-pared,
 * jugador-moneda, jugador-enemigo), IA de persecucion, estados de juego.
 *
 * El HUD (monedas restantes / resultado) va en el titulo de la ventana, para no
 * meter todavia una libreria de fuentes (eso es 07-SDL3-Cpp).
 */

#define ANCHO 800
#define ALTO  600
#define N_MONEDAS 6

typedef enum { JUGANDO, GANASTE, PERDISTE } Estado;

static bool aabb(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x &&
           a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(int argc, char **argv)
{
    double limite = (argc > 1) ? SDL_atof(argv[1]) : 0.0;

    if (!SDL_Init(SDL_INIT_VIDEO)) { fprintf(stderr, "%s\n", SDL_GetError()); return 1; }
    SDL_Window   *ventana  = SDL_CreateWindow("Junta las monedas - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(ventana, NULL);
    if (!ventana || !renderer) { SDL_Quit(); return 1; }
    SDL_SetRenderVSync(renderer, 1);

    SDL_FRect paredes[] = {
        {   0,   0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 },
        {   0,   0, 20, ALTO },  { ANCHO - 20, 0, 20, ALTO },
        { 180, 120, 260, 24 }, { 360, 300, 24, 200 }, { 500, 160, 24, 200 },
    };
    const int n_paredes = (int)(sizeof(paredes) / sizeof(paredes[0]));

    SDL_FRect monedas[N_MONEDAS] = {
        {  90,  90, 16, 16 }, { 700,  90, 16, 16 }, { 120, 460, 16, 16 },
        { 660, 500, 16, 16 }, { 300, 250, 16, 16 }, { 430, 420, 16, 16 },
    };
    bool tomada[N_MONEDAS] = { false };
    int  faltan = N_MONEDAS;

    SDL_FRect jugador = { ANCHO / 2.0f, ALTO / 2.0f, 30, 30 };
    SDL_FRect enemigo = { 60, ALTO - 60.0f, 28, 28 };
    const float VEL_J = 260.0f;
    const float VEL_E = 130.0f;

    Estado estado = JUGANDO;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    Uint64 inicio = antes;
    char titulo[128];

    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float)(ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) dt = 0.1f;

        SDL_Event ev;
        while (SDL_PollEvent(&ev)) {
            if (ev.type == SDL_EVENT_QUIT) corriendo = false;
            if (ev.type == SDL_EVENT_KEY_DOWN) {
                if (ev.key.key == SDLK_ESCAPE) corriendo = false;
                if (ev.key.key == SDLK_R && estado != JUGANDO) {
                    /* reiniciar */
                    for (int i = 0; i < N_MONEDAS; i++) tomada[i] = false;
                    faltan = N_MONEDAS;
                    jugador.x = ANCHO / 2.0f; jugador.y = ALTO / 2.0f;
                    enemigo.x = 60; enemigo.y = ALTO - 60.0f;
                    estado = JUGANDO;
                }
            }
        }

        if (estado == JUGANDO) {
            /* --- jugador --- */
            const bool *k = SDL_GetKeyboardState(NULL);
            float dx = 0, dy = 0;
            if (k[SDL_SCANCODE_W]) dy -= 1;
            if (k[SDL_SCANCODE_S]) dy += 1;
            if (k[SDL_SCANCODE_A]) dx -= 1;
            if (k[SDL_SCANCODE_D]) dx += 1;
            float l = sqrtf(dx * dx + dy * dy);
            if (l > 0) { dx /= l; dy /= l; }

            jugador.x += dx * VEL_J * dt;
            for (int i = 0; i < n_paredes; i++)
                if (aabb(jugador, paredes[i]))
                    jugador.x = (dx > 0) ? paredes[i].x - jugador.w
                                         : paredes[i].x + paredes[i].w;
            jugador.y += dy * VEL_J * dt;
            for (int i = 0; i < n_paredes; i++)
                if (aabb(jugador, paredes[i]))
                    jugador.y = (dy > 0) ? paredes[i].y - jugador.h
                                         : paredes[i].y + paredes[i].h;

            /* --- monedas --- */
            for (int i = 0; i < N_MONEDAS; i++)
                if (!tomada[i] && aabb(jugador, monedas[i])) {
                    tomada[i] = true;
                    faltan--;
                }

            /* --- enemigo persigue --- */
            float ex = (jugador.x + 15) - (enemigo.x + 14);
            float ey = (jugador.y + 15) - (enemigo.y + 14);
            float d = sqrtf(ex * ex + ey * ey);
            if (d > 1.0f) {
                enemigo.x += (ex / d) * VEL_E * dt;
                enemigo.y += (ey / d) * VEL_E * dt;
            }

            /* --- condiciones de fin --- */
            if (aabb(jugador, enemigo)) estado = PERDISTE;
            if (faltan == 0)            estado = GANASTE;
        }

        /* --- HUD en el titulo --- */
        if (estado == JUGANDO)
            SDL_snprintf(titulo, sizeof(titulo), "Junta las monedas  |  faltan: %d", faltan);
        else
            SDL_snprintf(titulo, sizeof(titulo), "%s  |  R = reiniciar, Esc = salir",
                         estado == GANASTE ? "GANASTE!" : "PERDISTE");
        SDL_SetWindowTitle(ventana, titulo);

        /* --- render --- */
        SDL_SetRenderDrawColor(renderer, 18, 20, 26, 255);
        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(renderer, 70, 80, 100, 255);
        SDL_RenderFillRects(renderer, paredes, n_paredes);

        SDL_SetRenderDrawColor(renderer, 245, 210, 70, 255);
        for (int i = 0; i < N_MONEDAS; i++)
            if (!tomada[i]) SDL_RenderFillRect(renderer, &monedas[i]);

        SDL_SetRenderDrawColor(renderer, 230, 80, 70, 255);
        SDL_RenderFillRect(renderer, &enemigo);

        SDL_SetRenderDrawColor(renderer,
                               estado == GANASTE ? 120 : 120,
                               estado == PERDISTE ? 120 : 220, 130, 255);
        SDL_RenderFillRect(renderer, &jugador);

        SDL_RenderPresent(renderer);

        if (limite > 0 && (ahora - inicio) > (Uint64)(limite * 1000))
            corriendo = false;
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Así empiezan los juegos independientes: un prototipo chico, con un bucle, entrada, colisiones y estados, que después crece con arte y sonido. Separar los niveles como datos es lo que permite que en los estudios haya diseñadores de niveles que no programan, y editores de mapas que guardan esos datos en archivos.

### Errores habituales

La Salamandra combina todo lo de la Senda:

- **Ogro**: seguir actualizando después de ganar o perder.
- **Ogro**: el enemigo que atraviesa paredes porque no usa la misma función de colisión.
- **Orco**: recorrer más gemas de las que tiene el nivel (usá la cantidad de cada nivel, no el máximo del array).
- **Ogro**: al pasar de nivel, olvidar reiniciar las gemas tomadas o las posiciones.
- **Troll**: no destruir la ventana y el renderer al salir.

### Misión S01-N04-M1 · Reiniciar y récord

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Partiendo del proyecto del ejemplo, agregá:

1. Un **tiempo**: cuántos segundos tardaste en juntar todas las monedas, mostrado en el título al ganar.
2. **Reiniciar** con `R` en cualquier momento (todo vuelve al estado inicial). Escribí una función `reiniciar` para no repetir código.
3. El **mejor tiempo** de la sesión, que sobrevive a los reinicios.

#### Criterio de aprobación

- Mide el tiempo de la partida con `SDL_GetTicks`.
- R reinicia todo con una función.
- Guarda el mejor tiempo entre partidas.

#### Código inicial

```c
#include <SDL3/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

/*
 * Proyecto de cierre de la etapa 06 (SDL3 en C, un solo archivo).
 *
 * "Junta las monedas": mueve al jugador con WASD por un cuarto con paredes,
 * junta las 6 monedas y evita al enemigo que te persigue.
 *   - ganas si juntas todas las monedas
 *   - perdes si el enemigo te toca
 *
 * Integra: game loop + dt, teclado por estado, colisiones AABB (jugador-pared,
 * jugador-moneda, jugador-enemigo), IA de persecucion, estados de juego.
 *
 * El HUD (monedas restantes / resultado) va en el titulo de la ventana, para no
 * meter todavia una libreria de fuentes (eso es 07-SDL3-Cpp).
 */

#define ANCHO 800
#define ALTO  600
#define N_MONEDAS 6

typedef enum { JUGANDO, GANASTE, PERDISTE } Estado;

static bool aabb(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x &&
           a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(int argc, char **argv)
{
    double limite = (argc > 1) ? SDL_atof(argv[1]) : 0.0;

    if (!SDL_Init(SDL_INIT_VIDEO)) { fprintf(stderr, "%s\n", SDL_GetError()); return 1; }
    SDL_Window   *ventana  = SDL_CreateWindow("Junta las monedas - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(ventana, NULL);
    if (!ventana || !renderer) { SDL_Quit(); return 1; }
    SDL_SetRenderVSync(renderer, 1);

    SDL_FRect paredes[] = {
        {   0,   0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 },
        {   0,   0, 20, ALTO },  { ANCHO - 20, 0, 20, ALTO },
        { 180, 120, 260, 24 }, { 360, 300, 24, 200 }, { 500, 160, 24, 200 },
    };
    const int n_paredes = (int)(sizeof(paredes) / sizeof(paredes[0]));

    SDL_FRect monedas[N_MONEDAS] = {
        {  90,  90, 16, 16 }, { 700,  90, 16, 16 }, { 120, 460, 16, 16 },
        { 660, 500, 16, 16 }, { 300, 250, 16, 16 }, { 430, 420, 16, 16 },
    };
    bool tomada[N_MONEDAS] = { false };
    int  faltan = N_MONEDAS;

    SDL_FRect jugador = { ANCHO / 2.0f, ALTO / 2.0f, 30, 30 };
    SDL_FRect enemigo = { 60, ALTO - 60.0f, 28, 28 };
    const float VEL_J = 260.0f;
    const float VEL_E = 130.0f;

    Estado estado = JUGANDO;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    Uint64 inicio = antes;
    char titulo[128];

    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float)(ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) dt = 0.1f;

        SDL_Event ev;
        while (SDL_PollEvent(&ev)) {
            if (ev.type == SDL_EVENT_QUIT) corriendo = false;
            if (ev.type == SDL_EVENT_KEY_DOWN) {
                if (ev.key.key == SDLK_ESCAPE) corriendo = false;
                if (ev.key.key == SDLK_R && estado != JUGANDO) {
                    /* reiniciar */
                    for (int i = 0; i < N_MONEDAS; i++) tomada[i] = false;
                    faltan = N_MONEDAS;
                    jugador.x = ANCHO / 2.0f; jugador.y = ALTO / 2.0f;
                    enemigo.x = 60; enemigo.y = ALTO - 60.0f;
                    estado = JUGANDO;
                }
            }
        }

        if (estado == JUGANDO) {
            /* --- jugador --- */
            const bool *k = SDL_GetKeyboardState(NULL);
            float dx = 0, dy = 0;
            if (k[SDL_SCANCODE_W]) dy -= 1;
            if (k[SDL_SCANCODE_S]) dy += 1;
            if (k[SDL_SCANCODE_A]) dx -= 1;
            if (k[SDL_SCANCODE_D]) dx += 1;
            float l = sqrtf(dx * dx + dy * dy);
            if (l > 0) { dx /= l; dy /= l; }

            jugador.x += dx * VEL_J * dt;
            for (int i = 0; i < n_paredes; i++)
                if (aabb(jugador, paredes[i]))
                    jugador.x = (dx > 0) ? paredes[i].x - jugador.w
                                         : paredes[i].x + paredes[i].w;
            jugador.y += dy * VEL_J * dt;
            for (int i = 0; i < n_paredes; i++)
                if (aabb(jugador, paredes[i]))
                    jugador.y = (dy > 0) ? paredes[i].y - jugador.h
                                         : paredes[i].y + paredes[i].h;

            /* --- monedas --- */
            for (int i = 0; i < N_MONEDAS; i++)
                if (!tomada[i] && aabb(jugador, monedas[i])) {
                    tomada[i] = true;
                    faltan--;
                }

            /* --- enemigo persigue --- */
            float ex = (jugador.x + 15) - (enemigo.x + 14);
            float ey = (jugador.y + 15) - (enemigo.y + 14);
            float d = sqrtf(ex * ex + ey * ey);
            if (d > 1.0f) {
                enemigo.x += (ex / d) * VEL_E * dt;
                enemigo.y += (ey / d) * VEL_E * dt;
            }

            /* --- condiciones de fin --- */
            if (aabb(jugador, enemigo)) estado = PERDISTE;
            if (faltan == 0)            estado = GANASTE;
        }

        /* --- HUD en el titulo --- */
        if (estado == JUGANDO)
            SDL_snprintf(titulo, sizeof(titulo), "Junta las monedas  |  faltan: %d", faltan);
        else
            SDL_snprintf(titulo, sizeof(titulo), "%s  |  R = reiniciar, Esc = salir",
                         estado == GANASTE ? "GANASTE!" : "PERDISTE");
        SDL_SetWindowTitle(ventana, titulo);

        /* --- render --- */
        SDL_SetRenderDrawColor(renderer, 18, 20, 26, 255);
        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(renderer, 70, 80, 100, 255);
        SDL_RenderFillRects(renderer, paredes, n_paredes);

        SDL_SetRenderDrawColor(renderer, 245, 210, 70, 255);
        for (int i = 0; i < N_MONEDAS; i++)
            if (!tomada[i]) SDL_RenderFillRect(renderer, &monedas[i]);

        SDL_SetRenderDrawColor(renderer, 230, 80, 70, 255);
        SDL_RenderFillRect(renderer, &enemigo);

        SDL_SetRenderDrawColor(renderer,
                               estado == GANASTE ? 120 : 120,
                               estado == PERDISTE ? 120 : 220, 130, 255);
        SDL_RenderFillRect(renderer, &jugador);

        SDL_RenderPresent(renderer);

        if (limite > 0 && (ahora - inicio) > (Uint64)(limite * 1000))
            corriendo = false;
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Misión S01-N04-M2 · Niveles

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, c
```

#### Consigna

Convertí el juego en uno de **tres niveles**, guardados como datos en un array de structs `Nivel` (paredes y gemas, con su cantidad). Al juntar todas las gemas se pasa al siguiente: se reinician las gemas y las posiciones, y la Salamandra va un 25 % más rápido. Mostrá el nivel y las gemas que faltan en el título. Al terminar el tercero, ganaste.

#### Criterio de aprobación

- Los niveles son datos en un array de structs.
- El mismo código juega cualquier nivel.
- Al pasar de nivel se reinicia lo necesario y sube la dificultad.

#### Código inicial

```c
#include <SDL3/SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

/*
 * Proyecto de cierre de la etapa 06 (SDL3 en C, un solo archivo).
 *
 * "Junta las monedas": mueve al jugador con WASD por un cuarto con paredes,
 * junta las 6 monedas y evita al enemigo que te persigue.
 *   - ganas si juntas todas las monedas
 *   - perdes si el enemigo te toca
 *
 * Integra: game loop + dt, teclado por estado, colisiones AABB (jugador-pared,
 * jugador-moneda, jugador-enemigo), IA de persecucion, estados de juego.
 *
 * El HUD (monedas restantes / resultado) va en el titulo de la ventana, para no
 * meter todavia una libreria de fuentes (eso es 07-SDL3-Cpp).
 */

#define ANCHO 800
#define ALTO  600
#define N_MONEDAS 6

typedef enum { JUGANDO, GANASTE, PERDISTE } Estado;

static bool aabb(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x &&
           a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(int argc, char **argv)
{
    double limite = (argc > 1) ? SDL_atof(argv[1]) : 0.0;

    if (!SDL_Init(SDL_INIT_VIDEO)) { fprintf(stderr, "%s\n", SDL_GetError()); return 1; }
    SDL_Window   *ventana  = SDL_CreateWindow("Junta las monedas - WASD", ANCHO, ALTO, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(ventana, NULL);
    if (!ventana || !renderer) { SDL_Quit(); return 1; }
    SDL_SetRenderVSync(renderer, 1);

    SDL_FRect paredes[] = {
        {   0,   0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 },
        {   0,   0, 20, ALTO },  { ANCHO - 20, 0, 20, ALTO },
        { 180, 120, 260, 24 }, { 360, 300, 24, 200 }, { 500, 160, 24, 200 },
    };
    const int n_paredes = (int)(sizeof(paredes) / sizeof(paredes[0]));

    SDL_FRect monedas[N_MONEDAS] = {
        {  90,  90, 16, 16 }, { 700,  90, 16, 16 }, { 120, 460, 16, 16 },
        { 660, 500, 16, 16 }, { 300, 250, 16, 16 }, { 430, 420, 16, 16 },
    };
    bool tomada[N_MONEDAS] = { false };
    int  faltan = N_MONEDAS;

    SDL_FRect jugador = { ANCHO / 2.0f, ALTO / 2.0f, 30, 30 };
    SDL_FRect enemigo = { 60, ALTO - 60.0f, 28, 28 };
    const float VEL_J = 260.0f;
    const float VEL_E = 130.0f;

    Estado estado = JUGANDO;
    bool corriendo = true;
    Uint64 antes = SDL_GetTicks();
    Uint64 inicio = antes;
    char titulo[128];

    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float)(ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) dt = 0.1f;

        SDL_Event ev;
        while (SDL_PollEvent(&ev)) {
            if (ev.type == SDL_EVENT_QUIT) corriendo = false;
            if (ev.type == SDL_EVENT_KEY_DOWN) {
                if (ev.key.key == SDLK_ESCAPE) corriendo = false;
                if (ev.key.key == SDLK_R && estado != JUGANDO) {
                    /* reiniciar */
                    for (int i = 0; i < N_MONEDAS; i++) tomada[i] = false;
                    faltan = N_MONEDAS;
                    jugador.x = ANCHO / 2.0f; jugador.y = ALTO / 2.0f;
                    enemigo.x = 60; enemigo.y = ALTO - 60.0f;
                    estado = JUGANDO;
                }
            }
        }

        if (estado == JUGANDO) {
            /* --- jugador --- */
            const bool *k = SDL_GetKeyboardState(NULL);
            float dx = 0, dy = 0;
            if (k[SDL_SCANCODE_W]) dy -= 1;
            if (k[SDL_SCANCODE_S]) dy += 1;
            if (k[SDL_SCANCODE_A]) dx -= 1;
            if (k[SDL_SCANCODE_D]) dx += 1;
            float l = sqrtf(dx * dx + dy * dy);
            if (l > 0) { dx /= l; dy /= l; }

            jugador.x += dx * VEL_J * dt;
            for (int i = 0; i < n_paredes; i++)
                if (aabb(jugador, paredes[i]))
                    jugador.x = (dx > 0) ? paredes[i].x - jugador.w
                                         : paredes[i].x + paredes[i].w;
            jugador.y += dy * VEL_J * dt;
            for (int i = 0; i < n_paredes; i++)
                if (aabb(jugador, paredes[i]))
                    jugador.y = (dy > 0) ? paredes[i].y - jugador.h
                                         : paredes[i].y + paredes[i].h;

            /* --- monedas --- */
            for (int i = 0; i < N_MONEDAS; i++)
                if (!tomada[i] && aabb(jugador, monedas[i])) {
                    tomada[i] = true;
                    faltan--;
                }

            /* --- enemigo persigue --- */
            float ex = (jugador.x + 15) - (enemigo.x + 14);
            float ey = (jugador.y + 15) - (enemigo.y + 14);
            float d = sqrtf(ex * ex + ey * ey);
            if (d > 1.0f) {
                enemigo.x += (ex / d) * VEL_E * dt;
                enemigo.y += (ey / d) * VEL_E * dt;
            }

            /* --- condiciones de fin --- */
            if (aabb(jugador, enemigo)) estado = PERDISTE;
            if (faltan == 0)            estado = GANASTE;
        }

        /* --- HUD en el titulo --- */
        if (estado == JUGANDO)
            SDL_snprintf(titulo, sizeof(titulo), "Junta las monedas  |  faltan: %d", faltan);
        else
            SDL_snprintf(titulo, sizeof(titulo), "%s  |  R = reiniciar, Esc = salir",
                         estado == GANASTE ? "GANASTE!" : "PERDISTE");
        SDL_SetWindowTitle(ventana, titulo);

        /* --- render --- */
        SDL_SetRenderDrawColor(renderer, 18, 20, 26, 255);
        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(renderer, 70, 80, 100, 255);
        SDL_RenderFillRects(renderer, paredes, n_paredes);

        SDL_SetRenderDrawColor(renderer, 245, 210, 70, 255);
        for (int i = 0; i < N_MONEDAS; i++)
            if (!tomada[i]) SDL_RenderFillRect(renderer, &monedas[i]);

        SDL_SetRenderDrawColor(renderer, 230, 80, 70, 255);
        SDL_RenderFillRect(renderer, &enemigo);

        SDL_SetRenderDrawColor(renderer,
                               estado == GANASTE ? 120 : 120,
                               estado == PERDISTE ? 120 : 220, 130, 255);
        SDL_RenderFillRect(renderer, &jugador);

        SDL_RenderPresent(renderer);

        if (limite > 0 && (ahora - inicio) > (Uint64)(limite * 1000))
            corriendo = false;
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Solución de referencia

```c
/*
 * S01-N04 Mision 2 - Niveles: al juntar todas las gemas se pasa al siguiente nivel
 * (otras paredes y gemas, y la Salamandra un 25 % mas rapida).
 * Los niveles son datos en un array de structs: agregar uno es agregar una fila.
 */
#include <SDL3/SDL.h>
#include <math.h>
#include <stdio.h>

#define ANCHO 800
#define ALTO 600
#define MAX_PAREDES 8
#define MAX_GEMAS 8

typedef struct {
    SDL_FRect paredes[MAX_PAREDES];
    int n_paredes;
    SDL_FRect gemas[MAX_GEMAS];
    int n_gemas;
} Nivel;

static const Nivel NIVELES[] = {
    { { { 180, 120, 260, 24 }, { 360, 300, 24, 200 } }, 2,
      { { 90, 90, 16, 16 }, { 700, 90, 16, 16 }, { 120, 460, 16, 16 }, { 660, 500, 16, 16 } }, 4 },
    { { { 100, 280, 600, 24 }, { 380, 60, 24, 180 }, { 200, 380, 24, 160 } }, 3,
      { { 60, 60, 16, 16 }, { 720, 60, 16, 16 }, { 60, 520, 16, 16 }, { 720, 520, 16, 16 }, { 420, 420, 16, 16 } }, 5 },
    { { { 150, 150, 500, 24 }, { 150, 420, 500, 24 }, { 150, 150, 24, 150 }, { 626, 300, 24, 144 } }, 4,
      { { 400, 300, 16, 16 }, { 60, 300, 16, 16 }, { 720, 300, 16, 16 }, { 400, 60, 16, 16 }, { 400, 520, 16, 16 }, { 200, 250, 16, 16 } }, 6 },
};
static const int CANTIDAD_NIVELES = (int) (sizeof NIVELES / sizeof NIVELES[0]);

static bool se_tocan(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

static bool choca_pared(SDL_FRect r, const Nivel *n)
{
    if (r.x < 20 || r.y < 20 || r.x + r.w > ANCHO - 20 || r.y + r.h > ALTO - 20) {
        return true;                                   /* el marco */
    }
    for (int i = 0; i < n->n_paredes; i++) {
        if (se_tocan(r, n->paredes[i])) {
            return true;
        }
    }
    return false;
}

static void mover(SDL_FRect *r, float dx, float dy, const Nivel *n)
{
    r->x += dx;
    if (choca_pared(*r, n)) r->x -= dx;
    r->y += dy;
    if (choca_pared(*r, n)) r->y -= dy;
}

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("La Salamandra del Horno", ANCHO, ALTO, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);

    int nivel = 0;
    bool tomada[MAX_GEMAS] = { false };
    int faltan = NIVELES[0].n_gemas;
    SDL_FRect heroe = { ANCHO / 2.0f, ALTO / 2.0f - 60, 28, 28 }, salamandra = { 40, ALTO - 70.0f, 28, 28 };
    float vel_salamandra = 120.0f;
    bool corriendo = true, perdiste = false, ganaste = false;
    Uint64 antes = SDL_GetTicks();

    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (float) (ahora - antes) / 1000.0f;
        antes = ahora;
        if (dt > 0.1f) {
            dt = 0.1f;
        }
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const Nivel *n = &NIVELES[nivel];
        if (!perdiste && !ganaste) {
            const bool *t = SDL_GetKeyboardState(NULL);
            float dx = (float) (t[SDL_SCANCODE_D] - t[SDL_SCANCODE_A]), dy = (float) (t[SDL_SCANCODE_S] - t[SDL_SCANCODE_W]);
            float largo = sqrtf(dx * dx + dy * dy);
            if (largo > 0) {
                mover(&heroe, dx / largo * 260 * dt, dy / largo * 260 * dt, n);
            }
            float sx = heroe.x - salamandra.x, sy = heroe.y - salamandra.y, d = sqrtf(sx * sx + sy * sy);
            if (d > 1) {
                mover(&salamandra, sx / d * vel_salamandra * dt, sy / d * vel_salamandra * dt, n);
            }
            for (int i = 0; i < n->n_gemas; i++) {
                if (!tomada[i] && se_tocan(heroe, n->gemas[i])) {
                    tomada[i] = true;
                    faltan--;
                }
            }
            if (se_tocan(heroe, salamandra)) {
                perdiste = true;
            } else if (faltan == 0) {
                if (++nivel == CANTIDAD_NIVELES) {
                    ganaste = true;
                    nivel = CANTIDAD_NIVELES - 1;
                } else {                                 /* nivel siguiente */
                    for (int i = 0; i < MAX_GEMAS; i++) {
                        tomada[i] = false;
                    }
                    faltan = NIVELES[nivel].n_gemas;
                    heroe = (SDL_FRect) { 40, 40, 28, 28 };
                    salamandra = (SDL_FRect) { ANCHO - 70.0f, ALTO - 70.0f, 28, 28 };
                    vel_salamandra *= 1.25f;
                }
            }
            char titulo[80];
            snprintf(titulo, sizeof titulo, "Nivel %d de %d - faltan %d gemas", nivel + 1, CANTIDAD_NIVELES, faltan);
            SDL_SetWindowTitle(ventana, perdiste ? "La Salamandra te alcanzo (Esc para salir)" : ganaste ? "Venciste a la Salamandra!" : titulo);
        }
        n = &NIVELES[nivel];
        SDL_SetRenderDrawColor(pincel, 30, 18, 14, 255);
        SDL_RenderClear(pincel);
        SDL_SetRenderDrawColor(pincel, 120, 80, 60, 255);
        SDL_FRect marco[] = { { 0, 0, ANCHO, 20 }, { 0, ALTO - 20, ANCHO, 20 }, { 0, 0, 20, ALTO }, { ANCHO - 20, 0, 20, ALTO } };
        SDL_RenderFillRects(pincel, marco, 4);
        SDL_RenderFillRects(pincel, n->paredes, n->n_paredes);
        SDL_SetRenderDrawColor(pincel, 90, 230, 200, 255);
        for (int i = 0; i < n->n_gemas; i++) {
            if (!tomada[i]) {
                SDL_RenderFillRect(pincel, &n->gemas[i]);
            }
        }
        SDL_SetRenderDrawColor(pincel, 90, 200, 240, 255);
        SDL_RenderFillRect(pincel, &heroe);
        SDL_SetRenderDrawColor(pincel, 250, 110, 30, 255);
        SDL_RenderFillRect(pincel, &salamandra);
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Encargo S01-N04-E1 · El marcador del torneo

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 30
extensiones: zip, c
```

#### Consigna

Para el torneo de pulseadas del Gremio: un marcador para dos jugadores. `A` suma un punto al rojo y `L` al azul (manteniendo la tecla no se suman puntos de más: usá `evento.key.repeat`). Cada jugador tiene una columna de 5 casillas que se van llenando; el primero en llegar a 5 gana y se muestra un mensaje. `R` reinicia.

#### Criterio de aprobación

- Suma un punto por pulsación, sin contar la repetición.
- Dibuja el puntaje como casillas y anuncia al ganador.
- R reinicia.

#### Solución de referencia

```c
/* S01-N04 Encargo - El marcador del torneo del Gremio: dos jugadores, un punto por tecla, gana el primero a 5. */
#include <SDL3/SDL.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    (void) argc;
    (void) argv;
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        fprintf(stderr, "%s\n", SDL_GetError());
        return 1;
    }
    SDL_Window *ventana = SDL_CreateWindow("Marcador: A suma al rojo, L al azul, R reinicia", 640, 300, 0);
    SDL_Renderer *pincel = SDL_CreateRenderer(ventana, NULL);
    if (ventana == NULL || pincel == NULL) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(pincel, 1);
    int puntos[2] = { 0, 0 };
    const int META = 5;
    bool corriendo = true;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_KEY_DOWN && !e.key.repeat) {   /* la tecla mantenida no suma de mas */
                bool termino = puntos[0] == META || puntos[1] == META;
                if (e.key.key == SDLK_R) {
                    puntos[0] = puntos[1] = 0;
                } else if (!termino && e.key.key == SDLK_A) {
                    puntos[0]++;
                } else if (!termino && e.key.key == SDLK_L) {
                    puntos[1]++;
                }
            }
        }
        SDL_SetRenderDrawColor(pincel, 18, 18, 26, 255);
        SDL_RenderClear(pincel);
        for (int j = 0; j < 2; j++) {
            for (int p = 0; p < META; p++) {
                SDL_FRect casilla = { 60.0f + j * 300, 240.0f - p * 36, 220, 28 };
                bool lleno = p < puntos[j];
                SDL_SetRenderDrawColor(pincel, j == 0 ? (lleno ? 230 : 70) : 40, 50, j == 1 ? (lleno ? 230 : 70) : 40, 255);
                SDL_RenderFillRect(pincel, &casilla);
            }
        }
        char texto[48];
        const char *ganador = puntos[0] == META ? "Gana el rojo!" : puntos[1] == META ? "Gana el azul!" : NULL;
        snprintf(texto, sizeof texto, "%d - %d", puntos[0], puntos[1]);
        SDL_SetRenderDrawColor(pincel, 240, 240, 240, 255);
        SDL_RenderDebugText(pincel, 300, 20, texto);
        if (ganador != NULL) {
            SDL_RenderDebugText(pincel, 270, 40, ganador);
        }
        SDL_RenderPresent(pincel);
    }
    SDL_DestroyRenderer(pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Para qué sirve un `enum` con los estados del juego?

Para decidir qué se actualiza y qué se muestra en cada momento (jugando, ganaste, perdiste) sin mezclar condiciones por todos lados.

#### ¿Qué ventaja tiene guardar los niveles como datos?

Que el mismo código sirve para todos: agregar un nivel es agregar una fila, sin copiar código.

#### Al pasar de nivel, ¿qué hay que reiniciar?

Las gemas tomadas, las que faltan y las posiciones del héroe y del enemigo.

#### ¿Qué limitación tiene `SDL_RenderDebugText`?

Usa una letra simple incorporada, sin tildes ni eñes; para textos lindos hace falta SDL_ttf.

### Soluciones (docente)

Jefe basado en `06-SDL3/13-Proyecto` (Junta las monedas). La misión 1 no tiene solución de referencia: se corrige probándola.
