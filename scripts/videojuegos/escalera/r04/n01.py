PLANTILLA = r'''
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
    //@ n2+
    float reloj = 0;       /* el tiempo juntado desde el último paso */
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    //@ end
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            //@ n3: acá: las flechas cambian hacia dónde va
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }
            }
            //@ end
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        //@ n2: acá: juntar el tiempo y, cada «paso» segundos, avanzar una celda
        reloj += dt;
        if (reloj >= paso) {
            reloj -= paso;
            x += dx;
            y += dy;
        }
        //@ end
        //@ n4: acá: si se sale por un borde, aparece por el de enfrente
        x = (x + COLS) % COLS;
        y = (y + FILAS) % FILAS;
        //@ end

        SDL_SetRenderDrawColor(lapiz, 16, 28, 22, 255);
        SDL_RenderClear(lapiz);
        //@ n1: acá: las líneas de la grilla, una cada CELDA píxeles
        SDL_SetRenderDrawColor(lapiz, 30, 50, 40, 255);
        for (int i = 0; i <= COLS; i++) {
            SDL_RenderLine(lapiz, i * CELDA, 0, i * CELDA, 480);
        }
        for (int j = 0; j <= FILAS; j++) {
            SDL_RenderLine(lapiz, 0, j * CELDA, 640, j * CELDA);
        }
        //@ end
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
'''

NODO = dict(
    codigo='R04-N01', titulo='La grilla y la cabeza', criatura='fantasma_fotograma', padre='R03-N07',
    lugar='El Jardín de la Serpiente',
    temas='col.matrices', usa='juegos.bucle, juegos.entrada, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    El cuarto pedazo de mapa lleva a un jardín escondido detrás de la plaza: canteros de flores de vidrio,
    caminitos de baldosas y, en el medio, una máquina vieja con la pantalla dividida en cuadraditos, como un
    cuaderno de matemática. —El Jardín de la Serpiente —dice {mentor}—. Acá no hay pelotas que rebotan: todo
    se mueve de a un cuadradito, como las piezas de un tablero. Primero el tablero, después la serpiente.
    Entre las flores, algo avanza a los saltos, unas veces rápido y otras lento: el **Fantasma del Fotograma**.
    ''',
    objetivos='''
    Dibujar la **grilla** del jardín con dos `for`, poner la **cabeza** de la serpiente en una celda, hacerla
    **avanzar de a una celda** cada un ratito con un reloj, cambiar la dirección con las **flechas** y que, si se
    sale por un borde, **aparezca por el de enfrente**.
    ''',
    antes='''
    Toda la escalera hasta acá. De R03: la grilla de la pared (N03). De R01: el delta time (N04) y las teclas
    (N02).
    ''',
    explicacion='''
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
    ''',
    para_que='''
    Pensar el mundo en **celdas** es la base del Tetris, del Pac-Man y de los juegos de tablero. Y el reloj que
    junta tiempo para hacer algo «cada tanto» lo vas a usar para los enemigos, las oleadas y las animaciones.
    ''',
    errores='''
    **Mezclar celdas con píxeles.** `x += 20` mueve la cabeza 20 **celdas**, no una. En la grilla se suma de a 1 y
    se multiplica por `CELDA` solo al dibujar.

    **Avanzar en cada cuadro.** Sin el reloj, la serpiente va a 60 celdas por segundo y nadie la puede manejar.

    **`reloj = 0` en lugar de `reloj -= paso`.** Se pierde el tiempo que sobró y la serpiente va un poquito más
    lenta en las compus lentas: es el Fantasma del Fotograma.

    **El resto de un negativo.** En C, `-1 % 32` da `-1`, no 31. Por eso se suma `COLS` antes: `(x + COLS) % COLS`.
    ''',
    misiones=[
        dict(titulo='El tablero del jardín',
             carta='Grilla | for i hasta COLS: línea en x = i * CELDA · for j hasta FILAS: línea en y = j * CELDA',
             escena='''
             {mentor} sopla el polvo de la pantalla: está toda negra, sin una sola línea. —Las máquinas del jardín
             tenían el tablero dibujado, como baldosas —dice—. Treinta y dos de ancho, veinticuatro de alto.
             ''',
             gheco='''
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
             ''',
             desafio='Dibujá la grilla del jardín: una línea cada 20 píxeles, vertical y horizontal.',
             pasos=['Buscá el comentario `/* acá: las líneas de la grilla, una cada CELDA píxeles */`.',
                    'Debajo, escribí el color y los dos `for` de la sugerencia.',
                    'Tocá **Jugar**: tiene que verse el tablero. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #1e3228',
             superarla='''
             La pantalla se llena de cuadraditos verdes, parejitos, como las baldosas del caminito. Gheco salta de una
             baldosa a otra del jardín, contando: —¡Uno, dos, tres…!
             ''',
             imagen=['La pantalla de la máquina del jardín con una grilla de cuadraditos verdes sobre fondo oscuro.',
                     'Arcadia sopla el polvo de la pantalla; Kira mira con curiosidad.',
                     'Gheco salta de baldosa en baldosa en el caminito del jardín, contando con los dedos.']),
        dict(titulo='Un paso cada tanto',
             carta='Reloj | reloj += dt · si reloj >= paso: reloj -= paso y la cabeza avanza una celda',
             criatura='fantasma_fotograma',
             escena='''
             En la pantalla hay un cuadradito verde claro: la cabeza de la serpiente. Pero está quieta, dormida. —La
             serpiente del jardín no corre —dice {mentor}—: da pasitos. Uno cada un ratito, siempre igual.
             ''',
             gheco='''
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
             ''',
             desafio='Hacé que la cabeza avance una celda cada 0,15 segundos, con un reloj que junta el tiempo.',
             pasos=['Buscá `/* acá: juntar el tiempo y, cada «paso» segundos, avanzar una celda */`.',
                    'Debajo, escribí las líneas del reloj de la sugerencia.',
                    'Tocá **Jugar**: la cabeza tiene que avanzar a pasitos. Después, **Comprobar**.'],
             eventos='cuadros 60', estado='buscar #78ff8c',
             superarla='''
             La cabeza avanza: *tic, tic, tic*, un cuadradito por vez, siempre al mismo ritmo. El Fantasma del Fotograma
             trata de apurarla y de frenarla, pero el reloj no se deja. Se va a buscar otra máquina.
             ''',
             imagen=['La pantalla con la grilla verde y un cuadradito verde claro avanzando de celda en celda, con huellas.',
                     'Un fantasma redondo y translúcido, borroso, se aleja entre las flores, aburrido.',
                     'Kira mira la pantalla; Arcadia lleva el ritmo con el pie; Gheco, sobre la máquina, mueve la cabeza al compás.']),
        dict(titulo='Doblar con las flechas',
             carta='Dirección | flecha arriba: dx = 0, dy = -1 · abajo: dy = 1 · izquierda: dx = -1 · derecha: dx = 1',
             escena='''
             La cabeza avanza derecho hasta el borde, como si no tuviera volante. Kira aprieta las flechas, pero la
             serpiente ni se entera. —Vos no la empujás —dice {mentor}—: le decís para dónde mirar.
             ''',
             gheco='''
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
             ''',
             desafio='Hacé que las flechas cambien hacia dónde avanza la cabeza.',
             pasos=['Buscá `/* acá: las flechas cambian hacia dónde va */` (en el `while` de los eventos).',
                    'Debajo, escribí el `if` con las cuatro flechas de la sugerencia.',
                    'Tocá **Jugar**, hacé clic en el juego y doblá con las flechas. Después, **Comprobar**.'],
             eventos='tecla Arriba\ncuadros 40', estado='buscar #78ff8c',
             superarla='''
             Kira aprieta la flecha de arriba y la cabeza dobla, obediente. Después a la izquierda, después abajo: dibuja
             un cuadrado entero en el tablero. Gheco aplaude con la cola.
             ''',
             imagen=['La pantalla con la grilla y el recorrido de la cabeza verde dibujando una esquina, con una flecha.',
                     'Kira aprieta las flechas, concentrada; Arcadia sonríe.',
                     'Gheco aplaude con la cola, sentado arriba de la máquina.']),
        dict(titulo='Del otro lado',
             carta='Dar la vuelta | x = (x + COLS) % COLS · y = (y + FILAS) % FILAS',
             escena='''
             La cabeza llega al borde derecho… y se va de la pantalla. Gheco la busca detrás de la máquina, entre las
             flores. —En el jardín del Vidriero no había cerco —dice {mentor}—: si salías por un lado, entrabas por el
             otro.
             ''',
             gheco='''
             El resto de una división, `%`, sirve para «dar la vuelta». `33 % 32` es 1; `32 % 32` es 0. Si la columna se
             pasa de 31, vuelve a empezar:
             ```c
             x = (x + COLS) % COLS;
             y = (y + FILAS) % FILAS;
             ```
             ¿Por qué `+ COLS`? Porque si la cabeza va para la izquierda y llega a -1, en C `-1 % 32` da -1. Sumando 32
             antes, queda `31 % 32 = 31`: la última columna.

             Va en cada cuadro, después del reloj. El robot va a dejar que la cabeza llegue al borde derecho.
             ''',
             desafio='Hacé que si la cabeza sale por un borde, aparezca por el de enfrente.',
             pasos=['Buscá `/* acá: si se sale por un borde, aparece por el de enfrente */`.',
                    'Debajo, escribí las dos líneas con `%` de la sugerencia.',
                    'Tocá **Jugar** y dejá que llegue al borde. Después, **Comprobar**.'],
             eventos='cuadros 300', estado='buscar #78ff8c',
             superarla='''
             La cabeza se va por la derecha y aparece por la izquierda, como si nada. Gheco sale de atrás de la máquina,
             desconcertado, y la encuentra del otro lado. —Un jardín sin cerco —se ríe Kira.
             ''',
             imagen=['La pantalla con la cabeza verde saliendo por el borde derecho y apareciendo por el izquierdo, con flechas curvas.',
                     'Gheco se asoma por detrás de la máquina, desconcertado.',
                     'Kira se ríe; Arcadia señala el otro lado de la pantalla.']),
    ],
)
