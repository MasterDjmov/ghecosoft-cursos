import motor
import n01

PLANTILLA = motor.crecer(motor.full(n01.PLANTILLA), [
    ('''
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */
''', '''
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */

/* ¿La pieza cabe con su cajita en la columna px y la fila py? */
static bool cabe(int pieza[4][4], int tablero[FILAS][COLS], int px, int py)
{
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            if (pieza[f][c] == 1) {
                int x = px + c;    /* la casilla del pozo donde caería este bloque */
                int y = py + f;
                //@ n1: acá: no cabe si el bloque se sale por un costado
                if (x < 0 || x >= COLS) {
                    return false;
                }
                //@ end
                //@ n2: acá: ni si se sale por abajo
                if (y >= FILAS) {
                    return false;
                }
                //@ end
                //@ n4: acá: ni si pisa un bloque que ya está en el pozo
                if (tablero[y][x] != 0) {
                    return false;
                }
                //@ end
            }
        }
    }
    return true;
}
'''),
    ('''
                if (evento.key.key == SDLK_LEFT) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT) {
                    px++;
                }''', '''
                //@ n1: acá: moverse solo si la pieza cabe en la columna de al lado
                if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                //@ else
                if (evento.key.key == SDLK_LEFT) {
                    px--;
                }
                if (evento.key.key == SDLK_RIGHT) {
                    px++;
                }
                //@ end'''),
    ('''
            reloj -= caida;
            py++;''', '''
            reloj -= caida;
            //@ n2: acá: bajar solo si la pieza cabe una fila más abajo
            if (cabe(pieza, tablero, px, py + 1)) {
                py++;
            }
            //@ else
            py++;
            //@ end
            //@ n3: acá: si ya no puede bajar, se queda en el pozo y sale otra arriba
            if (!cabe(pieza, tablero, px, py + 1)) {
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        if (pieza[f][c] == 1) {
                            tablero[py + f][px + c] = 1;
                        }
                    }
                }
                px = 3;
                py = 0;
            }
            //@ end'''),
])

NODO = dict(
    codigo='R05-N02', titulo='Chocar y quedarse', criatura='atraviesaparedes', padre='R05-N01',
    lugar='La Torre que no para',
    temas='prog.funciones', usa='col.matrices, juegos.colisiones, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    La T baja, Kira la corre a un costado… y la pieza sigue de largo, atraviesa la pared del pozo y se pierde fuera de
    la pantalla. La siguiente atraviesa el piso. Desde la máquina asoma, como si fuera de gelatina, el
    **Atraviesaparedes**: se ríe mientras pasa de un lado al otro del vidrio. —Una pieza tiene que chocar —dice
    {mentor}—: con las paredes, con el piso y con las que ya están. Y cuando no puede bajar más, se queda.
    ''',
    objetivos='''
    Escribir una **función** que pregunta si la pieza **cabe** en un lugar (sin salirse del pozo ni pisar otro bloque),
    usarla para que las paredes y el piso la frenen, **fijar** la pieza en el pozo cuando ya no puede bajar y sacar
    otra arriba, para que las piezas **se apilen**.
    ''',
    antes='''
    El nodo anterior. De R04: la función `libre` del jefe, que preguntaba si una celda estaba libre (N05). Del curso de
    C: las funciones que devuelven `bool` y las matrices como parámetro.
    ''',
    explicacion='''
    #### Preguntar antes de mover
    En el Pong o el Arkanoid, la pelota se movía y **después** se veía si chocaba. En el Tetris es al revés: antes de
    mover la pieza se pregunta **si va a caber** en el lugar nuevo. Si cabe, se mueve; si no, se queda donde está. Así
    nunca queda metida adentro de nada.

    #### La función `cabe`
    `cabe(pieza, tablero, px, py)` recorre los 16 lugares de la cajita y, por cada bloque (cada 1), calcula en qué
    casilla del pozo caería: columna `x = px + c` y fila `y = py + f`. Contesta `false` apenas encuentra un bloque que:
    - se sale por un costado (`x < 0` o `x >= COLS`);
    - se sale por abajo (`y >= FILAS`);
    - o cae en una casilla ocupada (`tablero[y][x] != 0`).

    Si revisa los cuatro bloques y ninguno molesta, contesta `true`. Es como la `libre` del Snake, pero para cuatro
    bloques a la vez.

    #### Una matriz como parámetro
    `int tablero[FILAS][COLS]` en los paréntesis de la función le dice que recibe la matriz entera. Como con los
    arreglos, no se copia: la función mira el mismo tablero del `main`.

    #### Fijar la pieza
    Cuando la pieza **no cabe una fila más abajo**, llegó: se copia al pozo. Cada bloque de la cajita pone un 1 en
    su casilla del tablero, y desde ese momento el pozo lo dibuja (celeste). Después sale otra pieza arriba, en la
    columna 3 y la fila 0.
    ''',
    para_que='''
    «Preguntar antes de mover» es la forma más segura de hacer chocar cosas en una grilla: el Pac-Man contra las paredes
    del laberinto y el personaje de un juego de tablero contra los obstáculos se hacen igual.
    ''',
    errores='''
    **Mover y después preguntar.** Si primero se hace `px--` y después se mira, la pieza ya quedó adentro de la pared.

    **Preguntar por el lugar de ahora.** Para bajar hay que preguntar por `py + 1`, no por `py`: el lugar donde
    **va a estar**.

    **Revisar los ceros.** La cajita tiene ceros que se pueden salir del pozo sin problema: solo importan los bloques.
    Por eso todo va adentro de `if (pieza[f][c] == 1)`.

    **Atraviesaparedes: el `return true` adentro del `for`.** Si contesta `true` después de mirar el primer bloque, los
    otros tres pueden estar adentro de la pared. El `true` va al final, cuando ya revisó todos.
    ''',
    misiones=[
        dict(titulo='Las paredes del pozo',
             carta='Función cabe | si x < 0 o x >= COLS: return false · flecha: moverse solo si cabe(…, px ± 1, py)',
             criatura='atraviesaparedes',
             escena='''
             Kira corre la T a la izquierda, otra vez, y otra… y la pieza atraviesa la pared del pozo como si fuera de aire.
             El Atraviesaparedes se asoma del otro lado y le saca la lengua.
             ''',
             gheco='''
             Ya está la función `cabe`: recorre los bloques de la cajita y calcula la casilla `x`, `y` de cada uno. Dos
             cosas:
             1. **Que conteste `false` si un bloque se sale por un costado:**
             ```c
             if (x < 0 || x >= COLS) {
                 return false;
             }
             ```
             2. **Que las flechas pregunten antes de mover**, por la columna de al lado:
             ```c
             if (evento.key.key == SDLK_LEFT && cabe(pieza, tablero, px - 1, py)) {
                 px--;
             }
             if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                 px++;
             }
             ```
             Si la pieza no cabe una columna más allá, la flecha no hace nada. El robot va a apretar la flecha de la
             izquierda cinco veces.
             ''',
             desafio='Hacé que las paredes del pozo frenen la pieza: moverse solo si cabe en la columna de al lado.',
             pasos=['Buscá `/* acá: no cabe si el bloque se sale por un costado */` (en la función `cabe`) y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: moverse solo si la pieza cabe en la columna de al lado */` y cambiá los dos `if` de las flechas por los de la sugerencia.',
                    'Tocá **Jugar** y llevá la T contra una pared. Después, **Comprobar**.'],
             eventos='tecla Izquierda\ntecla Izquierda\ntecla Izquierda\ntecla Izquierda\ntecla Izquierda\ncuadros 2',
             estado='buscar #aa50ff',
             superarla='''
             La T llega a la pared y se frena en seco. Kira aprieta la flecha diez veces más: nada, ni un píxel. El
             Atraviesaparedes empuja desde afuera, pero no puede entrar.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta en T pegada a la pared izquierda del pozo.',
                     'Una criatura de gelatina translúcida empuja el vidrio de la pantalla desde afuera, sin poder pasar.',
                     'Kira aprieta la flecha muchas veces; Arcadia se ríe; Gheco empuja la pared del pozo con las dos patas.']),
        dict(titulo='El piso',
             carta='Bajar si cabe | si y >= FILAS: return false · bajar solo si cabe(…, px, py + 1)',
             criatura='atraviesaparedes',
             escena='''
             La T baja, baja… y sigue de largo por el fondo del pozo, como si no tuviera piso. El Atraviesaparedes aparece
             debajo de la máquina con la pieza en la mano.
             ''',
             gheco='''
             Igual que las paredes, pero para abajo. Dos cosas:
             1. **En `cabe`, que un bloque tampoco se salga por abajo:**
             ```c
             if (y >= FILAS) {
                 return false;
             }
             ```
             2. **Bajar solo si cabe una fila más abajo** (en el reloj, en lugar del `py++` solo):
             ```c
             if (cabe(pieza, tablero, px, py + 1)) {
                 py++;
             }
             ```
             La última fila es la 19: un bloque en la fila 20 ya se salió. El robot va a esperar 12 segundos, más de lo
             que tarda en llegar al fondo.
             ''',
             desafio='Hacé que la pieza se frene en el fondo del pozo: bajar solo si cabe una fila más abajo.',
             pasos=['Buscá `/* acá: ni si se sale por abajo */` (en la función `cabe`) y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: bajar solo si la pieza cabe una fila más abajo */` y borrá el `py++;` de abajo.',
                    'En su lugar, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y dejá que la T llegue al fondo. Después, **Comprobar**.'],
             eventos='cuadros 720', estado='buscar #aa50ff',
             superarla='''
             La T llega al fondo y se queda ahí, apoyada, como una pieza de verdad sobre una mesa. El Atraviesaparedes
             golpea el piso del pozo desde abajo: *toc, toc*. No pasa.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta en T apoyada en el fondo del pozo.',
                     'Debajo de la máquina, una criatura de gelatina translúcida golpea el piso con el puño, sin poder pasar.',
                     'Kira se agacha a mirar; Arcadia sonríe; Gheco se sienta arriba de la máquina, tranquilo.']),
        dict(titulo='Se queda y sale otra',
             carta='Fijar | si no cabe(…, px, py + 1): cada bloque pone un 1 en tablero[py + f][px + c] · otra pieza en px = 3, py = 0',
             escena='''
             La T llegó al fondo y ahí se quedó… para siempre. No sale ninguna otra. —Cuando una pieza ya no puede bajar,
             se vuelve parte de la torre —dice {mentor}—. Y arriba aparece la siguiente.
             ''',
             gheco='''
             Después de bajar (o de intentarlo), se pregunta si todavía puede bajar otra fila. Si no puede, llegó:
             ```c
             if (!cabe(pieza, tablero, px, py + 1)) {
                 for (int f = 0; f < 4; f++) {
                     for (int c = 0; c < 4; c++) {
                         if (pieza[f][c] == 1) {
                             tablero[py + f][px + c] = 1;   /* el bloque pasa a ser del pozo */
                         }
                     }
                 }
                 px = 3;    /* y sale otra pieza arriba */
                 py = 0;
             }
             ```
             - `!` da vuelta la respuesta: «si **no** cabe».
             - Cada bloque pone un 1 en su casilla del pozo; el pozo dibuja los 1 en celeste.
             - Volver la cajita a la columna 3 y la fila 0 es sacar una pieza nueva (por ahora, siempre la T).
             ''',
             desafio='Hacé que la pieza se quede en el pozo cuando ya no puede bajar, y que salga otra arriba.',
             pasos=['Buscá `/* acá: si ya no puede bajar, se queda en el pozo y sale otra arriba */` (en el reloj).',
                    'Debajo, escribí el `if` de la sugerencia, con los dos `for` que copian la pieza al tablero.',
                    'Tocá **Jugar** y esperá a que llegue al fondo. Después, **Comprobar**.'],
             eventos='cuadros 600', estado='buscar #00dcff',
             superarla='''
             La T toca el fondo, se pone celeste y se queda. Arriba ya asoma otra T violeta, lista para bajar. Desde lo alto
             de la torre se oye un *clonc* contento: un piso más.
             ''',
             imagen=['La pantalla de la máquina con una pieza celeste en el fondo del pozo y una violeta nueva arriba.',
                     'Desde lo alto de la torre cae un bloque de colores que se acomoda con chispitas.',
                     'Kira festeja con el puño; Arcadia mira la torre; Gheco imita la forma de T con el cuerpo.']),
        dict(titulo='Una arriba de la otra',
             carta='Apilar | en cabe: si tablero[y][x] != 0: return false (la casilla ya está ocupada)',
             criatura='atraviesaparedes',
             escena='''
             La segunda T baja… y se mete adentro de la primera, como si fuera un fantasma. Las dos quedan encimadas en el
             fondo. El Atraviesaparedes, desde adentro del pozo, se frota las manos.
             ''',
             gheco='''
             A `cabe` le falta la última pregunta: si la casilla ya tiene un bloque. Va después de la del piso, cuando ya
             se sabe que `x` e `y` están adentro del pozo:
             ```c
             if (tablero[y][x] != 0) {
                 return false;
             }
             ```
             ¿Por qué después? Porque si `y` fuera 20, `tablero[20]` no existe. Primero se mira que esté adentro y recién
             después se mira la casilla.

             Como las flechas, la caída y el fijar usan `cabe`, con esto ya chocan todas. El robot va a esperar a que caigan
             dos piezas.
             ''',
             desafio='Hacé que la pieza no pueda meterse en una casilla ocupada, para que las piezas se apilen.',
             pasos=['Buscá `/* acá: ni si pisa un bloque que ya está en el pozo */` (en la función `cabe`).',
                    'Debajo, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y esperá dos piezas: la segunda tiene que quedar arriba. Después, **Comprobar**.'],
             eventos='cuadros 1100', estado='pixel 282 394',
             superarla='''
             La segunda T baja y se apoya **arriba** de la primera, encajada. Después una tercera, y una cuarta. El
             Atraviesaparedes se queda atrapado entre dos piezas, se escurre como gelatina y se va.
             ''',
             imagen=['La pantalla de la máquina con varias piezas en T apiladas en el fondo del pozo, una arriba de la otra.',
                     'Una criatura de gelatina translúcida se escurre entre dos bloques y huye.',
                     'Kira, Arcadia y Gheco miran la pila crecer, contentos.']),
    ],
)
