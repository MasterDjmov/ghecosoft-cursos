import motor
import n03

PLANTILLA = motor.crecer(motor.full(n03.PLANTILLA), [
    ('''
/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {''', '''
/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…); el 8, los escombros */
static const Uint8 COLORES[9][3] = {'''),
    ('''
    { 255, 150, 40 },    /* L: naranja */
};
''', '''
    { 255, 150, 40 },    /* L: naranja */
    { 110, 110, 120 },   /* escombros: gris */
};
//@ n4+

/* Los puntos según cuántas filas se borran juntas: 1, 2, 3 o 4 */
static const int PREMIO[5] = { 0, 100, 300, 500, 800 };
//@ end
'''),
    ('''
            pieza[f][c] = girada[f][c];
        }
    }
}
''', '''
            pieza[f][c] = girada[f][c];
        }
    }
}

/* Borra las filas llenas, baja lo que hay arriba y devuelve cuántas borró */
static int borrarLineas(int tablero[FILAS][COLS])
{
    int borradas = 0;
    //@ n2: acá: revisar cada fila de abajo para arriba; si está llena, bajar todo lo de arriba
    for (int f = FILAS - 1; f >= 0; f--) {
        int ocupadas = 0;
        for (int c = 0; c < COLS; c++) {
            if (tablero[f][c] != 0) {
                ocupadas++;
            }
        }
        if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
            for (int g = f; g > 0; g--) {       /* cada fila, desde esta para arriba, copia la de arriba */
                for (int c = 0; c < COLS; c++) {
                    tablero[g][c] = tablero[g - 1][c];
                }
            }
            for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                tablero[0][c] = 0;
            }
            borradas++;
            f++;                                /* se revisa otra vez la misma fila: ahora tiene lo que bajó */
        }
    }
    //@ end
    return borradas;
}
'''),
    ('''
    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */''', '''
    int tablero[FILAS][COLS] = { 0 };   /* el pozo: 0 es una casilla vacía */
    for (int c = 0; c < COLS; c++) {    /* la Torre dejó una fila de escombros abajo, con un hueco en la columna 4 */
        if (c != 4) {
            tablero[FILAS - 1][c] = 8;
        }
    }'''),
    ('''
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */''', '''
    float caida = 0.5f;     /* cada cuántos segundos baja una fila */
    //@ n3+
    int lineas = 0;         /* cuántas filas se borraron */
    //@ end
    //@ n4+
    int puntos = 0;
    //@ end'''),
    ('''
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */''', '''
                //@ n1: acá: con el espacio, la pieza cae de golpe hasta donde llegue
                if (evento.key.key == SDLK_SPACE) {
                    while (cabe(pieza, tablero, px, py + 1)) {
                        py++;
                    }
                    reloj = caida;   /* así se queda en el pozo en el cuadro que viene */
                }
                //@ end
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */'''),
    ('''
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }''', '''
                            tablero[py + f][px + c] = tipo + 1;
                        }
                    }
                }
                int borradas = borrarLineas(tablero);
                //@ n3: acá: sumar las filas borradas a las líneas
                lineas += borradas;
                //@ end
                //@ n4: acá: más puntos si se borran varias juntas
                puntos += PREMIO[borradas];
                //@ end'''),
    ('''
        SDL_RenderPresent(lapiz);''', '''
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        //@ n3: acá: mostrar las líneas a la izquierda del pozo
        SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
        //@ end
        //@ n4: acá: mostrar los puntos abajo de las líneas
        SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
        //@ end
        SDL_RenderPresent(lapiz);'''),
])

NODO = dict(
    codigo='R05-N04', titulo='Líneas completas', criatura='fuga_texturas', padre='R05-N03',
    lugar='La Torre que no para',
    temas='col.matrices', usa='prog.funciones, prog.bucles, prog.cadenas',
    plantilla=PLANTILLA,
    cronica='''
    En el fondo del pozo aparece una fila de bloques grises con un solo hueco: escombros que dejó la Torre. Las
    piezas se apilan arriba, el pozo se va llenando y nada se borra nunca. —El secreto de la Torre —dice {mentor}— es
    que una fila llena de punta a punta **desaparece**, y todo lo de arriba baja. Si no, se tapa enseguida. Entre los
    bloques grises, algo se infla como un globo: la **Fuga de Texturas**, que junta todo lo que nadie borra.
    ''',
    objetivos='''
    Hacer **caer de golpe** la pieza con el espacio, escribir una función que **borra las filas llenas** y baja lo que
    hay arriba, y llevar la cuenta de las **líneas** y los **puntos** (más puntos si se borran varias juntas).
    ''',
    antes='''
    El nodo anterior. De R03: contar los ladrillos que quedan (N05). De R02: el marcador (N02).
    ''',
    explicacion='''
    #### Caer de golpe
    Con el espacio, la pieza baja **mientras** quepa una fila más abajo: un `while` que repite `py++` hasta que ya no
    puede. Después se pone el reloj en `caida`, así en el cuadro siguiente el reloj ve que no puede bajar y la deja en
    el pozo.

    #### ¿Está llena esta fila?
    Para saberlo, se cuentan sus casillas ocupadas. Si son `COLS` (10), está llena de punta a punta.

    #### Borrar una fila: bajar todo lo de arriba
    No se «borra» nada: cada fila, desde la llena para arriba, **copia la de arriba suyo**. La llena queda pisada por la
    que tenía encima, esa por la de más arriba, y así hasta la fila 0, que queda vacía.

    #### Revisar la misma fila otra vez
    Se revisa de abajo para arriba (`f--`). Pero después de bajar todo, en la fila `f` quedó lo que estaba arriba, ¡y
    también puede estar llena! Por eso, al borrar, se hace `f++`: como el `for` le resta 1, la vuelta siguiente vuelve a
    mirar la misma fila.

    #### Una función que devuelve un número
    `borrarLineas` hace todo eso y **devuelve** cuántas filas borró (`return borradas;`). Con ese número se suman las
    líneas y los puntos. Borrar varias juntas vale más: la tabla `PREMIO` dice cuánto por 1, 2, 3 o 4 filas.
    ''',
    para_que='''
    Bajar los datos de un arreglo para tapar un hueco se usa para sacar algo de una lista: un enemigo que muere, un
    disparo que salió de la pantalla, un mensaje viejo del chat. Y devolver un número desde una función sirve para
    contar cualquier cosa que la función hizo.
    ''',
    errores='''
    **Revisar de arriba para abajo.** Al bajar las filas, la que se revisa después ya cambió y se saltea.

    **Olvidarse del `f++`.** Si dos filas seguidas están llenas, se borra una sola: la de arriba bajó y nadie la volvió a
    mirar.

    **`g >= 0` en el `for` que copia.** La fila 0 no tiene ninguna arriba: `tablero[-1]` no existe. Por eso va
    `g > 0`, y la fila 0 se vacía aparte.

    **Fuga de Texturas: no borrar nada.** Si la función cuenta las filas llenas pero no las borra, el pozo se llena en un
    minuto y suma puntos sin parar.
    ''',
    misiones=[
        dict(titulo='Caer de golpe',
             carta='Caída rápida | espacio: while (cabe(…, px, py + 1)) py++ · reloj = caida',
             escena='''
             Las piezas bajan despacito, medio segundo por fila, y Kira ya sabe dónde las quiere poner. —En la Torre se
             podía soltar la pieza —dice {mentor}— y caía de golpe, hasta donde llegara.
             ''',
             gheco='''
             Con el espacio, la pieza baja **mientras** quepa una fila más abajo:
             ```c
             if (evento.key.key == SDLK_SPACE) {
                 while (cabe(pieza, tablero, px, py + 1)) {
                     py++;            /* una fila más… y otra… hasta que no cabe */
                 }
                 reloj = caida;       /* así se queda en el pozo en el cuadro que viene */
             }
             ```
             - `while` repite mientras la condición sea verdadera: puede bajar 0 filas o 17.
             - Con el reloj lleno, en el cuadro siguiente la pieza ve que no puede bajar y se queda.

             El robot va a apretar el espacio apenas empieza: la T tiene que caer al fondo, con la pata en el hueco de los
             escombros.
             ''',
             desafio='Hacé que con el espacio la pieza caiga de golpe hasta donde llegue.',
             pasos=['Buscá `/* acá: con el espacio, la pieza cae de golpe hasta donde llegue */` (en los eventos).',
                    'Debajo, escribí el `if` del espacio, con el `while`, de la sugerencia.',
                    'Tocá **Jugar**, hacé clic en el juego y apretá el espacio. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 3', estado='pixel 306 466',
             superarla='''
             Kira aprieta el espacio y la T cae como una piedra: *¡clonc!*, con la pata justo en el hueco de los escombros.
             Gheco, del susto, salta a los brazos de Arcadia.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta en T cayendo de golpe al fondo del pozo, con rayas de velocidad.',
                     'En el fondo del pozo, una fila de bloques grises con un hueco donde encaja la pata de la T.',
                     'Gheco salta del susto a los brazos de Arcadia; Kira se ríe.']),
        dict(titulo='La fila llena desaparece',
             carta='Borrar | contar ocupadas · si son COLS: cada fila g copia la g - 1 · fila 0 vacía · f++ para revisarla otra vez',
             criatura='fuga_texturas',
             escena='''
             La pata de la T tapó el hueco: la fila de abajo quedó llena de punta a punta. Pero no pasa nada. La Fuga de
             Texturas se infla, contenta, entre los bloques grises. —Una fila llena se tiene que ir —dice {mentor}.
             ''',
             gheco='''
             La función `borrarLineas` ya se llama cada vez que una pieza se queda, pero está vacía. Adentro, revisá cada
             fila **de abajo para arriba**:
             ```c
             for (int f = FILAS - 1; f >= 0; f--) {
                 int ocupadas = 0;
                 for (int c = 0; c < COLS; c++) {
                     if (tablero[f][c] != 0) {
                         ocupadas++;
                     }
                 }
                 if (ocupadas == COLS) {                 /* ¡llena de punta a punta! */
                     for (int g = f; g > 0; g--) {       /* cada fila copia la de arriba */
                         for (int c = 0; c < COLS; c++) {
                             tablero[g][c] = tablero[g - 1][c];
                         }
                     }
                     for (int c = 0; c < COLS; c++) {    /* la de más arriba queda vacía */
                         tablero[0][c] = 0;
                     }
                     borradas++;
                     f++;                                /* revisar otra vez la misma fila */
                 }
             }
             ```
             La fila llena queda pisada por la que tenía arriba, y todo baja una. El `f++` hace que la vuelta siguiente
             mire otra vez la misma fila, por si lo que bajó también está lleno.
             ''',
             desafio='Hacé que las filas llenas se borren y todo lo de arriba baje una fila.',
             pasos=['Buscá `/* acá: revisar cada fila de abajo para arriba; si está llena, bajar todo lo de arriba */` (en la función `borrarLineas`).',
                    'Debajo, escribí el `for` grande de la sugerencia.',
                    'Tocá **Jugar**, apretá el espacio y mirá la fila de escombros. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 3', estado='pixel 210 466',
             superarla='''
             La T tapa el hueco y la fila entera se borra: los escombros grises desaparecen y la T baja una fila. La Fuga de
             Texturas se desinfla con un silbido, como un globo pinchado, y se va volando.
             ''',
             imagen=['La pantalla de la máquina con una fila del fondo brillando y desapareciendo, y los bloques de arriba bajando.',
                     'Una criatura como una nube que se desinfla con un silbido, volando lejos.',
                     'Kira festeja con los brazos en alto; Arcadia aplaude; Gheco salta en el aire.']),
        dict(titulo='Cuántas líneas',
             carta='Contar | lineas += borradas (lo que devolvió borrarLineas) · texto LINEAS %d',
             escena='''
             Las filas se borran, pero nadie lleva la cuenta. —La Torre se acuerda de cada fila que le sacaron —dice
             {mentor}—. Contalas, que después las vamos a necesitar.
             ''',
             gheco='''
             `borrarLineas` **devuelve** cuántas filas borró, y eso se guarda en `borradas`. Ya está `lineas` en 0. Dos
             cosas:
             1. **Sumarlas**, abajo de `int borradas = borrarLineas(tablero);`:
             ```c
             lineas += borradas;
             ```
             2. **Mostrarlas** a la izquierda del pozo (el color blanco ya está puesto):
             ```c
             SDL_RenderDebugTextFormat(lapiz, 40, 40, "LINEAS %d", lineas);
             ```
             El robot va a apretar el espacio para que la T borre la fila de escombros.
             ''',
             desafio='Contá las filas borradas y mostralas a la izquierda del pozo.',
             pasos=['Buscá `/* acá: sumar las filas borradas a las líneas */` y escribí `lineas += borradas;`.',
                    'Buscá `/* acá: mostrar las líneas a la izquierda del pozo */` y escribí el texto de la sugerencia.',
                    'Tocá **Jugar** y borrá la fila de escombros. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 3', estado='textos',
             superarla='''
             A la izquierda del pozo aparece **LINEAS 1**. Gheco lo anota con la cola en el vidrio empañado de la máquina,
             por las dudas.
             ''',
             imagen=['La pantalla de la máquina con el pozo y un contador blanco a la izquierda (sin letras legibles).',
                     'Gheco dibuja una rayita con la cola en el vidrio empañado de la máquina.',
                     'Kira y Arcadia sonríen.']),
        dict(titulo='Más juntas, más puntos',
             carta='Premio | puntos += PREMIO[borradas] (0, 100, 300, 500, 800) · texto PUNTOS %d',
             escena='''
             —En la Torre —dice {mentor}— borrar una fila vale poco, y borrar cuatro de una vez vale muchísimo. Los
             jugadores buenos esperan el palo largo para borrar cuatro juntas.
             ''',
             gheco='''
             Ya está la tabla `PREMIO`: cuántos puntos vale borrar 0, 1, 2, 3 o 4 filas juntas, y `puntos` en 0.
             ```c
             static const int PREMIO[5] = { 0, 100, 300, 500, 800 };
             ```
             Dos cosas:
             1. **Sumar el premio**, abajo de las líneas:
             ```c
             puntos += PREMIO[borradas];   /* borradas es 0, 1, 2, 3 o 4 */
             ```
             2. **Mostrarlos**, abajo de las líneas:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 40, 60, "PUNTOS %d", puntos);
             ```
             Borrar dos juntas (300) vale más que dos por separado (200): ahí está la gracia.
             ''',
             desafio='Sumá los puntos con la tabla PREMIO y mostralos abajo de las líneas.',
             pasos=['Buscá `/* acá: más puntos si se borran varias juntas */` y escribí `puntos += PREMIO[borradas];`.',
                    'Buscá `/* acá: mostrar los puntos abajo de las líneas */` y escribí el texto de la sugerencia.',
                    'Tocá **Jugar** y borrá la fila de escombros. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 3', estado='textos',
             superarla='''
             **PUNTOS 100**. Kira ya está mirando el pozo con otros ojos: deja un hueco largo a la derecha, esperando el
             palo celeste. Arcadia sonríe: —Ya pensás como la Torre.
             ''',
             imagen=['La pantalla de la máquina con el pozo, las piezas apiladas dejando un hueco largo a la derecha y dos contadores blancos (sin letras legibles).',
                     'Kira mira el pozo, estratega, con la mano en el mentón; Arcadia sonríe.',
                     'Gheco sostiene un palo de bloques celestes de verdad, listo para tirarlo.']),
    ],
)
