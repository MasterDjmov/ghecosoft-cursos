import motor
import n04

PLANTILLA = motor.crecer(motor.full(n04.PLANTILLA), [
    ('''
    return borradas;
}
''', '''
    return borradas;
}

/* Deja el pozo como al principio: vacío, con la fila de escombros abajo */
static void armar(int tablero[FILAS][COLS])
{
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLS; c++) {
            tablero[f][c] = 0;
        }
    }
    for (int c = 0; c < COLS; c++) {
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }
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

enum Estado { MENU, JUGANDO, PERDISTE };
'''),
    ('''
    SDL_Init(SDL_INIT_VIDEO);''', '''
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);'''),
    ('''
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);
''', '''
    SDL_CreateWindowAndRenderer("La Torre que no para", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);
'''),
    ('''
    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }''', '''
    int tablero[FILAS][COLS];   /* el pozo: 0 es una casilla vacía */
    armar(tablero);             /* vacío, con la fila de escombros que dejó la Torre */'''),
    ('''
    int puntos = 0;''', '''
    int puntos = 0;
    enum Estado estado = MENU;'''),
    ('''
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_LEFT''', '''
            //@ n1: acá: en el menú, el Enter empieza la partida
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            //@ end
            //@ n3: acá: después de perder, la R deja todo como al principio y se vuelve a jugar
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                armar(tablero);
                lineas = 0;
                puntos = 0;
                px = 3;
                py = 0;
                estado = JUGANDO;
            }
            //@ end
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == JUGANDO) {   /* las teclas de la pieza, solo jugando */
                if (evento.key.key == SDLK_LEFT'''),
    ('''
        reloj += dt;
        if (reloj >= caida) {''', '''
        //@ n1: acá: el reloj corre solo mientras se juega
        if (estado == JUGANDO) {
            reloj += dt;
        }
        //@ else
        reloj += dt;
        //@ end
        if (reloj >= caida) {'''),
    ('''
                int borradas = borrarLineas(tablero);''', '''
                //@ n4: acá: un toc grave cada vez que una pieza se queda
                pitido(parlante, 220, 0.05f);
                //@ end
                int borradas = borrarLineas(tablero);
                //@ n4: acá: y uno agudo si borró alguna fila
                if (borradas > 0) {
                    pitido(parlante, 880, 0.15f);
                }
                //@ end'''),
    ('''
                px = 3;
                py = 0;
            }''', '''
                px = 3;
                py = 0;
                //@ n2: acá: si la pieza nueva ya no cabe, la torre se tapó: perdiste
                if (!cabe(pieza, tablero, px, py)) {
                    estado = PERDISTE;
                }
                //@ end
            }'''),
    ('''
        SDL_RenderPresent(lapiz);''', '''
        //@ n2: acá: el cartel de perdiste, amarillo, sobre el pozo
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ end
        //@ n3: acá: avisar que con la R se juega otra vez
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        //@ end
        //@ n1: acá: el menú: el nombre grande y cómo se empieza
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
        }
        //@ end
        SDL_RenderPresent(lapiz);'''),
    ('''
    SDL_DestroyRenderer(lapiz);''', '''
    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);'''),
])

NODO = dict(
    codigo='R05-N05', titulo='Menú, fin y revancha', criatura='bucle_eterno', padre='R05-N04',
    lugar='La Torre que no para',
    temas='juegos.estados', usa='juegos.sonido, prog.funciones, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Kira juega y juega, y la pila llega hasta arriba de todo… y la máquina se queda colgada: la pieza nueva aparece
    encima de las otras y nada se mueve. Ni una tecla responde. —El **Bucle Eterno** —dice {mentor}, y le da un
    golpecito a la máquina—. Un juego tiene que saber cuándo empieza, cuándo se terminó y cómo se vuelve a empezar.
    Como el Pong y el Snake: un menú, el fin y la revancha.
    ''',
    objetivos='''
    Ordenar la Torre con **estados** (menú, jugando, perdiste) como en el Snake, darse cuenta de que **se tapó** cuando la
    pieza nueva ya no cabe, volver a jugar con la **R** y sumarle **sonido**.
    ''',
    antes='''
    El nodo anterior. De R04: el `enum`, el menú y la revancha (N04). De R01: el pitido (N09).
    ''',
    explicacion='''
    #### Los estados, otra vez
    El mismo `enum` del Snake: `MENU`, `JUGANDO` y `PERDISTE`. Cada parte del juego mira el estado: el reloj solo junta
    tiempo jugando, las teclas de la pieza solo andan jugando, y cada estado dibuja su cartel. En el menú se empieza
    con el **Enter** (el espacio ya hace caer la pieza).

    #### ¿Cuándo se pierde?
    En el Tetris no hay vidas: se pierde cuando la torre llega hasta arriba. ¿Cómo se sabe? Justo después de sacar una
    pieza nueva, se pregunta si **cabe** donde aparece. Si no cabe, es que ya hay bloques ahí: la torre se tapó.

    #### Volver a empezar
    La función `armar` deja el pozo como al principio: todas las casillas en 0 y la fila de escombros abajo. Es la
    misma que se usa al arrancar, así la revancha queda **igual** que la primera partida. Con la R se arma el pozo, se
    ponen las líneas y los puntos en 0 y se vuelve a jugar.

    #### El sonido
    El `pitido` de R01: uno grave y cortito cada vez que una pieza se queda (*toc*) y uno agudo, más largo, cuando se
    borra alguna fila.
    ''',
    para_que='''
    Todo juego tiene estados: el menú, la partida, la pausa, el fin. Y una función que deja todo «como al principio» es
    la manera segura de armar la revancha: si se usa la misma para arrancar, no se olvida nada.
    ''',
    errores='''
    **Empezar con el espacio.** El espacio hace caer la pieza: si también empieza, la primera pieza cae de golpe apenas
    se arranca. Por eso el menú usa el Enter.

    **Preguntar si se perdió antes de sacar la pieza.** Hay que preguntar por la pieza **nueva**, en el lugar donde
    aparece, recién sacada.

    **La revancha que no vacía el pozo.** Si la R solo cambia el estado, la pieza nueva sigue sin caber y se vuelve a
    perder en el acto.

    **Bucle Eterno: el juego que sigue sin cartel.** Si no se cambia el estado al perder, la pieza nueva se queda
    encimada y el juego parece colgado.
    ''',
    misiones=[
        dict(titulo='El menú de la Torre',
             carta='Estados | MENU: el reloj no corre, cartel LA TORRE · Enter: JUGANDO · las teclas de la pieza, solo JUGANDO',
             escena='''
             La máquina se prende y la pieza ya está cayendo, sin aviso. —Primero el nombre bien grande —dice {mentor}—,
             y que nada se mueva hasta que el jugador diga «empiezo».
             ''',
             gheco='''
             Ya están el `enum` (`MENU`, `JUGANDO`, `PERDISTE`), `estado` en `MENU` y las teclas de la pieza solo andan
             jugando. Tres cosas:
             1. **El Enter empieza**, en los eventos:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                 estado = JUGANDO;
             }
             ```
             2. **El reloj corre solo jugando**, en lugar del `reloj += dt;` solo:
             ```c
             if (estado == JUGANDO) {
                 reloj += dt;
             }
             ```
             3. **El cartel del menú**, al final del dibujo:
             ```c
             if (estado == MENU) {
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_SetRenderScale(lapiz, 4, 4);          /* letras cuatro veces más grandes */
                 SDL_RenderDebugText(lapiz, 48, 40, "LA TORRE");
                 SDL_SetRenderScale(lapiz, 1, 1);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
                 SDL_RenderDebugText(lapiz, 272, 260, "ENTER: JUGAR");
             }
             ```
             El robot va a esperar un segundo en el menú y después apretar el Enter.
             ''',
             desafio='Hacé el menú: la pieza quieta y el cartel hasta que se apriete el Enter.',
             pasos=['Buscá `/* acá: en el menú, el Enter empieza la partida */` y escribí el `if` del Enter.',
                    'Buscá `/* acá: el reloj corre solo mientras se juega */`, borrá el `reloj += dt;` de abajo y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: el menú: el nombre grande y cómo se empieza */` y escribí el `if (estado == MENU)` del cartel.',
                    'Tocá **Jugar**, mirá el menú y apretá el Enter. Después, **Comprobar**.'],
             eventos='cuadros 60\ntecla Enter\ncuadros 30', estado='buscar #aa50ff',
             superarla='''
             La pantalla se prende con **LA TORRE** en letras amarillas enormes, y la pieza espera, quieta. Kira aprieta el
             Enter: el cartel se va y la T empieza a bajar. Gheco aplaude como en el cine.
             ''',
             imagen=['La pantalla de la máquina con un cartel amarillo enorme sobre el pozo (sin letras legibles) y la pieza quieta arriba.',
                     'Kira apoya el dedo sobre un botón grande de la máquina; Arcadia sonríe.',
                     'Gheco aplaude, sentado arriba de la máquina, como en el cine.']),
        dict(titulo='La torre se tapó',
             carta='Fin | al sacar la pieza nueva: si no cabe(…, px, py): PERDISTE · cartel SE TAPO LA TORRE',
             criatura='bucle_eterno',
             escena='''
             Kira deja caer pieza tras pieza sin borrar nada, y la pila llega hasta arriba. La pieza nueva aparece encima
             de las otras y todo se cuelga. El Bucle Eterno da vueltas y vueltas alrededor de la máquina.
             ''',
             gheco='''
             Se pierde cuando la pieza nueva ya no cabe donde aparece. Dos cosas:
             1. **Preguntar**, justo después de sacarla (después de `px = 3;` y `py = 0;`):
             ```c
             if (!cabe(pieza, tablero, px, py)) {
                 estado = PERDISTE;
             }
             ```
             2. **El cartel**, al final del dibujo:
             ```c
             if (estado == PERDISTE) {
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_RenderDebugText(lapiz, 256, 220, "SE TAPO LA TORRE");
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             }
             ```
             Como el reloj solo corre jugando, al perder la pieza se queda quieta. El robot va a empezar y soltar piezas
             de golpe, sin moverlas, hasta llenar el pozo.
             ''',
             desafio='Hacé que se pierda cuando la pieza nueva ya no cabe, con el cartel SE TAPO LA TORRE.',
             pasos=['Buscá `/* acá: si la pieza nueva ya no cabe, la torre se tapó: perdiste */` y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: el cartel de perdiste, amarillo, sobre el pozo */` y escribí el `if` del cartel.',
                    'Tocá **Jugar**, empezá y soltá piezas con el espacio hasta llenar el pozo. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 2\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3', estado='textos',
             superarla='''
             La pila llega arriba de todo y la máquina dice, en amarillo, **SE TAPO LA TORRE**. La pieza se queda quieta.
             El Bucle Eterno se frena de golpe, mareado, y se va caminando en zigzag.
             ''',
             imagen=['La pantalla de la máquina con el pozo lleno de bloques de colores hasta arriba y un cartel amarillo (sin letras legibles).',
                     'Una criatura que es un aro de luz girando se frena, mareada, y se va caminando en zigzag.',
                     'Kira se rasca la cabeza; Arcadia sonríe; Gheco se tapa los ojos.']),
        dict(titulo='Otra vez',
             carta='Revancha | R en PERDISTE: armar(tablero) · lineas = 0 · puntos = 0 · px = 3, py = 0 · JUGANDO',
             escena='''
             La torre se tapó y ahí se quedó. Kira aprieta todas las teclas: nada. —Una revancha —pide—. —La función
             `armar` deja el pozo como al principio —dice {mentor}—: la misma que se usa al prender la máquina.
             ''',
             gheco='''
             Después de perder, la R deja todo como al principio y se vuelve a jugar:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                 armar(tablero);     /* el pozo vacío, con los escombros */
                 lineas = 0;
                 puntos = 0;
                 px = 3;             /* la pieza, arriba */
                 py = 0;
                 estado = JUGANDO;
             }
             ```
             Y avisarlo, abajo del cartel:
             ```c
             if (estado == PERDISTE) {
                 SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
             }
             ```
             `armar` es la misma función que arma el pozo al principio del `main`: así la revancha arranca igual.
             ''',
             desafio='Hacé que con la R, después de perder, el pozo quede como al principio y se vuelva a jugar.',
             pasos=['Buscá `/* acá: después de perder, la R deja todo como al principio y se vuelve a jugar */` y escribí el `if` de la R.',
                    'Buscá `/* acá: avisar que con la R se juega otra vez */` y escribí el `if` del aviso.',
                    'Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 2\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla Espacio\ncuadros 3\ntecla R\ncuadros 3', estado='textos',
             superarla='''
             Kira aprieta la R y el pozo se vacía de golpe, con un *fsss*, como si alguien hubiera barrido la torre. La
             fila de escombros vuelve a su lugar, y arriba asoma la pieza siguiente. —Ahora sí —dice Kira.
             ''',
             imagen=['La pantalla de la máquina con el pozo vacío otra vez, la fila de escombros grises abajo y una pieza nueva arriba.',
                     'Kira, decidida, se arremanga el brazal; Arcadia le guiña un ojo.',
                     'Gheco barre con la cola unos bloquecitos que quedaron sobre la máquina.']),
        dict(titulo='Toc y tin',
             carta='Sonido | al quedarse: pitido(parlante, 220, 0.05f) · si borradas > 0: pitido(parlante, 880, 0.15f)',
             escena='''
             La Torre de Kira anda entera, pero muda. Desde lo alto de la Torre de verdad, en cambio, cada bloque suena
             al acomodarse: *toc*. Y cuando se va una fila entera, *tiiin*.
             ''',
             gheco='''
             Ya están el parlante y la función `pitido` (la de R01). Dos sonidos, donde una pieza se queda en el pozo:
             ```c
             pitido(parlante, 220, 0.05f);         /* toc: grave y cortito */
             int borradas = borrarLineas(tablero);
             if (borradas > 0) {
                 pitido(parlante, 880, 0.15f);     /* tin: agudo y más largo */
             }
             ```
             El primero va **antes** de `int borradas = …` y el segundo, **después**. El robot va a empezar y soltar la
             primera pieza: tiene que sonar el toc y, como borra la fila de escombros, también el tin.
             ''',
             desafio='Hacé que suene un toc cuando una pieza se queda y un tin cuando se borra alguna fila.',
             pasos=['Buscá `/* acá: un toc grave cada vez que una pieza se queda */` y escribí el primer `pitido`.',
                    'Buscá `/* acá: y uno agudo si borró alguna fila */` y escribí el `if` con el segundo `pitido`.',
                    'Tocá **Jugar**, empezá y soltá la primera pieza. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 2\ntecla Espacio\ncuadros 5', estado='sonido',
             superarla='''
             *Toc… tiiin*. La primera fila se va con un sonido que hace sonreír a Arcadia. —Así sonaba la Torre cuando el
             Vidriero jugaba —dice, bajito.
             ''',
             imagen=['La pantalla de la máquina con una fila brillando al borrarse y notas musicales saliendo del parlante.',
                     'Arcadia sonríe con nostalgia, con los auriculares gamer al cuello; Kira juega concentrada.',
                     'Gheco baila con las notas musicales arriba de la máquina.']),
    ],
)
