PLANTILLA = r'''
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
    //@ n3+
    float reloj = 0;        /* el tiempo juntado desde que bajó */
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    //@ end
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            //@ n4: acá: las flechas de los costados mueven la pieza una columna
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT) {
                    px++;
                }
            }
            //@ end
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        //@ n3: acá: juntar el tiempo y, cada «caida» segundos, bajar una fila
        reloj += dt;
        if (reloj >= caida) {
            reloj -= caida;
            py++;
        }
        //@ end

        SDL_SetRenderDrawColor(lapiz, 12, 12, 20, 255);
        SDL_RenderClear(lapiz);
        //@ n1: acá: dibujar el pozo: una celda por cada casilla del tablero
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
        //@ end
        //@ n2: acá: dibujar la pieza: un cuadrado por cada 1 de la cajita
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (pieza[f][c] == 1) {
                    SDL_FRect bloque = { OX + (px + c) * CELDA, (py + f) * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        //@ end
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
    codigo='R05-N01', titulo='El pozo y la pieza', criatura='fantasma_fotograma', padre='R04-N05',
    lugar='La Torre que no para',
    temas='col.matrices', usa='juegos.bucle, juegos.entrada, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    El quinto pedazo de mapa lleva al borde de la ciudad, donde una torre altísima se pierde entre las nubes. No tiene
    puerta: tiene una máquina en la base, con la pantalla angosta y alta como un pozo. Desde arriba, muy de vez en
    cuando, cae un bloque de colores y se acomoda en la torre con un *clonc*. —La Torre que no para —dice {mentor}—.
    El Vidriero la hizo para jugar a apilar. Hace años que está trabada: los bloques caen solos, sin nadie que los
    acomode. Si la torre se llena sin orden, se tapa. Y en la pantalla, una pieza cae una vez a toda velocidad y otra
    vez despacito: el **Fantasma del Fotograma** anda por acá.
    ''',
    objetivos='''
    Dibujar el **pozo** del Tetris recorriendo una **matriz** con dos `for`, guardar la **pieza** que cae en una cajita
    de 4 × 4, hacerla **bajar de a una fila** con un reloj y moverla a los costados con las **flechas**.
    ''',
    antes='''
    Toda la escalera hasta acá. De R04: la grilla, el reloj que hace avanzar «cada tanto» (N01). De R03: la pared en
    un arreglo (N03).
    ''',
    explicacion='''
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
    ''',
    para_que='''
    Las matrices están en todos los juegos de tablero: el ta-te-tí, el buscaminas, el ajedrez, el laberinto del
    Pac-Man y los mapas de los juegos de plataformas, que se arman casilla por casilla.
    ''',
    errores='''
    **Dar vuelta fila y columna.** `tablero[f][c]`: primero la fila (la `y`), después la columna (la `x`). Al dibujar es
    al revés: la `x` sale de la columna (`OX + c * CELDA`) y la `y` de la fila (`f * CELDA`).

    **Olvidarse de `OX`.** Sin sumarlo, el pozo queda pegado al borde izquierdo de la ventana.

    **Usar `<=` en el `for`.** La última fila es la 19, no la 20: `f < FILAS`. Con `<=` se lee una fila que no existe.

    **Bajar en cada cuadro.** Sin el reloj, la pieza cruza el pozo en un tercio de segundo: es el Fantasma del
    Fotograma.
    ''',
    misiones=[
        dict(titulo='El pozo de la torre',
             carta='Matriz | for f hasta FILAS · for c hasta COLS · celda en (OX + c * CELDA, f * CELDA) · vacía: casi negra',
             escena='''
             {mentor} limpia la pantalla de la máquina con la manga: está toda negra. —Ahí había un pozo —dice—, diez
             casillas de ancho y veinte de alto. Cada casilla se acordaba de si tenía un bloque o no.
             ''',
             gheco='''
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
             ''',
             desafio='Dibujá el pozo: un cuadrado por cada casilla de la matriz, casi negro si está vacía.',
             pasos=['Buscá el comentario `/* acá: dibujar el pozo: una celda por cada casilla del tablero */`.',
                    'Debajo, escribí los dos `for` de la sugerencia, con el `if` del color y el cuadrado.',
                    'Tocá **Jugar**: tiene que verse el pozo en el medio. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #1c1c2c',
             superarla='''
             En el medio de la pantalla aparece el pozo: doscientas casillas oscuras, parejitas, como las ventanas de un
             edificio de noche. Gheco las cuenta con la cola y se rinde en la treinta y siete.
             ''',
             imagen=['La pantalla angosta y alta de la máquina, con un pozo de casillas oscuras en el medio.',
                     'Arcadia limpia la pantalla con la manga; Kira mira la torre altísima que se pierde entre las nubes.',
                     'Gheco, sentado arriba de la máquina, cuenta las casillas con la cola, mareado.']),
        dict(titulo='Una pieza en su cajita',
             carta='Pieza | for f hasta 4 · for c hasta 4 · si pieza[f][c] == 1: bloque en (OX + (px + c) * CELDA, (py + f) * CELDA)',
             escena='''
             Un bloque cae desde lo alto de la torre y rebota en el techo de la máquina: *clonc*. Kira lo levanta: son
             cuatro cubitos pegados en forma de T. —Cada pieza tiene cuatro —dice {mentor}—. La máquina la guarda en una
             cajita de cuatro por cuatro: un uno donde hay cubito, un cero donde no.
             ''',
             gheco='''
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
             ''',
             desafio='Dibujá la pieza: un cuadrado violeta por cada 1 de su cajita de 4 × 4.',
             pasos=['Buscá `/* acá: dibujar la pieza: un cuadrado por cada 1 de la cajita */`.',
                    'Debajo, escribí el color y los dos `for` de la sugerencia.',
                    'Tocá **Jugar**: arriba del pozo tiene que verse la T. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #aa50ff',
             superarla='''
             Arriba del pozo aparece una T violeta, quietita, esperando. Kira compara con la pieza de verdad que tiene en
             la mano: es igual. —Cuatro cubitos —dice—, y la cajita es el molde.
             ''',
             imagen=['La pantalla de la máquina con el pozo oscuro y una pieza violeta en forma de T arriba de todo.',
                     'Kira sostiene en la mano una pieza de cuatro cubitos violetas en forma de T, comparándola con la pantalla.',
                     'Arcadia señala la pantalla; Gheco se esconde detrás de la pieza de Kira, curioso.']),
        dict(titulo='Una fila cada medio segundo',
             carta='Reloj | reloj += dt · si reloj >= caida: reloj -= caida y py++ (baja una fila)',
             criatura='fantasma_fotograma',
             escena='''
             La T está quieta arriba del pozo. Desde lo alto de la torre se oye un *clonc*, después otro, cada vez más
             seguido y después más lento. —El Fantasma del Fotograma —dice {mentor}—. Las piezas tienen que caer siempre
             al mismo ritmo: una fila cada medio segundo, en cualquier máquina.
             ''',
             gheco='''
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
             ''',
             desafio='Hacé que la pieza baje una fila cada medio segundo, con un reloj que junta el tiempo.',
             pasos=['Buscá `/* acá: juntar el tiempo y, cada «caida» segundos, bajar una fila */`.',
                    'Debajo, escribí las líneas del reloj de la sugerencia.',
                    'Tocá **Jugar**: la T tiene que bajar a saltitos parejos. Después, **Comprobar**.'],
             eventos='cuadros 100', estado='pixel 300 100',
             superarla='''
             La T baja: *tic*, una fila, *tic*, otra, siempre igual. El Fantasma del Fotograma sopla para apurarla, pero
             el reloj no se deja, y se va flotando torre arriba, enojado.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta en T a mitad del pozo, con rayitas de movimiento hacia abajo.',
                     'Un fantasma redondo y translúcido, borroso, se aleja flotando torre arriba, enojado.',
                     'Kira lleva el ritmo con la mano; Arcadia sonríe; Gheco, sobre la máquina, mueve la cabeza al compás.']),
        dict(titulo='A los costados',
             carta='Flechas | izquierda: px-- · derecha: px++ (una columna por apretada)',
             escena='''
             La T cae siempre por el mismo lugar, derechito. Kira aprieta las flechas, pero la pieza ni se entera.
             —Mientras cae, la movés —dice {mentor}—. Una columna por apretada: ni más ni menos.
             ''',
             gheco='''
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
             ''',
             desafio='Hacé que las flechas de los costados muevan la pieza una columna.',
             pasos=['Buscá `/* acá: las flechas de los costados mueven la pieza una columna */` (en el `while` de los eventos).',
                    'Debajo, escribí el `if` con las dos flechas de la sugerencia.',
                    'Tocá **Jugar**, hacé clic en el juego y mové la T. Después, **Comprobar**.'],
             eventos='tecla Izquierda\ncuadros 2', estado='pixel 253 30',
             superarla='''
             Kira aprieta la flecha y la T se corre una casilla, obediente; otra vez, y otra. Desde la torre se oye un
             *clonc* más contento que los anteriores. Gheco aplaude con la cola.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta en T corrida hacia un costado del pozo, con una flecha.',
                     'Kira aprieta las flechas, concentrada; Arcadia mira la torre, donde cae un bloque de colores.',
                     'Gheco aplaude con la cola, sentado arriba de la máquina.']),
    ],
)
