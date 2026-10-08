# RAMA S01 · Senda de la Linterna Mágica: videojuegos con SDL3

```meta
tipo: senda
posicion: 7
```

## S01-N01 · La Linterna Mágica: ventana y bucle

```meta
tipo: tema
padre: R06-N06
precio: 3
moneda: comodin
criatura: slime
ejecutable: no
temas: graf.sdl, juegos.bucle
usa: mem.raii
```

### Crónica

Detrás del engranaje de la Encrucijada hay una sala oscura. En el centro, una **linterna mágica**: una caja de bronce con una lente que proyecta figuras en la pared. Y las figuras **se mueven**, solas, muchas veces por segundo.

Bron mete la mano delante de la lente y en la pared aparece una mano gigante. Lyn hace una sombra de conejo y le gana la carrera a la mano.

—Hasta ahora tus programas escribían y terminaban —dice {mentor}—. Acá se escriben mundos que **siguen andando** hasta que alguien apaga la linterna.

### Objetivos

- Instalar SDL3, compilar y enlazar un programa que abre una ventana.
- Envolver los recursos de SDL con **RAII** para que se liberen solos.
- Escribir el **bucle de juego** en tiempo real: tiempo, entrada, actualizar y dibujar, con *delta time*.

### Antes de empezar

Todo el camino principal, en especial RAII (rama 3), excepciones y el bucle de juego (rama 5).

### Explicación

#### Instalar SDL3 y compilar

SDL3 es una **biblioteca**: hay que tenerla instalada y **enlazarla**.
```bash
sudo apt install libsdl3-dev        # Ubuntu 25.04 o más nuevo; si tu versión no la trae, se compila desde el código de SDL
g++ -std=c++20 -Wall -Wextra -o juego main.cpp $(pkg-config --cflags --libs sdl3)
./juego
```
`pkg-config` le dice al compilador dónde están los headers (`-I...`) y la biblioteca (`-lSDL3`). Con CMake:
```cmake
find_package(SDL3 REQUIRED CONFIG)
target_link_libraries(juego PRIVATE SDL3::SDL3)
```
En Windows se usa MSYS2 (`pacman -S mingw-w64-ucrt-x86_64-sdl3`) y en macOS, `brew install sdl3`.

Estos programas abren una **ventana**: se prueban en tu compu, no en la plataforma, y las misiones se entregan como `.zip` con el código.

#### Las piezas de SDL

```cpp
SDL_Init(SDL_INIT_VIDEO);                                     // encender SDL (devuelve false si falla)
SDL_Window* ventana = SDL_CreateWindow("Título", 800, 600, 0);
SDL_Renderer* pincel = SDL_CreateRenderer(ventana, nullptr);  // el que dibuja (usa la placa de video)
...
SDL_DestroyRenderer(pincel);                                  // al final, todo se devuelve, al revés
SDL_DestroyWindow(ventana);
SDL_Quit();
```
SDL es una biblioteca de **C**: da punteros crudos que hay que liberar a mano. En C++ se envuelven en una clase **RAII**: el constructor los crea (y **lanza** una excepción si algo falla, con el mensaje de `SDL_GetError()`), el destructor los libera, y la copia está prohibida. Así la ventana se cierra bien aunque el programa termine por un error.

#### El bucle de juego en tiempo real

```cpp
while (corriendo) {
    // 1. tiempo:     dt = segundos desde el cuadro anterior
    // 2. entrada:    while (SDL_PollEvent(&e)) { ... }
    // 3. actualizar: mover todo usando dt
    // 4. dibujar:    SDL_RenderClear -> dibujar -> SDL_RenderPresent
}
```
- `SDL_PollEvent` saca de a uno los eventos pendientes (teclas, mouse, cerrar la ventana) y devuelve `false` cuando no quedan: va en un `while`.
- Se dibuja en un lienzo oculto y `SDL_RenderPresent` lo muestra de golpe (*doble búfer*).
- `SDL_SetRenderVSync(pincel, 1)` sincroniza con el monitor: el bucle corre a la velocidad de refresco (60, 144…) en vez de a mil por segundo.

#### Delta time
`SDL_GetTicks()` da los milisegundos desde que arrancó SDL:
```cpp
Uint64 ahora = SDL_GetTicks();
float dt = (ahora - antes) / 1000.0f;   // segundos
antes = ahora;
caja.x += velocidad * dt;               // velocidad en píxeles por SEGUNDO
```
Se limita `dt` (por ejemplo, a 0.1) para que una trabada de la compu no haga saltar todo de golpe.

#### Dibujar
- Los rectángulos son `SDL_FRect { x, y, ancho, alto }` con decimales. El `(0, 0)` está **arriba a la izquierda** y la `y` crece **hacia abajo**.
- `SDL_SetRenderDrawColor(p, r, g, b, a)` elige el color; `SDL_RenderFillRect(p, &rect)` pinta; `SDL_RenderRect` dibuja el borde; `SDL_RenderLine` una línea.
- `SDL_RenderDebugText(p, x, y, "texto")` escribe con una letra chiquita de 8 × 8: ideal para mostrar datos mientras programás (con `SDL_RenderDebugTextFormat` se usan `%d`, `%.1f`, como en `printf`).

### Código de ejemplo

```cpp
/*
 * S01-N01 - La Linterna Magica: una ventana, el bucle de juego y RAII.
 * Compilar: g++ -std=c++20 -Wall -Wextra -o juego main.cpp $(pkg-config --cflags --libs sdl3)
 */
#include <SDL3/SDL.h>

#include <iostream>
#include <stdexcept>
#include <string>

// La ventana y el pincel, envueltos en una clase RAII: se crean en el constructor
// y se destruyen solos en el destructor, pase lo que pase.
class Ventana {
public:
    Ventana(const std::string& titulo, int ancho, int alto)
    {
        if (!SDL_Init(SDL_INIT_VIDEO)) {
            throw std::runtime_error(std::string("SDL_Init: ") + SDL_GetError());
        }
        ventana_ = SDL_CreateWindow(titulo.c_str(), ancho, alto, 0);
        pincel_ = ventana_ ? SDL_CreateRenderer(ventana_, nullptr) : nullptr;
        if (pincel_ == nullptr) {
            std::string error = SDL_GetError();
            liberar();
            throw std::runtime_error("no se pudo crear la ventana: " + error);
        }
        SDL_SetRenderVSync(pincel_, 1);
    }

    ~Ventana() { liberar(); }
    Ventana(const Ventana&) = delete;
    Ventana& operator=(const Ventana&) = delete;

    SDL_Renderer* pincel() const { return pincel_; }

private:
    void liberar()
    {
        if (pincel_) {
            SDL_DestroyRenderer(pincel_);
        }
        if (ventana_) {
            SDL_DestroyWindow(ventana_);
        }
        SDL_Quit();
    }

    SDL_Window* ventana_ = nullptr;
    SDL_Renderer* pincel_ = nullptr;
};

int main()
{
    const float ANCHO = 800, ALTO = 600;
    try {
        Ventana v("La Linterna Mágica", static_cast<int>(ANCHO), static_cast<int>(ALTO));
        SDL_FRect caja{100, 100, 50, 50};
        float vx = 220, vy = 160;                 // pixeles por SEGUNDO
        bool corriendo = true;
        Uint64 antes = SDL_GetTicks();

        while (corriendo) {
            // 1) tiempo
            Uint64 ahora = SDL_GetTicks();
            float dt = (ahora - antes) / 1000.0f;
            antes = ahora;
            if (dt > 0.1f) {
                dt = 0.1f;                         // si la compu se traba, no saltar de golpe
            }
            // 2) entrada
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                    corriendo = false;
                }
            }
            // 3) actualizar
            caja.x += vx * dt;
            caja.y += vy * dt;
            if (caja.x < 0 || caja.x + caja.w > ANCHO) {
                vx = -vx;
                caja.x = caja.x < 0 ? 0 : ANCHO - caja.w;
            }
            if (caja.y < 0 || caja.y + caja.h > ALTO) {
                vy = -vy;
                caja.y = caja.y < 0 ? 0 : ALTO - caja.h;
            }
            // 4) dibujar
            SDL_Renderer* p = v.pincel();
            SDL_SetRenderDrawColor(p, 20, 22, 34, 255);
            SDL_RenderClear(p);
            SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
            SDL_RenderFillRect(p, &caja);
            SDL_SetRenderDrawColor(p, 230, 230, 230, 255);
            SDL_RenderDebugText(p, 10, 10, "ESC para salir");
            SDL_RenderPresent(p);
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }
    return 0;
}
```

### ¿Para qué sirve?

SDL es la biblioteca que usan cientos de juegos comerciales, emuladores y reproductores de video para abrir ventanas, leer teclado y joystick y dibujar en Windows, Linux, macOS, Android y consolas. El bucle con delta time es la base de todos los motores: Unity, Godot y Unreal hacen exactamente esto por dentro.

### Errores habituales

**Esqueleto: no enlazar SDL.** Compilar sin `$(pkg-config --libs sdl3)`:
```
undefined reference to `SDL_Init'
```

**Slime: el header que no aparece.** `fatal error: SDL3/SDL.h: No such file or directory`: SDL3 no está instalada o falta `--cflags`.

**Ogro: moverse sin `dt`.** El juego va distinto en cada compu.

**Ogro: leer un solo evento por cuadro.** La ventana tarda en responder o el sistema dice que "no responde". Los eventos se vacían con un `while`.

**Troll: liberar en el orden equivocado o no liberar.** Las texturas antes que el renderer, el renderer antes que la ventana, y `SDL_Quit` al final. Una clase RAII lo hace siempre bien.

### Misión S01-N01-M1 · Las linternas que rebotan

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Hacé rebotar **tres** cajas de distintos tamaños contra los cuatro bordes, guardadas en un `std::vector` de un `struct Caja` con su propio método `mover(dt, ancho, alto)`, que devuelve `true` si chocó. En cada choque, la caja rota sus colores (R → G → B) y el título de la ventana muestra el total de choques (`SDL_SetWindowTitle`). Usá una clase RAII para la ventana.

#### Criterio de aprobación

- Las tres cajas rebotan sin salirse y se mueven con `dt`.
- La ventana y el renderer se manejan con una clase RAII.
- El título cuenta los choques.

#### Solución de referencia

```cpp
// S01-N01-M1 - Las linternas que rebotan: un vector de cajas, color al chocar y contador en el titulo.
#include <SDL3/SDL.h>

#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

class Ventana {
public:
    Ventana(const std::string& titulo, int ancho, int alto)
    {
        if (!SDL_Init(SDL_INIT_VIDEO)) {
            throw std::runtime_error(SDL_GetError());
        }
        ventana_ = SDL_CreateWindow(titulo.c_str(), ancho, alto, 0);
        pincel_ = ventana_ ? SDL_CreateRenderer(ventana_, nullptr) : nullptr;
        if (!pincel_) {
            liberar();
            throw std::runtime_error("no se pudo crear la ventana");
        }
        SDL_SetRenderVSync(pincel_, 1);
    }
    ~Ventana() { liberar(); }
    Ventana(const Ventana&) = delete;
    Ventana& operator=(const Ventana&) = delete;
    SDL_Window* ventana() const { return ventana_; }
    SDL_Renderer* pincel() const { return pincel_; }

private:
    void liberar()
    {
        if (pincel_) {
            SDL_DestroyRenderer(pincel_);
        }
        if (ventana_) {
            SDL_DestroyWindow(ventana_);
        }
        SDL_Quit();
    }
    SDL_Window* ventana_ = nullptr;
    SDL_Renderer* pincel_ = nullptr;
};

struct Caja {
    SDL_FRect r;
    float vx;
    float vy;
    Uint8 color[3];

    // Mueve la caja; devuelve true si choco con algun borde.
    bool mover(float dt, float ancho, float alto)
    {
        r.x += vx * dt;
        r.y += vy * dt;
        bool choco = false;
        if (r.x < 0 || r.x + r.w > ancho) {
            vx = -vx;
            r.x = r.x < 0 ? 0 : ancho - r.w;
            choco = true;
        }
        if (r.y < 0 || r.y + r.h > alto) {
            vy = -vy;
            r.y = r.y < 0 ? 0 : alto - r.h;
            choco = true;
        }
        if (choco) {
            Uint8 t = color[0];                  // rota los canales R -> G -> B
            color[0] = color[2];
            color[2] = color[1];
            color[1] = t;
        }
        return choco;
    }
};

int main()
{
    const float ANCHO = 800, ALTO = 600;
    try {
        Ventana v("Linternas", 800, 600);
        std::vector<Caja> cajas = {
            {{50, 60, 40, 40}, 220, 150, {240, 190, 90}},
            {{300, 200, 60, 30}, -180, 240, {90, 200, 240}},
            {{600, 400, 30, 60}, 140, -200, {200, 90, 160}},
        };
        int choques = 0;
        Uint64 antes = SDL_GetTicks();
        bool corriendo = true;
        while (corriendo) {
            Uint64 ahora = SDL_GetTicks();
            float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
            antes = ahora;
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                    corriendo = false;
                }
            }
            bool hubo = false;
            for (auto& c : cajas) {
                if (c.mover(dt, ANCHO, ALTO)) {
                    choques++;
                    hubo = true;
                }
            }
            if (hubo) {
                SDL_SetWindowTitle(v.ventana(), ("Linternas - choques: " + std::to_string(choques)).c_str());
            }
            SDL_SetRenderDrawColor(v.pincel(), 20, 22, 34, 255);
            SDL_RenderClear(v.pincel());
            for (const auto& c : cajas) {
                SDL_SetRenderDrawColor(v.pincel(), c.color[0], c.color[1], c.color[2], 255);
                SDL_RenderFillRect(v.pincel(), &c.r);
            }
            SDL_RenderPresent(v.pincel());
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }
    return 0;
}
```

### Misión S01-N01-M2 · Contar los cuadros

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Medí los **cuadros por segundo**: contá las vueltas del bucle y, una vez por segundo, mostralas en el título. Con la tecla `V` (sin repetición: `!e.key.repeat`), prendé y apagá el VSync. Explicá en un comentario qué cambia en los FPS y por qué el cuadrado se mueve igual de rápido en los dos casos.

#### Criterio de aprobación

- Actualiza los FPS una vez por segundo.
- La tecla V alterna el VSync.
- El comentario explica el efecto del VSync y del delta time.

#### Solución de referencia

```cpp
// S01-N01-M2 - Contar los cuadros: FPS en el titulo y VSync con la tecla V.
//
// Con VSync, SDL_RenderPresent espera al refresco del monitor: los FPS quedan en 60
// (o 144, segun el monitor) y la placa descansa. Sin VSync, el bucle corre lo mas rapido
// que puede (cientos o miles de FPS) y la placa trabaja al maximo; como todo se mueve
// con dt, la velocidad del cuadrado es la misma en los dos casos.
#include <SDL3/SDL.h>

#include <iostream>
#include <string>

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* ventana = SDL_CreateWindow("FPS", 640, 480, 0);
    SDL_Renderer* pincel = ventana ? SDL_CreateRenderer(ventana, nullptr) : nullptr;
    if (!pincel) {
        std::cerr << SDL_GetError() << "\n";
        SDL_Quit();
        return 1;
    }
    bool vsync = true;
    SDL_SetRenderVSync(pincel, 1);

    float x = 0;
    int cuadros = 0;
    Uint64 inicio_segundo = SDL_GetTicks();
    Uint64 antes = inicio_segundo;
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_V && !e.key.repeat) {
                vsync = !vsync;
                SDL_SetRenderVSync(pincel, vsync ? 1 : 0);
            }
        }
        x += 200 * dt;
        if (x > 640) {
            x -= 640 + 40;
        }
        cuadros++;
        if (ahora - inicio_segundo >= 1000) {      // una vez por segundo
            std::string t = "FPS: " + std::to_string(cuadros) + (vsync ? " (VSync)" : " (sin VSync)");
            SDL_SetWindowTitle(ventana, t.c_str());
            cuadros = 0;
            inicio_segundo = ahora;
        }
        SDL_SetRenderDrawColor(pincel, 15, 15, 25, 255);
        SDL_RenderClear(pincel);
        SDL_FRect r{x, 220, 40, 40};
        SDL_SetRenderDrawColor(pincel, 120, 220, 140, 255);
        SDL_RenderFillRect(pincel, &r);
        SDL_SetRenderDrawColor(pincel, 255, 255, 255, 255);
        SDL_RenderDebugText(pincel, 10, 10, "V: VSync si/no   ESC: salir");
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
extensiones: zip, cpp, h, txt
```

#### Consigna

El Gremio quiere un reloj de pared: tres barras que se llenan según la hora (de 24), los minutos y los segundos. Tomá la hora con `std::chrono::system_clock` y `std::localtime`, y mostrala también en el título como `hh:mm:ss` (armada con `std::ostringstream` y `std::setw`).

#### Criterio de aprobación

- Tres barras proporcionales a hora, minuto y segundo.
- La hora del título tiene ceros adelante.

#### Solución de referencia

```cpp
// S01-N01-E1 - El reloj del Gremio: tres barras para hora, minutos y segundos.
#include <SDL3/SDL.h>

#include <chrono>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <sstream>

void barra(SDL_Renderer* p, float y, float fraccion, Uint8 r, Uint8 g, Uint8 b)
{
    SDL_FRect fondo{40, y, 560, 50};
    SDL_FRect lleno{40, y, 560 * fraccion, 50};
    SDL_SetRenderDrawColor(p, 50, 50, 60, 255);
    SDL_RenderFillRect(p, &fondo);
    SDL_SetRenderDrawColor(p, r, g, b, 255);
    SDL_RenderFillRect(p, &lleno);
}

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* ventana = SDL_CreateWindow("Reloj del Gremio", 640, 300, 0);
    SDL_Renderer* p = ventana ? SDL_CreateRenderer(ventana, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    bool corriendo = true;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) {
                corriendo = false;
            }
        }
        std::time_t t = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        std::tm hora = *std::localtime(&t);
        std::ostringstream titulo;
        titulo << std::setfill('0') << std::setw(2) << hora.tm_hour << ":" << std::setw(2) << hora.tm_min << ":"
               << std::setw(2) << hora.tm_sec;
        SDL_SetWindowTitle(ventana, titulo.str().c_str());

        SDL_SetRenderDrawColor(p, 20, 22, 34, 255);
        SDL_RenderClear(p);
        barra(p, 40, hora.tm_hour / 24.0f, 240, 190, 90);
        barra(p, 120, hora.tm_min / 60.0f, 90, 200, 240);
        barra(p, 200, hora.tm_sec / 60.0f, 200, 90, 160);
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Cuáles son las cuatro partes de cada vuelta del bucle en tiempo real?

Medir el tiempo, leer la entrada, actualizar el mundo y dibujar.

#### ¿Por qué conviene envolver la ventana y el renderer en una clase RAII?

Para que se liberen siempre, en el orden correcto, aunque el programa termine por un error.

#### ¿Qué hace `SDL_RenderPresent`?

Muestra de golpe lo que se dibujó en el lienzo oculto.

#### ¿Por qué `SDL_PollEvent` va dentro de un `while`?

Porque en un mismo cuadro puede haber varios eventos pendientes y hay que procesarlos todos.

#### Si aparece `undefined reference to SDL_Init`, ¿qué falta?

Enlazar la biblioteca: `$(pkg-config --libs sdl3)` o `SDL3::SDL3` en CMake.

### Soluciones (docente)

Senda basada en `FullCursos/07-SDL3-Cpp` (01 a 09). Las entregas son archivos: se prueban compilando con SDL3 (`g++ -std=c++20 main.cpp $(pkg-config --cflags --libs sdl3)`). Todo el código se verificó compilando y enlazando contra SDL 3.2.

## S01-N02 · Teclado, sprites y animación

```meta
tipo: tema
padre: S01-N01
precio: 10
criatura: ogro
ejecutable: no
temas: juegos.entrada, juegos.sprites
usa: graf.sdl
```

### Crónica

La linterna tiene un cajón con placas de vidrio pintadas: una heroína con el pie izquierdo adelante, otra con el derecho. Pasándolas rápido, la heroína **camina**. Lima reconoce la cara de la heroína: es la que Bron armó en el Taller del Juego, con su cara.

—Un sprite es una figura; una animación, varias figuras que se turnan —dice {mentor}—. Y para que la figura te obedezca, hay que saber qué teclas estás apretando **ahora**, no solo cuáles apretaste alguna vez.

Bron aprieta dos flechas a la vez y la heroína camina en diagonal. Lima dice que así no camina ella. Bron dice que sí.

### Objetivos

- Leer el teclado como **estado** (qué teclas están apretadas ahora) y distinguir "mantenida" de "recién apretada".
- Mover con diagonal normalizada, aceleración y fricción.
- Crear **texturas** con RAII (a partir de "pixel art" escrito como texto), dibujarlas agrandadas y espejadas, y **animarlas** con `dt`.
- Usar el mouse.

### Antes de empezar

La Linterna Mágica: ventana y bucle (nodo anterior). Mover objetos (rama 3) y `std::map`.

### Explicación

#### Eventos o estado
- **Eventos** (`SDL_EVENT_KEY_DOWN`): "se apretó una tecla". Sirven para acciones puntuales (saltar, pausar, disparar). Ojo con la repetición automática: `e.key.repeat` es `true` si la tecla se mantiene.
- **Estado** (`SDL_GetKeyboardState`): un array con cada tecla, `true` si está apretada **ahora**. Sirve para moverse mientras se mantiene.

Una clase `Input` guarda el estado del cuadro actual y el del anterior. Así se sabe si una tecla está **abajo** y si fue **recién** apretada (abajo ahora y no antes). Las teclas se nombran por su posición física (`SDL_SCANCODE_W`), que no cambia con la distribución del teclado.

#### Moverse bien
- **Diagonal**: si se aprietan `D` y `S`, la dirección es (1, 1), que mide 1.41: se va más rápido en diagonal. Se **normaliza**: se divide por el largo (`std::hypot`).
- **Aceleración y fricción**: en vez de fijar la velocidad, las teclas la **cambian** (`v += aceleracion * dt`) y la fricción la frena (`v -= v * friccion * dt`). Con poca fricción parece hielo.

#### Texturas
Una **textura** es una imagen guardada en la placa de video. SDL3 sola carga imágenes `.bmp` (`SDL_LoadBMP`); para PNG hace falta la biblioteca extra **SDL_image** (`IMG_Load`). En esta Senda las imágenes se **dibujan con texto**, así no hace falta ningún archivo:
```cpp
{"..pppp..",
 "..cccc..",
 ".rrrrrr.", ...}     // cada letra es un color de una paleta (std::map<char, SDL_Color>); '.' es transparente
```
Se crea una superficie (`SDL_CreateSurface`), se pintan los píxeles (`SDL_WriteSurfacePixel`) y se convierte en textura (`SDL_CreateTextureFromSurface`). La clase `Textura` es dueña de su `SDL_Texture*`: se **mueve** pero no se copia, como un `unique_ptr`.

Para dibujar: `SDL_RenderTexture(p, tex, nullptr, &destino)` (con un destino más grande, se agranda) o `SDL_RenderTextureRotated(...)` para girar o **espejar** (`SDL_FLIP_HORIZONTAL`). Con `SDL_SetTextureScaleMode(tex, SDL_SCALEMODE_NEAREST)` los píxeles quedan nítidos al agrandar.

**Las texturas se destruyen antes que el renderer.** Si las creás en `main`, ponelas dentro de un bloque `{ }` que termine antes de `SDL_DestroyRenderer`.

#### Animación
Una animación es una lista de cuadros y un reloj: se acumula `dt` y, cada tanto (por ejemplo, 0.15 s), se pasa al cuadro siguiente. Como depende del tiempo, se ve igual a 60 o a 144 FPS.

#### El mouse
`SDL_GetMouseState(&x, &y)` da la posición y qué botones están apretados (`SDL_BUTTON_LMASK`, `SDL_BUTTON_RMASK`). Los eventos `SDL_EVENT_MOUSE_BUTTON_DOWN` y `SDL_EVENT_MOUSE_WHEEL` avisan clics y rueda.

### Código de ejemplo

```cpp
/*
 * S01-N02 - Teclado, sprites y animacion.
 * Input guarda el estado del teclado; Textura envuelve SDL_Texture con RAII;
 * el sprite se dibuja con "pixel art" escrito como texto.
 */
#include <SDL3/SDL.h>

#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// --- Teclado: mantenida, recien apretada ---
class Input {
public:
    void actualizar()
    {
        anterior_ = actual_;
        int n = 0;
        const bool* estado = SDL_GetKeyboardState(&n);
        for (int i = 0; i < n && i < SDL_SCANCODE_COUNT; i++) {
            actual_[i] = estado[i];
        }
    }
    bool abajo(SDL_Scancode k) const { return actual_[k]; }
    bool recien(SDL_Scancode k) const { return actual_[k] && !anterior_[k]; }

private:
    std::array<bool, SDL_SCANCODE_COUNT> actual_{};
    std::array<bool, SDL_SCANCODE_COUNT> anterior_{};
};

// --- Textura: duenia unica de un SDL_Texture (se mueve, no se copia) ---
class Textura {
public:
    Textura(SDL_Renderer* p, const std::vector<std::string>& dibujo, const std::map<char, SDL_Color>& paleta)
    {
        int alto = static_cast<int>(dibujo.size());
        int ancho = static_cast<int>(dibujo[0].size());
        SDL_Surface* s = SDL_CreateSurface(ancho, alto, SDL_PIXELFORMAT_RGBA32);
        if (!s) {
            throw std::runtime_error(SDL_GetError());
        }
        for (int y = 0; y < alto; y++) {
            for (int x = 0; x < ancho; x++) {
                auto it = paleta.find(dibujo[y][x]);
                SDL_Color c = it != paleta.end() ? it->second : SDL_Color{0, 0, 0, 0};   // lo demas, transparente
                SDL_WriteSurfacePixel(s, x, y, c.r, c.g, c.b, c.a);
            }
        }
        tex_ = SDL_CreateTextureFromSurface(p, s);
        SDL_DestroySurface(s);
        if (!tex_) {
            throw std::runtime_error(SDL_GetError());
        }
        SDL_SetTextureScaleMode(tex_, SDL_SCALEMODE_NEAREST);    // pixeles nitidos al agrandar
        ancho_ = static_cast<float>(ancho);
        alto_ = static_cast<float>(alto);
    }
    ~Textura()
    {
        if (tex_) {
            SDL_DestroyTexture(tex_);
        }
    }
    Textura(Textura&& o) noexcept : tex_(std::exchange(o.tex_, nullptr)), ancho_(o.ancho_), alto_(o.alto_) {}
    Textura(const Textura&) = delete;
    Textura& operator=(const Textura&) = delete;

    void dibujar(SDL_Renderer* p, float x, float y, float escala, bool espejo = false) const
    {
        SDL_FRect destino{x, y, ancho_ * escala, alto_ * escala};
        SDL_RenderTextureRotated(p, tex_, nullptr, &destino, 0, nullptr, espejo ? SDL_FLIP_HORIZONTAL : SDL_FLIP_NONE);
    }

private:
    SDL_Texture* tex_ = nullptr;
    float ancho_ = 0;
    float alto_ = 0;
};

// --- Animacion: cambia de cuadro cada "duracion" segundos ---
class Animacion {
public:
    Animacion(std::size_t cuadros, float duracion) : cuadros_(cuadros), duracion_(duracion) {}
    void avanzar(float dt)
    {
        tiempo_ += dt;
        while (tiempo_ >= duracion_) {
            tiempo_ -= duracion_;
            actual_ = (actual_ + 1) % cuadros_;
        }
    }
    void reiniciar()
    {
        actual_ = 0;
        tiempo_ = 0;
    }
    std::size_t actual() const { return actual_; }

private:
    std::size_t cuadros_;
    float duracion_;
    std::size_t actual_ = 0;
    float tiempo_ = 0;
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* ventana = SDL_CreateWindow("Sprites", 800, 600, 0);
    SDL_Renderer* p = ventana ? SDL_CreateRenderer(ventana, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    {
        const std::map<char, SDL_Color> PALETA = {
            {'p', {60, 40, 30, 255}}, {'c', {240, 200, 160, 255}}, {'r', {200, 60, 60, 255}}, {'a', {60, 90, 200, 255}}};
        std::vector<Textura> caminar;
        caminar.emplace_back(p, std::vector<std::string>{"..pppp..", "..cccc..", "..c.c.c.", "..cccc..", ".rrrrrr.", "c.rrrr.c", "..aaaa..", "..a..a..", ".aa..aa."}, PALETA);
        caminar.emplace_back(p, std::vector<std::string>{"..pppp..", "..cccc..", "..c.c.c.", "..cccc..", ".rrrrrr.", "c.rrrr.c", "..aaaa..", "..aa.a..", "...a.aa."}, PALETA);

        Input input;
        Animacion anim(caminar.size(), 0.15f);
        float x = 380, y = 280;
        bool mira_izquierda = false;
        Uint64 antes = SDL_GetTicks();
        bool corriendo = true;
        while (corriendo) {
            Uint64 ahora = SDL_GetTicks();
            float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
            antes = ahora;
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT) {
                    corriendo = false;
                }
            }
            input.actualizar();
            if (input.recien(SDL_SCANCODE_ESCAPE)) {
                corriendo = false;
            }
            float dx = input.abajo(SDL_SCANCODE_D) - input.abajo(SDL_SCANCODE_A);
            float dy = input.abajo(SDL_SCANCODE_S) - input.abajo(SDL_SCANCODE_W);
            if (dx != 0 || dy != 0) {
                float largo = std::hypot(dx, dy);            // en diagonal no va mas rapido
                x += dx / largo * 200 * dt;
                y += dy / largo * 200 * dt;
                anim.avanzar(dt);
                if (dx != 0) {
                    mira_izquierda = dx < 0;
                }
            } else {
                anim.reiniciar();
            }
            SDL_SetRenderDrawColor(p, 40, 90, 60, 255);
            SDL_RenderClear(p);
            caminar[anim.actual()].dibujar(p, x, y, 6, mira_izquierda);
            SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
            SDL_RenderDebugText(p, 10, 10, "WASD para caminar, ESC para salir");
            SDL_RenderPresent(p);
        }
    }   // las texturas se destruyen ANTES que el renderer
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Leer el teclado por estado y animar sprites con el tiempo es lo que hace cualquier juego 2D, de un plataformas a un RPG. La aceleración y la fricción le dan "peso" al movimiento (hielo, barro, agua). Las texturas generadas por código se usan en herramientas, editores de niveles y efectos (ruido, degradés, mapas de calor).

### Errores habituales

**Ogro: la diagonal más rápida.** Sin normalizar, moverse en diagonal es un 41% más rápido.

**Ogro: acciones repetidas.** Usar el estado para "saltar" hace que salte en cada cuadro mientras la tecla está abajo. Para acciones puntuales, "recién apretada" o el evento sin `repeat`.

**Troll: destruir el renderer antes que las texturas.** Las texturas pertenecen al renderer: liberarlas después es usar algo ya destruido.

**Troll: copiar una textura.** Dos objetos con el mismo `SDL_Texture*` lo destruirían dos veces. Por eso la copia está prohibida y solo se mueve.

**Goblin: el sprite borroso.** Sin `SDL_SCALEMODE_NEAREST`, el pixel art agrandado se ve lavado.

### Misión S01-N02-M1 · El lago de hielo

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Hacé que Lima patine: las teclas **aceleran** (900 px/s²), la fricción frena (`v -= v * friccion * dt`) y la rapidez tiene un máximo. La diagonal va normalizada. Contra la orilla, rebota perdiendo la mitad de la velocidad. Con `H` (recién apretada), alterná entre hielo (fricción 1.5) y tierra (fricción 10), y cambiá el color del fondo. Mostrá la rapidez actual con `SDL_RenderDebugTextFormat`.

#### Criterio de aprobación

- El movimiento usa aceleración y fricción con `dt`.
- La diagonal está normalizada y la rapidez tiene un tope.
- `H` usa "recién apretada", no el estado.

#### Solución de referencia

```cpp
// S01-N02-M1 - El lago de hielo: aceleracion y friccion, con diagonal normalizada.
#include <SDL3/SDL.h>

#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>

class Input {
public:
    void actualizar()
    {
        anterior_ = actual_;
        int n = 0;
        const bool* estado = SDL_GetKeyboardState(&n);
        for (int i = 0; i < n && i < SDL_SCANCODE_COUNT; i++) {
            actual_[i] = estado[i];
        }
    }
    bool abajo(SDL_Scancode k) const { return actual_[k]; }
    bool recien(SDL_Scancode k) const { return actual_[k] && !anterior_[k]; }

private:
    std::array<bool, SDL_SCANCODE_COUNT> actual_{};
    std::array<bool, SDL_SCANCODE_COUNT> anterior_{};
};

struct Patinadora {
    float x = 400, y = 300;
    float vx = 0, vy = 0;
    float aceleracion = 900;     // px/s^2
    float friccion = 1.5f;       // cuanto frena por segundo (sobre hielo, poco)
    float maxima = 350;          // px/s

    void actualizar(float dirx, float diry, float dt)
    {
        float largo = std::hypot(dirx, diry);
        if (largo > 0) {
            vx += dirx / largo * aceleracion * dt;
            vy += diry / largo * aceleracion * dt;
        }
        vx -= vx * friccion * dt;
        vy -= vy * friccion * dt;
        float rapidez = std::hypot(vx, vy);
        if (rapidez > maxima) {
            vx = vx / rapidez * maxima;
            vy = vy / rapidez * maxima;
        }
        x += vx * dt;
        y += vy * dt;
        if (x < 0 || x > 780) {                  // rebota suave contra la orilla
            vx = -vx * 0.5f;
            x = std::clamp(x, 0.0f, 780.0f);
        }
        if (y < 0 || y > 580) {
            vy = -vy * 0.5f;
            y = std::clamp(y, 0.0f, 580.0f);
        }
    }
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("El lago de hielo", 800, 600, 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    Input input;
    Patinadora lima;
    bool hielo = true;
    Uint64 antes = SDL_GetTicks();
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) {
                corriendo = false;
            }
        }
        input.actualizar();
        if (input.recien(SDL_SCANCODE_ESCAPE)) {
            corriendo = false;
        }
        if (input.recien(SDL_SCANCODE_H)) {        // alterna hielo y tierra
            hielo = !hielo;
            lima.friccion = hielo ? 1.5f : 10.0f;
        }
        lima.actualizar(input.abajo(SDL_SCANCODE_D) - input.abajo(SDL_SCANCODE_A),
                        input.abajo(SDL_SCANCODE_S) - input.abajo(SDL_SCANCODE_W), dt);
        SDL_SetRenderDrawColor(p, hielo ? 180 : 110, hielo ? 220 : 90, hielo ? 240 : 60, 255);
        SDL_RenderClear(p);
        SDL_FRect r{lima.x, lima.y, 20, 20};
        SDL_SetRenderDrawColor(p, 200, 60, 60, 255);
        SDL_RenderFillRect(p, &r);
        SDL_SetRenderDrawColor(p, 20, 20, 20, 255);
        SDL_RenderDebugTextFormat(p, 10, 10, "WASD mover  H hielo/tierra  rapidez %.0f", std::hypot(lima.vx, lima.vy));
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### Misión S01-N02-M2 · La bandera del Gremio

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Dibujá una bandera flameando con **tres cuadros** de pixel art (texto con una paleta en un `std::map<char, SDL_Color>`). La clase `Textura` lanza `std::invalid_argument` si las filas del dibujo no miden lo mismo. Las flechas arriba y abajo cambian la velocidad de la animación (cuadros por segundo) y la rueda del mouse, la escala. Mostrá los dos valores en pantalla.

#### Criterio de aprobación

- `Textura` es RAII, se mueve y no se copia.
- La animación avanza con `dt`.
- Valida el dibujo y lanza si está mal.

#### Solución de referencia

```cpp
// S01-N02-M2 - La bandera del Gremio: un sprite de texto con paleta, animado y agrandado.
#include <SDL3/SDL.h>

#include <algorithm>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Textura {
public:
    Textura(SDL_Renderer* p, const std::vector<std::string>& dibujo, const std::map<char, SDL_Color>& paleta)
    {
        int alto = static_cast<int>(dibujo.size());
        int ancho = static_cast<int>(dibujo[0].size());
        for (const auto& fila : dibujo) {
            if (static_cast<int>(fila.size()) != ancho) {
                throw std::invalid_argument("todas las filas del dibujo tienen que medir lo mismo");
            }
        }
        SDL_Surface* s = SDL_CreateSurface(ancho, alto, SDL_PIXELFORMAT_RGBA32);
        if (!s) {
            throw std::runtime_error(SDL_GetError());
        }
        for (int y = 0; y < alto; y++) {
            for (int x = 0; x < ancho; x++) {
                auto it = paleta.find(dibujo[y][x]);
                SDL_Color c = it != paleta.end() ? it->second : SDL_Color{0, 0, 0, 0};
                SDL_WriteSurfacePixel(s, x, y, c.r, c.g, c.b, c.a);
            }
        }
        tex_ = SDL_CreateTextureFromSurface(p, s);
        SDL_DestroySurface(s);
        if (!tex_) {
            throw std::runtime_error(SDL_GetError());
        }
        SDL_SetTextureScaleMode(tex_, SDL_SCALEMODE_NEAREST);
        w_ = static_cast<float>(ancho);
        h_ = static_cast<float>(alto);
    }
    ~Textura()
    {
        if (tex_) {
            SDL_DestroyTexture(tex_);
        }
    }
    Textura(Textura&& o) noexcept : tex_(std::exchange(o.tex_, nullptr)), w_(o.w_), h_(o.h_) {}
    Textura(const Textura&) = delete;
    Textura& operator=(const Textura&) = delete;

    void dibujar(SDL_Renderer* p, float x, float y, float escala) const
    {
        SDL_FRect d{x, y, w_ * escala, h_ * escala};
        SDL_RenderTexture(p, tex_, nullptr, &d);
    }

private:
    SDL_Texture* tex_ = nullptr;
    float w_ = 0;
    float h_ = 0;
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("La bandera del Gremio", 640, 480, 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    try {
        const std::map<char, SDL_Color> PALETA = {{'|', {90, 60, 30, 255}}, {'a', {60, 110, 220, 255}}, {'b', {240, 240, 240, 255}}, {'s', {250, 200, 40, 255}}};
        std::vector<Textura> cuadros;
        cuadros.emplace_back(p, std::vector<std::string>{"|aaaaaaaa.", "|aaaaaaaa.", "|bbbsbbbb.", "|bbbbbbbb.", "|aaaaaaaa.", "|aaaaaaaa.", "|.........", "|.........", "|........."}, PALETA);
        cuadros.emplace_back(p, std::vector<std::string>{"|.aaaaaaaa", "|aaaaaaaa.", "|bbbbsbbbb", "|bbbbbbbb.", "|.aaaaaaaa", "|aaaaaaaa.", "|.........", "|.........", "|........."}, PALETA);
        cuadros.emplace_back(p, std::vector<std::string>{"|aaaaaaaa.", "|.aaaaaaaa", "|bbbsbbbb.", "|.bbbbbbbb", "|aaaaaaaa.", "|.aaaaaaaa", "|.........", "|.........", "|........."}, PALETA);
        float escala = 16;
        float velocidad = 6;                  // cuadros por segundo
        float tiempo = 0;
        std::size_t actual = 0;
        Uint64 antes = SDL_GetTicks();
        bool corriendo = true;
        while (corriendo) {
            Uint64 ahora = SDL_GetTicks();
            float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
            antes = ahora;
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                    corriendo = false;
                } else if (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_UP) {
                    velocidad = std::min(velocidad + 2, 30.0f);
                } else if (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_DOWN) {
                    velocidad = std::max(velocidad - 2, 2.0f);
                } else if (e.type == SDL_EVENT_MOUSE_WHEEL) {
                    escala = std::clamp(escala + e.wheel.y * 2, 4.0f, 40.0f);
                }
            }
            tiempo += dt;
            if (tiempo >= 1 / velocidad) {
                tiempo = 0;
                actual = (actual + 1) % cuadros.size();
            }
            SDL_SetRenderDrawColor(p, 140, 190, 230, 255);
            SDL_RenderClear(p);
            cuadros[actual].dibujar(p, 120, 60, escala);
            SDL_SetRenderDrawColor(p, 20, 20, 20, 255);
            SDL_RenderDebugTextFormat(p, 10, 10, "flechas: velocidad %.0f  rueda: escala %.0f", velocidad, escala);
            SDL_RenderPresent(p);
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
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
extensiones: zip, cpp, h, txt
```

#### Consigna

Hacé un tablero de pixel art de 32 × 24 casillas: con el botón izquierdo apretado se pinta (se puede arrastrar), con el derecho se borra. Las teclas `1`, `2` y `3` eligen el color, `C` limpia y `G` **guarda** el dibujo en `dibujo.txt`, una fila por línea con un carácter por color (`.`, `#`, `r`, `b`).

#### Criterio de aprobación

- Usa `SDL_GetMouseState` para pintar arrastrando.
- Guarda el dibujo como texto.

#### Solución de referencia

```cpp
// S01-N02-E1 - El tablero de dibujo: pintar una grilla con el mouse y guardarla en un archivo.
#include <SDL3/SDL.h>

#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

const int COLUMNAS = 32, FILAS = 24, LADO = 20;

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("Tablero de dibujo", COLUMNAS * LADO, FILAS * LADO, 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    const std::array<SDL_Color, 4> COLORES = {{{250, 250, 250, 255}, {30, 30, 30, 255}, {220, 60, 60, 255}, {60, 120, 220, 255}}};
    std::vector<std::vector<int>> grilla(FILAS, std::vector<int>(COLUMNAS, 0));
    int pincel = 1;
    bool corriendo = true;
    while (corriendo) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) {
                corriendo = false;
            } else if (e.type == SDL_EVENT_KEY_DOWN) {
                if (e.key.key >= SDLK_1 && e.key.key <= SDLK_3) {
                    pincel = static_cast<int>(e.key.key - SDLK_1) + 1;
                } else if (e.key.key == SDLK_C) {
                    for (auto& fila : grilla) {
                        std::fill(fila.begin(), fila.end(), 0);
                    }
                } else if (e.key.key == SDLK_G) {
                    std::ofstream out("dibujo.txt");
                    for (const auto& fila : grilla) {
                        for (int c : fila) {
                            out << ".#rb"[c];
                        }
                        out << "\n";
                    }
                    SDL_SetWindowTitle(v, "Tablero de dibujo - guardado en dibujo.txt");
                }
            }
        }
        float mx = 0, my = 0;
        SDL_MouseButtonFlags botones = SDL_GetMouseState(&mx, &my);
        int col = static_cast<int>(mx) / LADO, fila = static_cast<int>(my) / LADO;
        if (col >= 0 && col < COLUMNAS && fila >= 0 && fila < FILAS) {
            if (botones & SDL_BUTTON_LMASK) {
                grilla[fila][col] = pincel;            // izquierdo: pinta (se puede arrastrar)
            } else if (botones & SDL_BUTTON_RMASK) {
                grilla[fila][col] = 0;                 // derecho: borra
            }
        }
        for (int f = 0; f < FILAS; f++) {
            for (int c = 0; c < COLUMNAS; c++) {
                SDL_Color k = COLORES[grilla[f][c]];
                SDL_SetRenderDrawColor(p, k.r, k.g, k.b, 255);
                SDL_FRect r{static_cast<float>(c * LADO), static_cast<float>(f * LADO), LADO - 1.0f, LADO - 1.0f};
                SDL_RenderFillRect(p, &r);
            }
        }
        SDL_SetRenderDrawColor(p, 120, 120, 120, 255);
        SDL_RenderDebugTextFormat(p, 4, 4, "1-3 color (%d)  clic pinta  derecho borra  C limpia  G guarda", pincel);
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre leer eventos de teclado y leer el estado del teclado?

El evento avisa una vez que se apretó una tecla; el estado dice qué teclas están apretadas en cada cuadro.

#### ¿Cómo se sabe si una tecla fue "recién apretada"?

Está abajo en este cuadro y no lo estaba en el anterior.

#### ¿Por qué hay que normalizar la dirección?

Para no ir más rápido en diagonal.

#### ¿Por qué la clase `Textura` no se puede copiar?

Porque las dos copias liberarían la misma textura.

#### ¿Qué pasa si se destruye el renderer antes que las texturas?

Las texturas quedan inválidas y liberarlas después es un error.

### Soluciones (docente)

Basado en `07-SDL3-Cpp/02-Input` a `05-Animation`. Las texturas se generan por código (sin SDL_image), como en FullCursos.

## S01-N03 · Colisiones, cámara y escenas

```meta
tipo: tema
padre: S01-N02
precio: 10
criatura: orco
ejecutable: no
temas: juegos.colisiones, juegos.camara, juegos.estados
usa: graf.sdl
```

### Crónica

La pared de la sala ya no alcanza: el mundo de la linterna es más grande que la sala. {mentor} monta la lente sobre un riel, y la proyección **sigue** a la heroína mientras recorre un laberinto que no entra entero en la pared.

Bron la hace atravesar una pared, por error. La heroína queda del otro lado, en el comedor de Oto, proyectada sobre la olla.

—Tres trucos más y la linterna es un juego —dice {mentor}—: las paredes que frenan, la cámara que sigue, y las escenas que cambian (el título, el juego, el final).

### Objetivos

- Detectar colisiones entre rectángulos (**AABB**) y resolverlas eje por eje contra un mapa de baldosas.
- Usar una **cámara** para mundos más grandes que la ventana (coordenadas del mundo y de la pantalla).
- Organizar el juego en **escenas** polimórficas (menú, juego, fin) con `unique_ptr`.

### Antes de empezar

Teclado, sprites y animación (nodo anterior). Polimorfismo y `unique_ptr` (ramas 2 y 3).

### Explicación

#### AABB: ¿se tocan dos rectángulos?
Dos rectángulos alineados con los ejes (*axis-aligned bounding boxes*) se superponen si se superponen en `x` **y** en `y`:
```cpp
bool se_tocan(const SDL_FRect& a, const SDL_FRect& b)
{
    return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}
```
(SDL trae lo mismo: `SDL_HasRectIntersectionFloat`.)

#### Resolver contra paredes: eje por eje
Detectar no alcanza: hay que **sacar** al personaje de la pared. El truco más simple y sólido:
1. mover en `x` y, si toca una pared, empujarlo afuera por el lado más cercano;
2. **después** mover en `y` y hacer lo mismo.
Así el personaje se **desliza** a lo largo de las paredes en vez de trabarse en las esquinas.

#### Mapas de baldosas
El nivel es un `std::vector<std::string>` (como el Laberinto del Minotauro): cada carácter es una baldosa de, por ejemplo, 40 × 40 píxeles. La baldosa `(fila, columna)` está en `x = columna * 40`, `y = fila * 40`. Diseñar un nivel es editar texto.

#### La cámara
Si el mundo mide 2400 × 1800 y la ventana 800 × 600, se dibuja solo una parte. La cámara es un punto `(camx, camy)`: la esquina del mundo que se ve arriba a la izquierda.
- **Del mundo a la pantalla**: `pantalla = mundo - camara`.
- Para **seguir** a Lima, la cámara se centra en ella: `camx = lima.x - ANCHO / 2`, limitada con `std::clamp` para no mostrar afuera del mundo.
- Para que se mueva **suave**, se acerca de a poco a la posición deseada: `camx += (deseada - camx) * 5 * dt`.
- Lo que no se ve **no se dibuja**: es la optimización más simple.

La lógica (colisiones, IA) trabaja en coordenadas del **mundo**; solo el dibujo convierte a pantalla.

#### Escenas
Un juego tiene pantallas (título, juego, pausa, fin) que se dibujan y responden distinto. En C++ cada una es una clase derivada de una base abstracta:
```cpp
class Escena {
public:
    virtual ~Escena() = default;
    virtual void actualizar(const Input& in, float dt) = 0;
    virtual void dibujar(SDL_Renderer* p) const = 0;
    std::unique_ptr<Escena> siguiente;     // si se llena, el juego cambia a esa escena
};
```
El bucle principal tiene un `std::unique_ptr<Escena>` y no sabe cuál es: le pide que se actualice y se dibuje. Cuando una escena llena `siguiente`, el bucle la cambia (`escena = std::move(escena->siguiente)`) y la vieja se destruye sola. Es el polimorfismo de la rama 2 y la propiedad única de la rama 3, trabajando juntos.

### Código de ejemplo

```cpp
/*
 * S01-N03 - Colisiones, camara y escenas.
 * Un mundo de baldosas mas grande que la ventana; la camara sigue a Lima;
 * las paredes frenan (AABB, resuelto eje por eje); menu y juego son escenas polimorficas.
 */
#include <SDL3/SDL.h>

#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

const float TILE = 40;
const float ANCHO = 800, ALTO = 600;

class Input {
public:
    void actualizar()
    {
        anterior_ = actual_;
        int n = 0;
        const bool* estado = SDL_GetKeyboardState(&n);
        for (int i = 0; i < n && i < SDL_SCANCODE_COUNT; i++) {
            actual_[i] = estado[i];
        }
    }
    bool abajo(SDL_Scancode k) const { return actual_[k]; }
    bool recien(SDL_Scancode k) const { return actual_[k] && !anterior_[k]; }

private:
    std::array<bool, SDL_SCANCODE_COUNT> actual_{};
    std::array<bool, SDL_SCANCODE_COUNT> anterior_{};
};

bool se_tocan(const SDL_FRect& a, const SDL_FRect& b)       // AABB: se superponen en x Y en y
{
    return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}

// --- Escenas: cada una sabe actualizarse y dibujarse, y puede pedir cambiar a otra ---
class Escena {
public:
    virtual ~Escena() = default;
    virtual void actualizar(const Input& in, float dt) = 0;
    virtual void dibujar(SDL_Renderer* p) const = 0;
    std::unique_ptr<Escena> siguiente;     // si no esta vacio, el juego cambia de escena
};

class Juego : public Escena {
public:
    Juego()
        : mapa_{"##############################", "#............#...............#", "#..######....#..######.......#",
                "#..#....#....#..#....#.......#", "#..#....#.......#....#.......#", "#..#.............######......#",
                "#..######....#...............#", "#............#.......#########", "######..######...............#",
                "#............................#", "#....#########.......####....#", "#............#..........#....#",
                "#............#..........#....#", "##############################"}
    {
    }

    void actualizar(const Input& in, float dt) override
    {
        float dx = in.abajo(SDL_SCANCODE_D) - in.abajo(SDL_SCANCODE_A);
        float dy = in.abajo(SDL_SCANCODE_S) - in.abajo(SDL_SCANCODE_W);
        float largo = std::hypot(dx, dy);
        if (largo > 0) {
            dx /= largo;
            dy /= largo;
        }
        // Eje por eje: mover en x y corregir, despues mover en y y corregir. Asi se desliza por las paredes.
        lima_.x += dx * 220 * dt;
        resolver(true);
        lima_.y += dy * 220 * dt;
        resolver(false);
        // La camara centra a Lima, sin mostrar afuera del mundo.
        float mundo_w = mapa_[0].size() * TILE, mundo_h = mapa_.size() * TILE;
        camx_ = std::clamp(lima_.x + lima_.w / 2 - ANCHO / 2, 0.0f, mundo_w - ANCHO);
        camy_ = std::clamp(lima_.y + lima_.h / 2 - ALTO / 2, 0.0f, mundo_h - ALTO);
    }

    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 30, 34, 44, 255);
        SDL_RenderClear(p);
        for (std::size_t f = 0; f < mapa_.size(); f++) {
            for (std::size_t c = 0; c < mapa_[f].size(); c++) {
                if (mapa_[f][c] == '#') {
                    SDL_FRect r{c * TILE - camx_, f * TILE - camy_, TILE, TILE};     // mundo -> pantalla
                    SDL_SetRenderDrawColor(p, 110, 100, 90, 255);
                    SDL_RenderFillRect(p, &r);
                }
            }
        }
        SDL_FRect k{lima_.x - camx_, lima_.y - camy_, lima_.w, lima_.h};
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_RenderFillRect(p, &k);
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        SDL_RenderDebugText(p, 10, 10, "WASD mover   ESC menu");
    }

private:
    void resolver(bool en_x)
    {
        for (std::size_t f = 0; f < mapa_.size(); f++) {
            for (std::size_t c = 0; c < mapa_[f].size(); c++) {
                SDL_FRect pared{c * TILE, f * TILE, TILE, TILE};
                if (mapa_[f][c] != '#' || !se_tocan(lima_, pared)) {
                    continue;
                }
                if (en_x) {       // empujar afuera por el lado mas cercano
                    lima_.x = (lima_.x + lima_.w / 2 < pared.x + TILE / 2) ? pared.x - lima_.w : pared.x + TILE;
                } else {
                    lima_.y = (lima_.y + lima_.h / 2 < pared.y + TILE / 2) ? pared.y - lima_.h : pared.y + TILE;
                }
            }
        }
    }

    std::vector<std::string> mapa_;
    SDL_FRect lima_{60, 60, 26, 26};
    float camx_ = 0, camy_ = 0;
};

class Menu : public Escena {
public:
    void actualizar(const Input& in, float dt) override
    {
        parpadeo_ += dt;
        if (in.recien(SDL_SCANCODE_RETURN)) {
            siguiente = std::make_unique<Juego>();
        }
    }
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 70, 60, "LA LINTERNA MAGICA");
        SDL_SetRenderScale(p, 1, 1);
        if (static_cast<int>(parpadeo_ * 2) % 2 == 0) {
            SDL_RenderDebugText(p, 320, 330, "ENTER para jugar");
        }
    }

private:
    float parpadeo_ = 0;
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("Colisiones, cámara y escenas", static_cast<int>(ANCHO), static_cast<int>(ALTO), 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    Input input;
    std::unique_ptr<Escena> escena = std::make_unique<Menu>();
    Uint64 antes = SDL_GetTicks();
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) {
                corriendo = false;
            }
        }
        input.actualizar();
        if (input.recien(SDL_SCANCODE_ESCAPE)) {
            escena = std::make_unique<Menu>();
        }
        escena->actualizar(input, dt);
        if (escena->siguiente) {
            escena = std::move(escena->siguiente);     // la escena vieja se destruye sola
        }
        escena->dibujar(p);
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Colisiones AABB, mapas de baldosas y cámaras son la base de los juegos de plataformas, los RPG de vista cenital y los *roguelikes* gráficos. Las escenas organizan cualquier aplicación con pantallas: juegos, kioscos interactivos, aplicaciones de museo, instaladores.

### Errores habituales

**Ogro: resolver los dos ejes juntos.** Mover en `x` e `y` a la vez y después corregir hace que el personaje se trabe en las esquinas o atraviese paredes en diagonal.

**Ogro: el túnel.** Con un `dt` muy grande, un objeto rápido puede pasar de un lado al otro de una pared delgada en un solo cuadro. Por eso se limita `dt`.

**Ogro: mezclar coordenadas.** Comparar la posición del mouse (pantalla) con la de un enemigo (mundo) sin sumar la cámara.

**Ogro: la cámara que muestra el vacío.** Sin `std::clamp`, en los bordes del mundo se ve lo que hay "afuera".

**Troll: usar la escena después de cambiarla.** Después de `escena = std::move(escena->siguiente)`, la escena vieja ya no existe: no se puede seguir usando nada de ella en ese cuadro.

### Misión S01-N03-M1 · El laberinto de las monedas

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

Armá un laberinto de baldosas (`#` pared, `o` moneda) con una clase `Laberinto` que carga el mapa, guarda las monedas como rectángulos, resuelve colisiones eje por eje (`resolver(caja, en_x)`, un método `const`) y junta monedas con `std::erase_if` (devolviendo cuántas juntó). Lima se mueve con WASD. Cuando junta todas, mostrá el tiempo que tardó.

#### Criterio de aprobación

- Lima se desliza por las paredes sin trabarse.
- Las monedas se juntan con `erase_if` y AABB.
- Al final se muestra el tiempo.

#### Solución de referencia

```cpp
// S01-N03-M1 - El laberinto de las monedas: colision por ejes contra baldosas y monedas que se juntan.
#include <SDL3/SDL.h>

#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

const float T = 40;

bool se_tocan(const SDL_FRect& a, const SDL_FRect& b)
{
    return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}

class Laberinto {
public:
    explicit Laberinto(std::vector<std::string> filas) : filas_(std::move(filas))
    {
        for (std::size_t f = 0; f < filas_.size(); f++) {
            for (std::size_t c = 0; c < filas_[f].size(); c++) {
                if (filas_[f][c] == 'o') {
                    monedas_.push_back({c * T + 12, f * T + 12, 16, 16});
                    filas_[f][c] = '.';
                }
            }
        }
    }

    // Empuja la caja afuera de las paredes que toca, en un eje.
    void resolver(SDL_FRect& caja, bool en_x) const
    {
        for (std::size_t f = 0; f < filas_.size(); f++) {
            for (std::size_t c = 0; c < filas_[f].size(); c++) {
                SDL_FRect pared{c * T, f * T, T, T};
                if (filas_[f][c] == '#' && se_tocan(caja, pared)) {
                    if (en_x) {
                        caja.x = (caja.x + caja.w / 2 < pared.x + T / 2) ? pared.x - caja.w : pared.x + T;
                    } else {
                        caja.y = (caja.y + caja.h / 2 < pared.y + T / 2) ? pared.y - caja.h : pared.y + T;
                    }
                }
            }
        }
    }

    int juntar(const SDL_FRect& caja)
    {
        return static_cast<int>(std::erase_if(monedas_, [&caja](const SDL_FRect& m) { return se_tocan(caja, m); }));
    }

    bool sin_monedas() const { return monedas_.empty(); }

    void dibujar(SDL_Renderer* p) const
    {
        SDL_SetRenderDrawColor(p, 90, 80, 110, 255);
        for (std::size_t f = 0; f < filas_.size(); f++) {
            for (std::size_t c = 0; c < filas_[f].size(); c++) {
                if (filas_[f][c] == '#') {
                    SDL_FRect r{c * T, f * T, T, T};
                    SDL_RenderFillRect(p, &r);
                }
            }
        }
        SDL_SetRenderDrawColor(p, 250, 210, 60, 255);
        for (const auto& m : monedas_) {
            SDL_RenderFillRect(p, &m);
        }
    }

private:
    std::vector<std::string> filas_;
    std::vector<SDL_FRect> monedas_;
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("El laberinto de las monedas", 800, 600, 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    Laberinto lab({"####################", "#o.....#......o....#", "#.###..#..####.###.#", "#.#o...#.....#...#o#",
                   "#.#####.####.#.#.#.#", "#.......#o...#.#...#", "####.##.#.####.###.#", "#o...#..#......#...#",
                   "#.#.##.####.#..#.#o#", "#.#......o..#....#.#", "#.####.#######.#.#.#", "#o.....#o.......#..#",
                   "####################"});
    SDL_FRect lima{44, 44, 28, 28};
    int juntadas = 0;
    Uint64 inicio = SDL_GetTicks(), antes = inicio;
    float tiempo_final = 0;
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool* k = SDL_GetKeyboardState(nullptr);
        float dx = k[SDL_SCANCODE_D] - k[SDL_SCANCODE_A], dy = k[SDL_SCANCODE_S] - k[SDL_SCANCODE_W];
        float largo = std::hypot(dx, dy);
        if (largo > 0 && !lab.sin_monedas()) {
            lima.x += dx / largo * 200 * dt;
            lab.resolver(lima, true);
            lima.y += dy / largo * 200 * dt;
            lab.resolver(lima, false);
            juntadas += lab.juntar(lima);
            if (lab.sin_monedas()) {
                tiempo_final = (ahora - inicio) / 1000.0f;
            }
        }
        SDL_SetRenderDrawColor(p, 25, 25, 35, 255);
        SDL_RenderClear(p);
        lab.dibujar(p);
        SDL_SetRenderDrawColor(p, 90, 200, 240, 255);
        SDL_RenderFillRect(p, &lima);
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        if (lab.sin_monedas()) {
            SDL_RenderDebugTextFormat(p, 250, 290, "¡Todas! %d monedas en %.1f segundos", juntadas, tiempo_final);
        } else {
            SDL_RenderDebugTextFormat(p, 10, 525, "Monedas: %d", juntadas);
        }
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### Misión S01-N03-M2 · La cámara y el minimapa

```meta
entrega: archivo
entorno: local
monedas: 5
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

En un mundo de 2400 × 1800 con 120 árboles al azar (con semilla), la cámara sigue a Lima **suavemente** y no muestra fuera del mundo. Solo se dibujan los árboles visibles (mostrá cuántos se dibujan). En una esquina, un **minimapa**: el mundo entero a escala, con el rectángulo de lo que se ve y un punto para Lima.

#### Criterio de aprobación

- La cámara convierte del mundo a la pantalla y se limita con `std::clamp`.
- No se dibuja lo que queda fuera de la vista.
- El minimapa muestra la vista y a Lima.

#### Solución de referencia

```cpp
// S01-N03-M2 - La camara y el minimapa: un mundo tres veces mas grande que la ventana.
#include <SDL3/SDL.h>

#include <algorithm>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

const float ANCHO = 800, ALTO = 600;
const float MUNDO_W = 2400, MUNDO_H = 1800;

class Camara {
public:
    void seguir(const SDL_FRect& objetivo, float dt)
    {
        float deseada_x = std::clamp(objetivo.x + objetivo.w / 2 - ANCHO / 2, 0.0f, MUNDO_W - ANCHO);
        float deseada_y = std::clamp(objetivo.y + objetivo.h / 2 - ALTO / 2, 0.0f, MUNDO_H - ALTO);
        float suavidad = std::min(1.0f, 5 * dt);          // se acerca de a poco: movimiento suave
        x_ += (deseada_x - x_) * suavidad;
        y_ += (deseada_y - y_) * suavidad;
    }
    SDL_FRect a_pantalla(const SDL_FRect& r) const { return {r.x - x_, r.y - y_, r.w, r.h}; }
    bool se_ve(const SDL_FRect& r) const { return r.x + r.w > x_ && r.x < x_ + ANCHO && r.y + r.h > y_ && r.y < y_ + ALTO; }
    float x() const { return x_; }
    float y() const { return y_; }

private:
    float x_ = 0, y_ = 0;
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("Cámara y minimapa", static_cast<int>(ANCHO), static_cast<int>(ALTO), 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    std::mt19937 gen(7);
    std::uniform_real_distribution<float> rx(0, MUNDO_W - 60), ry(0, MUNDO_H - 60);
    std::vector<SDL_FRect> arboles;
    for (int i = 0; i < 120; i++) {
        arboles.push_back({rx(gen), ry(gen), 40, 40});
    }
    SDL_FRect lima{MUNDO_W / 2, MUNDO_H / 2, 24, 24};
    Camara cam;
    Uint64 antes = SDL_GetTicks();
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            }
        }
        const bool* k = SDL_GetKeyboardState(nullptr);
        float dx = k[SDL_SCANCODE_D] - k[SDL_SCANCODE_A], dy = k[SDL_SCANCODE_S] - k[SDL_SCANCODE_W];
        float largo = std::hypot(dx, dy);
        if (largo > 0) {
            lima.x = std::clamp(lima.x + dx / largo * 300 * dt, 0.0f, MUNDO_W - lima.w);
            lima.y = std::clamp(lima.y + dy / largo * 300 * dt, 0.0f, MUNDO_H - lima.h);
        }
        cam.seguir(lima, dt);

        SDL_SetRenderDrawColor(p, 60, 120, 60, 255);
        SDL_RenderClear(p);
        int dibujados = 0;
        SDL_SetRenderDrawColor(p, 30, 80, 40, 255);
        for (const auto& a : arboles) {
            if (cam.se_ve(a)) {                        // solo se dibuja lo que esta en pantalla
                SDL_FRect r = cam.a_pantalla(a);
                SDL_RenderFillRect(p, &r);
                dibujados++;
            }
        }
        SDL_FRect kk = cam.a_pantalla(lima);
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_RenderFillRect(p, &kk);

        // Minimapa: el mundo entero, a escala, en una esquina
        const float ESCALA = 0.08f;
        SDL_FRect marco{ANCHO - MUNDO_W * ESCALA - 10, 10, MUNDO_W * ESCALA, MUNDO_H * ESCALA};
        SDL_SetRenderDrawColor(p, 0, 0, 0, 200);
        SDL_RenderFillRect(p, &marco);
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        SDL_FRect vista{marco.x + cam.x() * ESCALA, marco.y + cam.y() * ESCALA, ANCHO * ESCALA, ALTO * ESCALA};
        SDL_RenderRect(p, &vista);
        SDL_FRect punto{marco.x + lima.x * ESCALA - 2, marco.y + lima.y * ESCALA - 2, 4, 4};
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_RenderFillRect(p, &punto);
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(p, 10, 10, "WASD  (%.0f, %.0f)  árboles dibujados: %d de %zu", lima.x, lima.y, dibujados, arboles.size());
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### Encargo S01-N03-E1 · El kiosco del museo

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 20
extensiones: zip, cpp, h, txt
```

#### Consigna

El museo de la Ciudadela quiere un kiosco interactivo: una **portada** que titila ("Tocá cualquier tecla"), un **recorrido** por salas (las flechas cambian de sala) y, si nadie toca nada durante 15 segundos, vuelve **solo** a la portada. Organizalo con escenas polimórficas y `unique_ptr`, con un método `evento` para que cada escena reciba los eventos que le interesan.

#### Criterio de aprobación

- Cada pantalla es una escena derivada de una base abstracta.
- La inactividad se mide con `dt`.

#### Solución de referencia

```cpp
// S01-N03-E1 - El kiosco interactivo del museo: escenas (portada, recorrido, pausa por inactividad).
#include <SDL3/SDL.h>

#include <algorithm>
#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

class Escena {
public:
    virtual ~Escena() = default;
    virtual void evento(const SDL_Event& e) = 0;
    virtual void actualizar(float dt) = 0;
    virtual void dibujar(SDL_Renderer* p) const = 0;
    std::unique_ptr<Escena> siguiente;
};

class Portada;

class Recorrido : public Escena {
public:
    void evento(const SDL_Event& e) override;
    void actualizar(float dt) override;
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 30, 40, 60, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, 240, 220, 180, 255);
        SDL_SetRenderScale(p, 2, 2);
        SDL_RenderDebugTextFormat(p, 20, 20, "Sala %zu de %zu", sala_ + 1, SALAS.size());
        SDL_RenderDebugText(p, 20, 60, SALAS[sala_].c_str());
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugText(p, 40, 540, "<- -> cambiar de sala   (sin tocar nada 15 s, vuelve a la portada)");
    }

private:
    inline static const std::vector<std::string> SALAS = {"Los relojes de la Ciudadela", "Autómatas de latón", "El primer vitral", "La linterna mágica"};
    std::size_t sala_ = 0;
    float quieto_ = 0;
};

class Portada : public Escena {
public:
    void evento(const SDL_Event& e) override
    {
        if (e.type == SDL_EVENT_KEY_DOWN || e.type == SDL_EVENT_MOUSE_BUTTON_DOWN) {
            siguiente = std::make_unique<Recorrido>();
        }
    }
    void actualizar(float dt) override { t_ += dt; }
    void dibujar(SDL_Renderer* p) const override
    {
        Uint8 brillo = static_cast<Uint8>(120 + 100 * (static_cast<int>(t_ * 2) % 2));
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, brillo, brillo, 255, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 40, 80, "MUSEO DE LA CIUDADELA");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugText(p, 300, 360, "Tocá cualquier tecla");
    }

private:
    float t_ = 0;
};

void Recorrido::evento(const SDL_Event& e)
{
    if (e.type == SDL_EVENT_KEY_DOWN) {
        quieto_ = 0;
        if (e.key.key == SDLK_RIGHT) {
            sala_ = std::min(sala_ + 1, SALAS.size() - 1);
        } else if (e.key.key == SDLK_LEFT && sala_ > 0) {
            sala_--;
        }
    }
}

void Recorrido::actualizar(float dt)
{
    quieto_ += dt;
    if (quieto_ > 15) {
        siguiente = std::make_unique<Portada>();       // inactividad: vuelve solo a la portada
    }
}

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("Kiosco del museo", 800, 600, 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    std::unique_ptr<Escena> escena = std::make_unique<Portada>();
    Uint64 antes = SDL_GetTicks();
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || (e.type == SDL_EVENT_KEY_DOWN && e.key.key == SDLK_ESCAPE)) {
                corriendo = false;
            } else {
                escena->evento(e);
            }
        }
        escena->actualizar(dt);
        if (escena->siguiente) {
            escena = std::move(escena->siguiente);
        }
        escena->dibujar(p);
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Cuándo se superponen dos rectángulos AABB?

Cuando se superponen en `x` y también en `y`.

#### ¿Por qué se resuelven las colisiones eje por eje?

Para que el personaje se deslice por las paredes en vez de trabarse en las esquinas.

#### ¿Cómo se pasa de coordenadas del mundo a la pantalla?

Restando la posición de la cámara.

#### ¿Por qué conviene no dibujar lo que no se ve?

Porque es trabajo inútil: en mundos grandes, la mayoría de los objetos está fuera de la vista.

#### ¿Cómo cambia de escena el bucle sin saber qué escena es?

La escena actual llena su `siguiente` y el bucle hace `escena = std::move(escena->siguiente)`.

### Soluciones (docente)

Basado en `07-SDL3-Cpp/06-Collision`, `07-Camera` y `08-Scene`.

## S01-N04 · Jefe de la Linterna: el Espectro

```meta
tipo: jefe
padre: S01-N03
precio: 10
criatura: dragon
ejecutable: no
insignia: Cazador del Espectro
insignia_descripcion: Venciste al Espectro de la Linterna: hiciste un videojuego completo en C++ con SDL3.
usa: graf.sdl, juegos.ia, prog.modulos
```

### Crónica

La linterna se apaga de golpe. En la oscuridad se oye un zumbido de proyector: el **Espectro de la Linterna** se escapó de las placas de vidrio y se llevó las gemas que la hacen brillar. Ahora flota por un laberinto, con otros espectros, atravesando paredes.

Lyn apuesta a que Bron no junta las gemas antes del amanecer. Oto apuesta a que sí, y le prepara un guiso para la espera.

—Juntá las gemas y la linterna se enciende otra vez —dice {mentor}—. Pero no dejes que te toquen: los espectros no tienen prisa, pero tampoco se cansan.

### Objetivos

Construir un videojuego completo en C++ con SDL3, repartido en módulos: recursos con RAII, mapa de baldosas con colisiones, actores con IA, cámara, escenas y un marcador.

### Antes de empezar

Toda la Senda.

### Explicación

#### El proyecto
| Archivo | Qué tiene |
|---|---|
| `Base.h` / `.cpp` | `Input`, `Textura` (RAII, se mueve), `se_tocan`, `Camara` |
| `Mundo.h` / `.cpp` | el mapa: paredes, gemas, dónde empiezan Lima y los espectros; lanza si el mapa es inválido |
| `Actores.h` / `.cpp` | `Lima` (movimiento con colisión, vidas, invulnerabilidad) y `Espectro` (vaga en círculos o persigue) |
| `main.cpp` | el nivel, las escenas (`Menu`, `Partida`, `Fin`) y el bucle |

Fijate en lo que **no** cambió desde el Laberinto del Minotauro: el mapa es texto, la lógica está separada del dibujo, el mundo valida y lanza, y el bucle es entrada → actualizar → dibujar. Lo nuevo es el tiempo real (`dt`), la cámara y las texturas.

#### Invulnerabilidad
Si un espectro toca a Lima, pierde una vida y queda **invulnerable** un segundo y medio (parpadea). Si no, un espectro encima le sacaría todas las vidas en unos pocos cuadros.

#### Cómo encararlo
1. Compilá el proyecto tal como está y jugalo.
2. Leé cada módulo: qué hace cada clase y quién llama a quién.
3. Recién después, las misiones: agregar cosas sin romper lo que anda.

### ¿Para qué sirve?

Este es el esqueleto de un juego 2D real: se puede agrandar con más niveles, sonido (SDL_mixer), imágenes (SDL_image), texto lindo (SDL_ttf) y menús. Muchos juegos independientes publicados empezaron exactamente así.

### Errores habituales

**Esqueleto: el `.cpp` que falta en CMake.** `undefined reference` a los métodos de ese módulo.

**Troll: la textura que sobrevive al renderer.** Las texturas viven dentro de la escena `Partida`; la escena se destruye antes que el renderer, porque vive dentro del bloque del bucle.

**Ogro: el golpe en cada cuadro.** Sin invulnerabilidad, un toque dura varios cuadros y descuenta varias vidas.

**Ogro: el mapa con filas de distinto largo.** `Mundo` lanza `std::invalid_argument`: el programa lo informa en vez de leer fuera del mapa.

### Misión S01-N04-M1 · El Espectro de la Linterna

```meta
entrega: archivo
entorno: local
monedas: 8
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Compilá el juego con CMake y jugalo hasta ganar. Después, agregale **dos** cosas:
1. **Un nuevo tipo de gema** (`G`, grande): vale 5 y hace a Lima invulnerable 3 segundos.
2. **Un segundo nivel**: al juntar todas las gemas del primero, la partida carga el segundo (otro `std::vector<std::string>`) en vez de terminar; el juego se gana al completar los dos.

Entregá el proyecto completo en un `.zip`.

#### Criterio de aprobación

- El proyecto compila con CMake sin advertencias.
- La gema grande suma 5 y da invulnerabilidad.
- Hay dos niveles y se pasa de uno al otro.
- No hay pérdidas de recursos (las texturas y SDL se liberan).

#### Código inicial

```cpp
/*
 * Jefe de la Linterna Magica: juntar todas las gemas del laberinto sin que los espectros te alcancen.
 * g++ -std=c++20 -Wall -Wextra -o espectro *.cpp $(pkg-config --cflags --libs sdl3)
 */
#include <SDL3/SDL.h>

#include <algorithm>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <utility>
#include <vector>

#include "Actores.h"
#include "Base.h"
#include "Mundo.h"

const std::vector<std::string> NIVEL = {
    "##############################",
    "#K...........#..........g....#",
    "#.######.###.#.#######.####..#",
    "#.#g...#...#...#.....#....#..#",
    "#.#....#.E.#####..g..#.E..#..#",
    "#.#....#.........#...#....#.g#",
    "#.####.#####.###.#.###.####..#",
    "#......g...#...#.........#...#",
    "#####.####.#.E.#.#######.#.###",
    "#g..#......#...#.#..g..#.#...#",
    "#...#.####.#####.#.....#.###.#",
    "#...#....#.......#..E..#.....#",
    "#.######.#########.....#####.#",
    "#..........g.......#......g..#",
    "##############################",
};

class Escena {
public:
    virtual ~Escena() = default;
    virtual void actualizar(const Input& in, float dt) = 0;
    virtual void dibujar(SDL_Renderer* p) const = 0;
    std::unique_ptr<Escena> siguiente;
};

class Fin : public Escena {
public:
    Fin(bool gano, int gemas, float segundos) : gano_(gano), gemas_(gemas), segundos_(segundos) {}
    void actualizar(const Input& in, float dt) override;
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, gano_ ? 120 : 230, gano_ ? 230 : 90, 120, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 50, 60, gano_ ? "LA LINTERNA SE ENCIENDE" : "LOS ESPECTROS GANAN");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugTextFormat(p, 280, 320, "Gemas: %d   Tiempo: %.1f s", gemas_, segundos_);
        SDL_RenderDebugText(p, 300, 360, "ENTER para volver al menu");
    }

private:
    bool gano_;
    int gemas_;
    float segundos_;
};

class Partida : public Escena {
public:
    Partida(SDL_Renderer* p) : mundo_(NIVEL), lima_(mundo_.inicio_lima())
    {
        const std::map<char, SDL_Color> PALETA = {{'p', {60, 40, 30, 255}}, {'c', {240, 200, 160, 255}}, {'r', {200, 60, 60, 255}}, {'a', {60, 90, 200, 255}}, {'b', {230, 235, 255, 200}}, {'o', {20, 20, 40, 255}}};
        sprites_.emplace_back(p, std::vector<std::string>{"..pppp..", "..cccc..", "..c.c.c.", "..cccc..", ".rrrrrr.", "c.rrrr.c", "..aaaa..", "..a..a..", ".aa..aa."}, PALETA);
        sprites_.emplace_back(p, std::vector<std::string>{"..bbbb..", ".bbbbbb.", "bboobbob", "bboobbob", "bbbbbbbb", "bbbbbbbb", "bbbbbbbb", "b.bb.bb.", "...b...b"}, PALETA);
        float fase = 0;
        for (const auto& e : mundo_.espectros()) {
            espectros_.emplace_back(e, fase);
            fase += 1.7f;
        }
    }

    void actualizar(const Input& in, float dt) override
    {
        tiempo_ += dt;
        lima_.actualizar(in, mundo_, dt);
        gemas_ += mundo_.juntar(lima_.caja());
        for (auto& e : espectros_) {
            e.actualizar(lima_.caja(), dt);
            if (se_tocan(e.caja(), lima_.caja())) {
                lima_.recibir_golpe();
            }
        }
        cam_.x = std::clamp(lima_.caja().x - ANCHO / 2, 0.0f, mundo_.ancho() - ANCHO);
        cam_.y = std::clamp(lima_.caja().y - ALTO / 2, 0.0f, mundo_.alto() - ALTO);
        if (mundo_.gemas() == 0 || !lima_.viva()) {
            siguiente = std::make_unique<Fin>(lima_.viva(), gemas_, tiempo_);
        }
    }

    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 25, 22, 35, 255);
        SDL_RenderClear(p);
        mundo_.dibujar(p, cam_, tiempo_);
        bool visible = !lima_.parpadea() || static_cast<int>(tiempo_ * 10) % 2 == 0;
        if (visible) {
            sprites_[0].dibujar(p, cam_.a_pantalla(lima_.caja()), lima_.mira_izquierda());
        }
        for (const auto& e : espectros_) {
            sprites_[1].dibujar(p, cam_.a_pantalla(e.caja()));
        }
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(p, 10, 10, "Vidas: %d   Gemas: %d (faltan %zu)   %.0f s", lima_.vidas(), gemas_, mundo_.gemas(), tiempo_);
    }

private:
    Mundo mundo_;
    Lima lima_;
    std::vector<Espectro> espectros_;
    std::vector<Textura> sprites_;
    Camara cam_;
    int gemas_ = 0;
    float tiempo_ = 0;
};

class Menu : public Escena {
public:
    explicit Menu(SDL_Renderer* p) : p_(p) {}
    void actualizar(const Input& in, float dt) override
    {
        t_ += dt;
        if (in.recien(SDL_SCANCODE_RETURN)) {
            siguiente = std::make_unique<Partida>(p_);
        }
    }
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 45, 50, "EL ESPECTRO DE LA LINTERNA");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugText(p, 230, 300, "Junta todas las gemas. WASD para moverte.");
        if (static_cast<int>(t_ * 2) % 2 == 0) {
            SDL_RenderDebugText(p, 330, 360, "ENTER para empezar");
        }
    }

private:
    SDL_Renderer* p_;
    float t_ = 0;
};

SDL_Renderer* g_pincel = nullptr;        // para que Fin pueda volver a crear el menu

void Fin::actualizar(const Input& in, float)
{
    if (in.recien(SDL_SCANCODE_RETURN)) {
        siguiente = std::make_unique<Menu>(g_pincel);
    }
}

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* ventana = SDL_CreateWindow("El Espectro de la Linterna", static_cast<int>(ANCHO), static_cast<int>(ALTO), 0);
    g_pincel = ventana ? SDL_CreateRenderer(ventana, nullptr) : nullptr;
    if (!g_pincel) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(g_pincel, 1);
    try {
        Input input;
        std::unique_ptr<Escena> escena = std::make_unique<Menu>(g_pincel);
        Uint64 antes = SDL_GetTicks();
        bool corriendo = true;
        while (corriendo) {
            Uint64 ahora = SDL_GetTicks();
            float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
            antes = ahora;
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT) {
                    corriendo = false;
                }
            }
            input.actualizar();
            if (input.recien(SDL_SCANCODE_ESCAPE)) {
                corriendo = false;
            }
            escena->actualizar(input, dt);
            if (escena->siguiente) {
                escena = std::move(escena->siguiente);
            }
            escena->dibujar(g_pincel);
            SDL_RenderPresent(g_pincel);
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
    SDL_DestroyRenderer(g_pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Solución de referencia

```cpp
// ===== Base.h =====
#pragma once
// Piezas comunes del juego: teclado, texturas con RAII y colisiones.

#include <SDL3/SDL.h>

#include <array>
#include <map>
#include <string>
#include <vector>

constexpr float ANCHO = 800;
constexpr float ALTO = 600;
constexpr float TILE = 40;

class Input {
public:
    void actualizar();
    bool abajo(SDL_Scancode k) const { return actual_[k]; }
    bool recien(SDL_Scancode k) const { return actual_[k] && !anterior_[k]; }

private:
    std::array<bool, SDL_SCANCODE_COUNT> actual_{};
    std::array<bool, SDL_SCANCODE_COUNT> anterior_{};
};

// Una textura hecha con "pixel art" de texto. Duenia unica: se mueve, no se copia.
class Textura {
public:
    Textura(SDL_Renderer* p, const std::vector<std::string>& dibujo, const std::map<char, SDL_Color>& paleta);
    ~Textura();
    Textura(Textura&& otra) noexcept;
    Textura& operator=(Textura&&) = delete;
    Textura(const Textura&) = delete;
    Textura& operator=(const Textura&) = delete;
    void dibujar(SDL_Renderer* p, const SDL_FRect& destino, bool espejo = false) const;

private:
    SDL_Texture* tex_ = nullptr;
};

bool se_tocan(const SDL_FRect& a, const SDL_FRect& b);

struct Camara {
    float x = 0;
    float y = 0;
    SDL_FRect a_pantalla(const SDL_FRect& r) const { return {r.x - x, r.y - y, r.w, r.h}; }
};

// ===== Base.cpp =====
#include "Base.h"

#include <stdexcept>
#include <utility>

void Input::actualizar()
{
    anterior_ = actual_;
    int n = 0;
    const bool* estado = SDL_GetKeyboardState(&n);
    for (int i = 0; i < n && i < SDL_SCANCODE_COUNT; i++) {
        actual_[i] = estado[i];
    }
}

Textura::Textura(SDL_Renderer* p, const std::vector<std::string>& dibujo, const std::map<char, SDL_Color>& paleta)
{
    int alto = static_cast<int>(dibujo.size());
    int ancho = static_cast<int>(dibujo.at(0).size());
    SDL_Surface* s = SDL_CreateSurface(ancho, alto, SDL_PIXELFORMAT_RGBA32);
    if (!s) {
        throw std::runtime_error(SDL_GetError());
    }
    for (int y = 0; y < alto; y++) {
        for (int x = 0; x < ancho; x++) {
            auto it = paleta.find(dibujo[y].at(x));
            SDL_Color c = it != paleta.end() ? it->second : SDL_Color{0, 0, 0, 0};
            SDL_WriteSurfacePixel(s, x, y, c.r, c.g, c.b, c.a);
        }
    }
    tex_ = SDL_CreateTextureFromSurface(p, s);
    SDL_DestroySurface(s);
    if (!tex_) {
        throw std::runtime_error(SDL_GetError());
    }
    SDL_SetTextureScaleMode(tex_, SDL_SCALEMODE_NEAREST);
}

Textura::~Textura()
{
    if (tex_) {
        SDL_DestroyTexture(tex_);
    }
}

Textura::Textura(Textura&& otra) noexcept : tex_(std::exchange(otra.tex_, nullptr)) {}

void Textura::dibujar(SDL_Renderer* p, const SDL_FRect& destino, bool espejo) const
{
    SDL_RenderTextureRotated(p, tex_, nullptr, &destino, 0, nullptr, espejo ? SDL_FLIP_HORIZONTAL : SDL_FLIP_NONE);
}

bool se_tocan(const SDL_FRect& a, const SDL_FRect& b)
{
    return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}

// ===== Mundo.h =====
#pragma once

#include <string>
#include <vector>

#include "Base.h"

// El mapa: '#' pared, 'g' gema, 'K' inicio de Lima, 'E' un espectro. Lanza si el mapa es invalido.
class Mundo {
public:
    explicit Mundo(const std::vector<std::string>& filas);

    void resolver(SDL_FRect& caja, bool en_x) const;       // saca la caja de las paredes, en un eje
    int juntar(const SDL_FRect& caja);                      // gemas que toca: las quita y dice cuantas
    std::size_t gemas() const { return gemas_.size(); }
    SDL_FRect inicio_lima() const { return inicio_; }
    const std::vector<SDL_FRect>& espectros() const { return espectros_; }
    float ancho() const { return static_cast<float>(filas_[0].size()) * TILE; }
    float alto() const { return static_cast<float>(filas_.size()) * TILE; }
    void dibujar(SDL_Renderer* p, const Camara& cam, float tiempo) const;

private:
    std::vector<std::string> filas_;
    std::vector<SDL_FRect> gemas_;
    std::vector<SDL_FRect> espectros_;
    SDL_FRect inicio_{};
};

// ===== Mundo.cpp =====
#include "Mundo.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>

Mundo::Mundo(const std::vector<std::string>& filas) : filas_(filas)
{
    bool hay_lima = false;
    for (std::size_t f = 0; f < filas_.size(); f++) {
        if (filas_[f].size() != filas_[0].size()) {
            throw std::invalid_argument("la fila " + std::to_string(f) + " del mapa tiene otro largo");
        }
        for (std::size_t c = 0; c < filas_[f].size(); c++) {
            float x = static_cast<float>(c) * TILE, y = static_cast<float>(f) * TILE;
            switch (filas_[f][c]) {
            case 'g':
                gemas_.push_back({x + 12, y + 12, 16, 16});
                break;
            case 'K':
                inicio_ = {x + 6, y + 6, 28, 28};
                hay_lima = true;
                break;
            case 'E':
                espectros_.push_back({x + 4, y + 4, 32, 32});
                break;
            default:
                continue;
            }
            filas_[f][c] = '.';
        }
    }
    if (!hay_lima || gemas_.empty()) {
        throw std::invalid_argument("el mapa necesita a Lima (K) y al menos una gema (g)");
    }
}

void Mundo::resolver(SDL_FRect& caja, bool en_x) const
{
    for (std::size_t f = 0; f < filas_.size(); f++) {
        for (std::size_t c = 0; c < filas_[f].size(); c++) {
            SDL_FRect pared{static_cast<float>(c) * TILE, static_cast<float>(f) * TILE, TILE, TILE};
            if (filas_[f][c] != '#' || !se_tocan(caja, pared)) {
                continue;
            }
            if (en_x) {
                caja.x = (caja.x + caja.w / 2 < pared.x + TILE / 2) ? pared.x - caja.w : pared.x + TILE;
            } else {
                caja.y = (caja.y + caja.h / 2 < pared.y + TILE / 2) ? pared.y - caja.h : pared.y + TILE;
            }
        }
    }
}

int Mundo::juntar(const SDL_FRect& caja)
{
    return static_cast<int>(std::erase_if(gemas_, [&caja](const SDL_FRect& g) { return se_tocan(caja, g); }));
}

void Mundo::dibujar(SDL_Renderer* p, const Camara& cam, float tiempo) const
{
    SDL_SetRenderDrawColor(p, 70, 60, 90, 255);
    for (std::size_t f = 0; f < filas_.size(); f++) {
        for (std::size_t c = 0; c < filas_[f].size(); c++) {
            if (filas_[f][c] == '#') {
                SDL_FRect r = cam.a_pantalla({static_cast<float>(c) * TILE, static_cast<float>(f) * TILE, TILE, TILE});
                SDL_RenderFillRect(p, &r);
            }
        }
    }
    Uint8 brillo = static_cast<Uint8>(190 + 60 * std::sin(tiempo * 6));      // las gemas titilan
    SDL_SetRenderDrawColor(p, 80, brillo, 240, 255);
    for (const auto& g : gemas_) {
        SDL_FRect r = cam.a_pantalla(g);
        SDL_RenderFillRect(p, &r);
    }
}

// ===== Actores.h =====
#pragma once

#include "Base.h"
#include "Mundo.h"

class Lima {
public:
    explicit Lima(SDL_FRect inicio) : caja_(inicio) {}
    void actualizar(const Input& in, const Mundo& mundo, float dt);
    void recibir_golpe();
    bool viva() const { return vidas_ > 0; }
    int vidas() const { return vidas_; }
    bool parpadea() const { return invulnerable_ > 0; }
    bool mira_izquierda() const { return izquierda_; }
    const SDL_FRect& caja() const { return caja_; }

private:
    SDL_FRect caja_;
    int vidas_ = 3;
    float invulnerable_ = 0;       // segundos sin recibir dano despues de un golpe
    bool izquierda_ = false;
};

// El espectro atraviesa paredes: vaga en circulos y, si Lima se acerca, la persigue.
class Espectro {
public:
    Espectro(SDL_FRect inicio, float fase) : caja_(inicio), centro_x_(inicio.x), centro_y_(inicio.y), fase_(fase) {}
    void actualizar(const SDL_FRect& lima, float dt);
    bool persigue() const { return persigue_; }
    const SDL_FRect& caja() const { return caja_; }

private:
    SDL_FRect caja_;
    float centro_x_;
    float centro_y_;
    float fase_;
    bool persigue_ = false;
};

// ===== Actores.cpp =====
#include "Actores.h"

#include <algorithm>
#include <cmath>

void Lima::actualizar(const Input& in, const Mundo& mundo, float dt)
{
    invulnerable_ = std::max(0.0f, invulnerable_ - dt);
    float dx = in.abajo(SDL_SCANCODE_D) - in.abajo(SDL_SCANCODE_A);
    float dy = in.abajo(SDL_SCANCODE_S) - in.abajo(SDL_SCANCODE_W);
    float largo = std::hypot(dx, dy);
    if (largo == 0) {
        return;
    }
    if (dx != 0) {
        izquierda_ = dx < 0;
    }
    caja_.x += dx / largo * 210 * dt;
    mundo.resolver(caja_, true);
    caja_.y += dy / largo * 210 * dt;
    mundo.resolver(caja_, false);
}

void Lima::recibir_golpe()
{
    if (invulnerable_ > 0) {
        return;
    }
    vidas_--;
    invulnerable_ = 1.5f;
}

void Espectro::actualizar(const SDL_FRect& lima, float dt)
{
    fase_ += dt;
    float dx = lima.x - caja_.x, dy = lima.y - caja_.y;
    float distancia = std::hypot(dx, dy);
    persigue_ = distancia < 220;
    if (persigue_) {
        caja_.x += dx / distancia * 120 * dt;             // mas lento que Lima: se lo puede esquivar
        caja_.y += dy / distancia * 120 * dt;
        centro_x_ = caja_.x;
        centro_y_ = caja_.y;
    } else {
        caja_.x = centro_x_ + 50 * std::cos(fase_);       // vaga en circulos
        caja_.y = centro_y_ + 50 * std::sin(fase_);
    }
}

// ===== main.cpp =====
/*
 * Jefe de la Linterna Magica: juntar todas las gemas del laberinto sin que los espectros te alcancen.
 * g++ -std=c++20 -Wall -Wextra -o espectro *.cpp $(pkg-config --cflags --libs sdl3)
 */
#include <SDL3/SDL.h>

#include <algorithm>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <utility>
#include <vector>

#include "Actores.h"
#include "Base.h"
#include "Mundo.h"

const std::vector<std::string> NIVEL = {
    "##############################",
    "#K...........#..........g....#",
    "#.######.###.#.#######.####..#",
    "#.#g...#...#...#.....#....#..#",
    "#.#....#.E.#####..g..#.E..#..#",
    "#.#....#.........#...#....#.g#",
    "#.####.#####.###.#.###.####..#",
    "#......g...#...#.........#...#",
    "#####.####.#.E.#.#######.#.###",
    "#g..#......#...#.#..g..#.#...#",
    "#...#.####.#####.#.....#.###.#",
    "#...#....#.......#..E..#.....#",
    "#.######.#########.....#####.#",
    "#..........g.......#......g..#",
    "##############################",
};

class Escena {
public:
    virtual ~Escena() = default;
    virtual void actualizar(const Input& in, float dt) = 0;
    virtual void dibujar(SDL_Renderer* p) const = 0;
    std::unique_ptr<Escena> siguiente;
};

class Fin : public Escena {
public:
    Fin(bool gano, int gemas, float segundos) : gano_(gano), gemas_(gemas), segundos_(segundos) {}
    void actualizar(const Input& in, float dt) override;
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, gano_ ? 120 : 230, gano_ ? 230 : 90, 120, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 50, 60, gano_ ? "LA LINTERNA SE ENCIENDE" : "LOS ESPECTROS GANAN");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugTextFormat(p, 280, 320, "Gemas: %d   Tiempo: %.1f s", gemas_, segundos_);
        SDL_RenderDebugText(p, 300, 360, "ENTER para volver al menu");
    }

private:
    bool gano_;
    int gemas_;
    float segundos_;
};

class Partida : public Escena {
public:
    Partida(SDL_Renderer* p) : mundo_(NIVEL), lima_(mundo_.inicio_lima())
    {
        const std::map<char, SDL_Color> PALETA = {{'p', {60, 40, 30, 255}}, {'c', {240, 200, 160, 255}}, {'r', {200, 60, 60, 255}}, {'a', {60, 90, 200, 255}}, {'b', {230, 235, 255, 200}}, {'o', {20, 20, 40, 255}}};
        sprites_.emplace_back(p, std::vector<std::string>{"..pppp..", "..cccc..", "..c.c.c.", "..cccc..", ".rrrrrr.", "c.rrrr.c", "..aaaa..", "..a..a..", ".aa..aa."}, PALETA);
        sprites_.emplace_back(p, std::vector<std::string>{"..bbbb..", ".bbbbbb.", "bboobbob", "bboobbob", "bbbbbbbb", "bbbbbbbb", "bbbbbbbb", "b.bb.bb.", "...b...b"}, PALETA);
        float fase = 0;
        for (const auto& e : mundo_.espectros()) {
            espectros_.emplace_back(e, fase);
            fase += 1.7f;
        }
    }

    void actualizar(const Input& in, float dt) override
    {
        tiempo_ += dt;
        lima_.actualizar(in, mundo_, dt);
        gemas_ += mundo_.juntar(lima_.caja());
        for (auto& e : espectros_) {
            e.actualizar(lima_.caja(), dt);
            if (se_tocan(e.caja(), lima_.caja())) {
                lima_.recibir_golpe();
            }
        }
        cam_.x = std::clamp(lima_.caja().x - ANCHO / 2, 0.0f, mundo_.ancho() - ANCHO);
        cam_.y = std::clamp(lima_.caja().y - ALTO / 2, 0.0f, mundo_.alto() - ALTO);
        if (mundo_.gemas() == 0 || !lima_.viva()) {
            siguiente = std::make_unique<Fin>(lima_.viva(), gemas_, tiempo_);
        }
    }

    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 25, 22, 35, 255);
        SDL_RenderClear(p);
        mundo_.dibujar(p, cam_, tiempo_);
        bool visible = !lima_.parpadea() || static_cast<int>(tiempo_ * 10) % 2 == 0;
        if (visible) {
            sprites_[0].dibujar(p, cam_.a_pantalla(lima_.caja()), lima_.mira_izquierda());
        }
        for (const auto& e : espectros_) {
            sprites_[1].dibujar(p, cam_.a_pantalla(e.caja()));
        }
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(p, 10, 10, "Vidas: %d   Gemas: %d (faltan %zu)   %.0f s", lima_.vidas(), gemas_, mundo_.gemas(), tiempo_);
    }

private:
    Mundo mundo_;
    Lima lima_;
    std::vector<Espectro> espectros_;
    std::vector<Textura> sprites_;
    Camara cam_;
    int gemas_ = 0;
    float tiempo_ = 0;
};

class Menu : public Escena {
public:
    explicit Menu(SDL_Renderer* p) : p_(p) {}
    void actualizar(const Input& in, float dt) override
    {
        t_ += dt;
        if (in.recien(SDL_SCANCODE_RETURN)) {
            siguiente = std::make_unique<Partida>(p_);
        }
    }
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 45, 50, "EL ESPECTRO DE LA LINTERNA");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugText(p, 230, 300, "Junta todas las gemas. WASD para moverte.");
        if (static_cast<int>(t_ * 2) % 2 == 0) {
            SDL_RenderDebugText(p, 330, 360, "ENTER para empezar");
        }
    }

private:
    SDL_Renderer* p_;
    float t_ = 0;
};

SDL_Renderer* g_pincel = nullptr;        // para que Fin pueda volver a crear el menu

void Fin::actualizar(const Input& in, float)
{
    if (in.recien(SDL_SCANCODE_RETURN)) {
        siguiente = std::make_unique<Menu>(g_pincel);
    }
}

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* ventana = SDL_CreateWindow("El Espectro de la Linterna", static_cast<int>(ANCHO), static_cast<int>(ALTO), 0);
    g_pincel = ventana ? SDL_CreateRenderer(ventana, nullptr) : nullptr;
    if (!g_pincel) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(g_pincel, 1);
    try {
        Input input;
        std::unique_ptr<Escena> escena = std::make_unique<Menu>(g_pincel);
        Uint64 antes = SDL_GetTicks();
        bool corriendo = true;
        while (corriendo) {
            Uint64 ahora = SDL_GetTicks();
            float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
            antes = ahora;
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT) {
                    corriendo = false;
                }
            }
            input.actualizar();
            if (input.recien(SDL_SCANCODE_ESCAPE)) {
                corriendo = false;
            }
            escena->actualizar(input, dt);
            if (escena->siguiente) {
                escena = std::move(escena->siguiente);
            }
            escena->dibujar(g_pincel);
            SDL_RenderPresent(g_pincel);
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
    SDL_DestroyRenderer(g_pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(espectro CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(SDL3 REQUIRED CONFIG)
add_executable(espectro main.cpp Base.cpp Mundo.cpp Actores.cpp)
target_link_libraries(espectro PRIVATE SDL3::SDL3)
target_compile_options(espectro PRIVATE -Wall -Wextra)
```

### Misión S01-N04-M2 · La tabla de récords

```meta
entrega: archivo
entorno: local
monedas: 8
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

Agregale al juego una **tabla de récords**: los 5 mejores tiempos de las partidas ganadas, guardados en `records.txt` (un tiempo por línea). Escribí un módulo `Records.h` / `Records.cpp` con una clase que carga el archivo al construirse (si no existe, empieza vacía), `registrar(segundos)` (devuelve si entró en la tabla, la mantiene ordenada con `std::ranges::upper_bound` y la guarda) y `tiempos()`. El menú muestra la tabla y la pantalla final avisa si hubo récord.

#### Criterio de aprobación

- La tabla se guarda y se carga del archivo.
- Nunca guarda más de 5 tiempos y siempre están ordenados.
- Se agrega `Records.cpp` al `CMakeLists.txt`.

#### Solución de referencia

```cpp
// ===== Base.h =====
#pragma once
// Piezas comunes del juego: teclado, texturas con RAII y colisiones.

#include <SDL3/SDL.h>

#include <array>
#include <map>
#include <string>
#include <vector>

constexpr float ANCHO = 800;
constexpr float ALTO = 600;
constexpr float TILE = 40;

class Input {
public:
    void actualizar();
    bool abajo(SDL_Scancode k) const { return actual_[k]; }
    bool recien(SDL_Scancode k) const { return actual_[k] && !anterior_[k]; }

private:
    std::array<bool, SDL_SCANCODE_COUNT> actual_{};
    std::array<bool, SDL_SCANCODE_COUNT> anterior_{};
};

// Una textura hecha con "pixel art" de texto. Duenia unica: se mueve, no se copia.
class Textura {
public:
    Textura(SDL_Renderer* p, const std::vector<std::string>& dibujo, const std::map<char, SDL_Color>& paleta);
    ~Textura();
    Textura(Textura&& otra) noexcept;
    Textura& operator=(Textura&&) = delete;
    Textura(const Textura&) = delete;
    Textura& operator=(const Textura&) = delete;
    void dibujar(SDL_Renderer* p, const SDL_FRect& destino, bool espejo = false) const;

private:
    SDL_Texture* tex_ = nullptr;
};

bool se_tocan(const SDL_FRect& a, const SDL_FRect& b);

struct Camara {
    float x = 0;
    float y = 0;
    SDL_FRect a_pantalla(const SDL_FRect& r) const { return {r.x - x, r.y - y, r.w, r.h}; }
};

// ===== Base.cpp =====
#include "Base.h"

#include <stdexcept>
#include <utility>

void Input::actualizar()
{
    anterior_ = actual_;
    int n = 0;
    const bool* estado = SDL_GetKeyboardState(&n);
    for (int i = 0; i < n && i < SDL_SCANCODE_COUNT; i++) {
        actual_[i] = estado[i];
    }
}

Textura::Textura(SDL_Renderer* p, const std::vector<std::string>& dibujo, const std::map<char, SDL_Color>& paleta)
{
    int alto = static_cast<int>(dibujo.size());
    int ancho = static_cast<int>(dibujo.at(0).size());
    SDL_Surface* s = SDL_CreateSurface(ancho, alto, SDL_PIXELFORMAT_RGBA32);
    if (!s) {
        throw std::runtime_error(SDL_GetError());
    }
    for (int y = 0; y < alto; y++) {
        for (int x = 0; x < ancho; x++) {
            auto it = paleta.find(dibujo[y].at(x));
            SDL_Color c = it != paleta.end() ? it->second : SDL_Color{0, 0, 0, 0};
            SDL_WriteSurfacePixel(s, x, y, c.r, c.g, c.b, c.a);
        }
    }
    tex_ = SDL_CreateTextureFromSurface(p, s);
    SDL_DestroySurface(s);
    if (!tex_) {
        throw std::runtime_error(SDL_GetError());
    }
    SDL_SetTextureScaleMode(tex_, SDL_SCALEMODE_NEAREST);
}

Textura::~Textura()
{
    if (tex_) {
        SDL_DestroyTexture(tex_);
    }
}

Textura::Textura(Textura&& otra) noexcept : tex_(std::exchange(otra.tex_, nullptr)) {}

void Textura::dibujar(SDL_Renderer* p, const SDL_FRect& destino, bool espejo) const
{
    SDL_RenderTextureRotated(p, tex_, nullptr, &destino, 0, nullptr, espejo ? SDL_FLIP_HORIZONTAL : SDL_FLIP_NONE);
}

bool se_tocan(const SDL_FRect& a, const SDL_FRect& b)
{
    return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}

// ===== Mundo.h =====
#pragma once

#include <string>
#include <vector>

#include "Base.h"

// El mapa: '#' pared, 'g' gema, 'K' inicio de Lima, 'E' un espectro. Lanza si el mapa es invalido.
class Mundo {
public:
    explicit Mundo(const std::vector<std::string>& filas);

    void resolver(SDL_FRect& caja, bool en_x) const;       // saca la caja de las paredes, en un eje
    int juntar(const SDL_FRect& caja);                      // gemas que toca: las quita y dice cuantas
    std::size_t gemas() const { return gemas_.size(); }
    SDL_FRect inicio_lima() const { return inicio_; }
    const std::vector<SDL_FRect>& espectros() const { return espectros_; }
    float ancho() const { return static_cast<float>(filas_[0].size()) * TILE; }
    float alto() const { return static_cast<float>(filas_.size()) * TILE; }
    void dibujar(SDL_Renderer* p, const Camara& cam, float tiempo) const;

private:
    std::vector<std::string> filas_;
    std::vector<SDL_FRect> gemas_;
    std::vector<SDL_FRect> espectros_;
    SDL_FRect inicio_{};
};

// ===== Mundo.cpp =====
#include "Mundo.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>

Mundo::Mundo(const std::vector<std::string>& filas) : filas_(filas)
{
    bool hay_lima = false;
    for (std::size_t f = 0; f < filas_.size(); f++) {
        if (filas_[f].size() != filas_[0].size()) {
            throw std::invalid_argument("la fila " + std::to_string(f) + " del mapa tiene otro largo");
        }
        for (std::size_t c = 0; c < filas_[f].size(); c++) {
            float x = static_cast<float>(c) * TILE, y = static_cast<float>(f) * TILE;
            switch (filas_[f][c]) {
            case 'g':
                gemas_.push_back({x + 12, y + 12, 16, 16});
                break;
            case 'K':
                inicio_ = {x + 6, y + 6, 28, 28};
                hay_lima = true;
                break;
            case 'E':
                espectros_.push_back({x + 4, y + 4, 32, 32});
                break;
            default:
                continue;
            }
            filas_[f][c] = '.';
        }
    }
    if (!hay_lima || gemas_.empty()) {
        throw std::invalid_argument("el mapa necesita a Lima (K) y al menos una gema (g)");
    }
}

void Mundo::resolver(SDL_FRect& caja, bool en_x) const
{
    for (std::size_t f = 0; f < filas_.size(); f++) {
        for (std::size_t c = 0; c < filas_[f].size(); c++) {
            SDL_FRect pared{static_cast<float>(c) * TILE, static_cast<float>(f) * TILE, TILE, TILE};
            if (filas_[f][c] != '#' || !se_tocan(caja, pared)) {
                continue;
            }
            if (en_x) {
                caja.x = (caja.x + caja.w / 2 < pared.x + TILE / 2) ? pared.x - caja.w : pared.x + TILE;
            } else {
                caja.y = (caja.y + caja.h / 2 < pared.y + TILE / 2) ? pared.y - caja.h : pared.y + TILE;
            }
        }
    }
}

int Mundo::juntar(const SDL_FRect& caja)
{
    return static_cast<int>(std::erase_if(gemas_, [&caja](const SDL_FRect& g) { return se_tocan(caja, g); }));
}

void Mundo::dibujar(SDL_Renderer* p, const Camara& cam, float tiempo) const
{
    SDL_SetRenderDrawColor(p, 70, 60, 90, 255);
    for (std::size_t f = 0; f < filas_.size(); f++) {
        for (std::size_t c = 0; c < filas_[f].size(); c++) {
            if (filas_[f][c] == '#') {
                SDL_FRect r = cam.a_pantalla({static_cast<float>(c) * TILE, static_cast<float>(f) * TILE, TILE, TILE});
                SDL_RenderFillRect(p, &r);
            }
        }
    }
    Uint8 brillo = static_cast<Uint8>(190 + 60 * std::sin(tiempo * 6));      // las gemas titilan
    SDL_SetRenderDrawColor(p, 80, brillo, 240, 255);
    for (const auto& g : gemas_) {
        SDL_FRect r = cam.a_pantalla(g);
        SDL_RenderFillRect(p, &r);
    }
}

// ===== Actores.h =====
#pragma once

#include "Base.h"
#include "Mundo.h"

class Lima {
public:
    explicit Lima(SDL_FRect inicio) : caja_(inicio) {}
    void actualizar(const Input& in, const Mundo& mundo, float dt);
    void recibir_golpe();
    bool viva() const { return vidas_ > 0; }
    int vidas() const { return vidas_; }
    bool parpadea() const { return invulnerable_ > 0; }
    bool mira_izquierda() const { return izquierda_; }
    const SDL_FRect& caja() const { return caja_; }

private:
    SDL_FRect caja_;
    int vidas_ = 3;
    float invulnerable_ = 0;       // segundos sin recibir dano despues de un golpe
    bool izquierda_ = false;
};

// El espectro atraviesa paredes: vaga en circulos y, si Lima se acerca, la persigue.
class Espectro {
public:
    Espectro(SDL_FRect inicio, float fase) : caja_(inicio), centro_x_(inicio.x), centro_y_(inicio.y), fase_(fase) {}
    void actualizar(const SDL_FRect& lima, float dt);
    bool persigue() const { return persigue_; }
    const SDL_FRect& caja() const { return caja_; }

private:
    SDL_FRect caja_;
    float centro_x_;
    float centro_y_;
    float fase_;
    bool persigue_ = false;
};

// ===== Actores.cpp =====
#include "Actores.h"

#include <algorithm>
#include <cmath>

void Lima::actualizar(const Input& in, const Mundo& mundo, float dt)
{
    invulnerable_ = std::max(0.0f, invulnerable_ - dt);
    float dx = in.abajo(SDL_SCANCODE_D) - in.abajo(SDL_SCANCODE_A);
    float dy = in.abajo(SDL_SCANCODE_S) - in.abajo(SDL_SCANCODE_W);
    float largo = std::hypot(dx, dy);
    if (largo == 0) {
        return;
    }
    if (dx != 0) {
        izquierda_ = dx < 0;
    }
    caja_.x += dx / largo * 210 * dt;
    mundo.resolver(caja_, true);
    caja_.y += dy / largo * 210 * dt;
    mundo.resolver(caja_, false);
}

void Lima::recibir_golpe()
{
    if (invulnerable_ > 0) {
        return;
    }
    vidas_--;
    invulnerable_ = 1.5f;
}

void Espectro::actualizar(const SDL_FRect& lima, float dt)
{
    fase_ += dt;
    float dx = lima.x - caja_.x, dy = lima.y - caja_.y;
    float distancia = std::hypot(dx, dy);
    persigue_ = distancia < 220;
    if (persigue_) {
        caja_.x += dx / distancia * 120 * dt;             // mas lento que Lima: se lo puede esquivar
        caja_.y += dy / distancia * 120 * dt;
        centro_x_ = caja_.x;
        centro_y_ = caja_.y;
    } else {
        caja_.x = centro_x_ + 50 * std::cos(fase_);       // vaga en circulos
        caja_.y = centro_y_ + 50 * std::sin(fase_);
    }
}

// ===== main.cpp =====
/*
 * Jefe de la Linterna Magica: juntar todas las gemas del laberinto sin que los espectros te alcancen.
 * g++ -std=c++20 -Wall -Wextra -o espectro *.cpp $(pkg-config --cflags --libs sdl3)
 */
#include <SDL3/SDL.h>

#include <algorithm>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <utility>
#include <vector>

#include "Actores.h"
#include "Base.h"
#include "Mundo.h"
#include "Records.h"

const std::vector<std::string> NIVEL = {
    "##############################",
    "#K...........#..........g....#",
    "#.######.###.#.#######.####..#",
    "#.#g...#...#...#.....#....#..#",
    "#.#....#.E.#####..g..#.E..#..#",
    "#.#....#.........#...#....#.g#",
    "#.####.#####.###.#.###.####..#",
    "#......g...#...#.........#...#",
    "#####.####.#.E.#.#######.#.###",
    "#g..#......#...#.#..g..#.#...#",
    "#...#.####.#####.#.....#.###.#",
    "#...#....#.......#..E..#.....#",
    "#.######.#########.....#####.#",
    "#..........g.......#......g..#",
    "##############################",
};

class Escena {
public:
    virtual ~Escena() = default;
    virtual void actualizar(const Input& in, float dt) = 0;
    virtual void dibujar(SDL_Renderer* p) const = 0;
    std::unique_ptr<Escena> siguiente;
};

Records g_records("records.txt");         // una sola tabla para todo el programa

class Fin : public Escena {
public:
    Fin(bool gano, int gemas, float segundos)
        : gano_(gano), gemas_(gemas), segundos_(segundos), record_(gano && g_records.registrar(segundos)) {}
    void actualizar(const Input& in, float dt) override;
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, gano_ ? 120 : 230, gano_ ? 230 : 90, 120, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 50, 60, gano_ ? "LA LINTERNA SE ENCIENDE" : "LOS ESPECTROS GANAN");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugTextFormat(p, 280, 320, "Gemas: %d   Tiempo: %.1f s", gemas_, segundos_);
        if (record_) {
            SDL_RenderDebugText(p, 320, 340, "¡Nuevo récord!");
        }
        SDL_RenderDebugText(p, 300, 380, "ENTER para volver al menu");
    }

private:
    bool gano_;
    int gemas_;
    float segundos_;
    bool record_;
};

class Partida : public Escena {
public:
    Partida(SDL_Renderer* p) : mundo_(NIVEL), lima_(mundo_.inicio_lima())
    {
        const std::map<char, SDL_Color> PALETA = {{'p', {60, 40, 30, 255}}, {'c', {240, 200, 160, 255}}, {'r', {200, 60, 60, 255}}, {'a', {60, 90, 200, 255}}, {'b', {230, 235, 255, 200}}, {'o', {20, 20, 40, 255}}};
        sprites_.emplace_back(p, std::vector<std::string>{"..pppp..", "..cccc..", "..c.c.c.", "..cccc..", ".rrrrrr.", "c.rrrr.c", "..aaaa..", "..a..a..", ".aa..aa."}, PALETA);
        sprites_.emplace_back(p, std::vector<std::string>{"..bbbb..", ".bbbbbb.", "bboobbob", "bboobbob", "bbbbbbbb", "bbbbbbbb", "bbbbbbbb", "b.bb.bb.", "...b...b"}, PALETA);
        float fase = 0;
        for (const auto& e : mundo_.espectros()) {
            espectros_.emplace_back(e, fase);
            fase += 1.7f;
        }
    }

    void actualizar(const Input& in, float dt) override
    {
        tiempo_ += dt;
        lima_.actualizar(in, mundo_, dt);
        gemas_ += mundo_.juntar(lima_.caja());
        for (auto& e : espectros_) {
            e.actualizar(lima_.caja(), dt);
            if (se_tocan(e.caja(), lima_.caja())) {
                lima_.recibir_golpe();
            }
        }
        cam_.x = std::clamp(lima_.caja().x - ANCHO / 2, 0.0f, mundo_.ancho() - ANCHO);
        cam_.y = std::clamp(lima_.caja().y - ALTO / 2, 0.0f, mundo_.alto() - ALTO);
        if (mundo_.gemas() == 0 || !lima_.viva()) {
            siguiente = std::make_unique<Fin>(lima_.viva(), gemas_, tiempo_);
        }
    }

    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 25, 22, 35, 255);
        SDL_RenderClear(p);
        mundo_.dibujar(p, cam_, tiempo_);
        bool visible = !lima_.parpadea() || static_cast<int>(tiempo_ * 10) % 2 == 0;
        if (visible) {
            sprites_[0].dibujar(p, cam_.a_pantalla(lima_.caja()), lima_.mira_izquierda());
        }
        for (const auto& e : espectros_) {
            sprites_[1].dibujar(p, cam_.a_pantalla(e.caja()));
        }
        SDL_SetRenderDrawColor(p, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(p, 10, 10, "Vidas: %d   Gemas: %d (faltan %zu)   %.0f s", lima_.vidas(), gemas_, mundo_.gemas(), tiempo_);
    }

private:
    Mundo mundo_;
    Lima lima_;
    std::vector<Espectro> espectros_;
    std::vector<Textura> sprites_;
    Camara cam_;
    int gemas_ = 0;
    float tiempo_ = 0;
};

class Menu : public Escena {
public:
    explicit Menu(SDL_Renderer* p) : p_(p) {}
    void actualizar(const Input& in, float dt) override
    {
        t_ += dt;
        if (in.recien(SDL_SCANCODE_RETURN)) {
            siguiente = std::make_unique<Partida>(p_);
        }
    }
    void dibujar(SDL_Renderer* p) const override
    {
        SDL_SetRenderDrawColor(p, 10, 10, 20, 255);
        SDL_RenderClear(p);
        SDL_SetRenderDrawColor(p, 240, 190, 90, 255);
        SDL_SetRenderScale(p, 3, 3);
        SDL_RenderDebugText(p, 45, 50, "EL ESPECTRO DE LA LINTERNA");
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugText(p, 230, 300, "Junta todas las gemas. WASD para moverte.");
        if (static_cast<int>(t_ * 2) % 2 == 0) {
            SDL_RenderDebugText(p, 330, 360, "ENTER para empezar");
        }
        SDL_RenderDebugText(p, 330, 420, "MEJORES TIEMPOS");
        float y = 440;
        for (std::size_t i = 0; i < g_records.tiempos().size(); i++) {
            SDL_RenderDebugTextFormat(p, 340, y, "%zu. %.1f s", i + 1, g_records.tiempos()[i]);
            y += 14;
        }
    }

private:
    SDL_Renderer* p_;
    float t_ = 0;
};

SDL_Renderer* g_pincel = nullptr;        // para que Fin pueda volver a crear el menu

void Fin::actualizar(const Input& in, float)
{
    if (in.recien(SDL_SCANCODE_RETURN)) {
        siguiente = std::make_unique<Menu>(g_pincel);
    }
}

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* ventana = SDL_CreateWindow("El Espectro de la Linterna", static_cast<int>(ANCHO), static_cast<int>(ALTO), 0);
    g_pincel = ventana ? SDL_CreateRenderer(ventana, nullptr) : nullptr;
    if (!g_pincel) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(g_pincel, 1);
    try {
        Input input;
        std::unique_ptr<Escena> escena = std::make_unique<Menu>(g_pincel);
        Uint64 antes = SDL_GetTicks();
        bool corriendo = true;
        while (corriendo) {
            Uint64 ahora = SDL_GetTicks();
            float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
            antes = ahora;
            SDL_Event e;
            while (SDL_PollEvent(&e)) {
                if (e.type == SDL_EVENT_QUIT) {
                    corriendo = false;
                }
            }
            input.actualizar();
            if (input.recien(SDL_SCANCODE_ESCAPE)) {
                corriendo = false;
            }
            escena->actualizar(input, dt);
            if (escena->siguiente) {
                escena = std::move(escena->siguiente);
            }
            escena->dibujar(g_pincel);
            SDL_RenderPresent(g_pincel);
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
    SDL_DestroyRenderer(g_pincel);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}

// ===== CMakeLists.txt =====
cmake_minimum_required(VERSION 3.16)
project(espectro CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(SDL3 REQUIRED CONFIG)
add_executable(espectro main.cpp Base.cpp Mundo.cpp Actores.cpp Records.cpp)
target_link_libraries(espectro PRIVATE SDL3::SDL3)
target_compile_options(espectro PRIVATE -Wall -Wextra)

// ===== Records.h =====
#pragma once

#include <string>
#include <vector>

// Los 5 mejores tiempos (en segundos), guardados en un archivo de texto.
class Records {
public:
    explicit Records(std::string ruta);
    bool registrar(float segundos);            // true si entro en la tabla
    const std::vector<float>& tiempos() const { return tiempos_; }

private:
    void guardar() const;
    std::string ruta_;
    std::vector<float> tiempos_;
};

// ===== Records.cpp =====
#include "Records.h"

#include <algorithm>
#include <fstream>
#include <utility>

Records::Records(std::string ruta) : ruta_(std::move(ruta))
{
    std::ifstream in(ruta_);                 // si no existe, la tabla empieza vacia
    float t = 0;
    while (in >> t && tiempos_.size() < 5) {
        if (t > 0) {
            tiempos_.push_back(t);
        }
    }
    std::ranges::sort(tiempos_);
}

bool Records::registrar(float segundos)
{
    if (tiempos_.size() == 5 && segundos >= tiempos_.back()) {
        return false;
    }
    tiempos_.insert(std::ranges::upper_bound(tiempos_, segundos), segundos);
    if (tiempos_.size() > 5) {
        tiempos_.pop_back();
    }
    guardar();
    return true;
}

void Records::guardar() const
{
    std::ofstream out(ruta_);
    for (float t : tiempos_) {
        out << t << "\n";
    }
}
```

### Encargo S01-N04-E1 · El protector de pantalla

```meta
entrega: archivo
entorno: local
monedas: 1
xp: 40
extensiones: zip, cpp, h, txt
```

#### Consigna

El Gremio quiere un protector de pantalla: **fuegos artificiales** con partículas (cada explosión lanza 120 partículas en todas las direcciones, con gravedad, que se desvanecen con el alfa y desaparecen con `std::erase_if`), un cohete nuevo cada tanto al azar y otro donde se hace clic, y la **hora** grande en el centro. Cualquier tecla lo cierra. Usá `SDL_SetRenderDrawBlendMode(p, SDL_BLENDMODE_BLEND)` para que el alfa se note.

#### Criterio de aprobación

- Las partículas se mueven con `dt` y gravedad, y se borran al morir.
- El azar sale de un único generador.
- Muestra la hora actual.

#### Solución de referencia

```cpp
// S01-N04-E1 - El protector de pantalla del Gremio: fuegos artificiales con particulas y la hora.
#include <SDL3/SDL.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <ctime>
#include <iostream>
#include <numbers>
#include <random>
#include <vector>

struct Particula {
    float x, y, vx, vy;
    float vida;                 // segundos que le quedan
    Uint8 r, g, b;
};

class Cielo {
public:
    explicit Cielo(unsigned semilla) : gen_(semilla) {}

    void explotar(float x, float y)
    {
        std::uniform_real_distribution<float> angulo(0, 2 * std::numbers::pi_v<float>), fuerza(60, 260);
        std::uniform_int_distribution<int> color(0, 2);
        const Uint8 PALETA[3][3] = {{250, 200, 60}, {90, 200, 250}, {240, 90, 160}};
        int c = color(gen_);
        for (int i = 0; i < 120; i++) {
            float a = angulo(gen_), f = fuerza(gen_);
            particulas_.push_back({x, y, std::cos(a) * f, std::sin(a) * f, 1.6f, PALETA[c][0], PALETA[c][1], PALETA[c][2]});
        }
    }

    void actualizar(float dt, float ancho, float alto)
    {
        espera_ -= dt;
        if (espera_ <= 0) {                                    // cada tanto, un cohete nuevo
            std::uniform_real_distribution<float> x(100, ancho - 100), y(80, alto / 2);
            explotar(x(gen_), y(gen_));
            espera_ = std::uniform_real_distribution<float>(0.4f, 1.2f)(gen_);
        }
        for (auto& p : particulas_) {
            p.vy += 120 * dt;                                  // gravedad
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.vida -= dt;
        }
        std::erase_if(particulas_, [](const Particula& p) { return p.vida <= 0; });
    }

    void dibujar(SDL_Renderer* p) const
    {
        for (const auto& q : particulas_) {
            Uint8 alfa = static_cast<Uint8>(std::clamp(q.vida / 1.6f, 0.0f, 1.0f) * 255);
            SDL_SetRenderDrawColor(p, q.r, q.g, q.b, alfa);
            SDL_FRect r{q.x, q.y, 3, 3};
            SDL_RenderFillRect(p, &r);
        }
    }

    std::size_t cantidad() const { return particulas_.size(); }

private:
    std::mt19937 gen_;
    std::vector<Particula> particulas_;
    float espera_ = 0;
};

int main()
{
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        std::cerr << SDL_GetError() << "\n";
        return 1;
    }
    SDL_Window* v = SDL_CreateWindow("Protector del Gremio", 900, 600, 0);
    SDL_Renderer* p = v ? SDL_CreateRenderer(v, nullptr) : nullptr;
    if (!p) {
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderVSync(p, 1);
    SDL_SetRenderDrawBlendMode(p, SDL_BLENDMODE_BLEND);          // para que el alfa se note
    Cielo cielo(static_cast<unsigned>(std::chrono::system_clock::now().time_since_epoch().count()));
    Uint64 antes = SDL_GetTicks();
    bool corriendo = true;
    while (corriendo) {
        Uint64 ahora = SDL_GetTicks();
        float dt = std::min((ahora - antes) / 1000.0f, 0.1f);
        antes = ahora;
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT || e.type == SDL_EVENT_KEY_DOWN) {
                corriendo = false;                               // un protector se cierra con cualquier tecla
            } else if (e.type == SDL_EVENT_MOUSE_BUTTON_DOWN) {
                cielo.explotar(e.button.x, e.button.y);
            }
        }
        cielo.actualizar(dt, 900, 600);
        SDL_SetRenderDrawColor(p, 5, 5, 20, 255);
        SDL_RenderClear(p);
        cielo.dibujar(p);
        std::time_t t = std::time(nullptr);
        std::tm h = *std::localtime(&t);
        SDL_SetRenderDrawColor(p, 200, 200, 220, 255);
        SDL_SetRenderScale(p, 4, 4);
        SDL_RenderDebugTextFormat(p, 80, 120, "%02d:%02d:%02d", h.tm_hour, h.tm_min, h.tm_sec);
        SDL_SetRenderScale(p, 1, 1);
        SDL_RenderDebugTextFormat(p, 10, 580, "partículas: %zu   (clic: un cohete; tecla: salir)", cielo.cantidad());
        SDL_RenderPresent(p);
    }
    SDL_DestroyRenderer(p);
    SDL_DestroyWindow(v);
    SDL_Quit();
    return 0;
}
```

### Prueba del sello

#### ¿Qué tienen en común este juego y el Laberinto del Minotauro?

El mapa como texto, la lógica separada del dibujo, la validación con excepciones y el bucle entrada → actualizar → dibujar.

#### ¿Para qué sirve la invulnerabilidad después de un golpe?

Para que un solo toque, que dura varios cuadros, no descuente varias vidas.

#### ¿Por qué los espectros persiguen más lento que Lima?

Para que se los pueda esquivar: el balance hace que el juego sea justo.

#### ¿Dónde viven las texturas y por qué importa?

Dentro de la escena de la partida, que se destruye antes que el renderer; así se liberan en el orden correcto.

### Soluciones (docente)

Jefe de la Senda, basado en `07-SDL3-Cpp/09-Game`. M1 parte del juego completo (la solución de referencia es el juego base; las dos ampliaciones se corrigen jugando). M2 agrega el módulo `Records`. Todo compilado y enlazado contra SDL 3.2 y probado con el driver de video "dummy".
