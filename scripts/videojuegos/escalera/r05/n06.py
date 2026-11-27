import motor
import n05

PLANTILLA = motor.crecer(motor.full(n05.PLANTILLA), [
    ('''
    int tipo = 2;   /* qué pieza es: la 2 es la T */''', '''
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    //@ n1+
    int siguiente = SDL_rand(7);   /* la que viene después */
    //@ end'''),
    ('''
    enum Estado estado = MENU;''', '''
    enum Estado estado = MENU;
    float relojTorre = 0;   /* cuánto pasó desde que la Torre empujó escombros */
    float relojNivel = 0;   /* cuánto pasó desde que la Torre se apuró */
    int nivel = 1;'''),
    ('''
                lineas = 0;
                puntos = 0;''', '''
                lineas = 0;
                puntos = 0;
                relojTorre = 0;
                relojNivel = 0;
                nivel = 1;
                caida = 0.5f;'''),
    ('''
                tipo = SDL_rand(7);''', '''
                //@ n1: acá: la pieza nueva es la que estaba esperando, y se elige otra para después
                tipo = siguiente;
                siguiente = SDL_rand(7);
                //@ else
                tipo = SDL_rand(7);
                //@ end'''),
    ('''
        if (reloj >= caida) {''', '''
        //@ n2: acá: cada 10 segundos, la Torre empuja una fila de escombros desde abajo
        if (estado == JUGANDO) {
            relojTorre += dt;
        }
        if (relojTorre >= 10) {
            relojTorre -= 10;
            for (int f = 0; f < FILAS - 1; f++) {      /* todo sube una fila */
                for (int c = 0; c < COLS; c++) {
                    tablero[f][c] = tablero[f + 1][c];
                }
            }
            int hueco = SDL_rand(COLS);                 /* abajo, escombros con un hueco al azar */
            for (int c = 0; c < COLS; c++) {
                tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
            }
            if (py > 0) {
                py--;                                   /* la pieza también sube, para no quedar adentro */
            }
        }
        //@ end
        //@ n3: acá: cada 20 segundos, la Torre se apura: sube el nivel y la pieza cae más rápido
        if (estado == JUGANDO) {
            relojNivel += dt;
        }
        if (relojNivel >= 20) {
            relojNivel -= 20;
            nivel++;
            caida = SDL_max(0.1f, caida * 0.8f);
        }
        //@ end
        if (reloj >= caida) {'''),
    ('''
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);''', '''
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        //@ n3: acá: mostrar el nivel abajo de los puntos
        SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
        //@ end
        //@ n1: acá: mostrar la pieza siguiente a la derecha del pozo
        SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
        SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
        for (int f = 0; f < 4; f++) {
            for (int c = 0; c < 4; c++) {
                if (PIEZAS[siguiente][f][c] == 1) {
                    SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                    SDL_RenderFillRect(lapiz, &bloque);
                }
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        //@ end'''),
    ('''
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }''', '''
        //@ n4: acá: el cartel del final, centrado: con 10 líneas o más, la Torre se detiene
        if (estado == PERDISTE) {
            const char *cartel = (lineas >= 10) ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ else
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ end'''),
])

NODO = dict(
    codigo='R05-N06', titulo='Jefe: La Torre que no para', tipo='jefe', criatura='glitch', padre='R05-N05',
    lugar='La Torre que no para',
    insignia='Sello de la Torre que no para',
    insignia_descripcion='Detuviste a la Torre que no para: un Tetris entero, con el pozo en una matriz, las siete piezas que giran, las líneas que se borran, la pieza siguiente, los escombros que empujan, la caída que se acelera, el menú, la revancha y el sonido.',
    temas='juegos.estados', usa='col.matrices, prog.funciones, prog.matematica-azar, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Cuando Kira borra la décima fila, la máquina tiembla. Los bloques de la torre de verdad empiezan a moverse solos,
    se despegan de las paredes y se acomodan en una figura enorme: un gigante hecho de bloques de colores, con dos
    ventanas encendidas por ojos y una pieza girando arriba, como un sombrero. Bosteza con un ruido de piedras. —Hace
    treinta años que apilo sin parar —dice, con voz cansada—. No sé frenar. Nadie me enseñó. Si me ganás, a lo mejor
    puedo dormir. Es **la Torre que no para**, y no va a esperar a nadie: empuja escombros desde abajo y se apura cada
    vez más.
    ''',
    objetivos='''
    Terminar el Tetris completo contra la Torre: mostrar la **pieza siguiente**, aguantar los **escombros** que la Torre
    empuja desde abajo cada 10 segundos, una **caída que se acelera** con el nivel y un **cartel final centrado** que dice
    si la Torre se detuvo.
    ''',
    antes='''
    Toda la rama R05. De R03: el muro que bajaba con un temporizador (N07). De R04: el cartel centrado del jefe (N05).
    ''',
    explicacion='''
    #### La pieza siguiente
    Los jugadores buenos miran qué viene. Se guarda `siguiente`, elegida al azar desde el principio. Cuando sale una
    pieza nueva, **es la que estaba esperando** (`tipo = siguiente`) y recién ahí se elige otra para después. Se
    dibuja a la derecha del pozo, con su cajita de la tabla `PIEZAS`.

    #### Los escombros desde abajo
    Un temporizador, `relojTorre`, como el muro de R03. Cada 10 segundos, todo el pozo **sube** una fila (cada fila
    copia la de abajo, al revés que al borrar) y la de abajo se llena de escombros grises con un hueco al azar. Si la
    pieza que cae puede, sube también, para no quedar adentro.

    #### Cada vez más rápido
    Otro temporizador, `relojNivel`. Cada 20 segundos sube el nivel y la caída se multiplica por 0,8: medio segundo
    pasa a ser 0,4, después 0,32… Con `SDL_max(0.1f, …)` nunca baja de una décima, para que se pueda jugar.

    #### El cartel del final
    Con 10 líneas o más, «LA TORRE SE DETIENE»; si no, «LA TORRE TE TAPO». Centrado como siempre: `320 - letras * 4`.
    ''',
    para_que='''
    «Lo que viene después» se usa en todos los juegos que se planifican (la próxima pieza, la próxima oleada, la
    próxima carta). Y el Tetris completo es tu cuarto juego entero: lo vas a poder bajar y jugar en tu compu.
    ''',
    errores='''
    **Elegir la siguiente antes de usarla.** Si se hace `siguiente = SDL_rand(7)` antes de `tipo = siguiente`, la pieza que
    se mostraba nunca sale: sale otra.

    **Subir las filas de arriba para abajo.** Para subir, cada fila copia la de **abajo**, empezando por la fila 0. Si se
    empieza por abajo, se copia la misma fila de escombros en todo el pozo.

    **La caída que llega a 0.** Sin `SDL_max`, después de muchos niveles la pieza cae en un solo cuadro y no se puede
    jugar.

    **Glitch: dibujar la siguiente con el color de la que cae.** Hay que usar `COLORES[siguiente + 1]`, no `tipo + 1`.
    ''',
    misiones=[
        dict(titulo='La que viene',
             carta='Siguiente | al sacar: tipo = siguiente · siguiente = SDL_rand(7) · dibujarla a la derecha en (470 + c * CELDA, 60 + f * CELDA)',
             personajes='Kira, Gheco, Arcadia, la Torre que no para',
             escena='''
             —Te voy a dar una ventaja —dice la Torre, y una de sus ventanas se enciende a un costado del pozo—. Vas a
             ver la pieza que viene. Yo siempre la sé. Si vos también la sabés, quizás me alcances.
             ''',
             gheco='''
             Ya está `siguiente`, elegida al azar al principio. Dos cosas:
             1. **La pieza nueva es la que esperaba**, en lugar de `tipo = SDL_rand(7);`:
             ```c
             tipo = siguiente;          /* sale la que se estaba mostrando */
             siguiente = SDL_rand(7);   /* y se elige otra para después */
             ```
             2. **Dibujarla** a la derecha del pozo, con su cajita de la tabla:
             ```c
             SDL_RenderDebugText(lapiz, 470, 40, "SIGUIENTE");
             SDL_SetRenderDrawColor(lapiz, COLORES[siguiente + 1][0], COLORES[siguiente + 1][1], COLORES[siguiente + 1][2], 255);
             for (int f = 0; f < 4; f++) {
                 for (int c = 0; c < 4; c++) {
                     if (PIEZAS[siguiente][f][c] == 1) {
                         SDL_FRect bloque = { 470 + c * CELDA, 60 + f * CELDA, CELDA - 1, CELDA - 1 };
                         SDL_RenderFillRect(lapiz, &bloque);
                     }
                 }
             }
             SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             ```
             El orden importa: primero se usa la que esperaba, después se elige otra.
             ''',
             desafio='Mostrá la pieza siguiente a la derecha del pozo, y hacé que sea la que sale después.',
             pasos=['Buscá `/* acá: la pieza nueva es la que estaba esperando, y se elige otra para después */`, borrá el `tipo = SDL_rand(7);` de abajo y escribí las dos líneas de la sugerencia.',
                    'Buscá `/* acá: mostrar la pieza siguiente a la derecha del pozo */` y escribí el texto, el color y los dos `for` de la sugerencia.',
                    'Tocá **Jugar** y empezá: a la derecha tiene que verse la que viene. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 3', estado='pixel 500 90',
             superarla='''
             A la derecha del pozo aparece un cuadrado amarillo: la que viene. Cuando la T se queda, sale justo el
             cuadrado, y a la derecha aparece otra. Kira ya no juega a ciegas. La Torre bosteza: —Bien. Ahora en serio.
             ''',
             imagen=['La Torre que no para: un gigante hecho de bloques de colores, con dos ventanas encendidas por ojos y una pieza girando arriba como sombrero, enciende una ventana a un costado.',
                     'En la pantalla de la máquina, el pozo y, a la derecha, una cajita con un cuadrado amarillo.',
                     'Kira mira la cajita de la derecha, atenta; Arcadia mira a la Torre; Gheco, sobre la máquina, señala la cajita.']),
        dict(titulo='Los escombros de la Torre',
             carta='Temporizador | relojTorre += dt · a los 10 s: cada fila copia la de abajo · abajo escombros con hueco = SDL_rand(COLS) · py--',
             personajes='Kira, Gheco, Arcadia, la Torre que no para',
             escena='''
             La Torre golpea el piso con un pie de bloques y desde abajo del pozo sube una fila gris, empujando todo para
             arriba. —Yo no paro —dice—. Mientras vos acomodás, yo apilo desde abajo.
             ''',
             gheco='''
             Ya está `relojTorre`. Cada 10 segundos (jugando), todo el pozo sube una fila y abajo aparecen escombros con un
             hueco al azar:
             ```c
             if (estado == JUGANDO) {
                 relojTorre += dt;
             }
             if (relojTorre >= 10) {
                 relojTorre -= 10;
                 for (int f = 0; f < FILAS - 1; f++) {      /* cada fila copia la de abajo */
                     for (int c = 0; c < COLS; c++) {
                         tablero[f][c] = tablero[f + 1][c];
                     }
                 }
                 int hueco = SDL_rand(COLS);                 /* escombros con un hueco al azar */
                 for (int c = 0; c < COLS; c++) {
                     tablero[FILAS - 1][c] = (c == hueco) ? 0 : 8;
                 }
                 if (py > 0) {
                     py--;                                   /* la pieza también sube */
                 }
             }
             ```
             `(c == hueco) ? 0 : 8` es un `if` en una línea: 0 (vacía) en el hueco, 8 (escombros) en las demás. El robot va
             a empezar y esperar 10 segundos: la primera pieza borra los escombros del principio, así que los grises
             tienen que ser los nuevos.
             ''',
             desafio='Hacé que cada 10 segundos todo suba una fila y abajo aparezcan escombros con un hueco al azar.',
             pasos=['Buscá `/* acá: cada 10 segundos, la Torre empuja una fila de escombros desde abajo */`.',
                    'Debajo, escribí los dos `if` de la sugerencia: el que junta el tiempo y el que empuja los escombros.',
                    'Tocá **Jugar**, empezá y esperá 10 segundos. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 620', estado='buscar #6e6e78',
             superarla='''
             Cada diez segundos, el pozo sube con un *grrr* de piedras y abajo aparece una fila gris con un hueco. Kira mete
             la pieza justo en el hueco y la fila se borra. La Torre gruñe, sorprendida: —Nadie me había devuelto los
             escombros.
             ''',
             imagen=['La Torre que no para, el gigante de bloques de colores, golpea el piso con un pie y hace subir una fila de bloques grises.',
                     'En la pantalla de la máquina, el pozo con una fila gris nueva abajo, con un hueco, empujando todo para arriba.',
                     'Kira juega rápido, decidida; Arcadia se agarra de la máquina que tiembla; Gheco se sujeta de los auriculares de Arcadia.']),
        dict(titulo='Cada vez más rápido',
             carta='Nivel | relojNivel += dt · a los 20 s: nivel++ · caida = SDL_max(0.1f, caida * 0.8f) · texto NIVEL %d',
             personajes='Kira, Gheco, Arcadia, la Torre que no para',
             escena='''
             La pieza en sombrero de la Torre gira cada vez más rápido. —Y cada rato —dice— me apuro un poquito. Nunca
             dejo de apurarme. Por eso me llaman así.
             ''',
             gheco='''
             Ya están `relojNivel` y `nivel` (en 1). Cada 20 segundos (jugando), sube el nivel y la caída se acorta:
             ```c
             if (estado == JUGANDO) {
                 relojNivel += dt;
             }
             if (relojNivel >= 20) {
                 relojNivel -= 20;
                 nivel++;
                 caida = SDL_max(0.1f, caida * 0.8f);   /* un 20 % más rápido, pero nunca menos de 0,1 s */
             }
             ```
             Y mostrar el nivel, abajo de los puntos:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 40, 80, "NIVEL %d", nivel);
             ```
             `SDL_max` devuelve el más grande de los dos: si `caida * 0.8f` quedara muy chiquito, se queda en 0,1. El robot
             va a empezar y esperar 20 segundos.
             ''',
             desafio='Hacé que cada 20 segundos suba el nivel y la pieza caiga más rápido, y mostrá el nivel.',
             pasos=['Buscá `/* acá: cada 20 segundos, la Torre se apura: sube el nivel y la pieza cae más rápido */` y escribí los dos `if` de la sugerencia.',
                    'Buscá `/* acá: mostrar el nivel abajo de los puntos */` y escribí el texto de la sugerencia.',
                    'Tocá **Jugar**, empezá y esperá 20 segundos. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 1220', estado='textos',
             superarla='''
             **NIVEL 2**, y las piezas bajan más ligero. **NIVEL 3**, más todavía. Kira ya no piensa: mira la siguiente,
             gira, suelta. Las ventanas de la Torre parpadean, como si se le cerraran los ojos.
             ''',
             imagen=['La Torre que no para, el gigante de bloques de colores, con la pieza en sombrero girando muy rápido y las ventanas parpadeando de sueño.',
                     'En la pantalla de la máquina, piezas cayendo rápido con rayas de velocidad.',
                     'Kira juega a toda velocidad, con los dedos en las flechas; Arcadia la alienta; Gheco gira como la pieza del sombrero.']),
        dict(titulo='La Torre se detiene',
             carta='Cartel centrado | al perder: cartel = lineas >= 10 ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO" · x = 320 - SDL_strlen(cartel) * 4',
             personajes='Kira, Gheco, Arcadia, la Torre que no para',
             recompensa='xp 20, monedas 5', item='Pieza Dorada',
             escena='''
             —Borrá diez filas —dice la Torre, con los ojos casi cerrados— y, cuando termine la partida, que la máquina lo
             diga en el medio, bien claro: que la Torre se detuvo. Y si no llegás, que diga la verdad: que te tapé.
             ''',
             gheco='''
             En lugar del cartel de antes («SE TAPO LA TORRE», corrido a ojo), uno centrado que depende de las líneas:
             ```c
             if (estado == PERDISTE) {
                 const char *cartel = (lineas >= 10) ? "LA TORRE SE DETIENE" : "LA TORRE TE TAPO";
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             }
             ```
             - Con 10 líneas o más, le ganaste a la Torre aunque después te haya tapado.
             - Cada letra mide 8 píxeles: un texto de `n` letras, centrado, empieza en `320 - n * 4` (como los carteles
               del Campeón, del Muro y de la Serpiente).

             El robot va a empezar y soltar piezas de golpe hasta llenar el pozo.
             ''',
             desafio='Cambiá el cartel del final por uno centrado: LA TORRE SE DETIENE con 10 líneas o más, LA TORRE TE TAPO si no.',
             pasos=['Buscá `/* acá: el cartel del final, centrado: con 10 líneas o más, la Torre se detiene */` y borrá el `if` de abajo.',
                    'En su lugar, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 2\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3', estado='textos',
             superarla='''
             Diez filas. Once. Doce. La pila de Kira llega por fin hasta arriba y la pantalla dice, en amarillo y en el
             medio, **LA TORRE SE DETIENE**. La Torre que no para deja de moverse. Por primera vez en treinta años, se sienta
             despacio, apoya la cabeza de bloques en las nubes y ronca: *grrr… clonc… grrr*.

             Antes de dormirse del todo, de su sombrero cae una pieza que brilla como el oro. Kira la ataja: la **Pieza
             Dorada**, una T que pesa como una pluma.

             En la pantalla aparece **otro pedazo del mapa del Vidriero**: una pista larga en las afueras, con biplanos de
             madera y nubes pintadas. {mentor} sonríe: —La Pista de los Biplanos. Ahí sí que se vuela.
             ''',
             imagen=['La Torre que no para, el gigante de bloques de colores, sentado y dormido con la cabeza apoyada en las nubes, roncando.',
                     'En la pantalla de la máquina, un pedazo de mapa antiguo con una pista larga y biplanos de madera.',
                     'Kira sostiene una pieza en forma de T que brilla como el oro; Arcadia mira el mapa, sonriente; Gheco abraza la pieza dorada.']),
    ],
)
