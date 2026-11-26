# RAMA R01 · El Banco de Pruebas de Arcadia: lo básico de un juego

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Rectángulos y coordenadas

```meta
tipo: tema
criatura: glitch
padre: R00-N01
precio: 10
temas: juegos.bucle
usa: prog.bucles
```

### Crónica

Detrás de la boletería hay un galpón largo con mesas llenas de pantallas chiquitas, cables y piezas sueltas: el
**Banco de Pruebas**. Acá {mentor} probaba cada pieza antes de ponerla en una máquina. —Todo juego está hecho
de cajas —dice, y dibuja un cuadrado con el dedo en el vidrio empañado—. La paleta del Pong es una caja. Un
ladrillo es una caja. Hasta el fantasma más feo, si lo mirás bien, vive adentro de una caja.

En una de las pantallas, un cuadrado blanco tiembla en una esquina, como si no supiera dónde quedarse. Gheco lo
señala con la cola: es un **glitch**.

### Objetivos

Dibujar rectángulos llenos y bordes, ubicarlos con **coordenadas** (dónde está el 0,0 y hacia dónde crece la
`y`), entender que lo que se dibuja después tapa lo anterior y repetir rectángulos con un `for`.

### Antes de empezar

La Clase 0: la ventana, los colores RGB y el bucle del juego. Del curso de C: structs (`SDL_FRect` es uno) y el
bucle `for`.

### Explicación

#### Las coordenadas de la pantalla
Cada píxel de la ventana tiene una dirección: su **x** (cuántos píxeles desde la izquierda) y su **y** (cuántos
desde arriba). El punto `0, 0` está **arriba a la izquierda**. La `x` crece hacia la derecha y la `y` crece
hacia **abajo** (al revés que en los gráficos de matemática).

En una ventana de 640 × 480, la esquina de abajo a la derecha es el punto `639, 479` (se empieza a contar
desde 0), y el centro está en `320, 240`.

#### Un rectángulo: `SDL_FRect`
`SDL_FRect` es un **struct** con cuatro números: dónde está la esquina de arriba a la izquierda (`x`, `y`) y
cuánto mide (`w` de ancho, *width*, y `h` de alto, *height*). La `F` es de *float*: los números pueden tener
decimales, y eso va a servir para mover las cosas despacito.
```c
SDL_FRect caja = { 100, 50, 80, 40 };   /* x 100, y 50, 80 de ancho y 40 de alto */
```
También se puede leer o cambiar cada parte: `caja.x = 200;`.

#### Dibujarlo: lleno o solo el borde
```c
SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);   /* primero, el color */
SDL_RenderFillRect(lapiz, &caja);                    /* lleno */
SDL_RenderRect(lapiz, &caja);                        /* solo el borde, de 1 píxel */
```
Las dos reciben la **dirección** del rectángulo (`&caja`), como `scanf` recibía `&numero`.

#### Para centrar algo
Para que una caja quede en el medio, su esquina tiene que ir medio ancho antes del centro:
`x = 640 / 2 - ancho / 2`. Con una caja de 80: `320 - 40 = 280`.

#### Lo último tapa
Dibujar es como pintar en una pared: lo que se pinta después queda **arriba**. Por eso primero se limpia
(el fondo), después lo de atrás y al final lo de adelante.

#### Muchas cajas con un `for`
Una fila de ladrillos es la misma caja repetida, corrida un poco cada vez:
```c
for (int i = 0; i < 5; i++) {
    SDL_FRect ladrillo = { 10 + i * 60, 40, 50, 20 };   /* cada uno, 60 píxeles más a la derecha */
    SDL_RenderFillRect(lapiz, &ladrillo);
}
```

### Código de ejemplo

```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Cajas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        /* Un piso verde de lado a lado */
        SDL_SetRenderDrawColor(lapiz, 60, 180, 90, 255);
        SDL_FRect piso = { 0, 420, 640, 60 };
        SDL_RenderFillRect(lapiz, &piso);

        /* Una fila de ladrillos naranjas */
        SDL_SetRenderDrawColor(lapiz, 255, 96, 64, 255);
        for (int i = 0; i < 8; i++) {
            SDL_FRect ladrillo = { 10 + i * 78, 40, 70, 20 };
            SDL_RenderFillRect(lapiz, &ladrillo);
        }

        /* Una caja blanca en el centro, con un marco cian */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect caja = { 280, 200, 80, 80 };
        SDL_RenderFillRect(lapiz, &caja);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_FRect marco = { 20, 20, 600, 440 };
        SDL_RenderRect(lapiz, &marco);
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

Casi todo lo que se ve en un juego 2D se ubica con un rectángulo: dónde se dibuja un personaje, de qué tamaño
es una plataforma, qué parte de la pantalla ocupa un botón. Y los mismos rectángulos sirven después para saber
si dos cosas se chocan.

### Errores habituales

**Glitch: la `y` al revés.** `y = 400` no está arriba: está **abajo**. La `y` crece hacia abajo.

**Glitch: dibujar antes de limpiar.** Si el `SDL_RenderClear` va después de los rectángulos, los tapa: la
ventana queda de un solo color.

**Glitch: olvidar el color.** Cada `SDL_RenderFillRect` usa el **último** color elegido. Si querías una caja
roja y otra azul, hace falta un `SDL_SetRenderDrawColor` antes de cada una.

**Slime: pasar el rectángulo sin `&`.** `SDL_RenderFillRect(lapiz, caja)` no compila: la función pide la
dirección, `&caja`.

### Micro-misión R01-N01-P1 · La caja en el medio

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: Un rectángulo | SDL_FRect caja = { x, y, ancho, alto }; · el 0,0 está arriba a la izquierda
recompensa: xp 10, oro 10
```

#### Escena
El cuadrado blanco de la pantallita sigue pegado a la esquina, temblando. —Ese es un glitch —dice
{mentor}—: algo que aparece donde no tenía que estar. Ponelo en el medio, que es su lugar.

#### Gheco sugiere
La caja se dibuja con un **rectángulo**, un `SDL_FRect`, que guarda cuatro números:
`{ x, y, ancho, alto }`. La `x` y la `y` dicen dónde está su esquina de **arriba a la izquierda**.

En la pantalla, el punto `0, 0` está arriba a la izquierda: por eso la caja quedó pegada a la esquina.
La `x` crece hacia la derecha y la `y` crece hacia **abajo**.

Para centrar algo, su esquina va **medio ancho antes** del centro. La ventana mide 640 × 480, así que
el centro es `320, 240`. Por ejemplo, una caja de 100 × 100 centrada va en `x = 320 - 50 = 270` y
`y = 240 - 50 = 190`.

El robot va a buscar dónde quedó lo blanco.

#### Desafío
Poné la caja blanca de 80 × 80 justo en el centro de la ventana.

#### Pasos
1. Buscá la línea `SDL_FRect caja = { 0, 0, 80, 80 };`.
2. La caja mide 80: la mitad es 40. Su `x` tiene que ser `320 - 40`, o sea `280`. Cambiá el primer `0` por `280`.
3. Su `y` tiene que ser `240 - 40`, o sea `200`. Cambiá el segundo `0` por `200`.
4. Tocá **Jugar** para verla, y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect caja = { 0, 0, 80, 80 };   /* x, y, ancho, alto */
        SDL_RenderFillRect(lapiz, &caja);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 280, y 200, ancho 80, alto 80
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect caja = { 280, 200, 80, 80 };   /* x, y, ancho, alto */
        SDL_RenderFillRect(lapiz, &caja);
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
La caja se queda quieta en el centro y deja de temblar. El glitch se desarma en chispas de colores.
—Así me gusta —dice {mentor}—. Cada cosa en su lugar.

#### Imagen
- El Banco de Pruebas de Arcadia: un galpón largo con mesas llenas de pantallas chiquitas, cables y piezas sueltas, luces de neón violetas.
- Kira (versión videojuegos: mono oscuro cerrado con líneas cian, visor, auricular, cinturón de herramientas, brazal con un control de juego) frente a una pantalla donde un cuadrado blanco queda en el centro.
- Un glitch (una criatura chiquita hecha de chispas de colores y píxeles sueltos) se desarma al costado de la pantalla.
- Arcadia (pelo rojizo en rodete, auriculares al cuello, mono mostaza con chaleco negro) mira por encima del hombro de Kira; Gheco sobre la mesa.

### Micro-misión R01-N01-P2 · El marco de la pantalla

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Solo el borde | SDL_RenderRect(lapiz, &rect); · dibuja el contorno de 1 píxel
recompensa: xp 10, monedas 4
```

#### Escena
—Las pantallas del Vidriero tenían un marco de luz —recuerda {mentor}—, cian, a veinte píxeles del borde.
Decía que así el ojo sabe dónde termina el juego.

#### Gheco sugiere
`SDL_RenderFillRect` pinta el rectángulo **lleno**. Su compañera, `SDL_RenderRect`, dibuja **solo el
borde**, una línea de 1 píxel alrededor:
```c
SDL_FRect cuadro = { 50, 50, 100, 60 };
SDL_RenderRect(lapiz, &cuadro);   /* un contorno de 100 × 60 */
```
Las dos usan el último color elegido con `SDL_SetRenderDrawColor`. El cian es `0, 229, 255`.

Un marco a 20 píxeles de cada borde empieza en `20, 20`. Su ancho es `640 - 20 - 20 = 600` y su alto,
`480 - 20 - 20 = 440`.

El robot va a mirar el color de la esquina del marco (`20, 20`), uno de afuera (`5, 5`) y uno de
adentro (`100, 100`), que tiene que seguir siendo el fondo.

#### Desafío
Dibujá un marco cian (0, 229, 255) de 600 × 440 que empiece en el punto 20, 20.

#### Pasos
1. Buscá el comentario `/* acá: el marco cian */`.
2. Debajo, elegí el cian: `SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);`.
3. Después, el rectángulo: `SDL_FRect marco = { 20, 20, 600, 440 };`.
4. Y el borde: `SDL_RenderRect(lapiz, &marco);`.
5. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect caja = { 280, 200, 80, 80 };
        SDL_RenderFillRect(lapiz, &caja);
        /* acá: el marco cian */
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
pixel 20 20
pixel 5 5
pixel 100 100
```

#### Salida esperada
```
── Estado ──
pixel 20 20: #00e5ff
pixel 5 5: #140c28
pixel 100 100: #140c28
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect caja = { 280, 200, 80, 80 };
        SDL_RenderFillRect(lapiz, &caja);
        /* acá: el marco cian */
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_FRect marco = { 20, 20, 600, 440 };
        SDL_RenderRect(lapiz, &marco);
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
Una línea cian recorre el borde de la pantalla y se cierra sola. {mentor} pasa el dedo por el vidrio
siguiendo el marco. —Igual que antes.

#### Imagen
- Primer plano de una pantalla del Banco de Pruebas: fondo violeta oscuro, un cuadrado blanco en el centro y un marco de luz cian cerca del borde.
- El dedo de Arcadia (guante de trabajo) recorre el marco sobre el vidrio.
- Kira y Gheco miran la pantalla, con el reflejo cian en el visor de Kira.

### Micro-misión R01-N01-P3 · Lo que va adelante

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: El orden de dibujo | lo que se dibuja después queda arriba · fondo → atrás → adelante
recompensa: xp 10, monedas 4
```

#### Escena
En otra pantalla hay dos cajas que se pisan: una roja y una azul. —La roja es la nave —dice {mentor}— y
la azul es una nube. ¿Quién vio una nube tapando una nave? La nave va adelante.

#### Gheco sugiere
Dibujar en la pantalla es como pintar una pared: lo que se pinta **después** queda **arriba** y tapa lo
de antes. Por eso el orden de las líneas importa.

En este código se dibuja primero la roja y después la azul: donde se pisan, gana la azul. Para que gane
la roja, hay que dibujarla **al final**. Cada caja necesita su color justo antes: el
`SDL_SetRenderDrawColor` viaja junto con su `SDL_RenderFillRect`.

Por ejemplo, para que el sol quede detrás de la montaña: primero el cielo, después el sol y al final la
montaña.

El robot va a mirar el color del punto `330, 250`, que está donde las dos cajas se pisan.

#### Desafío
Cambiá el orden para que la caja roja quede adelante de la azul.

#### Pasos
1. Buscá las dos líneas que dibujan la roja: el `SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);` y el `SDL_RenderFillRect(lapiz, &roja);`.
2. Cortalas (Ctrl+X) y pegalas (Ctrl+V) después del `SDL_RenderFillRect(lapiz, &azul);`.
3. Fijate que cada color quede justo antes de su caja.
4. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect roja = { 240, 160, 120, 120 };
        SDL_FRect azul = { 300, 220, 120, 120 };

        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderFillRect(lapiz, &roja);
        SDL_SetRenderDrawColor(lapiz, 40, 110, 230, 255);
        SDL_RenderFillRect(lapiz, &azul);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
pixel 330 250
```

#### Salida esperada
```
── Estado ──
pixel 330 250: #e6283c
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect roja = { 240, 160, 120, 120 };
        SDL_FRect azul = { 300, 220, 120, 120 };

        SDL_SetRenderDrawColor(lapiz, 40, 110, 230, 255);
        SDL_RenderFillRect(lapiz, &azul);
        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderFillRect(lapiz, &roja);
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
La caja roja salta adelante de la azul. {mentor} asiente. —Primero lo lejos, después lo cerca. Con eso
ya podés dibujar un cielo entero.

#### Imagen
- Una pantalla del Banco de Pruebas con dos cuadrados que se pisan: uno rojo adelante y uno azul detrás.
- Kira señala la pantalla; al costado, Arcadia sostiene una nave de juguete roja delante de una nube de algodón azul, para explicar.
- Gheco, sobre la nube de algodón.

### Micro-misión R01-N01-P4 · La fila de ladrillos

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Repetir cajas | for (int i = 0; i < 8; i++) { SDL_FRect r = { 10 + i * 78, 40, 70, 20 }; … }
recompensa: xp 10, monedas 4
```

#### Escena
{mentor} saca de un cajón la pantalla de una máquina que se llamaba **El Muro de Ladrillos**. Está
vacía. —Le faltan los ladrillos. Son ocho, uno al lado del otro. No los dibujes de a uno: ¿para qué
sabés C?

#### Gheco sugiere
Para dibujar muchas cajas iguales no hace falta escribir ocho veces lo mismo: se usa un `for`, como en
el curso de C. En cada vuelta, la `i` vale 0, 1, 2… y con ella se calcula dónde va cada caja.

Si cada ladrillo mide 70 de ancho y entre uno y otro hay 8 píxeles de aire, cada uno arranca **78**
píxeles más a la derecha que el anterior. El primero en `x = 10`; el segundo, en `10 + 78`; el tercero,
en `10 + 2 * 78`. O sea: `x = 10 + i * 78`.

Por ejemplo, este `for` dibuja tres postes separados por 100 píxeles:
```c
for (int i = 0; i < 3; i++) {
    SDL_FRect poste = { 50 + i * 100, 300, 10, 80 };
    SDL_RenderFillRect(lapiz, &poste);
}
```
El robot va a buscar dónde quedó todo lo naranja: si están los ocho, ocupa de lado a lado.

#### Desafío
Dibujá ocho ladrillos de 70 × 20 en la fila de `y = 40`, el primero en `x = 10` y cada uno 78 píxeles más a la derecha.

#### Pasos
1. En el `for`, cambiá `i < 1` por `i < 8`: así da ocho vueltas.
2. En el rectángulo, cambiá la `x`: donde dice `10`, escribí `10 + i * 78`.
3. Tocá **Jugar** (tienen que verse los ocho) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 96, 64, 255);
        for (int i = 0; i < 1; i++) {           /* acá: ¿cuántos ladrillos? */
            SDL_FRect ladrillo = { 10, 40, 70, 20 };   /* acá: la x de cada uno */
            SDL_RenderFillRect(lapiz, &ladrillo);
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

#### Estado
```
buscar #ff6040
```

#### Salida esperada
```
── Estado ──
buscar #ff6040: x 10, y 40, ancho 616, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 96, 64, 255);
        for (int i = 0; i < 8; i++) {           /* acá: ¿cuántos ladrillos? */
            SDL_FRect ladrillo = { 10 + i * 78, 40, 70, 20 };   /* acá: la x de cada uno */
            SDL_RenderFillRect(lapiz, &ladrillo);
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
Ocho ladrillos naranjas se encienden de un saque en la pantalla del Muro. {mentor} la levanta contra la
luz. —Cuando lleguemos a esa máquina, ya sabés por dónde empezar.

#### Imagen
- Arcadia sostiene la pantalla de una máquina vieja con una fila de ocho ladrillos naranjas brillando arriba.
- Kira, con el control de su brazal encendido, mira la pantalla; al fondo del galpón se ve un gabinete apagado con ladrillos dibujados en el costado.
- Gheco cuenta los ladrillos con la cola.

## R01-N02 · Eventos y teclado

```meta
tipo: tema
criatura: bucle_eterno
padre: R01-N01
precio: 10
temas: juegos.entrada
```

### Crónica

En la mesa del medio del Banco de Pruebas hay un teclado viejo con las letras gastadas, enchufado a una
pantalla donde espera un cuadrado blanco. {mentor} aprieta una tecla y no pasa nada. —Las máquinas de acá
escuchan de dos maneras —dice—. Como cuando alguien te toca el hombro una vez, o como cuando alguien se queda
apoyado. Hay juegos que necesitan una y juegos que necesitan la otra.

### Objetivos

Leer el teclado de las dos formas que tiene SDL: el **evento** de apretar una tecla (una vez por toque) y el
**estado** del teclado (si una tecla está apretada ahora, para moverse mientras se mantiene). Mover un cuadrado
con las flechas sin que se salga de la pantalla.

### Antes de empezar

Los rectángulos y las coordenadas (R01-N01). Del curso de C: arrays e `if`.

### Explicación

#### Dos maneras de escuchar el teclado
**1. El evento: «apretaron una tecla».** Llega **una vez** cada vez que se aprieta (si se la deja apretada un
rato, el sistema empieza a repetirla, como cuando escribís y mantenés una letra). Sirve para cosas que pasan
una vez: saltar, disparar, elegir en un menú, pausar.
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
    /* saltar */
}
```
- `SDL_EVENT_KEY_DOWN` es «tecla apretada»; `SDL_EVENT_KEY_UP`, «tecla soltada».
- `evento.key.key` dice qué tecla fue: `SDLK_SPACE`, `SDLK_A`… `SDLK_Z`, `SDLK_0`… `SDLK_9`, `SDLK_RETURN`
  (Enter), `SDLK_ESCAPE`, `SDLK_UP`, `SDLK_DOWN`, `SDLK_LEFT`, `SDLK_RIGHT`.
- `evento.key.repeat` vale `true` si es una repetición automática (para no saltar diez veces por dejar la
  tecla apretada).

**2. El estado: «¿está apretada ahora?».** Para moverse mientras se mantiene una flecha, no conviene esperar
eventos: se pregunta en cada vuelta del bucle.
```c
const bool *teclas = SDL_GetKeyboardState(NULL);
if (teclas[SDL_SCANCODE_RIGHT]) {
    x += 4;   /* mientras esté apretada, 4 píxeles por cuadro */
}
```
`SDL_GetKeyboardState` devuelve un **array** con una casilla por tecla: `true` si está apretada en este
momento. Las casillas se buscan por el **lugar** de la tecla (`SDL_SCANCODE_RIGHT`, `SDL_SCANCODE_W`,
`SDL_SCANCODE_SPACE`). Se lee **afuera** del `while (SDL_PollEvent…)`, en el paso de actualizar.

#### ¿`SDLK_` o `SDL_SCANCODE_`?
- `SDLK_A` es **la letra A**, esté donde esté en el teclado (en un teclado francés, la A está en otro lugar).
- `SDL_SCANCODE_A` es **el lugar** donde está la A en un teclado común. Para moverse con W, A, S y D conviene
  el lugar: así las cuatro teclas quedan juntas en cualquier teclado.
Regla práctica: eventos con `SDLK_`, estado con `SDL_SCANCODE_`.

#### Que no se escape
Si se mueve sin control, el cuadrado se va de la pantalla. Después de moverlo, se lo devuelve adentro:
```c
if (x < 0) x = 0;
if (x > 640 - 40) x = 640 - 40;   /* 40 es su ancho: el borde derecho del cuadrado no pasa de 640 */
```
SDL trae `SDL_clamp(valor, mínimo, máximo)` que hace lo mismo en una línea: `x = SDL_clamp(x, 0, 600);`.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Teclado", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float y = 220;
    int saltos = 0;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* Evento: una vez por toque (sin contar las repeticiones automáticas) */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && !evento.key.repeat) {
                saltos++;
            }
        }

        /* Estado: mientras esté apretada */
        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_RIGHT] || teclas[SDL_SCANCODE_D]) x += 4;
        if (teclas[SDL_SCANCODE_LEFT] || teclas[SDL_SCANCODE_A]) x -= 4;
        if (teclas[SDL_SCANCODE_DOWN] || teclas[SDL_SCANCODE_S]) y += 4;
        if (teclas[SDL_SCANCODE_UP] || teclas[SDL_SCANCODE_W]) y -= 4;
        x = SDL_clamp(x, 0, 640 - 40);
        y = SDL_clamp(y, 0, 480 - 40);

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, y, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "SALTOS: %d", saltos);
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

Todo juego decide, para cada acción, si es «de un toque» (saltar, disparar, abrir un menú) o «de mantener»
(caminar, acelerar, apuntar). Elegir mal se nota enseguida: un personaje que avanza a los saltitos o una nave
que dispara cien balas por apretar una vez.

### Errores habituales

**Moverse con el evento.** Si `x += 4` va adentro del `if (evento.type == SDL_EVENT_KEY_DOWN…)`, el cuadrado
se mueve a los tirones: un paso, una pausa, y después la repetición del sistema. Para moverse suave, el estado.

**Leer el estado adentro del `while (SDL_PollEvent…)`.** Ese `while` solo da vueltas cuando hay eventos: si
no llega ninguno, el código de adentro no corre. El estado va afuera, en el paso de actualizar.

**Mezclar los nombres.** `teclas[SDLK_RIGHT]` compila, pero busca en otra casilla: el array del estado se
busca con `SDL_SCANCODE_`.

**Atraviesaparedes: olvidar el ancho.** `if (x > 640) x = 640;` deja que el cuadrado se salga casi entero: su
borde derecho está en `x + 40`. El límite es `640 - 40`.

### Micro-misión R01-N02-P1 · Un paso por toque

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: El evento de una tecla | SDL_EVENT_KEY_DOWN · evento.key.key == SDLK_D · una vez por toque
recompensa: xp 10, oro 10
```

#### Escena
—Primero, la forma de un toque —dice {mentor}—. Cada vez que apretás la D, el cuadrado da un paso. Uno.
Como las fichas de un juego de mesa.

#### Gheco sugiere
Apretar una tecla manda un **evento** de tipo `SDL_EVENT_KEY_DOWN`, y `evento.key.key` dice cuál fue:
`SDLK_D` es la D. Se pregunta adentro del `while (SDL_PollEvent(&evento))`, como en la Clase 0 con ESC.

Para mover el cuadrado, se cambia su `x`: `x += 40;` lo corre 40 píxeles a la derecha (es lo mismo que
`x = x + 40;`). En el dibujo, el rectángulo usa esa `x`, así que en el cuadro siguiente aparece más a
la derecha.

Por ejemplo, esto sube el cuadrado 40 píxeles cada vez que se aprieta la W:
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_W) {
    y -= 40;
}
```
El robot va a apretar la D tres veces.

#### Desafío
Hacé que el cuadrado avance 40 píxeles a la derecha cada vez que se aprieta la D.

#### Pasos
1. Buscá el comentario `/* acá: si apretaron la D, un paso a la derecha */`.
2. Debajo, escribí `if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_D) {`.
3. Adentro, `x += 40;`, y cerrá la llave con `}`.
4. Tocá **Jugar**, hacé clic en el juego y apretá la D varias veces. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 100;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si apretaron la D, un paso a la derecha */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
tecla D
cuadros 3
tecla D
cuadros 3
tecla D
cuadros 3
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 220, y 220, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 100;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si apretaron la D, un paso a la derecha */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_D) {
                x += 40;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
Toc, toc, toc: el cuadrado salta tres casilleros. {mentor} se ríe. —Así se movía el caballito de la
máquina de carreras. Un toque, un paso.

#### Imagen
- El teclado viejo del Banco de Pruebas, con las letras gastadas; el dedo de Kira (guante cerrado) aprieta la D.
- En la pantalla, un cuadrado blanco con una estela de tres pasos, como huellas.
- Arcadia, divertida, sostiene un caballito de juguete de una máquina de carreras.

### Micro-misión R01-N02-P2 · Mantener apretado

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: El estado del teclado | const bool *teclas = SDL_GetKeyboardState(NULL); · if (teclas[SDL_SCANCODE_RIGHT]) …
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora la otra —dice {mentor}—. Para caminar nadie toca la tecla mil veces: la deja apretada. La máquina
tiene que darse cuenta de que **sigue** apretada.

#### Gheco sugiere
El evento llega una vez por toque. Para saber si una tecla **está apretada ahora**, SDL tiene otra
cosa: el **estado** del teclado.

`SDL_GetKeyboardState(NULL)` devuelve un **array** de `bool`: una casilla por tecla, que vale `true`
mientras está apretada. Este código ya lo guarda en `teclas`. Cada casilla se busca por el lugar de la
tecla: `teclas[SDL_SCANCODE_RIGHT]` es la flecha derecha.

Como se pregunta en **cada vuelta** del bucle (unas 60 por segundo), si la tecla sigue apretada, el
cuadrado avanza un poquito en cada cuadro y se ve suave.

Por ejemplo, esto lo baja 4 píxeles por cuadro mientras la S esté apretada:
```c
if (teclas[SDL_SCANCODE_S]) {
    y += 4;
}
```
El robot va a mantener la flecha derecha durante 20 cuadros.

#### Desafío
Hacé que el cuadrado avance 4 píxeles por cuadro mientras la flecha derecha esté apretada.

#### Pasos
1. Buscá el comentario `/* acá: mientras la flecha derecha esté apretada, avanzar 4 */`.
2. Debajo, escribí `if (teclas[SDL_SCANCODE_RIGHT]) {`.
3. Adentro, `x += 4;`, y cerrá la llave.
4. Tocá **Jugar**, hacé clic en el juego y mantené la flecha derecha. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 100;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        /* acá: mientras la flecha derecha esté apretada, avanzar 4 */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
apretar Derecha
cuadros 20
soltar Derecha
cuadros 5
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 180, y 220, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 100;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        /* acá: mientras la flecha derecha esté apretada, avanzar 4 */
        if (teclas[SDL_SCANCODE_RIGHT]) {
            x += 4;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
El cuadrado se desliza, suave, mientras Kira mantiene la flecha, y frena justo cuando la suelta.
{mentor} aplaude una vez. —Eso es caminar. Lo otro era saltar de baldosa en baldosa.

#### Imagen
- La pantalla del Banco de Pruebas con un cuadrado blanco que se desliza dejando una estela suave.
- Kira mantiene apretada la flecha del teclado; su brazal con el control brilla cian.
- Arcadia aplaude; Gheco corre al lado del cuadrado, dentro de la pantalla, como si lo acompañara.

### Micro-misión R01-N02-P3 · Las cuatro flechas

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Cuatro direcciones | RIGHT: x += 4 · LEFT: x -= 4 · DOWN: y += 4 · UP: y -= 4
recompensa: xp 10, monedas 4
```

#### Escena
—Un personaje que solo va a la derecha es un tren —dice {mentor}—. Que vaya para donde quieras.

#### Gheco sugiere
La flecha derecha ya está: suma 4 a la `x`. Las otras tres son iguales, cambiando la tecla y la cuenta:
- **izquierda** (`SDL_SCANCODE_LEFT`): la `x` **baja** (`x -= 4`);
- **abajo** (`SDL_SCANCODE_DOWN`): la `y` **sube** (`y += 4`), porque la `y` crece hacia abajo;
- **arriba** (`SDL_SCANCODE_UP`): la `y` **baja** (`y -= 4`).

Van como `if` separados (no `else if`): así se pueden apretar dos a la vez y moverse en diagonal.

El robot va a mantener la flecha abajo 10 cuadros y después la izquierda 5.

#### Desafío
Agregá las flechas izquierda, abajo y arriba, cada una moviendo 4 píxeles por cuadro.

#### Pasos
1. Buscá el comentario `/* acá: las otras tres flechas */`.
2. Escribí `if (teclas[SDL_SCANCODE_LEFT]) {`, adentro `x -= 4;` y cerrá la llave.
3. Otro `if` con `SDL_SCANCODE_DOWN` que haga `y += 4;`.
4. Otro con `SDL_SCANCODE_UP` que haga `y -= 4;`.
5. Tocá **Jugar**, probá las cuatro flechas y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float y = 220;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_RIGHT]) {
            x += 4;
        }
        /* acá: las otras tres flechas */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, y, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
apretar Abajo
cuadros 10
soltar Abajo
apretar Izquierda
cuadros 5
soltar Izquierda
cuadros 3
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 280, y 260, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float y = 220;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_RIGHT]) {
            x += 4;
        }
        /* acá: las otras tres flechas */
        if (teclas[SDL_SCANCODE_LEFT]) {
            x -= 4;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            y += 4;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            y -= 4;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, y, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
Kira dibuja una vuelta entera con el cuadrado por toda la pantalla. Gheco, mareado, se agarra del borde
de la mesa. —Ahora sí —dice {mentor}—. Eso ya es un personaje.

#### Imagen
- La pantalla del Banco de Pruebas con la estela de un cuadrado blanco que dio una vuelta entera, como un dibujo con un solo trazo.
- Kira con las dos manos sobre las flechas del teclado, concentrada.
- Gheco mareado agarrado del borde de la mesa; Arcadia sonríe.

### Micro-misión R01-N02-P4 · Que no se escape

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Los bordes | if (x < 0) x = 0; · if (x > 640 - 40) x = 640 - 40; · o SDL_clamp(x, 0, 600)
recompensa: xp 10, monedas 4
```

#### Escena
Kira mantiene la flecha izquierda y el cuadrado desaparece por el costado de la pantalla. Algo se ríe
adentro del vidrio: un **Atraviesaparedes**. —Esos bichos no respetan los bordes —dice {mentor}—.
Ponele un límite.

#### Gheco sugiere
Después de mover el cuadrado, hay que fijarse si se pasó del borde y, si se pasó, **devolverlo**:
```c
if (x < 0) {
    x = 0;              /* el borde izquierdo de la ventana */
}
```
Del lado derecho hay que tener en cuenta el **ancho** del cuadrado: su `x` es su borde izquierdo, pero
su borde derecho está en `x + 40`. Para que ese borde no pase de 640, la `x` no puede pasar de
`640 - 40 = 600`.

Va **después** de los `if` que lo mueven: primero se mueve, después se corrige.

Por ejemplo, para que no se salga por arriba: `if (y < 0) { y = 0; }`.

El robot va a mantener la flecha izquierda 100 cuadros (mucho más de lo que hace falta para llegar al
borde) y después la derecha otros 150.

#### Desafío
Hacé que el cuadrado no se salga por la izquierda ni por la derecha.

#### Pasos
1. Buscá el comentario `/* acá: que no se salga por la izquierda ni por la derecha */`.
2. Escribí `if (x < 0) {`, adentro `x = 0;` y cerrá la llave.
3. Escribí `if (x > 640 - 40) {`, adentro `x = 640 - 40;` y cerrá la llave.
4. Tocá **Jugar**, llevalo contra los dos bordes y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float y = 220;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_RIGHT]) x += 4;
        if (teclas[SDL_SCANCODE_LEFT]) x -= 4;
        if (teclas[SDL_SCANCODE_DOWN]) y += 4;
        if (teclas[SDL_SCANCODE_UP]) y -= 4;
        /* acá: que no se salga por la izquierda ni por la derecha */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, y, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
cuadros 100
soltar Izquierda
cuadros 2
apretar Derecha
cuadros 150
soltar Derecha
cuadros 2
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 600, y 220, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float y = 220;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_RIGHT]) x += 4;
        if (teclas[SDL_SCANCODE_LEFT]) x -= 4;
        if (teclas[SDL_SCANCODE_DOWN]) y += 4;
        if (teclas[SDL_SCANCODE_UP]) y -= 4;
        /* acá: que no se salga por la izquierda ni por la derecha */
        if (x < 0) {
            x = 0;
        }
        if (x > 640 - 40) {
            x = 640 - 40;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, y, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
El cuadrado choca contra el borde y se queda ahí, firme. El Atraviesaparedes se da la cabeza contra el
vidrio y se va, ofendido. —Primera regla de la ciudad —dice {mentor}—: nada sale de la pantalla sin
permiso.

#### Imagen
- Un Atraviesaparedes (criatura translúcida y gomosa, medio metida dentro de una pared de ladrillos) se da la cabeza contra el borde de una pantalla.
- En la pantalla, un cuadrado blanco firme contra el borde izquierdo.
- Kira cruzada de brazos; Arcadia levanta un dedo, como quien dicta una regla; Gheco saca la lengua al bicho.

## R01-N03 · El mouse

```meta
tipo: tema
criatura: glitch
padre: R01-N02
precio: 10
temas: juegos.entrada
usa: prog.funciones
```

### Crónica

Al fondo del Banco de Pruebas hay un **tiro al blanco** de feria con una pantalla en lugar de latitas. La
pistola de luz está rota, pero alguien le enchufó un mouse. —El Vidriero lo arregló así, con lo que tenía
—dice {mentor}—. Dice que el mouse es la pistola de luz de la gente que trabaja sentada.

### Objetivos

Leer el mouse: dónde está (el evento de movimiento), cuándo se hace clic y en qué lugar, y saber si un clic cayó
**adentro** de un rectángulo (un botón).

### Antes de empezar

El teclado (R01-N02). Del curso de C: funciones que devuelven `bool`.

### Explicación

#### Los eventos del mouse
| Evento | Cuándo llega | Qué trae |
|---|---|---|
| `SDL_EVENT_MOUSE_MOTION` | se movió | `evento.motion.x`, `evento.motion.y` |
| `SDL_EVENT_MOUSE_BUTTON_DOWN` | apretaron un botón | `evento.button.x`, `evento.button.y` y `evento.button.button` |
| `SDL_EVENT_MOUSE_BUTTON_UP` | lo soltaron | lo mismo |
| `SDL_EVENT_MOUSE_WHEEL` | giraron la rueda | `evento.wheel.y` (positivo hacia arriba) |

Las coordenadas son las de la ventana (0,0 arriba a la izquierda), como todo lo demás. `evento.button.button`
dice qué botón: `SDL_BUTTON_LEFT` (izquierdo), `SDL_BUTTON_RIGHT` (derecho) o `SDL_BUTTON_MIDDLE` (la rueda).

Ojo: adentro del `if` de cada tipo se usa **su** parte del evento. En un `SDL_EVENT_MOUSE_MOTION` se lee
`evento.motion`; en un clic, `evento.button`. Si se mezclan, se leen números que no son.

#### El estado del mouse
Como el teclado, el mouse también tiene estado: `SDL_GetMouseState(&x, &y)` llena `x` e `y` con dónde está
ahora, y devuelve qué botones están apretados.

#### ¿El clic cayó en el botón?
Un punto está **adentro** de un rectángulo si está entre su borde izquierdo y el derecho, **y** entre el de
arriba y el de abajo:
```c
px >= r.x && px <= r.x + r.w      /* entre izquierda y derecha */
&& py >= r.y && py <= r.y + r.h   /* entre arriba y abajo */
```
Conviene guardarlo en una función que devuelva `bool`, para usarla con cualquier botón.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static bool adentro(float px, float py, SDL_FRect r)
{
    return px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El tiro al blanco", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect blanco = { 280, 200, 80, 80 };
    int aciertos = 0;
    float mx = 0, my = 0;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_MOTION) {
                mx = evento.motion.x;
                my = evento.motion.y;
            }
            if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN && evento.button.button == SDL_BUTTON_LEFT
                && adentro(evento.button.x, evento.button.y, blanco)) {
                aciertos++;
                blanco.x = SDL_rand(560);   /* el blanco salta a otro lugar */
                blanco.y = SDL_rand(400);
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderFillRect(lapiz, &blanco);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderLine(lapiz, mx - 12, my, mx + 12, my);   /* la mira: una cruz */
        SDL_RenderLine(lapiz, mx, my - 12, mx, my + 12);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "ACIERTOS: %d", aciertos);
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

Los menús, los botones, las cartas que se arrastran, los juegos de apuntar y los de estrategia (elegir una
unidad y mandarla a un lugar) se juegan con el mouse. La cuenta de «¿cayó adentro?» es la misma que hace
cualquier botón de cualquier programa.

### Errores habituales

**Leer la parte equivocada del evento.** `evento.button.x` en un evento de movimiento da cualquier número: en
`SDL_EVENT_MOUSE_MOTION` es `evento.motion.x`.

**Glitch: la mira corrida.** Si el rectángulo de la mira empieza en `mx, my`, el mouse queda en su esquina,
no en el centro. Para centrarla: `mx - 10, my - 10` (la mitad de su tamaño).

**El botón que se aprieta de más.** Con `SDL_GetMouseState` adentro del bucle, un clic largo cuenta como
muchos (uno por cuadro). Para contar clics, el evento `SDL_EVENT_MOUSE_BUTTON_DOWN`, que llega una vez.

**Olvidar un `&&`.** `px >= r.x && px <= r.x + r.w` es solo la mitad: sin las dos condiciones de la `y`,
cuenta cualquier clic que esté a la altura del botón… o en cualquier altura.

### Micro-misión R01-N03-P1 · La mira que sigue al mouse

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Dónde está el mouse | SDL_EVENT_MOUSE_MOTION · evento.motion.x · evento.motion.y
recompensa: xp 10, oro 10
```

#### Escena
En la pantalla del tiro al blanco hay una mira roja clavada en el medio. —Tiene que seguir a tu mano
—dice {mentor}—. Si no, es un adorno.

#### Gheco sugiere
Cada vez que el mouse se mueve llega un evento de tipo `SDL_EVENT_MOUSE_MOTION`. Adentro trae dónde
quedó: `evento.motion.x` y `evento.motion.y`, en píxeles de la ventana.

El código ya tiene dos variables, `mx` y `my`, y dibuja la mira centrada ahí. Solo falta **guardar** la
posición cuando llega el evento:
```c
if (evento.type == SDL_EVENT_MOUSE_MOTION) {
    mx = evento.motion.x;
    /* … y lo mismo con la y */
}
```
El robot va a llevar el mouse al punto `100, 300`.

#### Desafío
Hacé que la mira roja siga al mouse.

#### Pasos
1. Buscá el comentario `/* acá: si se movió el mouse, guardar dónde está */`.
2. Debajo, escribí `if (evento.type == SDL_EVENT_MOUSE_MOTION) {`.
3. Adentro, `mx = evento.motion.x;` y `my = evento.motion.y;`. Cerrá la llave.
4. Tocá **Jugar**, mové el mouse sobre el juego y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float mx = 320;
    float my = 240;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si se movió el mouse, guardar dónde está */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 60, 255);
        SDL_FRect mira = { mx - 10, my - 10, 20, 20 };
        SDL_RenderFillRect(lapiz, &mira);
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
mouse 100 300
cuadros 3
```

#### Estado
```
buscar #ff3c3c
```

#### Salida esperada
```
── Estado ──
buscar #ff3c3c: x 90, y 290, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float mx = 320;
    float my = 240;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si se movió el mouse, guardar dónde está */
            if (evento.type == SDL_EVENT_MOUSE_MOTION) {
                mx = evento.motion.x;
                my = evento.motion.y;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 60, 255);
        SDL_FRect mira = { mx - 10, my - 10, 20, 20 };
        SDL_RenderFillRect(lapiz, &mira);
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
La mira se despega del centro y sigue a Kira por toda la pantalla, pegada como una sombra. {mentor}
levanta las cejas. —Buen pulso.

#### Imagen
- Un tiro al blanco de feria con una pantalla en lugar de latitas; una mira roja sobre la pantalla.
- Kira mueve un mouse viejo enchufado a la pistola de luz rota; la mira sigue su mano.
- Arcadia apoyada en el mostrador del puesto; Gheco con un ojo cerrado, como apuntando.

### Micro-misión R01-N03-P2 · El clic deja marca

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Un clic | SDL_EVENT_MOUSE_BUTTON_DOWN · evento.button.x · evento.button.y
recompensa: xp 10, monedas 4
```

#### Escena
—Una pistola de luz que no marca dónde pegó no sirve para practicar —dice {mentor}—. Que quede una
marquita amarilla donde hiciste clic.

#### Gheco sugiere
Al apretar un botón del mouse llega un evento de tipo `SDL_EVENT_MOUSE_BUTTON_DOWN`. Dónde estaba el
mouse en ese momento viene en `evento.button.x` y `evento.button.y` (ojo: en un clic es `button`, no
`motion`).

El código dibuja una marca amarilla en `marcaX, marcaY`. Al principio están en `-100`, afuera de la
ventana, para que no se vea hasta el primer clic. Solo falta guardar ahí la posición del clic.

Por ejemplo, para guardar dónde soltaron el botón:
```c
if (evento.type == SDL_EVENT_MOUSE_BUTTON_UP) {
    soltadoX = evento.button.x;
}
```
El robot va a hacer clic en `400, 120`.

#### Desafío
Hacé que la marca amarilla aparezca donde se hace clic.

#### Pasos
1. Buscá el comentario `/* acá: si hicieron clic, guardar dónde */`.
2. Debajo, `if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN) {`.
3. Adentro, `marcaX = evento.button.x;` y `marcaY = evento.button.y;`. Cerrá la llave.
4. Tocá **Jugar**, hacé clic en varios lugares y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float marcaX = -100;
    float marcaY = -100;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si hicieron clic, guardar dónde */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect marca = { marcaX - 5, marcaY - 5, 10, 10 };
        SDL_RenderFillRect(lapiz, &marca);
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
clic 400 120
cuadros 3
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 395, y 115, ancho 10, alto 10
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float marcaX = -100;
    float marcaY = -100;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si hicieron clic, guardar dónde */
            if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN) {
                marcaX = evento.button.x;
                marcaY = evento.button.y;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect marca = { marcaX - 5, marcaY - 5, 10, 10 };
        SDL_RenderFillRect(lapiz, &marca);
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
Clic: un puntito amarillo. Clic: otro lugar. {mentor} le alcanza a Kira una ficha. —La primera que
gano en este puesto desde que se apagó la ciudad.

#### Imagen
- La pantalla del tiro al blanco con una marquita amarilla brillante donde pegó el disparo.
- Kira hace clic, concentrada; el visor le marca la posición con una cruz cian.
- Arcadia le alcanza una ficha dorada; Gheco salta de alegría.

### Micro-misión R01-N03-P3 · ¿Le pegué al botón?

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Punto adentro de un rectángulo | px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h
recompensa: xp 10, monedas 4
```

#### Escena
En el mostrador del puesto hay un botón gris pintado en la pantalla: **ENCENDER**. Kira hace clic en el
medio y no pasa nada. —La función que se fija si el clic cayó adentro está vacía —dice {mentor}—.
Siempre dice que no.

#### Gheco sugiere
La función `adentro` recibe un punto (`px`, `py`) y un rectángulo `r`, y tiene que devolver `true` si
el punto cae adentro. Ahora devuelve siempre `false`.

Un punto está adentro si cumple **las cuatro** cosas a la vez:
- está a la derecha del borde izquierdo: `px >= r.x`;
- está a la izquierda del borde derecho: `px <= r.x + r.w`;
- está debajo del borde de arriba: `py >= r.y`;
- está arriba del borde de abajo: `py <= r.y + r.h`.

Se juntan con `&&` («y») en un solo `return`. Por ejemplo, para saber si un número está entre 1 y 10:
`return n >= 1 && n <= 10;`.

El robot va a hacer clic en `300, 220` (adentro del botón) y a mirar su color.

#### Desafío
Completá la función `adentro` para que el botón se prenda (verde) al hacer clic sobre él.

#### Pasos
1. Buscá la función `adentro`, arriba de `main`.
2. Cambiá `return false;` por `return px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h;`.
3. Tocá **Jugar**, hacé clic afuera del botón (no pasa nada) y adentro (se prende). Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

/* ¿El punto (px, py) cae adentro del rectángulo r? */
static bool adentro(float px, float py, SDL_FRect r)
{
    return false;   /* acá: la cuenta */
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect boton = { 240, 200, 160, 60 };
    bool prendido = false;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN && adentro(evento.button.x, evento.button.y, boton)) {
                prendido = true;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (prendido) {
            SDL_SetRenderDrawColor(lapiz, 60, 200, 90, 255);
        } else {
            SDL_SetRenderDrawColor(lapiz, 120, 120, 140, 255);
        }
        SDL_RenderFillRect(lapiz, &boton);
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
clic 600 50
cuadros 2
clic 300 220
cuadros 3
```

#### Estado
```
pixel 320 230
```

#### Salida esperada
```
── Estado ──
pixel 320 230: #3cc85a
```

#### Solución
```c
#include <SDL3/SDL.h>

/* ¿El punto (px, py) cae adentro del rectángulo r? */
static bool adentro(float px, float py, SDL_FRect r)
{
    return px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect boton = { 240, 200, 160, 60 };
    bool prendido = false;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN && adentro(evento.button.x, evento.button.y, boton)) {
                prendido = true;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (prendido) {
            SDL_SetRenderDrawColor(lapiz, 60, 200, 90, 255);
        } else {
            SDL_SetRenderDrawColor(lapiz, 120, 120, 140, 255);
        }
        SDL_RenderFillRect(lapiz, &boton);
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
El botón se pone verde y todo el puesto se ilumina: las lamparitas del techo, el cartel, la campana.
{mentor} se tapa los oídos riéndose. —¡Eso es lo que hacía cuando alguien ganaba!

#### Imagen
- El puesto de tiro al blanco iluminado de golpe: lamparitas de colores en el techo, una campana que suena y un botón verde en la pantalla.
- Kira con la mano en el mouse, sorprendida; Arcadia se tapa los oídos riendo.
- Gheco colgado de la campana.

### Micro-misión R01-N03-P4 · La cuenta de los clics

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Texto con números | SDL_RenderDebugTextFormat(lapiz, x, y, "CLICS: %d", clics);
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora que anda, quiero saber cuántas veces le pegás —dice {mentor}—. Las máquinas viejas llevaban la
cuenta en una esquina, en blanco.

#### Gheco sugiere
Para contar, una variable que empieza en 0 y suma 1 en cada acierto: `clics++;` (es lo mismo que
`clics = clics + 1;`). Va adentro del `if` que ya se fija si el clic cayó en el botón.

Para mostrar un número en pantalla está `SDL_RenderDebugTextFormat`, que funciona como `printf`: el
texto lleva `%d` donde va el número, y el número va después.
```c
SDL_RenderDebugTextFormat(lapiz, 10, 10, "VIDAS: %d", vidas);
```
El robot va a hacer tres clics en el botón y uno afuera, y va a leer el texto.

#### Desafío
Contá los clics que caen en el botón y mostrá la cuenta arriba a la izquierda, como `CLICS: 3`.

#### Pasos
1. Buscá el comentario `/* acá: contar el clic */` y debajo escribí `clics++;`.
2. Buscá la línea `SDL_RenderDebugText(lapiz, 10, 10, "CLICS: 0");`.
3. Cambiala por `SDL_RenderDebugTextFormat(lapiz, 10, 10, "CLICS: %d", clics);`.
4. Tocá **Jugar**, hacé algunos clics y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static bool adentro(float px, float py, SDL_FRect r)
{
    return px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect boton = { 240, 200, 160, 60 };
    int clics = 0;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN && adentro(evento.button.x, evento.button.y, boton)) {
                /* acá: contar el clic */
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 60, 200, 90, 255);
        SDL_RenderFillRect(lapiz, &boton);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "CLICS: 0");   /* acá: mostrar la cuenta */
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
clic 300 220
cuadros 2
clic 350 240
cuadros 2
clic 50 50
cuadros 2
clic 390 255
cuadros 3
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: CLICS: 3
```

#### Solución
```c
#include <SDL3/SDL.h>

static bool adentro(float px, float py, SDL_FRect r)
{
    return px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect boton = { 240, 200, 160, 60 };
    int clics = 0;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_MOUSE_BUTTON_DOWN && adentro(evento.button.x, evento.button.y, boton)) {
                /* acá: contar el clic */
                clics++;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 60, 200, 90, 255);
        SDL_RenderFillRect(lapiz, &boton);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "CLICS: %d", clics);
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
CLICS: 1, 2, 3… Kira no puede parar. {mentor} le saca el mouse de la mano. —Eso le pasaba a todos.
Cuando un juego cuenta lo que hacés, querés que el número suba. No lo olvides cuando hagas los tuyos.

#### Imagen
- La pantalla del tiro al blanco con un contador blanco en la esquina y el botón verde en el medio.
- Arcadia le saca el mouse de la mano a Kira, riéndose; Kira quiere seguir.
- Gheco anota la cuenta en una libretita.

## R01-N04 · Movimiento y delta time

```meta
tipo: tema
criatura: fantasma_fotograma
padre: R01-N03
precio: 10
temas: juegos.bucle, juegos.fisica
```

### Crónica

En el Banco de Pruebas hay dos máquinas iguales, una al lado de la otra, con la misma navecita cian. En una,
la nave cruza la pantalla en un suspiro; en la otra, se arrastra. Entre las dos flota una figura borrosa,
como una foto movida: el **Fantasma del Fotograma**.

—Ese bicho me arruinó medio parque —dice {mentor}—. Una máquina nueva iba rapidísimo, una vieja iba lenta, y
nadie sabía por qué. El Vidriero lo resolvió con un reloj.

### Objetivos

Medir cuánto tiempo pasa entre un cuadro y el siguiente (el **delta time**) y mover las cosas en **píxeles por
segundo**, para que el juego vaya igual de rápido en cualquier compu. Hacer rebotar algo en los bordes
cambiándole la velocidad de signo.

### Antes de empezar

El teclado y los bordes (R01-N02). Del curso de C: `float` y la división con decimales.

### Explicación

#### El problema: «4 píxeles por cuadro»
Hasta ahora, cada vuelta del bucle movía las cosas un número fijo de píxeles: `x += 4`. Pero no todas las
compus dan la misma cantidad de vueltas por segundo: una rápida puede dar 144 y una lenta, 30. Con
`x += 4`, en la rápida la nave recorre 576 píxeles por segundo y en la lenta, 120. Ese es el **Fantasma del
Fotograma**.

#### La solución: medir el tiempo
`SDL_GetTicks()` devuelve cuántos **milisegundos** pasaron desde que arrancó el programa (1000 milisegundos son
un segundo). Si se guarda el de la vuelta anterior, la resta dice cuánto duró este cuadro:
```c
Uint64 antes = SDL_GetTicks();          /* antes del bucle */
while (jugando) {
    Uint64 ahora = SDL_GetTicks();
    float dt = (ahora - antes) / 1000.0f;   /* en segundos: 0.016 si pasaron 16 ms */
    antes = ahora;
    ...
}
```
- `Uint64` es un entero sin signo muy grande (el tipo que devuelve `SDL_GetTicks`).
- `dt` se llama **delta time**: «la diferencia de tiempo». Delta (Δ) es la letra que se usa para las
  diferencias.
- Se divide por `1000.0f` (con `.0f`) para que la cuenta dé con decimales: `16 / 1000` daría 0 entero.

#### Moverse en píxeles por segundo
Con `dt`, la velocidad se escribe en **píxeles por segundo** y se multiplica:
```c
x += 200 * dt;   /* 200 píxeles por segundo */
```
En la compu rápida, `dt` es chico y avanza poquito por cuadro, pero hace muchos cuadros. En la lenta, `dt` es
grande y avanza más por cuadro. En un segundo, las dos recorren 200 píxeles.

Por eso las posiciones van en `float`: en un cuadro se puede avanzar 3,2 píxeles.

#### La velocidad como variable: rebotar
Si la velocidad se guarda en una variable (`vx`), cambiarle el signo invierte la dirección:
```c
x += vx * dt;
if (x < 0 || x > 640 - 20) {
    vx = -vx;                           /* da la vuelta */
    x = SDL_clamp(x, 0, 640 - 20);      /* y vuelve adentro, por si se pasó un poco */
}
```
`vx` positiva va a la derecha; negativa, a la izquierda. Con `vx` y `vy` se mueve en diagonal.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El reloj del Vidriero", 640, 480, 0, &ventana, &lapiz);

    float x = 100, y = 100;
    float vx = 220, vy = 160;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        /* Cuánto duró este cuadro, en segundos */
        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Mover en píxeles por segundo y rebotar en los bordes */
        x += vx * dt;
        y += vy * dt;
        if (x < 0 || x > 640 - 20) { vx = -vx; x = SDL_clamp(x, 0, 640 - 20); }
        if (y < 0 || y > 480 - 20) { vy = -vy; y = SDL_clamp(y, 0, 480 - 20); }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, y, 20, 20 };
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

Todos los juegos de verdad usan delta time: el mismo juego tiene que andar igual en una compu de escritorio, en
una notebook vieja y en un monitor de 144 Hz. Y la velocidad como variable es la base de todo lo que se mueve
solo: pelotas, balas, enemigos, nubes.

### Errores habituales

**Fantasma del Fotograma: moverse sin `dt`.** `x += 4` en lugar de `x += 240 * dt`. Anda bien en tu compu y
distinto en la de al lado.

**División entera.** `float dt = (ahora - antes) / 1000;` da **0** casi siempre: dos enteros se dividen sin
decimales. Hace falta `1000.0f`.

**Olvidar `antes = ahora`.** Sin esa línea, `dt` mide el tiempo desde que arrancó el programa y crece sin
parar: todo se acelera cada vez más.

**Atraviesaparedes: rebotar sin volver adentro.** Si la pelota se pasó del borde y solo se le da vuelta la
velocidad, puede quedar del otro lado, temblando y rebotando para siempre. Hay que devolverla adentro.

### Micro-misión R01-N04-P1 · El reloj del cuadro

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Medir el tiempo | Uint64 ahora = SDL_GetTicks(); · ms = ahora - antes; · antes = ahora;
recompensa: xp 10, oro 10
```

#### Escena
{mentor} desarma la máquina lenta y saca un reloj chiquito. —Lo primero es saber cuánto tarda cada
cuadro. Si no lo medís, el fantasma hace lo que quiere.

#### Gheco sugiere
`SDL_GetTicks()` dice cuántos **milisegundos** pasaron desde que arrancó el juego (1000 milisegundos son
un segundo). Solo, no sirve de mucho: lo que importa es **cuánto pasó desde el cuadro anterior**.

Para eso, el código guarda en `antes` la hora del cuadro anterior. En cada vuelta toma la hora nueva
(`ahora`) y la resta da lo que duró el cuadro: `ms = ahora - antes;`. Después, `antes = ahora;` la
deja lista para la vuelta siguiente.

Es como medir cuánto tardaste en una vuelta a la manzana: la hora al llegar menos la hora al salir.

El robot va a leer el texto de la pantalla: con `SDL_Delay(16)`, cada cuadro dura unos 16 o 17 milisegundos (16 de la espera, y un poquito más lo que tarda en dibujar).

#### Desafío
Calculá cuántos milisegundos pasaron desde el cuadro anterior y guardalo en `ms`.

#### Pasos
1. Buscá el comentario `/* acá: cuántos milisegundos pasaron desde el cuadro anterior */`.
2. Debajo, escribí `ms = ahora - antes;`.
3. Tocá **Jugar**: arriba tiene que aparecer un número cerca de 16 (en tu compu puede variar un poco). Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    Uint64 antes = SDL_GetTicks();
    Uint64 ms = 0;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        /* acá: cuántos milisegundos pasaron desde el cuadro anterior */
        antes = ahora;

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "MS: %d", (int)ms);
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
cuadros 20
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: MS: 17
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    Uint64 antes = SDL_GetTicks();
    Uint64 ms = 0;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        /* acá: cuántos milisegundos pasaron desde el cuadro anterior */
        ms = ahora - antes;
        antes = ahora;

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "MS: %d", (int)ms);
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
MS: 17. {mentor} da vuelta el reloj chiquito entre los dedos. —Diecisiete milésimas por cuadro. En la
máquina lenta eran cuarenta. Ahí está la diferencia que nadie veía.

#### Imagen
- Arcadia sostiene un reloj chiquito de engranajes sacado de una máquina desarmada; el Fantasma del Fotograma (figura borrosa como una foto movida, con varias copias de sí mismo) mira desde atrás.
- Una pantalla con un número blanco en la esquina.
- Kira y Gheco miran el reloj de cerca.

### Micro-misión R01-N04-P2 · Píxeles por segundo

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Delta time | float dt = (ahora - antes) / 1000.0f; · x += velocidad * dt;
recompensa: xp 10, monedas 4
```

#### Escena
—Con el reloj, la nave ya puede saber cuánto avanzar —dice {mentor}—. El Vidriero quería que cruzara la
pantalla a doscientos píxeles por segundo. En cualquier máquina.

#### Gheco sugiere
El código ya calcula `dt`: cuántos **segundos** duró el cuadro (por ejemplo 0.016). Se divide por
`1000.0f`, con el `.0f`, para que la cuenta tenga decimales.

Ahora la nave avanza `x += 3;`, 3 píxeles por cuadro: en una compu rápida iría volando y en una lenta,
despacio. Para que vaya a **200 píxeles por segundo** en cualquier compu, se multiplica la velocidad por
`dt`:
```c
x += 200 * dt;
```
Si el cuadro duró 0.016 segundos, avanza 3,2 píxeles. Si duró 0.033, avanza 6,6. En un segundo, siempre
200.

Por ejemplo, una nube a 30 píxeles por segundo: `nubeX += 30 * dt;`.

El robot va a dejar pasar 30 cuadros y buscar la nave.

#### Desafío
Hacé que la nave avance a 200 píxeles por segundo usando `dt`.

#### Pasos
1. Buscá la línea `x += 3;`.
2. Cambiala por `x += 200 * dt;`.
3. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 0;
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
        float dt = (ahora - antes) / 1000.0f;   /* segundos desde el cuadro anterior */
        antes = ahora;

        x += 3;   /* acá: 200 píxeles por segundo */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_FRect nave = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &nave);
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
cuadros 30
```

#### Estado
```
buscar #00e5ff
```

#### Salida esperada
```
── Estado ──
buscar #00e5ff: x 99, y 220, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 0;
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
        float dt = (ahora - antes) / 1000.0f;   /* segundos desde el cuadro anterior */
        antes = ahora;

        x += 200 * dt;

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_FRect nave = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &nave);
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
{mentor} enchufa el código en las dos máquinas, la rápida y la lenta. Las dos naves cruzan la pantalla
juntas, como si fueran una. El Fantasma del Fotograma se borronea todavía más y desaparece.

#### Imagen
- Dos máquinas iguales lado a lado; en las dos pantallas, la misma nave cian exactamente a la misma altura del recorrido.
- El Fantasma del Fotograma se deshace en copias borrosas entre las dos máquinas.
- Kira festeja con el puño en alto; Arcadia apoya una mano en cada gabinete; Gheco entre los dos.

### Micro-misión R01-N04-P3 · Rebotar en los bordes

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Rebote | if (x < 0 || x > 640 - 20) { vx = -vx; x = SDL_clamp(x, 0, 640 - 20); }
recompensa: xp 10, monedas 4
```

#### Escena
En otra pantalla, una pelota amarilla sale disparada y se pierde por el costado. —Una pelota que se va
no es una pelota —dice {mentor}—. Es una despedida. Que rebote.

#### Gheco sugiere
La velocidad ahora está en una variable, `vx`: cuántos píxeles por segundo se mueve, y hacia dónde.
Positiva va a la derecha; negativa, a la izquierda.

Para que rebote, cuando toca un borde se le da vuelta el signo: `vx = -vx;`. Si venía a 250, pasa a
-250 y vuelve.

Toca un borde si `x < 0` (se pasó por la izquierda) **o** si `x > 640 - 20` (su borde derecho pasó de
640; la pelota mide 20). «O» en C es `||`.

Además, conviene **devolverla adentro**, porque en un cuadro puede haberse pasado un poquito:
`x = SDL_clamp(x, 0, 640 - 20);`. Si no, puede quedar trabada afuera, rebotando para siempre.

El robot va a dejar pasar 200 cuadros: tiempo de sobra para varios rebotes.

#### Desafío
Hacé que la pelota rebote en el borde izquierdo y en el derecho.

#### Pasos
1. Buscá el comentario `/* acá: rebotar en los dos bordes */`.
2. Escribí `if (x < 0 || x > 640 - 20) {`.
3. Adentro, `vx = -vx;` y `x = SDL_clamp(x, 0, 640 - 20);`. Cerrá la llave.
4. Tocá **Jugar** (tiene que ir y venir) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float vx = 250;   /* píxeles por segundo: positivo a la derecha */
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

        x += vx * dt;
        /* acá: rebotar en los dos bordes */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, 230, 20, 20 };
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
cuadros 200
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 97, y 230, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 300;
    float vx = 250;   /* píxeles por segundo: positivo a la derecha */
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

        x += vx * dt;
        /* acá: rebotar en los dos bordes */
        if (x < 0 || x > 640 - 20) {
            vx = -vx;
            x = SDL_clamp(x, 0, 640 - 20);
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, 230, 20, 20 };
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
La pelota va y viene, va y viene, sin cansarse. {mentor} la mira hipnotizada. —Así empezó el primer
juego de esta ciudad. Una pelota que no se iba.

#### Imagen
- Una pantalla con una pelota amarilla cuadrada a mitad de camino, con marcas de rebote de luz en los dos bordes.
- Arcadia la mira hipnotizada, con la cabeza siguiendo el ir y venir.
- Kira y Gheco imitan el movimiento con la cabeza.

### Micro-misión R01-N04-P4 · En diagonal

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Dos velocidades | x += vx * dt; y += vy * dt; · cada una rebota en sus bordes
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora en serio —dice {mentor}—. El protector de pantalla de las máquinas del Vidriero era una pelota que
rebotaba por todos lados. Arriba, abajo, a los costados.

#### Gheco sugiere
Para moverse en diagonal hacen falta **dos** velocidades: `vx` para los costados y `vy` para arriba y
abajo. La `x` ya está hecha: se mueve y rebota.

La `y` es igual, cambiando las letras y el borde: la ventana mide **480** de alto, así que se pasa si
`y < 0` o si `y > 480 - 20`.
```c
y += vy * dt;
if (/* se pasó arriba o abajo */) {
    vy = -vy;
    y = SDL_clamp(y, 0, 480 - 20);
}
```
El robot va a dejar pasar 150 cuadros.

#### Desafío
Hacé que la pelota también se mueva y rebote arriba y abajo.

#### Pasos
1. Buscá el comentario `/* acá: lo mismo para la y (el alto es 480) */`.
2. Escribí `y += vy * dt;`.
3. Después, `if (y < 0 || y > 480 - 20) {`, con `vy = -vy;` y `y = SDL_clamp(y, 0, 480 - 20);` adentro. Cerrá la llave.
4. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 100, y = 100;
    float vx = 220, vy = 160;
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

        x += vx * dt;
        if (x < 0 || x > 640 - 20) {
            vx = -vx;
            x = SDL_clamp(x, 0, 640 - 20);
        }
        /* acá: lo mismo para la y (el alto es 480) */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, y, 20, 20 };
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
cuadros 150
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 586, y 416, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    float x = 100, y = 100;
    float vx = 220, vy = 160;
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

        x += vx * dt;
        if (x < 0 || x > 640 - 20) {
            vx = -vx;
            x = SDL_clamp(x, 0, 640 - 20);
        }
        /* acá: lo mismo para la y (el alto es 480) */
        y += vy * dt;
        if (y < 0 || y > 480 - 20) {
            vy = -vy;
            y = SDL_clamp(y, 0, 480 - 20);
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, y, 20, 20 };
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
La pelota rebota por toda la pantalla y, de vez en cuando, casi entra justo en una esquina. Gheco
contiene la respiración cada vez. {mentor} se ríe. —Nunca entra. Bueno, casi nunca.

#### Imagen
- Una pantalla con una pelota amarilla que deja un trazo en zigzag rebotando por los cuatro bordes.
- Gheco contiene la respiración mirando una esquina; Kira y Arcadia, divertidas.

## R01-N05 · Colisiones entre rectángulos

```meta
tipo: tema
criatura: atraviesaparedes
padre: R01-N04
precio: 10
temas: juegos.colisiones
usa: prog.funciones
```

### Crónica

En el rincón más desordenado del Banco de Pruebas hay una caja de vidrio llena de Atraviesaparedes: bichos
gomosos que se meten en todo. Uno está medio adentro de un ladrillo; otro atraviesa una paleta de ida y de
vuelta. —Los junté acá para que no anden sueltos por la ciudad —dice {mentor}—. Se escapan cada vez que un
juego no sabe si dos cosas se tocan.

### Objetivos

Saber si dos rectángulos se tocan (la cuenta que usan casi todos los juegos 2D), y qué hacer cuando se tocan:
juntar algo, frenar contra una pared o rebotar.

### Antes de empezar

El movimiento con delta time (R01-N04) y la función `adentro` del mouse (R01-N03).

### Explicación

#### ¿Se tocan dos rectángulos?
Es más fácil pensarlo al revés: dos rectángulos **no** se tocan si uno está entero a la izquierda del otro, o
entero a la derecha, o entero arriba, o entero abajo. Si no pasa ninguna de esas cuatro, se pisan.

Dicho como condición, se tocan si pasan **las cuatro** cosas:
```c
a.x < b.x + b.w      /* el borde izquierdo de a está antes del borde derecho de b */
a.x + a.w > b.x      /* el borde derecho de a está después del borde izquierdo de b */
a.y < b.y + b.h      /* lo mismo, de arriba a abajo */
a.y + a.h > b.y
```
Esta prueba se llama **AABB** (*axis-aligned bounding box*: «cajas alineadas con los ejes»), porque sirve
para rectángulos derechos, sin girar.

SDL trae la misma cuenta hecha: `SDL_HasRectIntersectionFloat(&a, &b)` devuelve `true` si se pisan. En el
curso la escribimos a mano primero, para entenderla.

#### Qué hacer cuando se tocan
- **Juntar:** la gema desaparece (una variable `bool agarrada`) y se suman puntos. Ojo: si no se marca como
  agarrada, se suma en **cada cuadro** que estén tocándose.
- **Frenar:** el personaje se metió un poco en la pared; se lo saca, pegado al borde:
  `kira.x = pared.x - kira.w;`.
- **Rebotar:** se da vuelta la velocidad, como contra los bordes de la pantalla, y se la saca de adentro.

#### Primero mover, después revisar
En cada cuadro: mover todo, preguntar quién toca a quién y corregir. Así lo que se dibuja ya está corregido.

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
    SDL_CreateWindowAndRenderer("Junta las gemas (adelanto)", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 300, 400, 40, 40 };
    SDL_FRect gema = { 300, 100, 20, 20 };
    int puntos = 0;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
        if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
        kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
        kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

        /* Al tocarla, punto y la gema salta a otro lugar al azar */
        if (toca(kira, gema)) {
            puntos++;
            gema.x = SDL_rand(620);
            gema.y = 40 + SDL_rand(420);
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);
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

Pong, Arkanoid, las naves, el laberinto y las plataformas: todos se arman con esta misma pregunta, cientos de
veces por segundo. ¿La pelota tocó la paleta? ¿La bala tocó al enemigo? ¿El personaje está parado sobre una
plataforma?

### Errores habituales

**Atraviesaparedes: usar `<=` en lugar de `<`.** Con `<=`, dos cajas que solo se rozan el borde ya cuentan
como tocándose. A veces da igual; en un juego de plataformas, el personaje queda «tocando» el piso de al lado.

**Sumar puntos en cada cuadro.** Si la gema no se marca como agarrada (o no se mueve a otro lugar), mientras se
toquen se suma en cada vuelta: 60 puntos por segundo.

**Atraviesaparedes: rebotar sin sacar.** La pelota se metió 3 píxeles en la paleta, se le da vuelta la
velocidad, pero en el cuadro siguiente sigue tocando y se la vuelve a dar vuelta: queda temblando adentro.

**Comparar con el rectángulo viejo.** Si se revisa antes de mover, se revisa dónde estaba, no dónde está.

### Micro-misión R01-N05-P1 · ¿Se tocan?

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Colisión AABB | a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y
recompensa: xp 10, oro 10
```

#### Escena
En la pantalla hay un cuadrado blanco (Kira) encima de una gema cian. Arriba, una luz tendría que estar
verde, porque se tocan, pero está roja. —La función que pregunta si se tocan siempre dice que no —dice
{mentor}—. Así se escapan los bichos.

#### Gheco sugiere
La función `toca` recibe dos rectángulos, `a` y `b`, y tiene que devolver `true` si se pisan.

Dos rectángulos se tocan si pasan **las cuatro** cosas a la vez:
- el borde izquierdo de `a` está antes del borde derecho de `b`: `a.x < b.x + b.w`;
- el borde derecho de `a` está después del borde izquierdo de `b`: `a.x + a.w > b.x`;
- el borde de arriba de `a` está antes del borde de abajo de `b`: `a.y < b.y + b.h`;
- el borde de abajo de `a` está después del borde de arriba de `b`: `a.y + a.h > b.y`.

Se juntan con `&&` en un solo `return`, como la función `adentro` del mouse. Es la misma idea: allá era
un punto adentro de una caja; acá, una caja contra otra.

El robot va a mirar el color de la luz de arriba.

#### Desafío
Completá la función `toca` para que la luz se ponga verde cuando Kira y la gema se pisan.

#### Pasos
1. Buscá la función `toca`, arriba de `main`.
2. Cambiá `return false;` por `return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;`.
3. Tocá **Jugar**: la luz de arriba tiene que estar verde. Después, **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

/* ¿Se pisan los rectángulos a y b? */
static bool toca(SDL_FRect a, SDL_FRect b)
{
    return false;   /* acá: las cuatro condiciones */
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 250, 200, 60, 60 };
    SDL_FRect gema = { 290, 230, 40, 40 };

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (toca(kira, gema)) {
            SDL_SetRenderDrawColor(lapiz, 40, 160, 80, 255);   /* verde: se tocan */
        } else {
            SDL_SetRenderDrawColor(lapiz, 160, 40, 60, 255);   /* rojo: no se tocan */
        }
        SDL_FRect luz = { 0, 0, 640, 30 };
        SDL_RenderFillRect(lapiz, &luz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
pixel 5 5
```

#### Salida esperada
```
── Estado ──
pixel 5 5: #28a050
```

#### Solución
```c
#include <SDL3/SDL.h>

/* ¿Se pisan los rectángulos a y b? */
static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 250, 200, 60, 60 };
    SDL_FRect gema = { 290, 230, 40, 40 };

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (toca(kira, gema)) {
            SDL_SetRenderDrawColor(lapiz, 40, 160, 80, 255);   /* verde: se tocan */
        } else {
            SDL_SetRenderDrawColor(lapiz, 160, 40, 60, 255);   /* rojo: no se tocan */
        }
        SDL_FRect luz = { 0, 0, 640, 30 };
        SDL_RenderFillRect(lapiz, &luz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
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
La luz se pone verde. Adentro de la caja de vidrio, los Atraviesaparedes se quedan quietos de golpe,
como si los hubieran descubierto. —Ahora saben que los vemos —dice {mentor}.

#### Imagen
- Una caja de vidrio llena de Atraviesaparedes (criaturas translúcidas y gomosas) quietos de golpe, sorprendidos.
- Al lado, una pantalla con un cuadrado blanco sobre una gema cian y una franja de luz verde arriba.
- Kira señala la caja; Arcadia sonríe; Gheco golpea el vidrio.

### Micro-misión R01-N05-P2 · Juntar la gema

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Juntar algo | if (!agarrada && toca(kira, gema)) { agarrada = true; puntos += 10; }
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora que sabés cuándo se tocan —dice {mentor}—, hacé que Kira junte la gema. Diez puntos. Y una sola
vez: las gemas no se juntan dos veces.

#### Gheco sugiere
Cuando Kira toca la gema hay que hacer dos cosas: marcarla como **agarrada** (así deja de dibujarse) y
sumar 10 puntos.

Pero ojo: mientras Kira siga encima de la gema, `toca` da `true` en **cada cuadro**. Si solo se suman
los puntos, se suman 10 sesenta veces por segundo. Por eso se pregunta también si **todavía no** estaba
agarrada: `!agarrada` (el `!` es «no»).
```c
if (!abierta && toca(kira, puerta)) {
    abierta = true;
    llaves -= 1;
}
```
El robot va a mantener la flecha derecha 110 cuadros (Kira pasa por encima de la gema y sigue).

#### Desafío
Cuando Kira toque la gema por primera vez, marcala como agarrada y sumá 10 puntos.

#### Pasos
1. Buscá el comentario `/* acá: si Kira toca la gema y todavía no la agarró, … */`.
2. Escribí `if (!agarrada && toca(kira, gema)) {`.
3. Adentro, `agarrada = true;` y `puntos += 10;`. Cerrá la llave.
4. Tocá **Jugar**, llevá a Kira hasta la gema y seguí de largo. Después, **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 40, 220, 40, 40 };
    SDL_FRect gema = { 400, 230, 20, 20 };
    bool agarrada = false;
    int puntos = 0;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 240 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 240 * dt;

        /* acá: si Kira toca la gema y todavía no la agarró, agarrarla y sumar 10 puntos */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        if (!agarrada) {
            SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
            SDL_RenderFillRect(lapiz, &gema);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);
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
apretar Derecha
cuadros 110
soltar Derecha
cuadros 3
```

#### Estado
```
textos
buscar #00e5ff
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS: 10
buscar #00e5ff: no está
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
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 40, 220, 40, 40 };
    SDL_FRect gema = { 400, 230, 20, 20 };
    bool agarrada = false;
    int puntos = 0;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 240 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 240 * dt;

        /* acá: si Kira toca la gema y todavía no la agarró, agarrarla y sumar 10 puntos */
        if (!agarrada && toca(kira, gema)) {
            agarrada = true;
            puntos += 10;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        if (!agarrada) {
            SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
            SDL_RenderFillRect(lapiz, &gema);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);
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
La gema desaparece con un brillo y el marcador salta a PUNTOS: 10. Kira pasa otra vez por encima: nada.
{mentor} asiente. —Bien. Una gema, una vez. Así nadie hace trampa.

#### Imagen
- Una pantalla con un cuadrado blanco que acaba de pasar por donde había una gema; queda un destello cian.
- Arriba, un marcador amarillo.
- Kira festeja; Gheco atrapa en el aire un brillo cian que salió de la pantalla.

### Micro-misión R01-N05-P3 · La pared

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Frenar contra una pared | if (toca(kira, pared)) { kira.x = pared.x - kira.w; }
recompensa: xp 10, monedas 4
```

#### Escena
En la pantalla hay una pared naranja. Kira camina hacia ella… y la atraviesa como si nada. Un
Atraviesaparedes aplaude desde la caja de vidrio. —Una pared que no frena es pintura —dice {mentor}.

#### Gheco sugiere
Cuando Kira camina hacia la derecha y se mete un poquito en la pared, hay que **sacarla**: dejarla
pegada al lado izquierdo de la pared.

El lado izquierdo de la pared está en `pared.x`. Para que el borde **derecho** de Kira quede justo ahí,
su `x` tiene que ser `pared.x - kira.w` (la pared menos el ancho de Kira).

Por ejemplo, si la pared está en 400 y Kira mide 40, Kira queda en 360: su borde derecho, en 400.

Va **después** de moverla: primero se mueve, después se revisa y se corrige. Así nunca se ve metida.

El robot va a mantener la flecha derecha 120 cuadros (mucho más de lo que hace falta para llegar).

#### Desafío
Hacé que Kira se frene contra el lado izquierdo de la pared.

#### Pasos
1. Buscá el comentario `/* acá: si se metió en la pared, … */`.
2. Escribí `if (toca(kira, pared)) {`.
3. Adentro, `kira.x = pared.x - kira.w;`. Cerrá la llave.
4. Tocá **Jugar**, caminá contra la pared y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 40, 220, 40, 40 };
    SDL_FRect pared = { 400, 120, 30, 240 };
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 240 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 240 * dt;

        /* acá: si se metió en la pared, dejarla pegada al lado izquierdo de la pared */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 96, 64, 255);
        SDL_RenderFillRect(lapiz, &pared);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
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
cuadros 120
soltar Derecha
cuadros 2
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 360, y 220, ancho 40, alto 40
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
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 40, 220, 40, 40 };
    SDL_FRect pared = { 400, 120, 30, 240 };
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 240 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 240 * dt;

        /* acá: si se metió en la pared, dejarla pegada al lado izquierdo de la pared */
        if (toca(kira, pared)) {
            kira.x = pared.x - kira.w;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 96, 64, 255);
        SDL_RenderFillRect(lapiz, &pared);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
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
Kira llega a la pared y se frena, pegadita. El Atraviesaparedes deja de aplaudir. {mentor} golpea la
pared de la pantalla con el nudillo. —Ahora sí es una pared.

#### Imagen
- Una pantalla con un cuadrado blanco frenado justo contra una pared naranja de ladrillos de píxeles.
- Un Atraviesaparedes, desde la caja de vidrio, deja de aplaudir con cara de fastidio.
- Arcadia golpea la pantalla con el nudillo; Kira y Gheco sonríen.

### Micro-misión R01-N05-P4 · La paleta

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Rebotar en una paleta | if (toca(pelota, paleta)) { vx = -vx; pelota.x = paleta.x + paleta.w; }
recompensa: xp 10, monedas 4
```

#### Escena
{mentor} saca de una caja la paleta blanca de una máquina vieja. —Esta es de la Cancha de las Paletas.
La pelota tiene que rebotar acá, no pasar de largo.

#### Gheco sugiere
La pelota viene hacia la izquierda (`vx` negativa) y la paleta está a la izquierda. Cuando se tocan:
- se le da vuelta la velocidad, `vx = -vx;`, para que vuelva hacia la derecha;
- se la saca de adentro de la paleta: que su borde izquierdo quede justo en el borde derecho de la
  paleta, `pelota.x = paleta.x + paleta.w;`.

Sin la segunda línea, la pelota puede seguir tocando en el cuadro siguiente, darse vuelta otra vez y
quedar temblando adentro de la paleta (el Atraviesaparedes otra vez).

El borde derecho de la ventana ya la hace rebotar. El robot va a dejar pasar 150 cuadros: la pelota
tiene que ir, rebotar en la paleta, volver y rebotar en la pared.

#### Desafío
Hacé que la pelota rebote en la paleta y vuelva hacia la derecha.

#### Pasos
1. Buscá el comentario `/* acá: si la pelota toca la paleta, que rebote hacia la derecha */`.
2. Escribí `if (toca(pelota, paleta)) {`.
3. Adentro, `vx = -vx;` y `pelota.x = paleta.x + paleta.w;`. Cerrá la llave.
4. Tocá **Jugar** y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 40, 180, 14, 120 };
    SDL_FRect pelota = { 400, 230, 14, 14 };
    float vx = -300;
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

        pelota.x += vx * dt;
        if (pelota.x > 640 - 14) {
            vx = -vx;
            pelota.x = 640 - 14;
        }
        /* acá: si la pelota toca la paleta, que rebote hacia la derecha */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
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
cuadros 150
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 467, y 230, ancho 14, alto 14
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
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 40, 180, 14, 120 };
    SDL_FRect pelota = { 400, 230, 14, 14 };
    float vx = -300;
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

        pelota.x += vx * dt;
        if (pelota.x > 640 - 14) {
            vx = -vx;
            pelota.x = 640 - 14;
        }
        /* acá: si la pelota toca la paleta, que rebote hacia la derecha */
        if (toca(pelota, paleta)) {
            vx = -vx;
            pelota.x = paleta.x + paleta.w;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
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
¡Toc! La pelota pega en la paleta y vuelve. Del fondo de la ciudad llega un sonido viejo, como si una
máquina lejana se hubiera despertado un segundo. {mentor} mira hacia la calle. —La Cancha. Te escuchó.

#### Imagen
- Una pantalla con una paleta blanca a la izquierda y una pelota amarilla que acaba de rebotar, con una chispa de luz.
- Arcadia sostiene una paleta de verdad de una máquina vieja y mira hacia la calle, donde a lo lejos parpadea el cartel de neón de la Cancha de las Paletas.
- Kira y Gheco miran hacia el mismo lado.

## R01-N06 · El joystick y el gamepad

```meta
tipo: tema
criatura: glitch
padre: R01-N05
precio: 10
temas: juegos.entrada
```

### Crónica

Kira mira su brazal: en lugar de escudo tiene un control de juego, con su cruz, su palanca y sus botones. Nunca
supo para qué servía. {mentor} lo mira con cariño. —Eso es un **gamepad**. El Vidriero hacía que todas las
máquinas se jugaran con uno. Decía que con el teclado se escribe y con el joystick se juega.

Le enchufa un cable al brazal y lo conecta a una pantalla del Banco de Pruebas. En la pantalla, nada.
Todavía nadie le enseñó a escucharlo.

### Objetivos

Usar un joystick o gamepad (USB o Bluetooth, de cualquier marca): saber cuándo se conecta, leer la cruz y los
botones, la palanca con su **zona muerta**, y el evento de un botón para las acciones de un toque.

### Antes de empezar

El teclado (R01-N02) y el delta time (R01-N04). Para jugar acá con un joystick de verdad, enchufalo y tocá un
botón: el navegador recién lo ve cuando lo usás. Si no tenés, no importa: el robot tiene uno de prueba.

### Explicación

#### Prender la parte de joysticks
Al iniciar SDL se pide también el gamepad, con `|` («y también»):
```c
SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);
```

#### Cuando se conecta uno
Al enchufarlo (o si ya estaba al arrancar) llega el evento `SDL_EVENT_GAMEPAD_ADDED`. Trae su número en
`evento.gdevice.which`, y con ese número se **abre**:
```c
SDL_Gamepad *pad = NULL;   /* NULL: todavía no hay ninguno */
...
if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
    pad = SDL_OpenGamepad(evento.gdevice.which);
}
```
`SDL_GetGamepadName(pad)` dice cómo se llama. Al terminar, `SDL_CloseGamepad(pad)`.

Un gamepad puede no estar: por eso, antes de leerlo, siempre `if (pad)`.

#### Los botones
SDL los nombra por su **lugar**, no por la letra, porque cada marca les pone otras letras:
| En SDL | Dónde está | Xbox | PlayStation |
|---|---|---|---|
| `SDL_GAMEPAD_BUTTON_SOUTH` | abajo | A | ✕ |
| `SDL_GAMEPAD_BUTTON_EAST` | a la derecha | B | ○ |
| `SDL_GAMEPAD_BUTTON_WEST` | a la izquierda | X | □ |
| `SDL_GAMEPAD_BUTTON_NORTH` | arriba | Y | △ |
| `SDL_GAMEPAD_BUTTON_START` | START | Menu | Options |
| `SDL_GAMEPAD_BUTTON_DPAD_UP`, `_DOWN`, `_LEFT`, `_RIGHT` | la cruz | | |

Hay dos formas de leerlos, como con el teclado:
- **estado**: `SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_RIGHT)` es `true` mientras esté apretado
  (para moverse);
- **evento**: `SDL_EVENT_GAMEPAD_BUTTON_DOWN`, con el botón en `evento.gbutton.button` (para saltar,
  disparar, elegir).

#### La palanca
`SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTX)` dice cuánto está inclinada la palanca izquierda hacia los
costados: de **-32768** (toda a la izquierda) a **32767** (toda a la derecha); 0 es el centro. `LEFTY` es
arriba y abajo (negativo arriba). Dividido por `32767.0f` queda de -1 a 1, y se multiplica por la velocidad:
con la palanca a medias, el personaje va a media velocidad.

Las palancas nunca vuelven exacto al 0: quedan en 0,03 o -0,05 y el personaje se movería solo, despacito. Por
eso se usa una **zona muerta**: si está muy cerca del centro, se toma como 0.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El brazal de Kira", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    float x = 300, y = 220;
    bool escudo = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }
            if (evento.type == SDL_EVENT_GAMEPAD_BUTTON_DOWN && evento.gbutton.button == SDL_GAMEPAD_BUTTON_SOUTH) {
                escudo = !escudo;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

            if (pad) {
                float lx = SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTX) / 32767.0f;
                float ly = SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTY) / 32767.0f;
                if (SDL_fabsf(lx) < 0.2f) lx = 0;
                if (SDL_fabsf(ly) < 0.2f) ly = 0;
                if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_RIGHT)) lx = 1;
                if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_LEFT)) lx = -1;
                if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_DOWN)) ly = 1;
                if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_UP)) ly = -1;
                x = SDL_clamp(x + lx * 240 * dt, 0, 600);
                y = SDL_clamp(y + ly * 240 * dt, 0, 440);
            }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (escudo) {
            SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
            SDL_FRect luz = { x - 8, y - 8, 56, 56 };
            SDL_RenderRect(lapiz, &luz);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, y, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "JOYSTICK: %s", pad ? SDL_GetGamepadName(pad) : "enchufalo y toca un boton");
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    if (pad) {
        SDL_CloseGamepad(pad);
    }
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Muchos juegos se disfrutan más con un control en la mano, y en consolas es lo único que hay. SDL hace que el
mismo código ande con un control de Xbox, de PlayStation, de Nintendo o uno genérico de USB, porque nombra los
botones por su lugar.

### Errores habituales

**Usar el gamepad sin abrirlo.** Sin el `SDL_OpenGamepad`, `pad` sigue en `NULL` y no se lee nada. Y sin el
`if (pad)`, el juego se rompe si nadie enchufó un control.

**Glitch: el personaje que camina solo.** Sin zona muerta, la palanca en reposo da 0,03 y el personaje se
desliza despacito sin que nadie lo toque.

**Olvidar `SDL_INIT_GAMEPAD`.** Sin eso, SDL no avisa cuando se conecta un control.

**Abrir dos veces el mismo.** Sin el `pad == NULL`, cada joystick nuevo reemplaza al anterior.

### Micro-misión R01-N06-P1 · Conectar el brazal

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Abrir un gamepad | SDL_EVENT_GAMEPAD_ADDED · pad = SDL_OpenGamepad(evento.gdevice.which);
recompensa: xp 10, oro 10
```

#### Escena
El brazal de Kira está enchufado a la pantalla, pero en la pantalla dice **JOYSTICK: ninguno**. —La
máquina sabe que algo se conectó —dice {mentor}—, pero nadie le dijo que lo abra.

#### Gheco sugiere
Cuando se conecta un joystick llega un evento de tipo `SDL_EVENT_GAMEPAD_ADDED`. Trae el número del
joystick en `evento.gdevice.which`, y con ese número se **abre**: `SDL_OpenGamepad(número)` devuelve el
joystick listo para leer, y se guarda en la variable `pad`.

`pad` empieza en `NULL`, que significa «todavía no hay ninguno». Se pregunta `pad == NULL` para abrir
solo el primero que se conecte.

El texto de la pantalla ya muestra el nombre con `SDL_GetGamepadName(pad)` cuando `pad` no es `NULL`.

El robot va a enchufar su joystick de prueba.

#### Desafío
Cuando se conecte un joystick, abrilo y guardalo en `pad`.

#### Pasos
1. Buscá el comentario `/* acá: si se conectó un joystick y todavía no hay ninguno, abrirlo */`.
2. Escribí `if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {`.
3. Adentro, `pad = SDL_OpenGamepad(evento.gdevice.which);`. Cerrá la llave.
4. Tocá **Jugar** (si tenés un joystick, enchufalo y tocá un botón) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si se conectó un joystick y todavía no hay ninguno, abrirlo */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "JOYSTICK: %s", pad ? SDL_GetGamepadName(pad) : "ninguno");
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
palanca centro
cuadros 5
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: JOYSTICK: Joystick de prueba
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si se conectó un joystick y todavía no hay ninguno, abrirlo */
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "JOYSTICK: %s", pad ? SDL_GetGamepadName(pad) : "ninguno");
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
La cruz del brazal se ilumina cian y en la pantalla aparece su nombre. Kira lo mira como si lo viera por
primera vez. —No era un escudo —dice—. Era esto.

#### Imagen
- Primer plano del brazal de Kira: un control de juego encendido con la cruz y los botones iluminados cian, con un cable que va a una pantalla del Banco de Pruebas.
- Kira mira el brazal sorprendida; Arcadia sostiene el cable.
- Gheco toca uno de los botones con la cola.

### Micro-misión R01-N06-P2 · La cruz

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Botón apretado | SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_RIGHT) · true mientras se mantiene
recompensa: xp 10, monedas 4
```

#### Escena
—Ahora que lo escucha —dice {mentor}—, que el cuadrado camine con la cruz. Como con las flechas, pero
con el brazal.

#### Gheco sugiere
La cruz del joystick se lee igual que el estado del teclado: se pregunta en cada cuadro si está
apretada. `SDL_GetGamepadButton(pad, botón)` devuelve `true` mientras ese botón esté apretado.

Los botones de la cruz se llaman `SDL_GAMEPAD_BUTTON_DPAD_UP`, `_DOWN`, `_LEFT` y `_RIGHT` (*D-pad* es
el nombre en inglés de la cruz).

La pregunta va adentro del `if (pad)` que ya está: si no hay joystick, no se lee nada.

Por ejemplo, para subir con la cruz:
```c
if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_UP)) {
    y -= 240 * dt;
}
```
El robot va a mantener apretada la cruz a la derecha durante 20 cuadros.

#### Desafío
Hacé que el cuadrado avance a 240 píxeles por segundo mientras la cruz esté apretada a la derecha.

#### Pasos
1. Buscá el comentario `/* acá: si la cruz está apretada a la derecha, … */`, adentro del `if (pad)`.
2. Debajo, escribí `if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_RIGHT)) {`.
3. Adentro, `x += 240 * dt;`. Cerrá la llave.
4. Tocá **Jugar** (con un joystick, si tenés) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    float x = 100;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (pad) {
            /* acá: si la cruz está apretada a la derecha, avanzar 240 píxeles por segundo */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
apretar boton derecha
cuadros 20
soltar boton derecha
cuadros 3
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 182, y 220, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    float x = 100;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (pad) {
            /* acá: si la cruz está apretada a la derecha, avanzar 240 píxeles por segundo */
            if (SDL_GetGamepadButton(pad, SDL_GAMEPAD_BUTTON_DPAD_RIGHT)) {
                x += 240 * dt;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
Kira aprieta la cruz del brazal y el cuadrado avanza en la pantalla. Se ríe sola. {mentor} también.
—Ahora sí tenés las manos libres para pensar.

#### Imagen
- Kira aprieta la cruz de su brazal con el pulgar; en la pantalla, un cuadrado blanco avanza dejando una estela.
- Arcadia sonríe con los brazos cruzados; Gheco imita el gesto con un brazal de juguete.

### Micro-misión R01-N06-P3 · La palanca y la zona muerta

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: glitch
carta: La palanca | SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTX) / 32767.0f · de -1 a 1 · zona muerta
recompensa: xp 10, monedas 4
```

#### Escena
—La cruz es todo o nada —dice {mentor}—. La palanca es más fina: si la inclinás un poquito, vas despacio;
si la llevás al fondo, corrés. Y cuidado con los glitches que caminan solos.

#### Gheco sugiere
`SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTX)` dice cuánto está inclinada la palanca izquierda hacia
los costados: un número de **-32768** (toda a la izquierda) a **32767** (toda a la derecha). En el
centro, 0.

Dividido por `32767.0f` queda de **-1 a 1**, que es más cómodo: con la palanca a medias da 0,5, y
multiplicado por la velocidad, el personaje va a media velocidad.

Debajo ya está la **zona muerta**: las palancas nunca vuelven justo al 0 (quedan en 0,03 o -0,05), y el
personaje caminaría solo. Si da menos de 0,2, se toma como 0.

Por ejemplo, la palanca hacia arriba y abajo es `SDL_GAMEPAD_AXIS_LEFTY` (negativa hacia arriba).

El robot va a llevar la palanca a la derecha durante 30 cuadros.

#### Desafío
Leé la palanca izquierda hacia los costados, de -1 a 1, en la variable `lx`.

#### Pasos
1. Buscá la línea `float lx = 0;   /* acá: la palanca izquierda, de -1 a 1 */`.
2. Cambiá el `0` por `SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTX) / 32767.0f`.
3. Tocá **Jugar** (con un joystick, si tenés) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    float x = 300;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (pad) {
            float lx = 0;   /* acá: la palanca izquierda, de -1 a 1 */
            if (SDL_fabsf(lx) < 0.2f) {
                lx = 0;     /* la zona muerta: si casi no se mueve, es 0 */
            }
            x += lx * 240 * dt;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
palanca derecha
cuadros 30
palanca centro
cuadros 3
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 422, y 220, ancho 40, alto 40
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    float x = 300;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (pad) {
            float lx = SDL_GetGamepadAxis(pad, SDL_GAMEPAD_AXIS_LEFTX) / 32767.0f;
            if (SDL_fabsf(lx) < 0.2f) {
                lx = 0;     /* la zona muerta: si casi no se mueve, es 0 */
            }
            x += lx * 240 * dt;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_FRect kira = { x, 220, 40, 40 };
        SDL_RenderFillRect(lapiz, &kira);
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
El cuadrado acelera y frena como un patinador. Un glitch que caminaba solo por el borde de la pantalla
se queda quieto, sin saber qué hacer. —La zona muerta —dice {mentor}—. Los deja sin trabajo.

#### Imagen
- Primer plano de la palanca del brazal de Kira inclinada hacia la derecha, con un halo cian.
- En la pantalla, un cuadrado blanco que se desliza; un glitch quieto y confundido en una esquina.
- Arcadia señala el glitch; Gheco le hace burla.

### Micro-misión R01-N06-P4 · El escudo de luz

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Evento de un botón | SDL_EVENT_GAMEPAD_BUTTON_DOWN · evento.gbutton.button == SDL_GAMEPAD_BUTTON_SOUTH
recompensa: xp 10, monedas 4
```

#### Escena
—Y el botón de abajo —dice {mentor}—. El que en todas las máquinas era «acción». En tu brazal, prende el
escudo de luz. Una vez lo prende y otra vez lo apaga.

#### Gheco sugiere
Para algo que pasa **una vez por toque** (prender y apagar) se usa el evento, como con el teclado:
`SDL_EVENT_GAMEPAD_BUTTON_DOWN` llega una vez al apretar un botón, y `evento.gbutton.button` dice cuál.

El botón de abajo se llama `SDL_GAMEPAD_BUTTON_SOUTH` (*south* es «sur»): es la **A** en un control de
Xbox y la **✕** en uno de PlayStation. SDL lo nombra por el lugar para que ande con cualquier marca.

Para prender y apagar se usa `escudo = !escudo;`: el `!` lo da vuelta (si era `false` pasa a `true`, y
al revés).

El robot va a apretar el botón A una vez.

#### Desafío
Hacé que el botón A (abajo) prenda y apague el escudo.

#### Pasos
1. Buscá el comentario `/* acá: si apretaron el botón A, prender o apagar el escudo */`.
2. Escribí `if (evento.type == SDL_EVENT_GAMEPAD_BUTTON_DOWN && evento.gbutton.button == SDL_GAMEPAD_BUTTON_SOUTH) {`.
3. Adentro, `escudo = !escudo;`. Cerrá la llave.
4. Tocá **Jugar** (con un joystick, si tenés) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    bool escudo = false;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }

            /* acá: si apretaron el botón A, prender o apagar el escudo */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (escudo) {
            SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        } else {
            SDL_SetRenderDrawColor(lapiz, 90, 90, 110, 255);
        }
        SDL_FRect hexagono = { 270, 190, 100, 100 };
        SDL_RenderFillRect(lapiz, &hexagono);
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
boton A
cuadros 3
```

#### Estado
```
pixel 320 240
```

#### Salida esperada
```
── Estado ──
pixel 320 240: #00e5ff
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMEPAD);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Gamepad *pad = NULL;
    bool escudo = false;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_GAMEPAD_ADDED && pad == NULL) {
                pad = SDL_OpenGamepad(evento.gdevice.which);
            }

            /* acá: si apretaron el botón A, prender o apagar el escudo */
            if (evento.type == SDL_EVENT_GAMEPAD_BUTTON_DOWN && evento.gbutton.button == SDL_GAMEPAD_BUTTON_SOUTH) {
                escudo = !escudo;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        if (escudo) {
            SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        } else {
            SDL_SetRenderDrawColor(lapiz, 90, 90, 110, 255);
        }
        SDL_FRect hexagono = { 270, 190, 100, 100 };
        SDL_RenderFillRect(lapiz, &hexagono);
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
Del brazal de Kira sale un escudo hexagonal de luz cian, el mismo que aparecía en sus sueños. Lo apaga y
lo prende otra vez. {mentor} silba bajito. —Eso no lo hizo el Vidriero. Eso lo trajiste vos.

#### Imagen
- Kira con el brazo extendido: de su brazal con el control sale un escudo de luz hexagonal cian.
- Arcadia la mira con admiración; Gheco se esconde detrás del escudo.
- Detrás, las pantallas del Banco de Pruebas reflejan la luz cian.

## R01-N07 · Texto en pantalla y puntaje

```meta
tipo: tema
criatura: glitch
padre: R01-N06
precio: 10
temas: juegos.estados
usa: prog.salida, prog.cadenas
```

### Crónica

Arriba de la puerta del Banco de Pruebas hay un tablero enorme de récords, con lugar para diez nombres. Está
vacío. —Acá se anotaban los mejores de la ciudad —dice {mentor}—. Una máquina que no muestra el puntaje es
como una carrera sin meta: nadie sabe si ganó.

### Objetivos

Mostrar texto y números en la pantalla (puntos, vidas, mensajes), alinear un texto en el centro y escribirlo
más grande, con la letra de 8 × 8 que trae SDL.

### Antes de empezar

El evento de una tecla (R01-N02). Del curso de C: `printf` con `%d` y `%s`, y `strlen`.

### Explicación

#### La letra de SDL
`SDL_RenderDebugText` escribe con una letra chiquita que trae SDL: cada carácter mide **8 × 8** píxeles. Se
llama *debug* («depurar») porque está pensada para mostrar datos mientras se programa, pero alcanza para un
juego retro. Solo tiene las letras sin tilde (como las máquinas viejas): «GAME OVER», «VIDAS», «R PARA JUGAR».
Para letras con tilde y de cualquier tamaño está **SDL3_ttf**, que viene más adelante.

```c
SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);   /* el color del texto */
SDL_RenderDebugText(lapiz, 10, 10, "HOLA");
```

#### Con números: como `printf`
`SDL_RenderDebugTextFormat` funciona como `printf`: el texto lleva `%d` (entero), `%s` (texto) o `%.1f`
(decimal con uno después de la coma), y los valores van después:
```c
SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d   VIDAS: %d", puntos, vidas);
```

#### Varios renglones
Cada renglón va en su propia llamada, más abajo. Las letras miden 8 de alto: con 12 píxeles entre un renglón y
el otro, queda un poquito de aire.

#### Centrar un texto
Un texto de `n` letras mide `n * 8` píxeles de ancho (`SDL_strlen` cuenta las letras, como `strlen`). Para
centrarlo, empieza medio ancho antes del centro:
```c
float x = (640 - SDL_strlen(texto) * 8) / 2.0f;
```

#### Más grande: la escala
`SDL_SetRenderScale(lapiz, 4, 4)` hace que **todo** lo que se dibuje después salga 4 veces más grande (las
coordenadas también se multiplican por 4). Después se vuelve con `SDL_SetRenderScale(lapiz, 1, 1)`. Así se
hacen los títulos grandes con la misma letra.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El tablero", 640, 480, 0, &ventana, &lapiz);

    int puntos = 0;
    int vidas = 3;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                if (evento.key.key == SDLK_SPACE) puntos += 10;
                if (evento.key.key == SDLK_X && vidas > 0) vidas--;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);
        SDL_RenderDebugTextFormat(lapiz, 10, 22, "VIDAS: %d", vidas);

        if (vidas == 0) {
            /* Un título grande y centrado: con escala 4, la ventana «mide» 160 x 120 */
            const char *texto = "GAME OVER";
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
            SDL_RenderDebugText(lapiz, (160 - SDL_strlen(texto) * 8) / 2.0f, 50, texto);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 460, "ESPACIO: puntos   X: perder una vida");
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

El puntaje, las vidas, el tiempo que queda, el nivel, «PAUSA», «GAME OVER»: todo juego necesita mostrar texto.
Y el puntaje es lo que hace que alguien quiera jugar «una más».

### Errores habituales

**Glitch: el texto tapado.** Si se escribe antes del `SDL_RenderClear`, el fondo lo tapa.

**Olvidar volver la escala.** Después de `SDL_SetRenderScale(lapiz, 4, 4)`, todo sale gigante (y en otro
lugar, porque las coordenadas también se multiplican) hasta que se vuelve a `1, 1`.

**Las tildes.** La letra de SDL no tiene `á` ni `ñ`: salen como un cuadradito. En los textos de pantalla,
sin tilde (o con SDL3_ttf).

**`%d` con un `float`.** `SDL_RenderDebugTextFormat(lapiz, 10, 10, "%d", tiempo)` con `tiempo` decimal muestra
cualquier número: para `float`, `%.0f` o `(int)tiempo`.

### Micro-misión R01-N07-P1 · Las vidas

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Texto con un número | SDL_RenderDebugTextFormat(lapiz, x, y, "VIDAS: %d", vidas); · renglones cada 12 píxeles
recompensa: xp 10, oro 10
```

#### Escena
En la pantalla de prueba dice PUNTOS: 120, en amarillo. —Le falta lo que más miran los jugadores
—dice {mentor}—: cuántas vidas les quedan. Abajo de los puntos.

#### Gheco sugiere
`SDL_RenderDebugTextFormat` es como `printf`, pero escribe en la ventana: el texto lleva `%d` donde va
el número, y el número va después. Antes, dos datos más: dónde (x, y).

Las letras miden 8 píxeles de alto. Si los puntos están en `y = 10`, el renglón siguiente puede ir en
`y = 22` (12 más abajo: 8 de la letra y 4 de aire).

Usa el último color elegido: como los puntos ya pusieron el amarillo, las vidas salen amarillas
también.

Por ejemplo: `SDL_RenderDebugTextFormat(lapiz, 10, 34, "NIVEL: %d", nivel);`.

El robot va a leer los textos de la pantalla.

#### Desafío
Mostrá `VIDAS: 3` (con la variable `vidas`) en `x = 10`, `y = 22`.

#### Pasos
1. Buscá el comentario `/* acá: las vidas, un renglón más abajo */`.
2. Debajo, escribí `SDL_RenderDebugTextFormat(lapiz, 10, 22, "VIDAS: %d", vidas);`.
3. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    int puntos = 120;
    int vidas = 3;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);

        /* acá: las vidas, un renglón más abajo */
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: PUNTOS: 120 | VIDAS: 3
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    int puntos = 120;
    int vidas = 3;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);

        /* acá: las vidas, un renglón más abajo */
        SDL_RenderDebugTextFormat(lapiz, 10, 22, "VIDAS: %d", vidas);
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
VIDAS: 3 aparece debajo de los puntos. En el tablero de récords de la puerta se enciende la primera
línea, vacía, esperando un nombre.

#### Imagen
- Un tablero enorme de récords sobre la puerta del Banco de Pruebas, con diez renglones de luces; el primero se acaba de encender.
- Debajo, una pantalla con dos renglones amarillos en la esquina.
- Kira, Arcadia y Gheco miran el tablero desde abajo.

### Micro-misión R01-N07-P2 · Sumar puntos

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Sumar con una tecla | if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && !evento.key.repeat) puntos += 10;
recompensa: xp 10, monedas 4
```

#### Escena
—Un puntaje que no se mueve es un adorno —dice {mentor}—. Probalo: cada vez que apretás la barra, diez
puntos.

#### Gheco sugiere
Para sumar puntos al apretar la barra espaciadora se usa el **evento** de la tecla (`SDLK_SPACE`), que
llega una vez por toque.

Pero si alguien deja la tecla apretada, el sistema la empieza a **repetir** (como cuando mantenés una
letra mientras escribís) y sumaría sin parar. `evento.key.repeat` vale `true` en esas repeticiones:
con `!evento.key.repeat` se cuentan solo los toques de verdad.

`puntos += 10;` es lo mismo que `puntos = puntos + 10;`.

El texto ya muestra `puntos` en cada cuadro, así que se actualiza solo.

El robot va a apretar la barra tres veces.

#### Desafío
Sumá 10 puntos cada vez que se aprieta la barra espaciadora, sin contar las repeticiones.

#### Pasos
1. Buscá el comentario `/* acá: con la barra espaciadora, 10 puntos más … */`.
2. Escribí `if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && !evento.key.repeat) {`.
3. Adentro, `puntos += 10;`. Cerrá la llave.
4. Tocá **Jugar**, apretá la barra y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    int puntos = 0;
    int vidas = 3;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con la barra espaciadora, 10 puntos más (sin contar las repeticiones) */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 10, 22, "VIDAS: %d", vidas);
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
tecla Espacio
cuadros 2
tecla Espacio
cuadros 2
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
textos: PUNTOS: 30 | VIDAS: 3
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    int puntos = 0;
    int vidas = 3;

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con la barra espaciadora, 10 puntos más (sin contar las repeticiones) */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && !evento.key.repeat) {
                puntos += 10;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 10, 22, "VIDAS: %d", vidas);
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
10, 20, 30. Gheco aprieta la barra con la cola sin parar y {mentor} lo deja, divertida. —Así empiezan
todos los récords: con alguien que no quiere soltar.

#### Imagen
- Gheco salta sobre la barra espaciadora de un teclado viejo; en la pantalla, el puntaje amarillo sube.
- Kira se ríe; Arcadia mira el número con una ceja levantada.

### Micro-misión R01-N07-P3 · GAME OVER en el medio

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Centrar un texto | x = (640 - SDL_strlen(texto) * 8) / 2 · cada letra mide 8
recompensa: xp 10, monedas 4
```

#### Escena
En la pantalla dice GAME OVER, pero pegado a la izquierda, como si se estuviera yendo. —El final se dice
en el medio —dice {mentor}—. Si no, parece un error.

#### Gheco sugiere
El código ya calcula cuánto mide el texto: `SDL_strlen(texto)` cuenta sus letras (como `strlen` del
curso de C) y cada una mide 8 píxeles. «GAME OVER» tiene 9 caracteres (el espacio también cuenta):
mide 72.

Para centrarlo, empieza **medio ancho antes** del centro, como las cajas: `x = (640 - ancho) / 2;`. Lo
que sobra de la ventana se reparte mitad a cada lado.

Por ejemplo, un texto de 100 píxeles en una ventana de 640: `(640 - 100) / 2 = 270`.

El robot va a buscar dónde quedó lo rojo.

#### Desafío
Centrá el texto `GAME OVER` a lo ancho.

#### Pasos
1. Buscá la línea `float x = 0;                           /* acá: centrado */`.
2. Cambiá el `0` por `(640 - ancho) / 2`.
3. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        const char *texto = "GAME OVER";
        float ancho = SDL_strlen(texto) * 8;   /* cada letra mide 8 píxeles */
        float x = 0;                           /* acá: centrado */
        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderDebugText(lapiz, x, 236, texto);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
textos
buscar #e6283c
```

#### Salida esperada
```
── Estado ──
textos: GAME OVER
buscar #e6283c: x 284, y 236, ancho 71, alto 7
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        const char *texto = "GAME OVER";
        float ancho = SDL_strlen(texto) * 8;   /* cada letra mide 8 píxeles */
        float x = (640 - ancho) / 2;
        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderDebugText(lapiz, x, 236, texto);
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
GAME OVER queda justo en el medio. {mentor} hace una mueca. —Nunca me gustó ver ese cartel. Pero bien
puesto, por lo menos, da ganas de jugar otra vez.

#### Imagen
- Una pantalla del Banco de Pruebas con un cartel rojo centrado (sin texto legible, solo las letras de píxeles brillando).
- Arcadia hace una mueca; Kira señala el centro de la pantalla con una regla; Gheco sostiene el otro extremo.

### Micro-misión R01-N07-P4 · Letras grandes

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: La escala | SDL_SetRenderScale(lapiz, 4, 4); … SDL_SetRenderScale(lapiz, 1, 1); · todo sale 4 veces más grande
recompensa: xp 10, monedas 4
```

#### Escena
—Así no lo ve nadie desde la calle —dice {mentor}, y se aleja hasta la puerta—. Las máquinas del
Vidriero ponían el GAME OVER enorme. Cuatro veces más grande.

#### Gheco sugiere
La letra de SDL siempre mide 8 × 8. Para agrandarla se cambia la **escala** del lápiz:
`SDL_SetRenderScale(lapiz, 4, 4)` hace que todo lo que se dibuje **después** salga 4 veces más ancho y
4 veces más alto.

Ojo: las coordenadas también se multiplican por 4. Por eso el texto está en `44, 56`: con escala 4
termina en `176, 224` de la ventana. Con la escala puesta, es como si la ventana midiera 160 × 120.

Después del título, el código vuelve a la escala normal con `SDL_SetRenderScale(lapiz, 1, 1)`, para que
el resto salga del tamaño de siempre.

El robot va a buscar dónde quedó lo rojo y cuánto mide.

#### Desafío
Hacé que `GAME OVER` salga 4 veces más grande (y lo de abajo, normal).

#### Pasos
1. Buscá el comentario `/* acá: todo lo que sigue, 4 veces más grande */`.
2. Debajo, escribí `SDL_SetRenderScale(lapiz, 4, 4);`.
3. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        /* acá: todo lo que sigue, 4 veces más grande */
        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderDebugText(lapiz, 44, 56, "GAME OVER");
        SDL_SetRenderScale(lapiz, 1, 1);   /* y vuelve al tamaño normal */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 260, 300, "R para jugar");
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
buscar #e6283c
```

#### Salida esperada
```
── Estado ──
buscar #e6283c: x 176, y 224, ancho 284, alto 28
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        /* acá: todo lo que sigue, 4 veces más grande */
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
        SDL_RenderDebugText(lapiz, 44, 56, "GAME OVER");
        SDL_SetRenderScale(lapiz, 1, 1);   /* y vuelve al tamaño normal */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 260, 300, "R para jugar");
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
El GAME OVER ocupa media pantalla, gordo y rojo, con sus cuadraditos bien marcados. Desde la puerta,
{mentor} levanta el pulgar. —Ese se lee desde la otra cuadra.

#### Imagen
- Una pantalla con un cartel rojo enorme de letras de píxeles grandes (sin texto legible) y un renglón chico blanco debajo.
- Arcadia, lejos, en la puerta del Banco de Pruebas, levanta el pulgar.
- Kira y Gheco, cerca de la pantalla, iluminados de rojo.

## R01-N08 · Imágenes y sprites

```meta
tipo: tema
criatura: fuga_texturas
padre: R01-N07
precio: 10
temas: juegos.sprites
usa: mem.punteros
```

### Crónica

En un estante del Banco de Pruebas hay cuadernos cuadriculados llenos de dibujitos hechos con cuadraditos:
naves, gemas, fantasmas, una chica con un mechón. Son los **sprites** del Vidriero, dibujados a mano, píxel por
píxel. —Las máquinas no ven dibujos —dice {mentor}—. Ven grillas de colores. Cada cuadradito, un número.

Al fondo del estante flota una niebla de imágenes repetidas, todas iguales, apiladas una sobre otra: una
**Fuga de Texturas**. —Esa es de alguien que cargaba el mismo dibujo sesenta veces por segundo.

### Objetivos

Entender qué es un **sprite** y una **textura**: un dibujo hecho de píxeles que se guarda en la placa de video
y se dibuja muchas veces. Armar uno desde una grilla, dibujarlo en cualquier lugar y tamaño, animarlo cambiando
de cuadro y darlo vuelta. Y no crear texturas de más (la Fuga de Texturas).

### Antes de empezar

El texto en pantalla (R01-N07). Del curso de C: arrays de textos (`const char *dibujo[8]`), arrays de dos
dimensiones como fila × columna, y punteros.

### Explicación

#### Sprites y texturas
Un **sprite** es un dibujo chico que se mueve por la pantalla: el personaje, una gema, una bala. Por dentro es
una grilla de píxeles, cada uno con su color.

Para dibujarlo rápido, SDL lo guarda en la placa de video como una **textura** (`SDL_Texture`). Se crea **una
vez**, al principio, y después se dibuja todas las veces que haga falta, en cualquier lugar y de cualquier
tamaño:
```c
SDL_FRect donde = { 100, 200, 64, 64 };       /* dónde y de qué tamaño */
SDL_RenderTexture(lapiz, textura, NULL, &donde);
```
El `NULL` es «la textura entera» (se puede dibujar solo un pedazo, para las hojas con muchos cuadros).

#### De dónde salen
En los juegos de verdad, las texturas salen de **archivos de imagen**: `SDL_LoadBMP("nave.bmp")` lee un BMP, y
la biblioteca **SDL3_image** lee PNG (`IMG_LoadTexture(lapiz, "nave.png")`). En las máquinas que vienen se usan
así. En este nodo los armamos **desde el código**, con una grilla de texto, para ver qué hay adentro: la
función `crear_sprite` recorre la grilla y donde hay una `X` pone el color.

#### Los colores como un número
Cada píxel es un `Uint32` (un entero de 32 bits) con el formato `0xRRGGBBAA`: dos cifras hexadecimales para el
rojo, dos para el verde, dos para el azul y dos para la opacidad. `0xFFDC00FF` es amarillo opaco;
`0x00000000` es transparente (alfa 0: no se ve, y deja ver lo de atrás).

#### Agrandar sin borronear
Un sprite de 8 × 8 dibujado en 64 × 64 se agranda 8 veces. SDL, de entrada, lo **suaviza** (queda borroso).
Para el estilo de píxeles se pide «el más cercano»: `SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST)`.

#### Animar: cambiar de cuadro
Una animación son varios dibujos que se turnan, como un libro de dibujitos. Con el reloj se elige cuál:
```c
int cual = (SDL_GetTicks() / 250) % 2;   /* 0, 1, 0, 1… cambiando cada 250 milisegundos */
```
`SDL_GetTicks() / 250` sube de a uno cada cuarto de segundo, y `% 2` (el resto de dividir por 2) lo deja
en 0 o 1.

#### Darlo vuelta
`SDL_RenderTextureRotated` dibuja la textura girada o en **espejo**: con `SDL_FLIP_HORIZONTAL`, el personaje
mira para el otro lado sin dibujarlo dos veces.

#### La Fuga de Texturas
Cada `SDL_CreateTexture` ocupa memoria de la placa de video. Si se crea una textura adentro del bucle, se
crean 60 por segundo y nunca se devuelven: la memoria crece hasta que el juego se ahoga. Regla: se crean
**antes** del bucle y se destruyen con `SDL_DestroyTexture` **al final**, una por cada una que se creó.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

static const char *ALAS_ARRIBA[8] = {
    "X......X",
    "XX....XX",
    ".XX..XX.",
    "..XXXX..",
    "..XXXX..",
    "...XX...",
    "...XX...",
    "........",
};
static const char *ALAS_ABAJO[8] = {
    "........",
    "...XX...",
    "..XXXX..",
    "..XXXX..",
    ".XX..XX.",
    "XX....XX",
    "X......X",
    "........",
};

static const char *KIRA[8] = {
    "..XXX...",
    ".XXXXX..",
    ".XX.XXXX",
    ".XXXXX..",
    "..XXX...",
    ".XXXXX..",
    ".X...X..",
    "XX...XX.",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Los cuadernos del Vidriero", 640, 480, 0, &ventana, &lapiz);

    /* Las texturas se crean una vez, antes del bucle */
    SDL_Texture *nave[2];
    nave[0] = crear_sprite(lapiz, ALAS_ARRIBA, 0xFFDC00FF);
    nave[1] = crear_sprite(lapiz, ALAS_ABAJO, 0xFFDC00FF);
    SDL_Texture *kira = crear_sprite(lapiz, KIRA, 0xFFFFFFFF);
    float x = 300;
    bool izquierda = false;
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
            if (teclas[SDL_SCANCODE_RIGHT]) { x += 200 * dt; izquierda = false; }
            if (teclas[SDL_SCANCODE_LEFT]) { x -= 200 * dt; izquierda = true; }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        /* La nave aletea: cambia de cuadro cada 250 milisegundos */
        int cual = (SDL_GetTicks() / 250) % 2;
        SDL_FRect arriba = { 288, 80, 64, 64 };
        SDL_RenderTexture(lapiz, nave[cual], NULL, &arriba);

        /* Kira mira hacia donde camina */
        SDL_FRect donde = { x, 300, 64, 64 };
        SDL_RenderTextureRotated(lapiz, kira, NULL, &donde, 0, NULL, izquierda ? SDL_FLIP_HORIZONTAL : SDL_FLIP_NONE);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    /* …y se destruyen al final, una por una */
    SDL_DestroyTexture(nave[0]);
    SDL_DestroyTexture(nave[1]);
    SDL_DestroyTexture(kira);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

### ¿Para qué sirve?

Los personajes, los enemigos, los fondos, las balas y las explosiones de un juego 2D son texturas. Saber que por
dentro son grillas de colores sirve para dibujarlos (el *pixel art*) y para no gastar memoria de más.

### Errores habituales

**Fuga de Texturas: crear adentro del bucle.** `SDL_Texture *t = crear_sprite(…)` adentro del `while` crea una
textura nueva en cada cuadro. Se crean una vez, antes del bucle.

**Olvidar `SDL_DestroyTexture`.** Al terminar, cada textura creada se destruye. En un juego chico no se nota;
en uno que cambia de nivel muchas veces, sí.

**Glitch: el sprite borroso.** Sin `SDL_SCALEMODE_NEAREST`, al agrandarlo se ve como una mancha.

**Glitch: un renglón corto.** Si un renglón del dibujo tiene 7 caracteres en lugar de 8, la función lee un
carácter que no es suyo: el dibujo sale corrido. Todos los renglones, del mismo largo.

### Micro-misión R01-N08-P1 · La gema del cuaderno

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Un sprite | una grilla de píxeles · SDL_RenderTexture(lapiz, textura, NULL, &donde);
recompensa: xp 10, oro 10
```

#### Escena
{mentor} abre un cuaderno del Vidriero en una página con una gema dibujada con cuadraditos. —A esta le
falta un renglón —dice—. El del medio, el más ancho. Se ve que lo borró la humedad.

#### Gheco sugiere
El sprite de la gema está dibujado con texto: es un array de 8 renglones, y cada renglón tiene 8
caracteres. Donde hay una `X` va un píxel cian; donde hay un `.`, nada (transparente). La función
`crear_sprite` recorre esa grilla y arma la **textura**: el dibujo, guardado en la placa de video.

Después se dibuja con `SDL_RenderTexture`, en un rectángulo de 64 × 64: como el dibujo es de 8 × 8,
cada píxel se ve como un cuadrado de 8 × 8.

El renglón 5 está vacío (`........`). La gema es más ancha en el medio: los renglones 4 y 5 van
llenos, de lado a lado.

El robot va a buscar dónde quedó lo cian y mirar un píxel del renglón que falta.

#### Desafío
Completá el renglón que falta: la gema tiene dos renglones anchos en el medio.

#### Pasos
1. Buscá en `GEMA` el renglón `"........",   /* acá: este renglón */`.
2. Cambiá los ocho puntos por ocho `X`: `"XXXXXXXX",`. Tienen que ser 8 justos.
3. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static const char *GEMA[8] = {
    "...XX...",
    "..XXXX..",
    ".XXXXXX.",
    "XXXXXXXX",
    "........",   /* acá: este renglón */
    ".XXXXXX.",
    "..XXXX..",
    "...XX...",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *gema = crear_sprite(lapiz, GEMA, 0x00E5FFFF);   /* cian */

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect donde = { 288, 208, 64, 64 };   /* 8 x 8 dibujado en 64 x 64: cada píxel, un cuadrado de 8 */
        SDL_RenderTexture(lapiz, gema, NULL, &donde);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(gema);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
buscar #00e5ff
pixel 292 244
```

#### Salida esperada
```
── Estado ──
buscar #00e5ff: x 288, y 208, ancho 64, alto 64
pixel 292 244: #00e5ff
```

#### Solución
```c
#include <SDL3/SDL.h>

static const char *GEMA[8] = {
    "...XX...",
    "..XXXX..",
    ".XXXXXX.",
    "XXXXXXXX",
    "XXXXXXXX",
    ".XXXXXX.",
    "..XXXX..",
    "...XX...",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *gema = crear_sprite(lapiz, GEMA, 0x00E5FFFF);   /* cian */

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect donde = { 288, 208, 64, 64 };   /* 8 x 8 dibujado en 64 x 64: cada píxel, un cuadrado de 8 */
        SDL_RenderTexture(lapiz, gema, NULL, &donde);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(gema);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La gema aparece entera, brillando cian, cada cuadradito en su lugar. {mentor} cierra el cuaderno con
cuidado. —Así dibujaba él. Cuadradito por cuadradito.

#### Imagen
- Un cuaderno cuadriculado abierto con una gema dibujada con cuadraditos y, al lado, la misma gema brillando cian en una pantalla.
- Arcadia sostiene el cuaderno con cuidado; Kira compara el dibujo con la pantalla.
- Gheco con un lápiz detrás de la oreja.

### Micro-misión R01-N08-P2 · Una textura, muchas gemas

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Reusar una textura | se crea una vez · se dibuja muchas veces, en otros lugares
recompensa: xp 10, monedas 4
```

#### Escena
—Una gema sola no hace un juego —dice {mentor}—. Pero no hace falta dibujarla de nuevo: la misma figura
sirve para todas.

#### Gheco sugiere
Una textura se crea **una vez** y se puede dibujar **muchas**: cada `SDL_RenderTexture` la dibuja en el
rectángulo que se le pase. Para otra gema, otro rectángulo en otro lugar y otra llamada, con la misma
textura `gema`.

Así trabajan los juegos: una sola textura de «moneda» y cien monedas en el nivel, cada una con su
rectángulo.

Por ejemplo, una gema más chica arriba: `SDL_FRect chica = { 300, 40, 32, 32 };` y
`SDL_RenderTexture(lapiz, gema, NULL, &chica);`.

El robot va a buscar dónde quedó lo cian: si hay dos gemas, ocupa de una a la otra.

#### Desafío
Dibujá la misma gema otra vez, del mismo tamaño, en `x = 476` (misma `y`).

#### Pasos
1. Buscá el comentario `/* acá: la misma gema otra vez, en x 476 */`.
2. Debajo, `SDL_FRect otra = { 476, 208, 64, 64 };`.
3. Y después, `SDL_RenderTexture(lapiz, gema, NULL, &otra);`.
4. Tocá **Jugar** y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static const char *GEMA[8] = {
    "...XX...",
    "..XXXX..",
    ".XXXXXX.",
    "XXXXXXXX",
    "XXXXXXXX",
    ".XXXXXX.",
    "..XXXX..",
    "...XX...",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *gema = crear_sprite(lapiz, GEMA, 0x00E5FFFF);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect donde = { 100, 208, 64, 64 };
        SDL_RenderTexture(lapiz, gema, NULL, &donde);
        /* acá: la misma gema otra vez, en x 476 */
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(gema);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Estado
```
buscar #00e5ff
```

#### Salida esperada
```
── Estado ──
buscar #00e5ff: x 100, y 208, ancho 440, alto 64
```

#### Solución
```c
#include <SDL3/SDL.h>

static const char *GEMA[8] = {
    "...XX...",
    "..XXXX..",
    ".XXXXXX.",
    "XXXXXXXX",
    "XXXXXXXX",
    ".XXXXXX.",
    "..XXXX..",
    "...XX...",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *gema = crear_sprite(lapiz, GEMA, 0x00E5FFFF);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect donde = { 100, 208, 64, 64 };
        SDL_RenderTexture(lapiz, gema, NULL, &donde);
        /* acá: la misma gema otra vez, en x 476 */
        SDL_FRect otra = { 476, 208, 64, 64 };
        SDL_RenderTexture(lapiz, gema, NULL, &otra);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(gema);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
Dos gemas iguales brillan en la pantalla. Gheco intenta agarrar una a través del vidrio. —Son la misma
—le dice {mentor}—. Una sola figura, dos lugares. Como un sello.

#### Imagen
- Una pantalla con dos gemas cian iguales de cuadraditos, a los dos costados.
- Arcadia sostiene un sello de goma con la forma de la gema; Gheco intenta agarrar una gema de la pantalla.
- Kira sonríe.

### Micro-misión R01-N08-P3 · La nave que aletea

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Animar | int cual = (SDL_GetTicks() / 250) % 2; · se turnan dos cuadros
recompensa: xp 10, monedas 4
```

#### Escena
En otra página del cuaderno hay dos dibujos de la misma nave: uno con las alas arriba y otro con las
alas abajo. —Pasalos rápido —dice {mentor}— y la nave vuela.

#### Gheco sugiere
Una animación son varios dibujos que se turnan, como un libro de dibujitos que se pasa rápido. Acá hay
dos texturas guardadas en un array: `cuadros[0]` (alas arriba) y `cuadros[1]` (alas abajo). La
variable `cual` elige cuál se dibuja.

Para que cambie cada 250 milisegundos (cuatro veces por segundo), se usa el reloj:
`(SDL_GetTicks() / 250) % 2`.
- `SDL_GetTicks() / 250` sube de a 1 cada 250 milisegundos: 0, 1, 2, 3, 4…
- `% 2` es el resto de dividir por 2: 0, 1, 0, 1, 0… Justo lo que hace falta.

Con `% 3` se turnarían tres cuadros (0, 1, 2, 0, 1, 2…).

El robot va a dejar pasar 20 cuadros (un poco más de 250 milisegundos) y mirar qué dibujo quedó.

#### Desafío
Hacé que `cual` valga 0 o 1, cambiando cada 250 milisegundos.

#### Pasos
1. Buscá la línea `int cual = 0;   /* acá: 0 o 1, cambiando cada 250 milisegundos */`.
2. Cambiá el `0` por `(SDL_GetTicks() / 250) % 2`.
3. Tocá **Jugar** (tiene que aletear) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static const char *ALAS_ARRIBA[8] = {
    "X......X",
    "XX....XX",
    ".XX..XX.",
    "..XXXX..",
    "..XXXX..",
    "...XX...",
    "...XX...",
    "........",
};
static const char *ALAS_ABAJO[8] = {
    "........",
    "...XX...",
    "..XXXX..",
    "..XXXX..",
    ".XX..XX.",
    "XX....XX",
    "X......X",
    "........",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *cuadros[2];
    cuadros[0] = crear_sprite(lapiz, ALAS_ARRIBA, 0xFFDC00FF);   /* amarillo */
    cuadros[1] = crear_sprite(lapiz, ALAS_ABAJO, 0xFFDC00FF);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        int cual = 0;   /* acá: 0 o 1, cambiando cada 250 milisegundos */
        SDL_FRect donde = { 288, 208, 64, 64 };
        SDL_RenderTexture(lapiz, cuadros[cual], NULL, &donde);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(cuadros[0]);
    SDL_DestroyTexture(cuadros[1]);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 20
```

#### Estado
```
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
buscar #ffdc00: x 288, y 216, ancho 64, alto 48
```

#### Solución
```c
#include <SDL3/SDL.h>

static const char *ALAS_ARRIBA[8] = {
    "X......X",
    "XX....XX",
    ".XX..XX.",
    "..XXXX..",
    "..XXXX..",
    "...XX...",
    "...XX...",
    "........",
};
static const char *ALAS_ABAJO[8] = {
    "........",
    "...XX...",
    "..XXXX..",
    "..XXXX..",
    ".XX..XX.",
    "XX....XX",
    "X......X",
    "........",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *cuadros[2];
    cuadros[0] = crear_sprite(lapiz, ALAS_ARRIBA, 0xFFDC00FF);   /* amarillo */
    cuadros[1] = crear_sprite(lapiz, ALAS_ABAJO, 0xFFDC00FF);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        int cual = (SDL_GetTicks() / 250) % 2;
        SDL_FRect donde = { 288, 208, 64, 64 };
        SDL_RenderTexture(lapiz, cuadros[cual], NULL, &donde);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(cuadros[0]);
    SDL_DestroyTexture(cuadros[1]);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La nave aletea: arriba, abajo, arriba, abajo. {mentor} la sigue con los ojos, como si fuera a salir de
la pantalla. —La Pista de los Biplanos estaba llena de estas.

#### Imagen
- Un cuaderno abierto con dos dibujos de la misma nave amarilla de cuadraditos, alas arriba y alas abajo; en la pantalla de al lado, la nave en pleno aleteo con líneas de movimiento.
- Arcadia la sigue con los ojos; Kira pasa las hojas del cuaderno rápido con el pulgar, como un libro animado.
- Gheco aletea con los brazos.

### Micro-misión R01-N08-P4 · Mirar para el otro lado

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: fuga_texturas
carta: Espejo | SDL_RenderTextureRotated(lapiz, t, NULL, &donde, 0, NULL, SDL_FLIP_HORIZONTAL);
recompensa: xp 10, monedas 4
```

#### Escena
En el cuaderno, la última página: una chica de pelo corto con un mechón. Kira se reconoce. Pero cuando
camina a la izquierda en la pantalla, la figura sigue mirando a la derecha, como si caminara para atrás.
—No la dibujes dos veces —dice {mentor}—. Ponela frente a un espejo.

#### Gheco sugiere
`SDL_RenderTextureRotated` es como `SDL_RenderTexture`, pero puede **girar** el dibujo (el `0` son los
grados) y darlo vuelta en **espejo** (el último dato):
- `SDL_FLIP_NONE`: como está;
- `SDL_FLIP_HORIZONTAL`: espejado de izquierda a derecha;
- `SDL_FLIP_VERTICAL`: de arriba a abajo.

El código ya guarda en `izquierda` si la última flecha fue la izquierda. Solo falta elegir el espejo
según eso, con el operador `? :` del curso de C: `condición ? si_es_verdad : si_es_falso`.

Por ejemplo: `SDL_FlipMode m = cabeza_abajo ? SDL_FLIP_VERTICAL : SDL_FLIP_NONE;`.

Ojo con la **Fuga de Texturas**: la textura de Kira se crea una sola vez, antes del bucle, y se destruye
al final. Dar vuelta el dibujo no crea otra.

El robot va a caminar a la izquierda y mirar dos píxeles del pelo: si mira para el otro lado, cambian.

#### Desafío
Si Kira camina a la izquierda, dibujala en espejo.

#### Pasos
1. Buscá la línea `SDL_FlipMode espejo = SDL_FLIP_NONE;   /* acá: … */`.
2. Cambiá `SDL_FLIP_NONE` por `izquierda ? SDL_FLIP_HORIZONTAL : SDL_FLIP_NONE`.
3. Tocá **Jugar**, caminá para los dos lados y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

static const char *KIRA[8] = {
    "..XXX...",
    ".XXXXX..",
    ".XX.XXXX",
    ".XXXXX..",
    "..XXX...",
    ".XXXXX..",
    ".X...X..",
    "XX...XX.",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *kira = crear_sprite(lapiz, KIRA, 0xFFFFFFFF);
    float x = 300;
    bool izquierda = false;
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
        if (teclas[SDL_SCANCODE_RIGHT]) { x += 200 * dt; izquierda = false; }
        if (teclas[SDL_SCANCODE_LEFT]) { x -= 200 * dt; izquierda = true; }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect donde = { x, 208, 64, 64 };
        SDL_FlipMode espejo = SDL_FLIP_NONE;   /* acá: si va a la izquierda, dado vuelta */
        SDL_RenderTextureRotated(lapiz, kira, NULL, &donde, 0, NULL, espejo);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(kira);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Eventos
```
cuadros 3
apretar Izquierda
cuadros 30
soltar Izquierda
cuadros 3
```

#### Estado
```
buscar #ffffff
pixel 218 212
pixel 242 212
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 198, y 208, ancho 64, alto 64
pixel 218 212: #140c28
pixel 242 212: #ffffff
```

#### Solución
```c
#include <SDL3/SDL.h>

static const char *KIRA[8] = {
    "..XXX...",
    ".XXXXX..",
    ".XX.XXXX",
    ".XXXXX..",
    "..XXX...",
    ".XXXXX..",
    ".X...X..",
    "XX...XX.",
};

/* Arma una textura de 8 x 8 a partir de un dibujo: 'X' es del color, '.' es transparente. */
static SDL_Texture *crear_sprite(SDL_Renderer *lapiz, const char *dibujo[8], Uint32 color)
{
    Uint32 pixeles[8 * 8];
    for (int fila = 0; fila < 8; fila++) {
        for (int col = 0; col < 8; col++) {
            pixeles[fila * 8 + col] = dibujo[fila][col] == 'X' ? color : 0x00000000;
        }
    }
    SDL_Texture *t = SDL_CreateTexture(lapiz, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 8, 8);
    SDL_UpdateTexture(t, NULL, pixeles, 8 * sizeof(Uint32));
    SDL_SetTextureScaleMode(t, SDL_SCALEMODE_NEAREST);   /* que se vean los cuadraditos, sin borronear */
    return t;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_Texture *kira = crear_sprite(lapiz, KIRA, 0xFFFFFFFF);
    float x = 300;
    bool izquierda = false;
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
        if (teclas[SDL_SCANCODE_RIGHT]) { x += 200 * dt; izquierda = false; }
        if (teclas[SDL_SCANCODE_LEFT]) { x -= 200 * dt; izquierda = true; }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_FRect donde = { x, 208, 64, 64 };
        SDL_FlipMode espejo = izquierda ? SDL_FLIP_HORIZONTAL : SDL_FLIP_NONE;
        SDL_RenderTextureRotated(lapiz, kira, NULL, &donde, 0, NULL, espejo);
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyTexture(kira);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
```

#### Al superarla
La Kira de cuadraditos se da vuelta al cambiar de dirección. La Kira de verdad se queda mirando la
pantalla un rato largo. —El Vidriero me dibujó —dice bajito—. Antes de que yo llegara.

{mentor} no contesta. Pero guarda el cuaderno en el bolsillo del chaleco, cerca del corazón.

#### Imagen
- Un cuaderno abierto en una página con una chica de pelo corto y un mechón dibujada con cuadraditos.
- En la pantalla, la misma figura blanca mirando hacia la izquierda.
- Kira mira la pantalla muy seria; Arcadia guarda el cuaderno en el bolsillo del chaleco; al fondo del estante, una niebla de imágenes repetidas (la Fuga de Texturas) se disipa.

## R01-N09 · Sonido

```meta
tipo: tema
criatura: glitch
padre: R01-N08
precio: 10
temas: juegos.sonido
usa: prog.matematica-azar, mem.dinamica
```

### Crónica

En el Banco de Pruebas todo se mueve, pero nada suena. {mentor} abre un cajón lleno de parlantes de todos los
tamaños, desde uno como una moneda hasta uno como una rueda. —Esta ciudad tenía ruido —dice—. Pitidos,
campanas, explosiones de mentira. Cuando se apagó, lo primero que noté fue el silencio.

### Objetivos

Entender qué es el sonido digital (muestras, frecuencia, volumen), abrir el parlante con SDL3 y hacer sonar
pitidos: al arrancar, al apretar una tecla y cuando algo choca.

### Antes de empezar

El delta time y los rebotes (R01-N04). Del curso de C: arrays, `malloc` y `free`. Para escucharlo, subí el
volumen de la compu: el sonido arranca cuando tocás **Jugar** (los navegadores no dejan sonar sin que toques algo).

### Explicación

#### El sonido es una onda
Un parlante suena porque una membrana va y viene muy rápido y empuja el aire. Cuántas veces por segundo va y
viene es la **frecuencia**, en **hertz** (Hz): 440 Hz es la nota *la*; más hertz, más agudo; menos, más grave.
Cuánto se mueve es el **volumen**.

#### Muestras
La compu no guarda la onda entera: guarda cuánto está corrida la membrana en muchos momentos, una **muestra**
por momento. La calidad de un CD son **44 100 muestras por segundo**. Cada muestra es un número de **-1 a 1**
(0 es la membrana en reposo).

Para hacer un pitido de 440 Hz se calcula cada muestra con un **seno**, la curva que sube y baja suave:
```c
onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * 440 * t);   /* t: en qué segundo cae la muestra i */
```
El `0.2f` es el volumen (un quinto del máximo: un pitido al máximo aturde).

Medio segundo de sonido son `44100 * 0.5 = 22050` muestras: un array de 22 050 `float`. Por eso se pide con
`SDL_malloc` (memoria dinámica, como `malloc`) y se devuelve con `SDL_free` después de mandarlo.

#### El parlante: un stream de audio
```c
SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);
SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* float, 1 canal (mono), 44100 por segundo */
SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
SDL_ResumeAudioStreamDevice(parlante);                 /* arranca en pausa: hay que darle play */
```
Un **stream** es una fila: lo que se manda con `SDL_PutAudioStreamData` se pone al final y suena en orden.
Al terminar, `SDL_DestroyAudioStream(parlante)`.

#### Y los archivos de sonido
En los juegos de verdad, los sonidos salen de archivos: `SDL_LoadWAV` lee un WAV, y la biblioteca
**SDL3_mixer** lee OGG y MP3 y mezcla varios a la vez (la música de fondo con los efectos). Las máquinas que
vienen los usan. En este nodo los fabricamos con matemática para ver qué hay adentro.

### Código de ejemplo

```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("El cajón de los parlantes", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                /* Una escala: cada número, una nota */
                if (evento.key.key == SDLK_1) pitido(parlante, 262, 0.25f);   /* do */
                if (evento.key.key == SDLK_2) pitido(parlante, 294, 0.25f);   /* re */
                if (evento.key.key == SDLK_3) pitido(parlante, 330, 0.25f);   /* mi */
                if (evento.key.key == SDLK_4) pitido(parlante, 349, 0.25f);   /* fa */
                if (evento.key.key == SDLK_5) pitido(parlante, 392, 0.25f);   /* sol */
                if (evento.key.key == SDLK_6) pitido(parlante, 440, 0.25f);   /* la */
                if (evento.key.key == SDLK_7) pitido(parlante, 494, 0.25f);   /* si */
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 200, 236, "Del 1 al 7: do re mi fa sol la si");
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

El sonido es la mitad de un juego: avisa que agarraste algo, que te pegaron o que se acaba el tiempo, sin que
tengas que mirar. Las primeras máquinas de juegos hacían todos sus sonidos así, con ondas fabricadas: es el
sonido *chiptune* que todavía se usa.

### Errores habituales

**No suena nada.** El stream arranca en pausa: falta `SDL_ResumeAudioStreamDevice(parlante)`. O falta
`SDL_INIT_AUDIO` en el `SDL_Init`. O el volumen de la compu está bajo.

**Un pitido que aturde.** Una muestra de 1 es el máximo. Con `0.2f` alcanza.

**Mandar los bytes mal.** `SDL_PutAudioStreamData` pide cuántos **bytes**, no cuántas muestras: cada `float`
ocupa 4, así que es `muestras * sizeof(float)`.

**Olvidar el `SDL_free`.** Cada pitido pide memoria con `SDL_malloc`; sin devolverla, en un juego que suena
mucho, la memoria crece (el primo de la Fuga de Texturas).

### Micro-misión R01-N09-P1 · El primer pitido

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Hacer sonar | pitido(parlante, 440, 0.5f); · 440 Hz es la nota la · el stream suena en orden
recompensa: xp 10, oro 10
```

#### Escena
{mentor} saca del cajón el parlante más chiquito y lo conecta. —Este era el de la boletería. Hacía
*biip* al encenderse. Despertalo.

#### Gheco sugiere
El parlante ya está abierto y en marcha (`parlante`), y la función `pitido` ya sabe fabricar el sonido:
recibe el parlante, la **frecuencia** (cuántas veces por segundo vibra: más, más agudo) y cuántos
**segundos** dura.

Solo falta **llamarla**. Va antes del bucle, así suena una vez al arrancar:
```c
pitido(parlante, 262, 1.0f);   /* un do, durante un segundo */
```
El `f` del final dice que el número es `float`.

El robot no tiene oídos, pero se da cuenta de si el juego mandó algo al parlante.

#### Desafío
Hacé sonar un pitido de 440 Hz durante medio segundo al arrancar.

#### Pasos
1. Buscá el comentario `/* acá: un pitido de 440 Hz durante medio segundo, al arrancar */`.
2. Debajo, escribí `pitido(parlante, 440, 0.5f);`.
3. Subí el volumen, tocá **Jugar** (tiene que sonar *biip*) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

        SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
        SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
        SDL_ResumeAudioStreamDevice(parlante);
    /* acá: un pitido de 440 Hz durante medio segundo, al arrancar */

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "ESPACIO: pitido");
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

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

        SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
        SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
        SDL_ResumeAudioStreamDevice(parlante);
    /* acá: un pitido de 440 Hz durante medio segundo, al arrancar */
    pitido(parlante, 440, 0.5f);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "ESPACIO: pitido");
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
*Biiip.* El parlante chiquito suena y, a lo lejos, en la boletería, la máquina vieja contesta con el
mismo pitido. {mentor} cierra los ojos. —Ese sonido. Lo extrañaba.

#### Imagen
- Un cajón abierto lleno de parlantes de todos los tamaños; Arcadia sostiene el más chiquito, del que salen ondas de sonido dibujadas como anillos cian.
- Arcadia con los ojos cerrados, emocionada; Kira y Gheco se tapan un oído, sonriendo.

### Micro-misión R01-N09-P2 · Un pitido por tecla

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Sonar al apretar | if (… SDLK_SPACE && !evento.key.repeat) pitido(parlante, 660, 0.1f);
recompensa: xp 10, monedas 4
```

#### Escena
—Un sonido al arrancar está bien —dice {mentor}—. Pero los juegos suenan cuando **hacés** algo. Que la
barra haga *pip*.

#### Gheco sugiere
Igual que para sumar puntos: el **evento** de la barra espaciadora (`SDLK_SPACE`), sin contar las
repeticiones (`!evento.key.repeat`), y adentro, el pitido.

Un pitido **corto** (0,1 segundos) y más **agudo** (660 Hz) suena como un efecto de juego: *pip*. Los
largos y graves suenan a alarma.

El robot va a apretar la barra una vez.

#### Desafío
Con la barra espaciadora, hacé sonar un pitido de 660 Hz de 0,1 segundos.

#### Pasos
1. Buscá el comentario `/* acá: con la barra espaciadora, un pitido … */`.
2. Escribí `if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && !evento.key.repeat) {`.
3. Adentro, `pitido(parlante, 660, 0.1f);`. Cerrá la llave.
4. Tocá **Jugar**, apretá la barra y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con la barra espaciadora, un pitido de 660 Hz de 0.1 segundos */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "ESPACIO: pitido");
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
cuadros 5
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

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: con la barra espaciadora, un pitido de 660 Hz de 0.1 segundos */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && !evento.key.repeat) {
                pitido(parlante, 660, 0.1f);
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "ESPACIO: pitido");
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
*Pip, pip, pip.* Gheco descubre que puede tocar una canción con la barra y no para más. {mentor} se
ríe. —Así empezaron todos los músicos de la ciudad.

#### Imagen
- Gheco con auriculares gigantes toca la barra espaciadora como si fuera un piano; salen notas de luz cian.
- Kira y Arcadia se ríen.

### Micro-misión R01-N09-P3 · Cuántas muestras

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Muestras | 44100 por segundo · muestras = (int)(44100 * segundos)
recompensa: xp 10, monedas 4
```

#### Escena
El parlante grande hace un ruido raro, cortado, como un pitido que no llega a salir. —Le estás mandando
un sonido vacío —dice {mentor}—. Cero pedacitos. Contá bien cuántos hacen falta.

#### Gheco sugiere
La compu guarda el sonido como una lista de números, las **muestras**: cuánto está corrida la membrana
del parlante en cada momento. Se usan **44 100 muestras por cada segundo** de sonido (la calidad de un
CD).

Entonces, para un sonido de `segundos` de duración hacen falta `44100 * segundos` muestras. Como es una
cantidad, tiene que ser entera: se convierte con `(int)`.

Por ejemplo, 2 segundos son `44100 * 2 = 88200` muestras; un décimo de segundo, 4410.

El juego imprime con `SDL_Log` cuántas muestras armó, y el robot lee esa salida.

#### Desafío
Calculá en `muestras` cuántas muestras hacen falta para `segundos` de sonido.

#### Pasos
1. Buscá, en la función `pitido`, la línea `int muestras = 0;   /* acá: cuántas muestras hacen falta */`.
2. Cambiá el `0` por `(int)(44100 * segundos)`.
3. Tocá **Jugar** (abajo tiene que decir cuántas muestras) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = 0;   /* acá: cuántas muestras hacen falta */
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
    SDL_Log("pitido de %d muestras", muestras);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

        SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
        SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
        SDL_ResumeAudioStreamDevice(parlante);
    pitido(parlante, 440, 0.25f);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "ESPACIO: pitido");
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

#### Estado
```
sonido
```

#### Salida esperada
```
pitido de 11025 muestras
── Estado ──
sonido: sí
```

#### Solución
```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
    SDL_Log("pitido de %d muestras", muestras);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

        SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
        SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
        SDL_ResumeAudioStreamDevice(parlante);
    pitido(parlante, 440, 0.25f);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugText(lapiz, 10, 10, "ESPACIO: pitido");
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
El parlante grande suena entero, redondo: un *la* de un cuarto de segundo. {mentor} asiente. —Once mil
veinticinco pedacitos. Ni uno más, ni uno menos.

#### Imagen
- El parlante más grande del cajón, como una rueda, vibrando con una onda cian dibujada en el aire hecha de muchos puntitos.
- Kira cuenta con los dedos; Arcadia sostiene una libreta con cuentas; Gheco mira los puntitos de la onda de cerca.

### Micro-misión R01-N09-P4 · El rebote que suena

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Sonido de choque | en el if del rebote: pitido(parlante, 880, 0.05f);
recompensa: xp 10, monedas 4
```

#### Escena
La pelota amarilla rebota de un lado al otro de la pantalla, en silencio. —En la Cancha de las Paletas
—dice {mentor}— cada rebote hacía *tic*. Sin el *tic*, no parece que choque.

#### Gheco sugiere
El rebote ya está hecho: el `if` que se fija si la pelota tocó un borde le da vuelta la velocidad. Ese
es el momento justo del choque: ahí adentro va el sonido.

Un *tic* es un pitido **muy corto** (0,05 segundos) y **agudo** (880 Hz, un *la* más arriba).

Así se hacen los sonidos de los juegos: se busca el `if` donde pasa la cosa (chocar, agarrar, perder) y
se suma el sonido ahí.

El robot va a dejar pasar 80 cuadros: la pelota llega al borde y rebota.

#### Desafío
Hacé sonar un pitido de 880 Hz de 0,05 segundos en cada rebote.

#### Pasos
1. Buscá el comentario `/* acá: un pitido corto de 880 Hz en cada rebote */`, adentro del `if` del rebote.
2. Debajo, escribí `pitido(parlante, 880, 0.05f);`.
3. Tocá **Jugar** (tic… tic…) y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

        SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
        SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
        SDL_ResumeAudioStreamDevice(parlante);
    float x = 300;
    float vx = 400;
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

        x += vx * dt;
        if (x < 0 || x > 640 - 20) {
            vx = -vx;
            x = SDL_clamp(x, 0, 640 - 20);
            /* acá: un pitido corto de 880 Hz en cada rebote */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, 230, 20, 20 };
        SDL_RenderFillRect(lapiz, &pelota);
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
cuadros 80
```

#### Estado
```
sonido
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
sonido: sí
buscar #ffdc00: x 409, y 230, ancho 20, alto 20
```

#### Solución
```c
#include <SDL3/SDL.h>

/* Arma un pitido: una onda que sube y baja «frecuencia» veces por segundo, durante «segundos». */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        float t = (float)i / 44100;              /* en qué segundo cae esta muestra */
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * t);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Banco de Pruebas", 640, 480, 0, &ventana, &lapiz);

        SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };   /* números con coma, un canal, 44100 por segundo */
        SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
        SDL_ResumeAudioStreamDevice(parlante);
    float x = 300;
    float vx = 400;
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

        x += vx * dt;
        if (x < 0 || x > 640 - 20) {
            vx = -vx;
            x = SDL_clamp(x, 0, 640 - 20);
            /* acá: un pitido corto de 880 Hz en cada rebote */
            pitido(parlante, 880, 0.05f);
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_FRect pelota = { x, 230, 20, 20 };
        SDL_RenderFillRect(lapiz, &pelota);
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
*Tic… tic… tic.* Desde la calle llega otro *tic*, y otro: la Cancha de las Paletas contesta, como un eco.
{mentor} sale corriendo a la puerta. —¡Se despierta! ¡La Cancha se está despertando!

#### Imagen
- La puerta del Banco de Pruebas abierta: afuera, en la calle de neón, el cartel de la Cancha de las Paletas parpadea con cada tic.
- Arcadia corre hacia la puerta; Kira mira la pantalla con la pelota amarilla rebotando y un anillo de sonido en el borde.
- Gheco salta al hombro de Kira.

## R01-N10 · Jefe: Junta las gemas

```meta
tipo: jefe
criatura: fantasma_fotograma
padre: R01-N09
precio: 10
insignia: Sello del Banco de Pruebas
insignia_descripcion: Encendiste tu primer juego entero en Ciudad Arcadia: teclado, delta time, colisiones, azar, texto y un fin con revancha.
temas: juegos.estados
usa: juegos.bucle, juegos.entrada, juegos.colisiones, prog.matematica-azar
```

### Crónica

En el centro del Banco de Pruebas hay una máquina tapada con una lona. {mentor} la destapa: es un gabinete
chico, pintado a mano, con una gema en el costado. —**Junta las gemas** —dice—. El primer juego que hizo el
Vidriero en esta ciudad. Corto, simple y completo. Todo lo que aprendiste en el Banco, junto.

Cuando Kira se acerca, la pantalla se llena de copias borrosas de sí misma, que van rápido y lento a la vez:
el **Fantasma del Fotograma**, el más viejo de todos, vive adentro. —Si lo hacés andar bien, se va —dice
{mentor}—. Si no, se queda para siempre.

### Objetivos

Armar un juego entero y chico con todo lo de la rama: moverse con delta time sin salirse, juntar gemas que
aparecen al azar, un reloj que se acaba, el fin del juego y volver a jugar.

### Antes de empezar

Todo R01: rectángulos, teclado, delta time, colisiones y texto.

### Explicación

#### Un juego completo, aunque sea chico
En Ciudad Arcadia un juego no está terminado hasta que tiene:
1. algo que se **controla** (Kira, con las flechas);
2. un **objetivo** (juntar gemas) y un **puntaje**;
3. un **límite** (10 segundos);
4. un **fin** que se ve (el cartel de FIN);
5. y **volver a jugar** sin cerrar la ventana (la R).

#### Los estados del juego
Un juego cambia de **estado**: jugando, terminado (y más adelante: el menú, la pausa). Acá alcanza con un
`bool terminado`. Según el estado, el mismo bucle hace cosas distintas: mientras se juega, Kira se mueve y el
reloj corre; terminado, todo se queda quieto y se espera la R.

#### El azar
`SDL_rand(n)` da un número entero al azar de **0 a n - 1**. Para que la gema aparezca adentro de la ventana:
`gema.x = SDL_rand(640 - 16)` (16 es su ancho). Y en la `y`, desde 40, para que no tape el puntaje.

#### Un reloj que baja
Con el delta time, el tiempo se descuenta en segundos de verdad: `tiempo -= dt;`. Para mostrarlo entero,
`SDL_ceilf` lo redondea para arriba (con 2,3 segundos muestra 3: el 0 aparece recién cuando se acabó).

#### Volver a jugar
Empezar de nuevo es volver a poner **todo** como al principio: los puntos, el tiempo, las posiciones y el
estado. Si se olvida una variable, la segunda partida arranca rara.

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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && terminado) {
                puntos = 0;
                tiempo = 10;
                terminado = false;
                kira.x = 304;
                kira.y = 400;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (!terminado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
            if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
            if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
            kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
            kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

            if (toca(kira, gema)) {
                puntos++;
                gema.x = SDL_rand(640 - 16);
                gema.y = 40 + SDL_rand(480 - 56);
            }

            tiempo -= dt;
            if (tiempo <= 0) {
                tiempo = 0;
                terminado = true;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 540, 10, "TIEMPO: %d", (int)SDL_ceilf(tiempo));
        if (terminado) {
            SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
            SDL_RenderDebugText(lapiz, 236, 236, "FIN: R PARA JUGAR");
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

Esta es la forma de todos los juegos que vienen: Pong, Arkanoid, Tetris y los demás tienen controles, objetivo,
puntaje, límite, fin y revancha. Cambian las reglas, pero el esqueleto es este.

### Errores habituales

**Fantasma del Fotograma: el reloj sin `dt`.** `tiempo -= 0.016;` anda en tu compu y en otra no. El tiempo se
descuenta con `dt`.

**Seguir jugando después del fin.** Si el movimiento no está adentro del `if (!terminado)`, Kira sigue
juntando gemas con el cartel de FIN puesto.

**La revancha a medias.** Si al apretar R no se vuelve a poner `tiempo = 10`, la partida nueva termina apenas
empieza.

**La gema afuera.** `SDL_rand(640)` puede dar 639: la gema quedaría casi toda afuera. Se resta su ancho.

### Micro-misión R01-N10-P1 · Kira en el tablero

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: atraviesaparedes
carta: Moverse sin salirse | cuatro flechas con dt · SDL_clamp(kira.x, 0, 640 - kira.w)
recompensa: xp 15, monedas 4
```

#### Escena
En la pantalla de Junta las gemas hay un cuadrado blanco abajo y una gema cian arriba. Kira se mueve a
los costados, pero no puede subir. —El Vidriero dejó el juego a medio armar —dice {mentor}—. Como si
supiera que alguien lo iba a terminar.

#### Gheco sugiere
Esto ya lo hiciste por partes. Las flechas izquierda y derecha ya están (con `dt`, a 260 píxeles por
segundo). Faltan:
- **abajo** (`SDL_SCANCODE_DOWN`): `kira.y += 260 * dt;`
- **arriba** (`SDL_SCANCODE_UP`): `kira.y -= 260 * dt;`
- y que no se salga: `kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);` y lo mismo con la `y` y el alto
  (`480 - kira.h`).

`SDL_clamp(valor, mínimo, máximo)` deja el valor entre los dos límites: si se pasó, lo devuelve al
borde.

El robot va a subir un rato largo (Kira tiene que frenar arriba, sin salirse) y después ir a la derecha.

#### Desafío
Agregá las flechas arriba y abajo, y que Kira no se salga de la ventana por ningún lado.

#### Pasos
1. Buscá el comentario `/* acá: arriba y abajo, y que no se salga de la ventana */`.
2. Escribí `if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;` y `if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;`.
3. Después, `kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);` y `kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);`.
4. Tocá **Jugar**, recorré toda la ventana y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
        /* acá: arriba y abajo, y que no se salga de la ventana */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);
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
apretar Arriba
cuadros 120
soltar Arriba
apretar Derecha
cuadros 150
soltar Derecha
cuadros 3
```

#### Estado
```
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
buscar #ffffff: x 608, y 0, ancho 32, alto 32
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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
        /* acá: arriba y abajo, y que no se salga de la ventana */
        if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
        if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
        kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
        kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);
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
Kira recorre todo el tablero y frena firme en cada borde. Las copias borrosas del Fantasma se juntan en
un rincón, nerviosas.

#### Imagen
- Un gabinete chico pintado a mano con una gema en el costado, recién destapado (la lona en el piso).
- En la pantalla, un cuadrado blanco en una esquina y una gema cian; en un rincón, el Fantasma del Fotograma (copias borrosas) nervioso.
- Kira juega con el brazal; Arcadia sostiene la lona; Gheco en el techo del gabinete.

### Micro-misión R01-N10-P2 · Gemas al azar

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
carta: Azar | SDL_rand(n) da de 0 a n - 1 · gema.x = SDL_rand(640 - 16);
recompensa: xp 15, monedas 4
```

#### Escena
Kira llega a la gema y la atraviesa: no pasa nada. —Le falta lo más lindo —dice {mentor}—: que la gema
se escape a otro lugar cada vez que la agarrás. Nunca al mismo. Al azar.

#### Gheco sugiere
Cuando Kira toca la gema (la función `toca` ya está, la de las colisiones):
1. un punto más: `puntos++;`
2. la gema se va a otro lugar **al azar**.

`SDL_rand(n)` da un número entero al azar entre **0 y n - 1**. Para que la gema (16 de ancho) quede
adentro de la ventana: `gema.x = SDL_rand(640 - 16);`. En la `y`, que empiece en 40 para no tapar el
puntaje: `gema.y = 40 + SDL_rand(480 - 56);`.

Acá no hace falta un `bool agarrada` como en las colisiones: la gema se va a otro lugar, así que en el
cuadro siguiente ya no se tocan.

El robot juega con un azar fijo (siempre sale la misma serie), para poder comprobarlo. Va a subir hasta
la gema.

#### Desafío
Si Kira toca la gema: un punto más y la gema a otro lugar al azar, adentro de la ventana.

#### Pasos
1. Buscá el comentario `/* acá: si toca la gema, un punto y la gema a otro lugar al azar */`.
2. Escribí `if (toca(kira, gema)) {`.
3. Adentro: `puntos++;`, `gema.x = SDL_rand(640 - 16);` y `gema.y = 40 + SDL_rand(480 - 56);`. Cerrá la llave.
4. Tocá **Jugar**, juntá algunas y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
        if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
        kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
        kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

        /* acá: si toca la gema, un punto y la gema a otro lugar al azar */

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);
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
apretar Arriba
cuadros 80
soltar Arriba
cuadros 3
```

#### Estado
```
textos
buscar #00e5ff
```

#### Salida esperada
```
── Estado ──
textos: GEMAS: 1
buscar #00e5ff: x 170, y 184, ancho 16, alto 16
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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
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
        if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
        if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
        if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
        kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
        kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

        /* acá: si toca la gema, un punto y la gema a otro lugar al azar */
        if (toca(kira, gema)) {
            puntos++;
            gema.x = SDL_rand(640 - 16);
            gema.y = 40 + SDL_rand(480 - 56);
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);
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
La gema salta a otro lugar, y a otro, y a otro. GEMAS: 1, 2, 3. El Fantasma del Fotograma se encoge:
le quedan menos copias.

#### Imagen
- La pantalla de Junta las gemas: el cuadrado blanco toca la gema y la gema aparece en otro lugar con un destello; marcador amarillo arriba.
- El Fantasma del Fotograma con menos copias, encogido.
- Kira concentrada; Arcadia mira el marcador; Gheco festeja.

### Micro-misión R01-N10-P3 · Se acaba el tiempo

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Un reloj | tiempo -= dt; · if (tiempo <= 0) { tiempo = 0; terminado = true; }
recompensa: xp 15, monedas 4
```

#### Escena
—Sin límite, cualquiera junta mil —dice {mentor}—. Diez segundos. Y cuando se acaban, se acaban: el
juego se queda quieto y dice FIN.

#### Gheco sugiere
El juego tiene un **estado**: `terminado` (al principio, `false`). Todo lo de jugar (moverse y juntar)
ya está adentro de `if (!terminado)`: cuando termine, se queda quieto solo.

Falta el reloj. `tiempo` empieza en 10 segundos. En cada cuadro se le descuenta lo que duró el cuadro,
**con delta time** (si no, el Fantasma del Fotograma lo acelera en una compu y lo frena en otra):
`tiempo -= dt;`.

Cuando llega a 0 (o se pasa un poquito, `tiempo <= 0`): se deja en 0 justo y se pasa a
`terminado = true;`. El cartel de FIN ya se dibuja cuando `terminado` es `true`.

El robot va a dejar pasar 650 cuadros (un poco más de 10 segundos del reloj de mentira).

#### Desafío
Descontá el tiempo con `dt` y, al llegar a 0, terminá el juego.

#### Pasos
1. Buscá el comentario `/* acá: descontar el tiempo; al llegar a 0, terminado */`.
2. Debajo, `tiempo -= dt;`.
3. Después, `if (tiempo <= 0) {`, con `tiempo = 0;` y `terminado = true;` adentro. Cerrá la llave.
4. Tocá **Jugar**, esperá los 10 segundos y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
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

        if (!terminado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
            if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
            if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
            kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
            kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

            if (toca(kira, gema)) {
                puntos++;
                gema.x = SDL_rand(640 - 16);
                gema.y = 40 + SDL_rand(480 - 56);
            }

            /* acá: descontar el tiempo; al llegar a 0, terminado */
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 540, 10, "TIEMPO: %d", (int)SDL_ceilf(tiempo));
        if (terminado) {
            SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
            SDL_RenderDebugText(lapiz, 236, 236, "FIN: R PARA JUGAR");
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
cuadros 650
```

#### Estado
```
textos
```

#### Salida esperada
```
── Estado ──
textos: GEMAS: 0 | TIEMPO: 0 | FIN: R PARA JUGAR
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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
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

        if (!terminado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
            if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
            if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
            kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
            kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

            if (toca(kira, gema)) {
                puntos++;
                gema.x = SDL_rand(640 - 16);
                gema.y = 40 + SDL_rand(480 - 56);
            }

            /* acá: descontar el tiempo; al llegar a 0, terminado */
            tiempo -= dt;
            if (tiempo <= 0) {
                tiempo = 0;
                terminado = true;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 540, 10, "TIEMPO: %d", (int)SDL_ceilf(tiempo));
        if (terminado) {
            SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
            SDL_RenderDebugText(lapiz, 236, 236, "FIN: R PARA JUGAR");
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
TIEMPO: 3, 2, 1… FIN. La pantalla se queda quieta, con el cartel rojo. El Fantasma del Fotograma, con una
sola copia, mira el reloj que corrió parejo, sin dejarse apurar ni frenar.

#### Imagen
- La pantalla de Junta las gemas quieta con un cartel rojo de fin (sin texto legible) y el reloj en cero.
- El Fantasma del Fotograma, con una sola copia, mira un reloj de arena que cae parejo.
- Kira suelta el control; Arcadia y Gheco miran la pantalla.

### Micro-misión R01-N10-P4 · Revancha

```meta
lugar: El Banco de Pruebas de Arcadia
personajes: Kira, Gheco, Arcadia
criatura: fantasma_fotograma
carta: Volver a jugar | con R y terminado: puntos = 0; tiempo = 10; terminado = false; posiciones de nuevo
recompensa: xp 20, monedas 4
```

#### Escena
Kira mira el FIN y lo primero que dice es: —Una más. {mentor} sonríe de oreja a oreja. —Eso. Eso es lo
que dice todo el mundo. Que la R le dé la revancha.

#### Gheco sugiere
Para volver a jugar hay que dejar **todo** como al principio. Si se olvida algo, la partida nueva
arranca rara (con los puntos de antes, o sin tiempo).

Va en los eventos: si apretaron la R (`SDLK_R`) **y** el juego terminó (`terminado`), se vuelve a poner:
- `puntos = 0;`
- `tiempo = 10;`
- `terminado = false;`
- Kira en su lugar de salida: `kira.x = 304;` y `kira.y = 400;`

Se pregunta `terminado` para que la R no reinicie en medio de una partida.

El robot va a jugar los 10 segundos, apretar la R y dejar pasar unos cuadros.

#### Desafío
Si el juego terminó y se aprieta la R, empezá una partida nueva desde cero.

#### Pasos
1. Buscá el comentario `/* acá: si terminó y apretan la R, empezar de nuevo */`.
2. Escribí `if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && terminado) {`.
3. Adentro: `puntos = 0;`, `tiempo = 10;`, `terminado = false;`, `kira.x = 304;` y `kira.y = 400;`. Cerrá la llave.
4. Tocá **Jugar**, jugá dos partidas y después **Comprobar**.

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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si terminó y apretan la R, empezar de nuevo */
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (!terminado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
            if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
            if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
            kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
            kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

            if (toca(kira, gema)) {
                puntos++;
                gema.x = SDL_rand(640 - 16);
                gema.y = 40 + SDL_rand(480 - 56);
            }

            tiempo -= dt;
            if (tiempo <= 0) {
                tiempo = 0;
                terminado = true;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 540, 10, "TIEMPO: %d", (int)SDL_ceilf(tiempo));
        if (terminado) {
            SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
            SDL_RenderDebugText(lapiz, 236, 236, "FIN: R PARA JUGAR");
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
apretar Arriba
cuadros 80
soltar Arriba
cuadros 600
tecla R
cuadros 30
```

#### Estado
```
textos
buscar #ffffff
```

#### Salida esperada
```
── Estado ──
textos: GEMAS: 0 | TIEMPO: 10
buscar #ffffff: x 304, y 400, ancho 32, alto 32
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
    SDL_CreateWindowAndRenderer("Junta las gemas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect kira = { 304, 400, 32, 32 };
    SDL_FRect gema = { 312, 100, 16, 16 };
    int puntos = 0;
    float tiempo = 10;      /* segundos que quedan */
    bool terminado = false;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si terminó y apretan la R, empezar de nuevo */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && terminado) {
                puntos = 0;
                tiempo = 10;
                terminado = false;
                kira.x = 304;
                kira.y = 400;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        if (!terminado) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_RIGHT]) kira.x += 260 * dt;
            if (teclas[SDL_SCANCODE_LEFT]) kira.x -= 260 * dt;
            if (teclas[SDL_SCANCODE_DOWN]) kira.y += 260 * dt;
            if (teclas[SDL_SCANCODE_UP]) kira.y -= 260 * dt;
            kira.x = SDL_clamp(kira.x, 0, 640 - kira.w);
            kira.y = SDL_clamp(kira.y, 0, 480 - kira.h);

            if (toca(kira, gema)) {
                puntos++;
                gema.x = SDL_rand(640 - 16);
                gema.y = 40 + SDL_rand(480 - 56);
            }

            tiempo -= dt;
            if (tiempo <= 0) {
                tiempo = 0;
                terminado = true;
            }
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &gema);
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderFillRect(lapiz, &kira);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "GEMAS: %d", puntos);

        SDL_RenderDebugTextFormat(lapiz, 540, 10, "TIEMPO: %d", (int)SDL_ceilf(tiempo));
        if (terminado) {
            SDL_SetRenderDrawColor(lapiz, 230, 40, 60, 255);
            SDL_RenderDebugText(lapiz, 236, 236, "FIN: R PARA JUGAR");
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
R: GEMAS: 0, TIEMPO: 10, y Kira otra vez abajo. Juega otra, y otra. El Fantasma del Fotograma se
deshace en un último parpadeo y, donde estaba, la pantalla muestra un dibujo nuevo: **otro pedazo del
mapa del Vidriero**. Este tiene una torre que no para de crecer.

{mentor} lo mira mucho rato. —Ese lugar existe —dice—. Pero queda lejos todavía. Primero, la Cancha:
ya te está llamando.

#### Imagen
- El gabinete de Junta las gemas encendido a pleno, con luces en los costados; en la pantalla, un pedazo de mapa antiguo con una torre muy alta.
- El Fantasma del Fotograma se deshace en un último parpadeo de copias.
- Kira con los brazos en alto; Arcadia mira el mapa muy seria; Gheco abraza el gabinete.
