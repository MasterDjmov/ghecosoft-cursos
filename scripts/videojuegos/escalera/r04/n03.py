import motor
import n02

PLANTILLA = motor.crecer(motor.full(n02.PLANTILLA), [
    ('''
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */''', '''
    float paso = 0.15f;    /* cada cuántos segundos avanza una celda */
    int fx = 20;           /* la fruta: columna y fila */
    int fy = 12;
    //@ n2+
    int puntos = 0;
    //@ end'''),
    ('''
        cy[0] = (cy[0] + FILAS) % FILAS;''', '''
        cy[0] = (cy[0] + FILAS) % FILAS;

        /* ¿la cabeza llegó a la fruta? */
        if (cx[0] == fx && cy[0] == fy) {
            //@ n2: acá: un punto y una fruta nueva en un lugar al azar
            puntos++;
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            //@ end
            //@ n3: acá: crecer: una parte nueva, encima de la última
            cx[largo] = cx[largo - 1];
            cy[largo] = cy[largo - 1];
            largo++;
            //@ end
            //@ n4: acá: cada fruta, un poco más rápido (con un tope)
            paso = SDL_max(0.06f, paso * 0.9f);
            //@ end
        }'''),
    ('''
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte''', '''
        //@ n1: acá: dibujar la fruta en su celda, roja
        SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
        SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);
        SDL_RenderFillRect(lapiz, &fruta);
        //@ end
        for (int i = 0; i < largo; i++) {
            SDL_FRect parte'''),
    ('''
        SDL_RenderPresent(lapiz);''', '''
        //@ n2: acá: los puntos arriba a la izquierda
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        //@ end
        SDL_RenderPresent(lapiz);'''),
])

NODO = dict(
    codigo='R04-N03', titulo='La fruta y crecer', criatura='fuga_texturas', padre='R04-N02',
    lugar='El Jardín de la Serpiente',
    usa='col.arrays, prog.matematica-azar, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    La serpiente ya pasea por el jardín, pero no tiene para qué. {mentor} arranca una fruta roja de vidrio de un
    arbolito y la deja en el caminito. —En el Snake se juega a comer —dice—. Cada fruta, un punto. Y cada fruta,
    la serpiente crece un anillo. Cuanto más larga, más difícil no morderse. Sobre las flores flota una niebla de
    frutas repetidas, todas iguales: la **Fuga de Texturas**, que dibuja cada fruta mil veces sin borrar ninguna.
    ''',
    objetivos='''
    Poner una **fruta** en una celda, que la serpiente **se la coma** (un punto y una fruta nueva en un lugar al
    azar), que **crezca** un anillo con cada fruta y que vaya **cada vez más rápido**, sin pasarse de un tope.
    ''',
    antes='''
    R04-N02 (la cola). De R01: el azar con `SDL_rand` (N10). De R03: la pelota que se apura con un tope (N04).
    ''',
    explicacion='''
    #### La fruta
    Una celda más, con su columna `fx` y su fila `fy`. Arranca en `(20, 12)`, justo en el camino de la serpiente,
    para que la primera sea fácil. Se dibuja igual que una parte de la serpiente, pero roja.

    #### Comer
    La cabeza se come la fruta cuando están **en la misma celda**: `cx[0] == fx && cy[0] == fy`. En la grilla no
    hace falta la prueba de los dos rectángulos: alcanza con comparar dos números. Se suma un punto y la fruta pasa a
    otra celda al azar: `SDL_rand(COLS)` da una columna de 0 a 31 y `SDL_rand(FILAS)` una fila de 0 a 23.

    #### Crecer
    La parte nueva aparece **encima de la última** (`cx[largo] = cx[largo - 1]`) y recién después se suma uno a
    `largo`. En el paso siguiente, todo el cuerpo se corre y la última parte se queda donde estaba: la parte nueva
    queda atrás, en la punta de la cola. Así la serpiente crece sin que se vea ningún salto.

    #### Cada vez más rápido
    Con cada fruta, `paso` se multiplica por 0,9 (un 10 % menos de espera entre pasos). `SDL_max(0.06f, …)` lo frena
    en 0,06 segundos: más rápido que eso, nadie podría doblar a tiempo.
    ''',
    para_que='''
    Comparar celdas para saber si dos cosas se tocan, poner premios al azar y hacer que el juego se acelere a medida
    que ganás son tres ideas que vas a usar en todos los juegos de tablero y de laberinto.
    ''',
    errores='''
    **Crecer sin copiar la última parte.** Si solo se hace `largo++`, la parte nueva tiene lo que haya en el arreglo
    (un 0): aparece un cuadradito suelto en el rincón por un instante.

    **Usar `SDL_rand(32)` a mano.** Funciona, pero si mañana cambiás el tamaño de la grilla, la fruta puede caer
    afuera. Mejor `SDL_rand(COLS)`.

    **Acelerar sin tope.** Después de 30 frutas, `paso` sería tan chico que la serpiente cruzaría la pantalla en un
    segundo.

    **Fuga de Texturas.** Si se dibujara la fruta cargando una imagen nueva en cada cuadro sin liberarla, la memoria
    se llenaría. Acá se dibuja un rectángulo: no hay nada que liberar.
    ''',
    misiones=[
        dict(titulo='Una fruta en el camino',
             carta='Dibujar la fruta | SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA } · roja',
             escena='''
             {mentor} deja la fruta de vidrio en el caminito, justo delante de la serpiente. En la pantalla, en cambio,
             no hay nada. —La máquina sabe dónde está —dice—, pero no la dibuja.
             ''',
             gheco='''
             Ya están `fx` y `fy`: la columna y la fila de la fruta (20 y 12, en el camino). Se dibuja como una parte de
             la serpiente, pasando de celda a píxeles, pero roja. Va **antes** de la serpiente, para que la serpiente
             quede arriba cuando pasa:
             ```c
             SDL_FRect fruta = { fx * CELDA, fy * CELDA, CELDA, CELDA };
             SDL_SetRenderDrawColor(lapiz, 255, 70, 90, 255);   /* rojo frutilla */
             SDL_RenderFillRect(lapiz, &fruta);
             ```
             ''',
             desafio='Dibujá la fruta roja en su celda, antes que la serpiente.',
             pasos=['Buscá `/* acá: dibujar la fruta en su celda, roja */`.',
                    'Debajo, escribí las tres líneas de la sugerencia.',
                    'Tocá **Jugar**: tiene que aparecer la fruta en el camino. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #ff465a',
             superarla='''
             Un cuadradito rojo se enciende en el camino de la serpiente. Gheco se relame. —Esa no es para vos —le dice
             Kira, riéndose.
             ''',
             imagen=['La pantalla con la grilla verde, la serpiente en fila y un cuadradito rojo más adelante, en su camino.',
                     'Arcadia deja una fruta roja de vidrio en el caminito del jardín; Kira mira la pantalla.',
                     'Gheco se relame mirando la fruta, sentado arriba de la máquina.']),
        dict(titulo='¡A comer!',
             carta='Comer | si cx[0] == fx y cy[0] == fy: puntos++ · fx = SDL_rand(COLS) · fy = SDL_rand(FILAS)',
             escena='''
             La serpiente pasa por encima de la fruta y la fruta sigue ahí, como si fuera de vidrio de verdad. —Tiene que
             comérsela —dice {mentor}—. Y después, que aparezca otra en cualquier lado.
             ''',
             gheco='''
             Ya está el `if` que pregunta si la cabeza está en la misma celda que la fruta: `cx[0] == fx && cy[0] == fy`.
             En la grilla alcanza con comparar números. Adentro falta lo que pasa al comer:
             ```c
             puntos++;                 /* un punto más */
             fx = SDL_rand(COLS);      /* una columna al azar, de 0 a 31 */
             fy = SDL_rand(FILAS);     /* una fila al azar, de 0 a 23 */
             ```
             Y los puntos, arriba a la izquierda:
             ```c
             SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
             ```
             ''',
             desafio='Hacé que la serpiente se coma la fruta: un punto y una fruta nueva en un lugar al azar.',
             pasos=['Buscá `/* acá: un punto y una fruta nueva en un lugar al azar */` (adentro del `if` de la fruta) y escribí las tres líneas.',
                    'Buscá `/* acá: los puntos arriba a la izquierda */` y escribí las dos líneas de los puntos.',
                    'Tocá **Jugar** y dejá que la serpiente llegue a la fruta. Después, **Comprobar**.'],
             eventos='cuadros 160', estado='textos',
             superarla='''
             *¡Ñam!* La fruta desaparece, arriba se enciende **PUNTOS 1** y otra fruta aparece en otra punta del jardín.
             Kira ya está doblando para ir a buscarla.
             ''',
             imagen=['La pantalla con la serpiente verde comiéndose la fruta roja con unas chispitas, y otra fruta roja lejos.',
                     'Kira dobla con las flechas, decidida; Arcadia aplaude.',
                     'Gheco, sentado arriba de la máquina, hace como que mastica.']),
        dict(titulo='Un anillo más',
             carta='Crecer | cx[largo] = cx[largo - 1] · cy[largo] = cy[largo - 1] · largo++',
             escena='''
             La serpiente come y come, pero sigue igual de cortita. —En el Snake, cada fruta es un anillo más —dice
             {mentor}, y engancha un anillo de vidrio nuevo en la cola de la serpiente del caminito.
             ''',
             gheco='''
             Crecer es sumar una parte al final. La parte nueva aparece **encima de la última** y después se agranda el
             largo:
             ```c
             cx[largo] = cx[largo - 1];   /* la nueva, donde está la última */
             cy[largo] = cy[largo - 1];
             largo++;
             ```
             - `cx[largo]` es el primer lugar libre del arreglo (si hay 5 partes, son de la 0 a la 4: la 5 está libre).
             - En el paso siguiente el cuerpo se corre, pero la parte nueva copia a la que estaba en su mismo lugar:
               así queda atrás, en la punta de la cola.

             Va adentro del `if` de la fruta, después de los puntos.
             ''',
             desafio='Hacé que la serpiente crezca una parte cada vez que come una fruta.',
             pasos=['Buscá `/* acá: crecer: una parte nueva, encima de la última */` (adentro del `if` de la fruta).',
                    'Debajo, escribí las tres líneas de la sugerencia.',
                    'Tocá **Jugar**, comé la fruta y mirá la cola. Después, **Comprobar**.'],
             eventos='cuadros 160', estado='buscar #28be5a',
             superarla='''
             La serpiente se come la fruta y, un paso después, tiene un anillo más en la cola. Kira cuenta: seis. —Cuanto
             más larga, más cuidado —le avisa {mentor}.
             ''',
             imagen=['La pantalla con la serpiente verde un poco más larga, con un anillo nuevo brillando en la punta de la cola.',
                     'Arcadia engancha un anillo de vidrio verde nuevo a la cola de la serpiente de anillos del caminito.',
                     'Kira cuenta con los dedos; Gheco, sobre la máquina, levanta seis dedos.']),
        dict(titulo='Cada vez más rápido',
             carta='Apurar con tope | paso = SDL_max(0.06f, paso * 0.9f)',
             escena='''
             Con diez frutas, Kira juega con una mano. —Muy fácil —dice, y bosteza. {mentor} sonríe: —En el jardín del
             Vidriero, la serpiente se apuraba con cada fruta. Al final había que tener reflejos de gato.
             ''',
             gheco='''
             `paso` es cuánto espera la serpiente entre un paso y otro. Si se achica, va más rápido. Con cada fruta:
             ```c
             paso = SDL_max(0.06f, paso * 0.9f);
             ```
             - `paso * 0.9f` es un 10 % menos de espera: 0,15, después 0,135, después 0,12…
             - `SDL_max(a, b)` da el más grande de los dos: si `paso * 0.9f` baja de 0,06, queda en 0,06. Es el tope:
               más rápido que eso, nadie podría doblar.

             Va adentro del `if` de la fruta. El robot va a dejar que coma la primera y a mirar dónde llega después.
             ''',
             desafio='Hacé que la serpiente vaya un 10 % más rápido con cada fruta, sin bajar de 0,06 segundos por paso.',
             pasos=['Buscá `/* acá: cada fruta, un poco más rápido (con un tope) */`.',
                    'Debajo, escribí la línea con `SDL_max` de la sugerencia.',
                    'Tocá **Jugar** y comé varias frutas: tiene que ir cada vez más rápido. Después, **Comprobar**.'],
             eventos='cuadros 300', estado='buscar #78ff8c',
             superarla='''
             Fruta tras fruta, la serpiente se apura. Kira deja de bostezar y agarra el teclado con las dos manos. La
             niebla de frutas repetidas de la Fuga de Texturas no alcanza a seguirla y se deshace en el aire.
             ''',
             imagen=['La pantalla con una serpiente verde larga avanzando rápido, con líneas de velocidad, hacia una fruta roja.',
                     'Una niebla de frutas repetidas, todas iguales, se deshace en el aire entre las flores.',
                     'Kira juega con las dos manos, concentrada; Arcadia se ríe; Gheco se agarra de la máquina.']),
    ],
)
