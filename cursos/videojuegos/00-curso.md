# CURSO

```meta
slug: videojuegos
titulo: Videojuegos: Ciudad Arcadia
lenguaje: c
nivel: intermedio
descripcion_corta: Hacé videojuegos de verdad en C con SDL3: del primer cuadrado que se mueve a Pong, Tetris, naves y plataformas.
precio_raiz: 10
dias_abono: 30
destacado: no
proximamente: no
publicado: si
micromisiones_completan: si
requiere: c:R02-N07
```

### Descripción

Aprendé a **hacer videojuegos** en C con **SDL3**, la biblioteca con la que se hicieron cientos de juegos de verdad. Cada juego se escribe acá mismo, se **juega en la página** (con el teclado, el mouse o un joystick) y se puede bajar para correrlo en tu compu, con Linux o con Windows.

Acompañás a **Kira**, la de las Forjas, que ahora es **Forjadora de Mundos**: llegó a **Ciudad Arcadia**, la ciudad de los videojuegos, y la encontró apagada. Cada máquina y cada atracción hay que programarla para que vuelva a andar. Te guía **Arcadia**, la maquinista que se quedó a cuidarla.

Se aprende de a poco: primero la ventana, los colores, el teclado y las colisiones; después, un juego entero por máquina, cada uno completo (menú, partida, puntaje, vidas y volver a jugar): **Pong**, **Arkanoid**, **Snake**, **Tetris**, naves tipo **1942**, un laberinto con fantasmas y uno de **plataformas**.

> Qué hace falta: haber hecho el curso de **C** hasta el jefe de la rama R02 (arrays, textos, structs y punteros). La Clase 0 se prueba igual, sin eso. Para jugar alcanza con este navegador (**Chrome** o **Edge**). Las micro-misiones las comprueba solo el **robot de Arcadia**, que juega tu juego y mira la pantalla.

### Temario

- La ventana, el bucle del juego, los colores y los rectángulos
- El teclado, el mouse y el joystick
- Movimiento con delta time y colisiones
- Texto, imágenes (sprites) y sonido
- Una máquina por juego: Pong, Arkanoid, Snake, Tetris, naves, el laberinto y plataformas

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | crédito | créditos | m | La moneda de Ciudad Arcadia (INSERT COIN): se gana con las micro-misiones que vienen de una misión y abre los nodos del curso. | | curso |
| mentor.name | Arcadia | | f | La maquinista de la ciudad: guía de Ciudad Arcadia. | Aprendiz de Maese Ferrum, como Tesla y Tesela, pero eligió las máquinas que juegan. Cuando el Vidriero se fue y la ciudad se apagó, fue la única que se quedó a cuidarla: por eso la ciudad lleva su nombre. Conoce cada máquina por su ruido. Dice que un juego es un bucle que nunca deja de escuchar. | curso |
| world.region | Ciudad Arcadia | | f | La ciudad de los videojuegos, cuya lengua es C con SDL3. | | curso |
| story.course_intro | Bienvenida a Ciudad Arcadia | | f | | Kira cruzó el portal-vitral otra vez. Ya no es la aprendiz que rompió su espada contra un portón: en las Forjas aprendió a medir cada byte. Ahora despierta en una ciudad de calles de neón apagado, con máquinas en cada esquina y atracciones quietas.<br><br>Soy {mentor}, la maquinista. Esta ciudad la construyó el Vidriero, y se apagó cuando él se fue. Cada máquina guarda un juego, y cada juego hay que **programarlo** para que vuelva a andar. Vos vas a ser su mente: cada micro-misión enciende algo, y las que vienen de una misión te dan créditos para abrir la máquina siguiente. | curso |
| story.branch_completed | ¡Otra máquina encendida! | | f | | Arcadia apoya la oreja contra el gabinete, escucha el zumbido y sonríe. —Esa ya anda sola. Suena como sonaba antes. | curso |
| story.course_completed | ¡Ciudad Arcadia está encendida! | | f | | Todas las luces de la ciudad se prenden a la vez. Arcadia le da a Kira la ficha más vieja que tiene, gastada de tanto uso. —La primera que puso el Vidriero. Ahora es tuya: la ciudad ya tiene otra persona que sabe hacerla andar. | curso |
| beast.glitch | glitch | glitches | m | Un sprite que aparece corrido o parpadea: se dibujó antes de limpiar o con las coordenadas mal. | Los glitches son chispas de colores que se cuelan en la pantalla: un cuadrado que deja rastro, una figura que tiembla, algo que aparece donde no tenía que estar. | curso |
| beast.fantasma_fotograma | Fantasma del Fotograma | Fantasmas del Fotograma | m | El juego va rápido en una compu y lento en otra: se mueve sin delta time. | Un fantasma que acelera y frena el tiempo a su antojo. En una compu rápida, la nave vuela; en una lenta, se arrastra. Se lo vence midiendo cuánto tiempo pasó entre un cuadro y el otro. | curso |
| beast.atraviesaparedes | Atraviesaparedes | Atraviesaparedes | m | La colisión mal calculada: la pelota se mete en el ladrillo. | Una criatura que no respeta los bordes: se mete en las paredes, atraviesa paletas y queda trabada adentro de los ladrillos. | curso |
| beast.bucle_eterno | Bucle Eterno | Bucles Eternos | m | La ventana no responde: un bucle que no lee los eventos. | Una serpiente que se muerde la cola. Mientras da vueltas, la ventana no escucha a nadie: ni el teclado, ni el mouse, ni la cruz de cerrar. | curso |
| beast.fuga_texturas | Fuga de Texturas | Fugas de Texturas | f | La memoria crece porque se cargan texturas en cada cuadro y no se liberan. | Una niebla de imágenes repetidas que llena la memoria de a poco, hasta que la máquina se ahoga. | curso |

## R00-N01 · Clase 0 · La máquina que se enciende

```meta
tipo: raiz
criatura: bucle_eterno
temas: juegos.bucle
usa: prog.bucles, prog.funciones
```

### Crónica

Kira despierta de cara al piso, junto a un vitral apagado. Ya conoce ese vitral: es el mismo portal que la llevó a las Forjas. Pero esto no son las Forjas. Es una **ciudad**: calles con letreros de neón apagados, máquinas de juegos en cada esquina, una vuelta al mundo quieta contra el cielo y una montaña rusa que no se mueve.

En la entrada hay una **boletería** con una ventanita. Del otro lado, una mujer de mono mostaza y chaleco negro, con auriculares al cuello y el pelo rojizo atado, le pega con la palma a una máquina vieja, que no hace nada. —No anda desde que él se fue —dice sin darse vuelta—. Ninguna anda.

Es **{mentor}**, la maquinista. Mira el brazal de Kira, que tiene un control de juego en lugar de escudo, y se le iluminan los ojos. —¿Vos sabés C? Entonces sabés más de lo que creés. Acá cada máquina es un programa. Vamos a encender la primera.

Sobre el hombro de Kira aparece Gheco, con las antiparras puestas. Ya se le notan las ganas de jugar.

### Objetivos

Entender qué es **SDL3** y cómo está hecho cualquier juego: abrir una **ventana**, pintarla de un **color**, y el **bucle del juego**, que escucha lo que pasa (las teclas, la cruz de cerrar), cambia lo que tiene que cambiar y vuelve a dibujar, una y otra vez.

### Antes de empezar

Tenés que saber C hasta structs y punteros (el curso de C hasta el jefe de la rama R02): acá se usan `while`, `if`, funciones, structs y el `&` para pasar la dirección de una variable. Para jugar alcanza con este navegador, **Chrome** o **Edge**: tocá **Jugar** y se abre la ventana del juego en la página (la primera vez baja el compilador y tarda un poco).

### Explicación

#### ¿Qué es SDL3?
**SDL** (*Simple DirectMedia Layer*) es una **biblioteca**: un montón de funciones ya escritas que podés usar desde tu programa, como `printf` viene en `stdio.h`. SDL sabe abrir ventanas, dibujar, leer el teclado, el mouse y los joysticks, y hacer sonar audio. Funciona igual en Linux, Windows, Mac y celulares. La versión de este curso es **SDL3**.

Todas sus funciones empiezan con `SDL_` (`SDL_CreateWindow`, `SDL_RenderClear`…) y se traen con una línea:
```c
#include <SDL3/SDL.h>
```

#### La ventana y el lápiz
Para dibujar hacen falta dos cosas:
- una **ventana** (`SDL_Window`): el rectángulo que aparece en la pantalla, con su título;
- un **renderer** (`SDL_Renderer`): el que dibuja adentro de la ventana. En el curso lo llamamos **lápiz**.

Las dos se crean juntas:
```c
SDL_Window *ventana = NULL;
SDL_Renderer *lapiz = NULL;
SDL_CreateWindowAndRenderer("Mi juego", 640, 480, 0, &ventana, &lapiz);
```
- `"Mi juego"` es el **título** de la ventana.
- `640, 480` es el **tamaño**: 640 píxeles de ancho y 480 de alto. Un **píxel** es cada puntito de la pantalla.
- `0` son opciones (ninguna, por ahora).
- `&ventana` y `&lapiz`: la función **llena** esas dos variables. Por eso se le pasa su dirección con `&`, como con `scanf` en el curso de C.

#### Pintar: elegir el color, limpiar y mostrar
```c
SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);   /* elegir el color del lápiz */
SDL_RenderClear(lapiz);                            /* pintar toda la ventana con ese color */
SDL_RenderPresent(lapiz);                          /* mostrar lo dibujado */
```
Un color se arma con tres números de **0 a 255**: cuánto **rojo**, cuánto **verde** y cuánto **azul** (*RGB*). `0, 0, 0` es negro; `255, 255, 255`, blanco; `255, 0, 0`, rojo puro. El cuarto número es la opacidad (255 = opaco: casi siempre va 255).

Lo que se dibuja **no se ve enseguida**: SDL dibuja en una hoja escondida y recién `SDL_RenderPresent` la muestra entera, de una vez. Así la pantalla no parpadea.

#### El bucle del juego
Un juego no termina después de dibujar una vez: repite tres pasos muchas veces por segundo (unas 60), hasta que alguien lo cierra.

1. **Escuchar**: leer los **eventos**, todo lo que pasó desde la vuelta anterior (una tecla, el mouse, la cruz de cerrar).
2. **Actualizar**: cambiar lo que tiene que cambiar (mover al personaje, sumar puntos).
3. **Dibujar**: limpiar, dibujar todo de nuevo y mostrar.

Cada vuelta del bucle dibuja un **cuadro** (*frame*), como los dibujitos de un libro que se pasan rápido.

```c
bool jugando = true;
while (jugando) {
    SDL_Event evento;
    while (SDL_PollEvent(&evento)) {       /* 1. escuchar: uno por uno */
        if (evento.type == SDL_EVENT_QUIT) {
            jugando = false;               /* tocaron la cruz de la ventana */
        }
    }
    /* 2. actualizar (todavía nada) */
    SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);   /* 3. dibujar */
    SDL_RenderClear(lapiz);
    SDL_RenderPresent(lapiz);
    SDL_Delay(16);                         /* esperar 16 milésimas: unos 60 cuadros por segundo */
}
```
- `SDL_PollEvent(&evento)` saca el próximo evento de la fila y lo copia en `evento`. Devuelve `true` si había uno y `false` si la fila quedó vacía: por eso va en un `while`.
- `evento.type` dice **qué** pasó. `SDL_EVENT_QUIT` es «quieren cerrar la ventana».
- `SDL_Delay(16)` hace esperar 16 milésimas de segundo, para no dibujar más rápido de lo necesario.

Si el bucle **no lee los eventos**, la ventana no escucha a nadie: no se puede cerrar y el sistema dice que «no responde». Ese es el **Bucle Eterno**.

#### Cerrar bien
Al salir del bucle se devuelve todo lo que se pidió, en orden inverso:
```c
SDL_DestroyRenderer(lapiz);
SDL_DestroyWindow(ventana);
SDL_Quit();
return 0;
```

#### Cómo se juega acá
- **Jugar** compila tu código y abre la ventana del juego en la página. Hacé clic en el juego para que el teclado vaya ahí.
- **Comprobar** (en las micro-misiones) lo prueba el **robot de Arcadia**: juega solo, con las teclas que dice la prueba, y mira la pantalla al final (el título, un color, dónde está algo, los textos, si el juego terminó). Lo que vio se compara con lo esperado.
- **Cerrar el juego** es como tocar la cruz de la ventana.

#### Y en tu compu
El mismo archivo compila con SDL3 de verdad (más adelante el curso trae un paquete para bajar con todo listo):
- **Linux:** instalá SDL3 (`sudo apt install libsdl3-dev` en Ubuntu 25.04 o más nuevo) y compilá con
  `gcc -Wall -Wextra -std=c11 main.c -o juego $(pkg-config --cflags --libs sdl3)`; se abre con `./juego`.
- **Windows:** con MSYS2 (el de la Clase 0 de C), en la terminal **UCRT64**: `pacman -S mingw-w64-ucrt-x86_64-sdl3` y
  `gcc -Wall -Wextra -std=c11 main.c -o juego.exe $(pkg-config --cflags --libs sdl3)`; se abre con `juego.exe`.

### Código de ejemplo

```c
/*
 * La Boletería: la primera máquina de Ciudad Arcadia.
 * Abre una ventana violeta y espera a que la cierres.
 */
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);                  /* prender la parte de video de SDL */

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Boletería", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        /* 1. Escuchar */
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        /* 2. Actualizar: todavía no se mueve nada */

        /* 3. Dibujar */
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);     /* violeta */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);     /* amarillo */
        SDL_RenderDebugText(lapiz, 276, 236, "INSERT COIN");
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

Todos los juegos, desde el Pong de 1972 hasta los de ahora, tienen este mismo bucle: escuchar, actualizar, dibujar. Los motores grandes (Unity, Godot, Unreal) lo esconden, pero está ahí adentro. SDL lo deja a la vista: por eso es la mejor forma de entender cómo funciona un juego por dentro. Y SDL no es de juguete: lo usan juegos comerciales, emuladores y hasta Steam.

### Errores habituales

**Bucle Eterno: el bucle no lee los eventos.** La ventana no se puede cerrar y el sistema dice que «no responde». En la página, a los 3 segundos sin dibujar ni leer eventos, el juego se corta solo.
```c
while (jugando) {
    SDL_RenderPresent(lapiz);   /* falta el while (SDL_PollEvent(&evento)) */
}
```

**Glitch: dibujar sin limpiar.** Sin `SDL_RenderClear`, lo de la vuelta anterior queda en la pantalla y las cosas que se mueven dejan rastro.

**Glitch: olvidar `SDL_RenderPresent`.** Se dibuja todo en la hoja escondida, pero nunca se muestra: la ventana queda negra.

**Slime: un color con números de más.** Cada número va de 0 a 255. `SDL_SetRenderDrawColor(lapiz, 300, 0, 0, 255)` no da «más rojo»: el número no entra en un byte y da otro color.

### Micro-misión R00-N01-P1 · La máquina se enciende

```meta
lugar: La Boletería
personajes: Kira, Gheco, Arcadia
carta: Abrir una ventana | SDL_CreateWindowAndRenderer("Título", ancho, alto, 0, &ventana, &lapiz);
recompensa: xp 10, oro 10
```

#### Escena
En la boletería hay una máquina vieja con la pantalla apagada. {mentor} le saca la tapa de atrás. —Adentro tiene su programa, pero perdió el nombre. Una máquina sin nombre no arranca. Ponele el de la ciudad.

#### Gheco sugiere
Este programa ya abre una **ventana**: tocá **Jugar** y la vas a ver arriba de la consola, con un título raro (`????`).

La ventana la abre esta línea:
```c
SDL_CreateWindowAndRenderer("????", 640, 480, 0, &ventana, &lapiz);
```
El primer dato, entre comillas, es el **título** de la ventana: el texto que aparece arriba de todo. Los números `640, 480` son el tamaño en **píxeles** (los puntitos de la pantalla): 640 de ancho y 480 de alto.

Por ejemplo, `SDL_CreateWindowAndRenderer("Hola", 320, 200, 0, &ventana, &lapiz);` abre una ventana más chica que se llama **Hola**.

Cuando termines, tocá **Comprobar**: el robot de Arcadia abre tu juego y lee el título y el tamaño de la ventana.

#### Desafío
Cambiá el título de la ventana por `Ciudad Arcadia`. El tamaño queda igual.

#### Pasos
1. Buscá la línea que dice `SDL_CreateWindowAndRenderer`.
2. Adentro de las comillas dice `????`. Borralo y escribí `Ciudad Arcadia`.
3. No borres las comillas.
4. Tocá **Jugar** para verla, y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("????", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 0, 0, 255);
        SDL_RenderClear(lapiz);
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
ventana
```

#### Salida esperada
```
── Estado ──
ventana: «Ciudad Arcadia» 640x480
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 0, 0, 255);
        SDL_RenderClear(lapiz);
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
La pantalla de la máquina parpadea una vez y se queda prendida, negra. Arriba se lee **Ciudad Arcadia**. {mentor} se ríe sola. —Hace años que no la veía despierta.

#### Imagen
- La entrada de Ciudad Arcadia de noche: una boletería de neón apagado, calles con máquinas de juegos quietas, una vuelta al mundo y una montaña rusa detenidas al fondo, contra el cielo.
- Kira, versión videojuegos (mono oscuro cerrado con líneas cian, visor, auricular, cinturón de herramientas y un brazal con un control de juego), se agacha frente a una máquina vieja con la tapa de atrás abierta.
- Arcadia (pelo rojizo en rodete, auriculares gamer al cuello, mono mostaza cerrado con chaleco negro) sostiene la tapa y señala la pantalla, que acaba de prenderse.
- Gheco, el gecko cian con antiparras, sobre el hombro de Kira.

### Micro-misión R00-N01-P2 · El color de la noche

```meta
lugar: La Boletería
personajes: Kira, Gheco, Arcadia
carta: Colores RGB | SDL_SetRenderDrawColor(lapiz, rojo, verde, azul, 255); · cada número de 0 a 255
recompensa: xp 10, oro 10
```

#### Escena
—Negra no —dice {mentor}—. Las máquinas de la ciudad eran **violetas**, como la noche de acá. El Vidriero decía que el negro es para cuando algo está apagado.

#### Gheco sugiere
Antes de pintar, se elige el **color del lápiz** con `SDL_SetRenderDrawColor`, y después `SDL_RenderClear` pinta **toda** la ventana con ese color.

Un color de pantalla se arma mezclando tres luces: **rojo**, **verde** y **azul** (por eso se llama **RGB**, por *red*, *green* y *blue*). Cada una va de **0** (apagada) a **255** (al máximo):
- `0, 0, 0` es negro (todo apagado).
- `255, 255, 255` es blanco (todo prendido).
- `255, 0, 0` es rojo; `0, 0, 255`, azul.
- `255, 255, 0` es amarillo: en la pantalla, rojo y verde juntos dan amarillo.

En `SDL_SetRenderDrawColor(lapiz, 255, 0, 0, 255);` el primer dato es el lápiz, después vienen rojo, verde y azul, y el último `255` es la opacidad (que tape todo lo de abajo).

El robot va a mirar el color del píxel del medio de la ventana (x 320, y 240).

#### Desafío
Pintá el fondo de violeta: **60** de rojo, **20** de verde y **110** de azul.

#### Pasos
1. Buscá la línea `SDL_SetRenderDrawColor(lapiz, 0, 0, 0, 255);`.
2. Cambiá el primer `0` por `60` (el rojo).
3. Cambiá el segundo `0` por `20` (el verde).
4. Cambiá el tercer `0` por `110` (el azul). El último `255` queda igual.
5. Tocá **Jugar** para verla, y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 0, 0, 255);
        SDL_RenderClear(lapiz);
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
pixel 320 240
```

#### Salida esperada
```
── Estado ──
pixel 320 240: #3c146e
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
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
La pantalla se tiñe de violeta y, por un segundo, el letrero de la boletería parpadea del mismo color. {mentor} levanta la vista hacia la calle. —¿Viste eso? La ciudad te escuchó.

#### Imagen
- Primer plano de la máquina de la boletería con la pantalla violeta encendida; el reflejo violeta en el visor de Kira.
- Arriba, el letrero de neón de la boletería se prende apenas, violeta.
- Arcadia mira el letrero, sorprendida; Gheco aplaude sobre el hombro de Kira.

### Micro-misión R00-N01-P3 · La cruz de la ventana

```meta
lugar: La Boletería
personajes: Kira, Gheco, Arcadia
criatura: bucle_eterno
carta: Cerrar la ventana | if (evento.type == SDL_EVENT_QUIT) { jugando = false; }
recompensa: xp 10, monedas 4
```

#### Escena
Kira quiere apagar la máquina para seguir, pero la pantalla no le hace caso. —Esa es la peor falla que hay —dice {mentor}—. Una máquina que no escucha. La llamamos el **Bucle Eterno**: da vueltas y vueltas y no oye a nadie.

#### Gheco sugiere
En este código el bucle **lee** los eventos con `SDL_PollEvent`, pero no hace nada con ellos: por eso tocar la cruz de la ventana no la cierra. Probalo: tocá **Jugar** y después **Cerrar el juego**.

Cada evento tiene un **tipo**, en `evento.type`. Cuando alguien toca la cruz para cerrar la ventana, llega un evento de tipo `SDL_EVENT_QUIT`. Para que el juego termine hay que preguntar por él y, si llegó, poner `jugando` en `false`:
```c
if (evento.type == SDL_EVENT_QUIT) {
    jugando = false;
}
```
`jugando` es la condición del `while` grande: cuando vale `false`, el bucle termina, se ejecuta lo que está después (cerrar todo) y el programa llega al `return 0`.

El `if` va **adentro** del `while (SDL_PollEvent(&evento))`, donde dice `/* acá */`: así se pregunta por cada evento que llega.

El robot va a tocar la cruz de la ventana y se va a fijar si tu juego **terminó**.

#### Desafío
Hacé que el juego termine cuando tocan la cruz de la ventana.

#### Pasos
1. Buscá el comentario `/* acá: si tocaron la cruz, terminar */`.
2. Debajo, escribí `if (evento.type == SDL_EVENT_QUIT) {`.
3. En la línea siguiente, `jugando = false;`.
4. Cerrá la llave: `}`.
5. Tocá **Jugar**, después **Cerrar el juego** (tiene que decir que terminó), y al final **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            /* acá: si tocaron la cruz, terminar */
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
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
cerrar
cuadros 5
```

#### Estado
```
terminó
```

#### Salida esperada
```
── Estado ──
terminó: sí (devolvió 0)
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            /* acá: si tocaron la cruz, terminar */
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
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
Kira toca la cruz y la máquina se apaga, tranquila, como quien se va a dormir. —Escuchó —dice {mentor}, y le da a Kira la primera ficha de la ciudad: un **crédito**—. Con estos se abren las máquinas. Guardalos.

#### Imagen
- Una serpiente de luz que se muerde la cola, el Bucle Eterno, se deshace en chispas violetas frente a la pantalla de la máquina, que se apaga tranquila.
- Arcadia le da a Kira una ficha dorada que dice INSERT COIN (sin texto legible: solo el brillo de la ficha).
- Gheco mira la ficha con los ojos grandes.

### Micro-misión R00-N01-P4 · La tecla de escape

```meta
lugar: La Boletería
personajes: Kira, Gheco, Arcadia
carta: Una tecla | if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) { … }
recompensa: xp 10, monedas 4
```

#### Escena
—En las máquinas de la ciudad, el botón rojo de abajo siempre fue «salir» —dice {mentor}—. En tu teclado, ese botón es **ESC**. Que la máquina también lo escuche.

#### Gheco sugiere
Apretar una tecla también es un evento. Su tipo es `SDL_EVENT_KEY_DOWN` (*key down*: «tecla abajo», o sea, apretada). Además, el evento dice **qué** tecla fue, en `evento.key.key`. Cada tecla tiene su nombre: `SDLK_ESCAPE` es ESC, `SDLK_SPACE` es la barra espaciadora, `SDLK_A` es la A.

Para preguntar las dos cosas a la vez se usa `&&` («y», del curso de C):
```c
if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
    /* apretaron la barra espaciadora */
}
```
Primero se pregunta si es una tecla, y recién después cuál: si el evento fuera del mouse, `evento.key.key` no tendría sentido.

El robot va a apretar ESC y se va a fijar si tu juego **terminó**.

#### Desafío
Hacé que el juego también termine al apretar ESC.

#### Pasos
1. Buscá el comentario `/* acá: si apretaron ESC, terminar */`.
2. Debajo, escribí `if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) {`.
3. En la línea siguiente, `jugando = false;`, y cerrá la llave con `}`.
4. Tocá **Jugar**, hacé clic en el juego, apretá ESC (tiene que terminar) y después tocá **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si apretaron ESC, terminar */
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
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
tecla Escape
cuadros 5
```

#### Estado
```
terminó
```

#### Salida esperada
```
── Estado ──
terminó: sí (devolvió 0)
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            /* acá: si apretaron ESC, terminar */
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
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
Kira aprieta el botón rojo de la máquina y la pantalla se apaga al instante. {mentor} asiente. —Así se apagaban todas. Un botón, una orden. Te ganaste otro crédito.

#### Imagen
- Primer plano del tablero de la máquina: una palanca y botones de colores, el botón rojo grande abajo, apretado por el dedo de Kira (guante cerrado).
- La pantalla se apaga en una línea de luz violeta.
- Arcadia, al costado, con los brazos cruzados y una sonrisa.

### Micro-misión R00-N01-P5 · INSERT COIN

```meta
lugar: La Boletería
personajes: Kira, Gheco, Arcadia
carta: Texto en pantalla | SDL_RenderDebugText(lapiz, x, y, "texto"); · letras de 8 x 8 píxeles · del color del lápiz
recompensa: xp 15, monedas 4
```

#### Escena
—Falta lo más importante —dice {mentor}, y golpea el vidrio con el nudillo—. Toda máquina que se precie dice **INSERT COIN** en amarillo. Si no, nadie sabe que está esperando.

#### Gheco sugiere
`SDL_RenderDebugText` escribe un texto en la ventana:
```c
SDL_RenderDebugText(lapiz, 100, 50, "HOLA");
```
- `100, 50` es **dónde**: 100 píxeles desde la izquierda y 50 desde arriba. En la pantalla, el punto `0, 0` está **arriba a la izquierda**, y la `y` crece hacia **abajo** (al revés que en matemática).
- Cada letra mide 8 × 8 píxeles.
- El texto sale **del color del lápiz**: antes hay que elegir el color con `SDL_SetRenderDrawColor`.

Ojo con el orden: primero se limpia (`SDL_RenderClear`), después se escribe, y al final se muestra (`SDL_RenderPresent`). Si escribís antes de limpiar, el `SDL_RenderClear` lo tapa.

El robot va a leer los textos de la pantalla y a buscar dónde quedó lo amarillo (`#ffdc00`: 255 de rojo, 220 de verde y 0 de azul, escrito en hexadecimal).

#### Desafío
Escribí `INSERT COIN` en amarillo (255, 220, 0) en el punto x 276, y 236.

#### Pasos
1. Buscá el comentario `/* acá: el cartel amarillo */`, que está después de `SDL_RenderClear`.
2. Debajo, elegí el amarillo: `SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);`.
3. En la línea siguiente, escribí el texto: `SDL_RenderDebugText(lapiz, 276, 236, "INSERT COIN");`.
4. Tocá **Jugar** para verlo, y después **Comprobar**.

#### Código inicial
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
        /* acá: el cartel amarillo */
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
buscar #ffdc00
```

#### Salida esperada
```
── Estado ──
textos: INSERT COIN
buscar #ffdc00: x 277, y 236, ancho 86, alto 7
```

#### Solución
```c
#include <SDL3/SDL.h>

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("Ciudad Arcadia", 640, 480, 0, &ventana, &lapiz);

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_ESCAPE) {
                jugando = false;
            }
        }
        SDL_SetRenderDrawColor(lapiz, 60, 20, 110, 255);
        SDL_RenderClear(lapiz);
        /* acá: el cartel amarillo */
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderDebugText(lapiz, 276, 236, "INSERT COIN");
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
**INSERT COIN** parpadea en amarillo sobre el violeta. Kira mete un crédito por la ranura, casi sin pensarlo, y la máquina hace un *clinc* que se oye en toda la calle. En la pantalla aparece, por un instante, un dibujo que no estaba: **un pedazo de mapa**. {mentor} se queda muy quieta. —Eso lo puso él. El Vidriero.

#### Imagen
- La máquina de la boletería encendida: pantalla violeta con un cartel amarillo brillante (sin texto legible, solo el brillo de las letras).
- Kira mete una ficha dorada por la ranura; de la pantalla sale un destello que dibuja en el aire un pedazo de mapa antiguo, con calles y una torre.
- Arcadia, quieta, mira el mapa con la mano en la boca; Gheco señala el mapa.
