import motor
import n02

PLANTILLA = motor.crecer(motor.full(n02.PLANTILLA), [
    ('''
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10''', '''
    SDL_FRect caja;
    bool vivo;
    int fila;     /* 0 es la de arriba */
    int golpes;   /* cuántos golpes le faltan para romperse */
} Ladrillo;

#define COLUMNAS 10
#define FILAS 5'''),
    ('''
    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }''', '''
    Ladrillo pared[FILAS * COLUMNAS] = { 0 };   /* 5 filas de 10: 50 ladrillos */
    //@ n1: acá: armar la pared: cinco filas de diez, con dos for
    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    //@ else
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    //@ end
    //@ n4: acá: la fila de abajo es de metal: necesita dos golpes
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    //@ end
    //@ n2+
    SDL_Color colores[FILAS] = {
        { 255, 60, 100, 255 },    /* rosa */
        { 255, 150, 40, 255 },    /* naranja */
        { 80, 220, 100, 255 },    /* verde */
        { 150, 100, 255, 255 },   /* violeta */
        { 180, 180, 200, 255 },   /* metal */
    };
    //@ end'''),
    ('''
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                pared[i].vivo = false;
                vy = -vy;
                puntos += 10;''', '''
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                //@ n4: acá: un golpe menos; se rompe cuando no le quedan
                pared[i].golpes--;
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }
                //@ else
                pared[i].vivo = false;
                //@ end
                vy = -vy;
                //@ n3: acá: más puntos cuanto más arriba esté la fila
                puntos += 10 * (FILAS - pared[i].fila);
                //@ else
                puntos += 10;
                //@ end'''),
    ('''
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);''', '''
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                //@ n2: acá: pintarlo con el color de su fila
                SDL_Color color = colores[pared[i].fila];
                SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
                //@ end
                SDL_RenderFillRect(lapiz, &pared[i].caja);'''),
])

NODO = dict(
    codigo='R03-N03', titulo='La pared entera', criatura='glitch', padre='R03-N02',
    lugar='El Muro de Ladrillos',
    temas='col.matrices', usa='col.registros, col.arrays, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    Una fila sola se rompe en un minuto. {mentor} señala el paredón de la plaza: cinco hileras de vidrio de
    colores, una arriba de la otra, y la de abajo, gris, de metal. —Así era el Muro de verdad —dice—. Rosa,
    naranja, verde, violeta y metal. Y cuanto más arriba, más difícil llegar, así que más puntos. Sobre la
    pantalla, un **glitch** pinta todos los ladrillos del mismo color y se ríe.
    ''',
    objetivos='''
    Pasar de una fila a una **pared de cinco filas** con dos `for` (uno adentro del otro), pintar **cada fila de su
    color** con un arreglo de colores, dar **más puntos** a las filas de arriba y hacer la fila de abajo **de metal**:
    necesita dos golpes.
    ''',
    antes='''
    R03-N02 (un arreglo de `struct`, armar con `for`, romper y `break`). Del curso de C: los `for` anidados.
    ''',
    explicacion='''
    #### Dos `for`, uno adentro del otro
    Para recorrer filas y columnas se pone un `for` adentro de otro. El de afuera elige la fila (`f`, de 0 a 4) y,
    para cada fila, el de adentro recorre las columnas (`c`, de 0 a 9). El cuerpo se repite 5 × 10 = 50 veces.

    #### Una pared en un arreglo largo
    Los 50 ladrillos van en un solo arreglo, `pared[FILAS * COLUMNAS]`, fila por fila: primero los 10 de la fila
    0, después los 10 de la fila 1… El ladrillo de la fila `f` y la columna `c` es el número `f * COLUMNAS + c`. Por
    ejemplo, fila 2, columna 3: `2 * 10 + 3 = 23`. Así, chocar y dibujar sigue siendo **un solo `for`** (y el
    `break` sigue funcionando).

    #### Cada fila, más abajo
    La `y` de cada fila es `60 + f * 24`: 20 de alto del ladrillo y 4 de junta. Cada ladrillo guarda también su
    `fila`, porque después la vamos a necesitar para su color y sus puntos.

    #### Un arreglo de colores
    `SDL_Color` es un `struct` de SDL con `r`, `g`, `b` y `a`. Un arreglo con un color por fila, y al dibujar, el
    ladrillo usa `colores[pared[i].fila]`.

    #### Los ladrillos de metal
    Un dato más en el `struct`: `golpes`, cuántos le faltan para romperse. Los de la fila de abajo arrancan con 2 y
    los demás con 1. En cada golpe se le resta uno, y se rompe recién cuando llega a 0.
    ''',
    para_que='''
    Recorrer filas y columnas con dos `for` es la base de todo lo que es una **grilla**: el tablero del Tetris, el
    laberinto del Pac-Man, los mapas de baldosas de un juego de plataformas.
    ''',
    errores='''
    **Mezclar filas y columnas.** `c * COLUMNAS + f` da números repetidos y ladrillos encimados. Es la fila por el
    ancho, más la columna: `f * COLUMNAS + c`.

    **Glitch: todos del mismo color.** Si `SDL_SetRenderDrawColor` va antes del `for`, todos salen del último color
    elegido. Cada ladrillo elige el suyo adentro del `for`.

    **Romper el metal de una.** Si se deja `vivo = false` sin mirar los `golpes`, el metal se rompe como los demás.

    **Recorrer solo diez.** Si un `for` quedó con `i < COLUMNAS`, solo mira la fila de arriba: la pelota atraviesa
    las otras cuatro.
    ''',
    misiones=[
        dict(titulo='Cinco filas',
             carta='Grilla con dos for | i = f * COLUMNAS + c · y = 60 + f * 24 · pared[i].fila = f',
             escena='''
             {mentor} trae una escalera y la apoya en el paredón. —Cinco hileras de diez —dice—. No las vamos a
             escribir de a una: una vuelta por fila, y en cada fila, una vuelta por ladrillo.
             ''',
             gheco='''
             El arreglo ya tiene lugar para 50 ladrillos (`FILAS * COLUMNAS`). Cambiá el `for` de la fila por dos,
             uno adentro del otro:
             ```c
             for (int f = 0; f < FILAS; f++) {            /* cada fila */
                 for (int c = 0; c < COLUMNAS; c++) {     /* cada ladrillo de esa fila */
                     int i = f * COLUMNAS + c;            /* su número en el arreglo */
                     pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
                     pared[i].vivo = true;
                     pared[i].fila = f;
                 }
             }
             ```
             - `i = f * COLUMNAS + c`: la fila 0 usa del 0 al 9, la fila 1 del 10 al 19, y así.
             - `60 + f * 24`: cada fila, 24 píxeles más abajo (20 del ladrillo y 4 de junta).
             - Cada uno guarda su `fila`, que vamos a usar para el color.
             ''',
             desafio='Armá la pared de cinco filas de diez ladrillos con dos for.',
             pasos=['Buscá `/* acá: armar la pared: cinco filas de diez, con dos for */` y borrá el `for` de abajo (el de una sola fila).',
                    'En su lugar, escribí los dos `for` de la sugerencia.',
                    'Tocá **Jugar**: tienen que aparecer cinco filas. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #ff3c64',
             superarla='''
             Cinco filas rosadas se encienden una debajo de la otra. En la plaza, el paredón entero tiembla y se
             ilumina de arriba abajo. —Ahora sí es un muro —dice {mentor}.
             ''',
             imagen=['La pantalla de la máquina con una pared de cinco filas de ladrillos rosados, todas iguales.',
                     'Arcadia, subida a una escalera, encaja ladrillos de vidrio en el paredón de la plaza; Kira le alcanza uno.',
                     'Gheco, en la palma de Kira, cuenta las filas con la cola.']),
        dict(titulo='Un color por fila',
             carta='Colores por fila | SDL_Color color = colores[pared[i].fila] · SetRenderDrawColor con color.r, .g, .b',
             criatura='glitch',
             escena='''
             La pared entera es rosada. Un glitch salta de ladrillo en ladrillo, pintándolos todos igual. —Así no se
             sabe cuál es cuál —dice {mentor}—. Cada fila tenía su color.
             ''',
             gheco='''
             Ya está el arreglo `colores`, con un `SDL_Color` por fila (rosa, naranja, verde, violeta y metal).
             `SDL_Color` es un `struct` de SDL con cuatro números: `r`, `g`, `b` y `a`.

             Al dibujar, antes de pintar cada ladrillo vivo, elegí el color de **su** fila:
             ```c
             SDL_Color color = colores[pared[i].fila];
             SDL_SetRenderDrawColor(lapiz, color.r, color.g, color.b, 255);
             ```
             Va adentro del `for`, porque cada ladrillo tiene que elegir el suyo.
             ''',
             desafio='Pintá cada ladrillo con el color de su fila.',
             pasos=['Buscá `/* acá: pintarlo con el color de su fila */` (adentro del `for` que dibuja).',
                    'Debajo, escribí las dos líneas de la sugerencia.',
                    'Tocá **Jugar** y mirá los colores. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #50dc64',
             superarla='''
             Rosa, naranja, verde, violeta y gris metal: la pared se enciende como un arcoíris. El glitch intenta
             pintarla de nuevo y se le acaba la pintura. Se deshace en píxeles.
             ''',
             imagen=['La pantalla con la pared de cinco filas: rosa, naranja, verde, violeta y gris metal.',
                     'Un glitch pixelado con un pincel se deshace en píxeles al costado de la pantalla.',
                     'Kira sonríe; Arcadia mira el paredón de la plaza, que se ilumina de colores; Gheco aplaude.']),
        dict(titulo='Más arriba, más puntos',
             carta='Puntos por fila | puntos += 10 * (FILAS - pared[i].fila)',
             escena='''
             —Romper uno de abajo y uno de arriba vale lo mismo —protesta Kira—. ¡Y los de arriba son mucho más
             difíciles! {mentor} asiente. —Tenés razón. Cuanto más arriba, más puntos.
             ''',
             gheco='''
             Cada ladrillo sabe su `fila`: 0 es la de arriba y 4 la de abajo. Si se hace `FILAS - fila`, la de arriba
             da 5 y la de abajo da 1. Por 10:
             ```c
             puntos += 10 * (FILAS - pared[i].fila);
             ```
             | Fila | Color | Puntos |
             |---|---|---|
             | 0 | rosa | 50 |
             | 1 | naranja | 40 |
             | 2 | verde | 30 |
             | 3 | violeta | 20 |
             | 4 | metal | 10 |

             El robot va a sacar dos veces por el mismo lugar: la primera rompe uno de abajo y la segunda, el de
             arriba de ese.
             ''',
             desafio='Hacé que cada ladrillo dé más puntos cuanto más arriba esté su fila.',
             pasos=['Buscá `/* acá: más puntos cuanto más arriba esté la fila */` y borrá la línea `puntos += 10;`.',
                    'En su lugar, escribí `puntos += 10 * (FILAS - pared[i].fila);`.',
                    'Tocá **Jugar**, rompé un ladrillo de abajo y otro más arriba. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 200\ntecla Espacio\ncuadros 90', estado='textos',
             superarla='''
             El de metal da 10 y el violeta de arriba, 20. Kira ya está calculando cómo meter la pelota hasta la
             fila rosa. —Cincuenta cada uno —dice, con los ojos brillando.
             ''',
             imagen=['La pantalla con la pared de colores y un hueco que sube por dos filas; el puntaje blanco arriba.',
                     'Kira apunta hacia la fila rosa de arriba con el dedo, decidida.',
                     'Arcadia sonríe; Gheco, sobre la máquina, levanta cinco dedos.']),
        dict(titulo='La fila de metal',
             carta='Dos golpes | golpes = 2 en la fila de abajo · golpes-- · si llega a 0: vivo = false',
             escena='''
             {mentor} golpea con los nudillos la fila de abajo del paredón: suena a lata. —Estos son de metal —dice—.
             Con un golpe se abollan; con dos, se rompen.
             ''',
             gheco='''
             El `struct` ya tiene `golpes`: cuántos golpes le faltan a cada ladrillo. Dos cosas:
             1. **Al armar la pared**, después de los dos `for`: los de la fila de abajo arrancan con 2 y el resto con 1.
             ```c
             for (int i = 0; i < FILAS * COLUMNAS; i++) {
                 pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
             }
             ```
             `condición ? a : b` vale `a` si la condición es verdadera y `b` si no (lo usaste en el Pong).
             2. **Al chocar**, en lugar de romperlo directo, se le resta un golpe y se rompe si ya no le quedan:
             ```c
             pared[i].golpes--;
             if (pared[i].golpes == 0) {
                 pared[i].vivo = false;
             }
             ```
             La pelota rebota igual, se rompa o no.
             ''',
             desafio='Hacé que los ladrillos de la fila de abajo necesiten dos golpes para romperse.',
             pasos=['Buscá `/* acá: la fila de abajo es de metal: necesita dos golpes */` (antes del bucle) y escribí el `for` que reparte los golpes.',
                    'Buscá `/* acá: un golpe menos; se rompe cuando no le quedan */` y borrá la línea `pared[i].vivo = false;` de abajo.',
                    'En su lugar, escribí `pared[i].golpes--;` y el `if` de la sugerencia.',
                    'Tocá **Jugar** y pegale a uno de metal. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 80', estado='pixel 470 166',
             superarla='''
             *¡Clonc!* La pelota pega en el metal y rebota, pero el ladrillo sigue ahí. Al segundo golpe, se rompe con
             un ruido de lata. Gheco se tapa los oídos. —Ahora el muro se defiende —dice {mentor}, contenta.
             ''',
             imagen=['La pelota amarilla rebota en un ladrillo gris de metal de la fila de abajo, que queda entero, con una chispa.',
                     'Arcadia golpea con los nudillos la fila de metal del paredón de la plaza; Kira escucha.',
                     'Gheco, sobre la máquina, se tapa los oídos.']),
    ],
)
