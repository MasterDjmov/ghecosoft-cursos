import motor
import n01

FLECHAS = '''                if (evento.key.key == SDLK_UP) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT) { dx = 1; dy = 0; }'''

PLANTILLA = motor.crecer(motor.full(n01.PLANTILLA), [
    ('''
#define FILAS 24    /* 480 / 20: celdas de alto */''', '''
#define FILAS 24    /* 480 / 20: celdas de alto */
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */'''),
    ('''
    int x = 5;     /* la cabeza: columna y fila de la grilla (no píxeles) */
    int y = 12;''', '''
    int cx[MAX] = { 0 };   /* la columna de cada parte: cx[0] es la cabeza */
    int cy[MAX] = { 0 };   /* la fila de cada parte */
    int largo = 5;         /* cuántas partes tiene */
    //@ n2: acá: armar la serpiente: cinco partes en fila, con la cabeza adelante
    for (int i = 0; i < largo; i++) {
        cx[i] = 5 - i;
        cy[i] = 12;
    }
    //@ else
    cx[0] = 5;
    cy[0] = 12;
    //@ end'''),
    ('\n' + FLECHAS, '''
                //@ n4: acá: no se puede dar media vuelta, solo doblar
                if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }
                if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }
                if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }
                if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }
                //@ else
''' + FLECHAS + '''
                //@ end'''),
    ('''
            x += dx;
            y += dy;''', '''
            //@ n3: acá: cada parte va adonde estaba la de adelante (de atrás para adelante)
            for (int i = largo - 1; i > 0; i--) {
                cx[i] = cx[i - 1];
                cy[i] = cy[i - 1];
            }
            //@ end
            cx[0] += dx;
            cy[0] += dy;'''),
    ('''
        x = (x + COLS) % COLS;
        y = (y + FILAS) % FILAS;''', '''
        cx[0] = (cx[0] + COLS) % COLS;
        cy[0] = (cy[0] + FILAS) % FILAS;'''),
    ('''
        SDL_FRect cabeza = { x * CELDA, y * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);''', '''
        //@ n1: acá: dibujar todas las partes, no solo la cabeza
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
            if (i == 0) {
                SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
            } else {
                SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
            }
            SDL_RenderFillRect(lapiz, &parte);
        }
        //@ else
        SDL_FRect cabeza = { cx[0] * CELDA, cy[0] * CELDA, CELDA, CELDA };   /* de celda a píxeles */
        SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);
        SDL_RenderFillRect(lapiz, &cabeza);
        //@ end'''),
])

NODO = dict(
    codigo='R04-N02', titulo='La cola que sigue', criatura='glitch', padre='R04-N01',
    lugar='El Jardín de la Serpiente',
    temas='col.arrays', usa='prog.bucles, juegos.entrada',
    plantilla=PLANTILLA,
    cronica='''
    Una cabeza sola no es una serpiente. {mentor} saca de un cantero cinco anillos de vidrio verde, enganchados
    uno detrás del otro como un tren. —El cuerpo va siguiendo a la cabeza —explica—: cada anillo pisa donde estaba
    el de adelante. Si lo armás mal, la cola se queda atrás o aparece donde no tiene que estar. Sobre la pantalla,
    un **glitch** acomoda los anillos en un rincón, todos encimados, y se ríe.
    ''',
    objetivos='''
    Guardar la serpiente en **dos arreglos** (la columna y la fila de cada parte), dibujar **todas** las partes,
    armarla al empezar con cinco partes en fila, hacer que **cada parte siga a la de adelante** y que la serpiente
    **no pueda dar media vuelta**.
    ''',
    antes='''
    R04-N01 (la grilla y la cabeza). De R03: los arreglos y los `for` (N02). Del curso de C: recorrer un arreglo
    de atrás para adelante.
    ''',
    explicacion='''
    #### La serpiente en dos arreglos
    Cada parte de la serpiente está en una celda: tiene su columna y su fila. Dos arreglos las guardan:
    `cx[i]` es la columna de la parte `i` y `cy[i]` su fila. La parte 0 es la **cabeza**; la última, la punta de la
    cola. `largo` dice cuántas partes se usan. Los arreglos tienen lugar para `MAX` partes (todas las celdas del
    jardín), porque la serpiente va a crecer.

    #### Armarla en fila
    Al empezar, la cabeza está en la columna 5 y las demás partes, una a la izquierda de la otra: 4, 3, 2 y 1. Es
    `cx[i] = 5 - i`, todas en la fila 12.

    #### Cada parte, adonde estaba la de adelante
    El truco del Snake: en cada paso, **la cola sigue a la cabeza**. La parte 4 va adonde estaba la 3, la 3 adonde
    estaba la 2… y la 1 adonde estaba la cabeza. Recién después la cabeza avanza a una celda nueva.

    Hay que hacerlo **de atrás para adelante** (`i` desde `largo - 1` hasta 1): si se empezara por adelante, la
    parte 1 copiaría la cabeza, la 2 copiaría a la 1 (que ya es la cabeza)… y todas terminarían encimadas en el
    mismo lugar.

    #### No dar media vuelta
    Si la serpiente va para la derecha y se aprieta la izquierda, la cabeza se metería en su propio cuello. Por eso
    cada flecha pregunta antes: la de la izquierda solo funciona si **no** va para la derecha (`dx != 1`).
    ''',
    para_que='''
    Mover una fila de cosas donde cada una sigue a la anterior sirve para colas de enemigos, para los vagones de un
    tren y para los rastros de luz. Y recorrer un arreglo **de atrás para adelante** para no pisar datos es un truco
    que se usa siempre que se corren elementos de lugar.
    ''',
    errores='''
    **Glitch: todas las partes en el rincón.** Si se dibujan todas las partes pero no se arman, las que no tienen
    lugar quedan en `(0, 0)`: el rincón de arriba a la izquierda.

    **Correr de adelante para atrás.** `for (i = 1; i < largo; i++)` copia la cabeza en todas: la serpiente queda
    hecha una sola celda.

    **Mover la cabeza antes que el cuerpo.** Si la cabeza avanza primero, la parte 1 copia la cabeza **nueva** y
    quedan las dos encimadas.

    **Media vuelta.** Sin las condiciones `dy != 1` y compañía, una flecha hacia atrás mete la cabeza en el cuello.
    ''',
    misiones=[
        dict(titulo='Todas las partes',
             carta='Dibujar el cuerpo | for i < largo: rectángulo en (cx[i] * CELDA, cy[i] * CELDA) · la cabeza más clara',
             escena='''
             La pantalla muestra solo la cabeza, aunque la serpiente ya tiene cinco partes guardadas. —Están, pero no se
             ven —dice {mentor}—. Dibujalas todas, cada una en su celda.
             ''',
             gheco='''
             Ahora la serpiente está en dos arreglos, `cx` y `cy`, y `largo` dice cuántas partes tiene (5). En lugar de
             dibujar solo la cabeza, un `for` dibuja cada parte en su celda:
             ```c
             for (int i = 0; i < largo; i++) {
                 SDL_FRect parte = { cx[i] * CELDA, cy[i] * CELDA, CELDA, CELDA };
                 if (i == 0) {
                     SDL_SetRenderDrawColor(lapiz, 120, 255, 140, 255);   /* la cabeza, más clara */
                 } else {
                     SDL_SetRenderDrawColor(lapiz, 40, 190, 90, 255);     /* el cuerpo */
                 }
                 SDL_RenderFillRect(lapiz, &parte);
             }
             ```
             Ojo: todavía no armamos las partes, así que puede pasar algo raro. Lo arreglamos en la que sigue.
             ''',
             desafio='Dibujá todas las partes de la serpiente con un for, con la cabeza más clara que el cuerpo.',
             pasos=['Buscá `/* acá: dibujar todas las partes, no solo la cabeza */` y borrá las tres líneas de abajo (las de `cabeza`).',
                    'En su lugar, escribí el `for` de la sugerencia.',
                    'Tocá **Jugar** y mirá bien toda la pantalla. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #28be5a',
             superarla='''
             Aparece el cuerpo… pero todo encimado en el rincón de arriba a la izquierda. Un glitch se ríe sentado
             arriba de los anillos. —Se dibujan bien —dice {mentor}—. El problema es que no les dijimos dónde van.
             ''',
             imagen=['La pantalla con la grilla, la cabeza verde clara en el medio y unos cuadraditos verdes encimados en el rincón de arriba a la izquierda.',
                     'Un glitch pixelado se ríe sentado arriba de los cuadraditos del rincón.',
                     'Kira se rasca la cabeza; Arcadia sostiene cinco anillos de vidrio verde enganchados; Gheco señala el rincón.']),
        dict(titulo='Cinco en fila',
             carta='Armar | for i < largo: cx[i] = 5 - i · cy[i] = 12',
             criatura='glitch',
             escena='''
             {mentor} acomoda los cinco anillos de vidrio en el caminito, uno detrás del otro. —La cabeza adelante y
             el resto atrás, en fila —dice—. Así tiene que arrancar la serpiente.
             ''',
             gheco='''
             Las partes que no se armaron valen 0: por eso aparecían en la celda `(0, 0)`, el rincón. Al empezar, se
             arman en fila:
             ```c
             for (int i = 0; i < largo; i++) {
                 cx[i] = 5 - i;   /* la cabeza en la 5, las demás en 4, 3, 2 y 1 */
                 cy[i] = 12;      /* todas en la fila 12 */
             }
             ```
             Reemplaza a las dos líneas que armaban solo la cabeza.
             ''',
             desafio='Armá la serpiente al empezar: cinco partes en fila, con la cabeza adelante.',
             pasos=['Buscá `/* acá: armar la serpiente: cinco partes en fila, con la cabeza adelante */` y borrá las dos líneas de abajo.',
                    'En su lugar, escribí el `for` de la sugerencia.',
                    'Tocá **Jugar**: la serpiente tiene que aparecer entera, en fila. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #28be5a',
             superarla='''
             La serpiente aparece entera en el medio del jardín, cinco cuadraditos en fila. El glitch se queda sin
             rincón donde esconderse y se deshace en píxeles.
             ''',
             imagen=['La pantalla con la grilla y una serpiente de cinco cuadraditos verdes en fila, la cabeza más clara.',
                     'Un glitch pixelado se deshace en píxeles al costado de la pantalla.',
                     'Arcadia acomoda cinco anillos de vidrio verde en fila sobre el caminito; Kira y Gheco miran.']),
        dict(titulo='La cola que sigue',
             carta='Seguir | for i desde largo - 1 hasta 1: cx[i] = cx[i - 1] · cy[i] = cy[i - 1] · después avanza la cabeza',
             escena='''
             La cabeza avanza, pero el cuerpo se queda quieto atrás, como un tren sin enganche. Gheco se ríe tan fuerte
             que se cae de la máquina. —Cada anillo tiene que pisar donde estaba el de adelante —dice {mentor}.
             ''',
             gheco='''
             En cada paso, **antes** de que la cabeza avance, cada parte se corre adonde estaba la de adelante:
             ```c
             for (int i = largo - 1; i > 0; i--) {
                 cx[i] = cx[i - 1];   /* la parte i va adonde estaba la i - 1 */
                 cy[i] = cy[i - 1];
             }
             ```
             - Empieza por la **última** (`largo - 1`) y termina en la 1. La cabeza (0) no se copia: avanza después.
             - ¿Por qué de atrás para adelante? Si se empezara por la 1, copiaría la cabeza; la 2 copiaría a la 1 (que
               ya es la cabeza)… y todas quedarían encimadas.
             ''',
             desafio='Hacé que en cada paso cada parte vaya adonde estaba la de adelante, antes de mover la cabeza.',
             pasos=['Buscá `/* acá: cada parte va adonde estaba la de adelante (de atrás para adelante) */` (adentro del `if` del reloj).',
                    'Debajo, escribí el `for` de la sugerencia, que va de `largo - 1` hasta 1.',
                    'Tocá **Jugar** y doblá con las flechas: el cuerpo tiene que seguir a la cabeza. Después, **Comprobar**.'],
             eventos='cuadros 60', estado='buscar #28be5a',
             superarla='''
             Ahora el cuerpo sigue a la cabeza por cada esquina, como un tren enganchado. Kira dibuja una S en la
             pantalla y la serpiente la copia, anillo por anillo.
             ''',
             imagen=['La pantalla con una serpiente verde doblando una esquina, el cuerpo siguiendo exactamente el camino de la cabeza.',
                     'Kira dobla con las flechas, contenta; Arcadia asiente.',
                     'Gheco, recién caído de la máquina, se ríe en el piso del jardín.']),
        dict(titulo='Sin media vuelta',
             carta='Solo doblar | izquierda si dx != 1 · derecha si dx != -1 · arriba si dy != 1 · abajo si dy != -1',
             escena='''
             Kira aprieta la flecha de la izquierda mientras la serpiente va para la derecha, y la cabeza se da vuelta y
             se mete en su propio cuello. —Eso no lo hace ninguna serpiente —dice {mentor}—. Doblan, pero no dan media
             vuelta.
             ''',
             gheco='''
             Cada flecha tiene que preguntar antes si no es justo **la contraria** de hacia dónde va:
             ```c
             if (evento.key.key == SDLK_UP && dy != 1) { dx = 0; dy = -1; }      /* arriba, si no iba para abajo */
             if (evento.key.key == SDLK_DOWN && dy != -1) { dx = 0; dy = 1; }    /* abajo, si no iba para arriba */
             if (evento.key.key == SDLK_LEFT && dx != 1) { dx = -1; dy = 0; }    /* izquierda, si no iba a la derecha */
             if (evento.key.key == SDLK_RIGHT && dx != -1) { dx = 1; dy = 0; }   /* derecha, si no iba a la izquierda */
             ```
             `!=` es «distinto de». El robot va a apretar la izquierda mientras la serpiente va para la derecha.
             ''',
             desafio='Hacé que la serpiente pueda doblar pero no dar media vuelta.',
             pasos=['Buscá `/* acá: no se puede dar media vuelta, solo doblar */` y borrá las cuatro líneas de abajo.',
                    'En su lugar, escribí las cuatro de la sugerencia, con su condición cada una.',
                    'Tocá **Jugar** y probá apretar la flecha contraria. Después, **Comprobar**.'],
             eventos='tecla Izquierda\ncuadros 30', estado='buscar #78ff8c',
             superarla='''
             La flecha contraria ya no hace nada: la serpiente sigue su camino, tranquila. Kira dobla para arriba, después
             a la izquierda, y recién ahí vuelve: en dos esquinas, como una serpiente de verdad.
             ''',
             imagen=['La pantalla con la serpiente verde haciendo una vuelta en U por dos esquinas, con flechas curvas.',
                     'Kira prueba las flechas, divertida; Arcadia le explica con las manos cómo dobla una serpiente.',
                     'Gheco imita una serpiente con su cola, sentado arriba de la máquina.']),
    ],
)
