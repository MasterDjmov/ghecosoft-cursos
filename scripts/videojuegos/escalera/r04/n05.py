import motor
import n04

PLANTILLA = motor.crecer(motor.full(n04.PLANTILLA), [
    ('''
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */''', '''
#define MAX (COLS * FILAS)   /* lo más larga que puede llegar a ser */
#define MACETAS 6

/* Las macetas del jardín: la columna y la fila de cada una */
static const int MX[MACETAS] = { 8, 23, 8, 23, 15, 26 };
static const int MY[MACETAS] = { 8, 8, 16, 16, 4, 12 };

//@ n2: acá: una función que dice si una celda está libre (sin serpiente ni maceta)
static bool libre(int x, int y, int cx[], int cy[], int largo)
{
    for (int i = 0; i < largo; i++) {
        if (cx[i] == x && cy[i] == y) {
            return false;
        }
    }
    for (int m = 0; m < MACETAS; m++) {
        if (MX[m] == x && MY[m] == y) {
            return false;
        }
    }
    return true;
}
//@ end'''),
    ('''
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);''', '''
    SDL_CreateWindowAndRenderer("La Serpiente Jardinera", 640, 480, 0, &ventana, &lapiz);'''),
    ('''
    enum Estado estado = MENU;''', '''
    enum Estado estado = MENU;
    //@ n3+
    bool hayDorada = false;   /* true: hay una fruta dorada en el jardín */
    int gx = 0;               /* la fruta dorada: columna y fila */
    int gy = 0;
    float relojDorado = 0;    /* cuánto pasó desde que apareció (o desde que se fue) */
    //@ end'''),
    ('''
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);''', '''
            //@ n2: acá: elegir lugares al azar hasta encontrar uno libre
            do {
                fx = SDL_rand(COLS);
                fy = SDL_rand(FILAS);
            } while (!libre(fx, fy, cx, cy, largo));
            //@ else
            fx = SDL_rand(COLS);
            fy = SDL_rand(FILAS);
            //@ end'''),
    ('''
        /* ¿la cabeza llegó a la fruta? */''', '''
        //@ n1: acá: si la cabeza choca una maceta, perdiste
        for (int m = 0; m < MACETAS; m++) {
            if (cx[0] == MX[m] && cy[0] == MY[m]) {
                estado = PERDISTE;
            }
        }
        //@ end

        //@ n3: acá: la fruta dorada: aparece cada 8 segundos, dura 4 y vale 5 puntos
        if (estado == JUGANDO) {
            relojDorado += dt;
            if (!hayDorada && relojDorado >= 8) {
                do {
                    gx = SDL_rand(COLS);
                    gy = SDL_rand(FILAS);
                } while (!libre(gx, gy, cx, cy, largo));
                hayDorada = true;
                relojDorado = 0;
            }
            if (hayDorada && relojDorado >= 4) {
                hayDorada = false;
                relojDorado = 0;
            }
            if (hayDorada && cx[0] == gx && cy[0] == gy) {
                puntos += 5;
                hayDorada = false;
                relojDorado = 0;
            }
        }
        //@ end

        /* ¿la cabeza llegó a la fruta? */'''),
    ('''
        SDL_RenderFillRect(lapiz, &fruta);''', '''
        SDL_RenderFillRect(lapiz, &fruta);
        //@ n3: acá: dibujar la fruta dorada, si hay
        if (hayDorada) {
            SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
            SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
            SDL_RenderFillRect(lapiz, &dorada);
        }
        //@ end
        //@ n1: acá: dibujar las macetas, marrones
        SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);
        for (int m = 0; m < MACETAS; m++) {
            SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
            SDL_RenderFillRect(lapiz, &maceta);
        }
        //@ end'''),
    ('''
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }''', '''
        //@ n4: acá: el cartel del final, centrado: con 15 partes o más, el jardín florece
        if (estado == PERDISTE) {
            const char *cartel = (largo >= 15) ? "EL JARDIN FLORECE" : "TE ENREDASTE";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ else
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        //@ end'''),
])

NODO = dict(
    codigo='R04-N05', titulo='Jefe: La Serpiente Jardinera', tipo='jefe', criatura='glitch', padre='R04-N04',
    lugar='El Jardín de la Serpiente',
    insignia='Sello del Jardín de la Serpiente',
    insignia_descripcion='Despertaste a la Serpiente Jardinera: un Snake entero, con la grilla, la cola que sigue, la fruta al azar en un lugar libre, la fruta dorada, las macetas, el menú, la revancha y el sonido.',
    temas='prog.funciones', usa='juegos.estados, col.arrays, prog.matematica-azar, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Cuando la serpiente de la pantalla llega a doce anillos, las flores de vidrio se apagan todas juntas. Del cantero
    más grande se desenrosca una serpiente de luz enorme, verde y dorada, con un sombrerito de paja de jardinera y una
    regadera colgada de la cola. —¡Por fin alguien que cuida mi jardín! —dice, con voz de abuela contenta—. Treinta
    años sin que nadie juegue. Pero mi jardín tiene macetas, y frutas que se esconden, y frutas de oro que no esperan
    a nadie. Llegá a quince anillos y mis flores se vuelven a encender. Es **la Serpiente Jardinera**, la que el
    Vidriero dejó cuidando el jardín.
    ''',
    objetivos='''
    Terminar el Snake completo contra la Serpiente Jardinera: **macetas** que estorban (chocarlas es perder), una
    **función** que dice si una celda está libre para que la fruta nunca caiga encima de nada, una **fruta dorada**
    que aparece cada tanto y se va si no la agarrás, y un **cartel final centrado** que dice si el jardín floreció.
    ''',
    antes='''
    Toda la rama R04. De R03: el temporizador (N07) y el cartel centrado. Del curso de C: las funciones que devuelven
    `bool` y el `do … while`.
    ''',
    explicacion='''
    #### Las macetas
    Seis macetas en celdas fijas, en dos arreglos constantes `MX` y `MY` (como la serpiente, pero no se mueven). Se
    dibujan marrones y, si la cabeza llega a la celda de una, perdiste: igual que morderse, pero contra una maceta.

    #### Una función que pregunta
    `libre(x, y, …)` devuelve `true` si en la celda `(x, y)` no hay ninguna parte de la serpiente ni ninguna maceta.
    Recorre las dos cosas y, apenas encuentra algo ahí, devuelve `false` (`return` corta la función en el momento).
    Si llega al final sin encontrar nada, devuelve `true`.

    #### Probar hasta que salga bien: `do … while`
    Para poner la fruta, se elige una celda al azar y, **si no está libre, se elige otra**, hasta que salga una libre.
    `do { … } while (condición);` hace el bloque **por lo menos una vez** y lo repite mientras la condición sea
    verdadera. Es justo lo que hace falta: elegir primero, preguntar después.

    #### La fruta dorada
    Un temporizador, `relojDorado`. Cuando junta 8 segundos sin fruta dorada, aparece una en un lugar libre; cuando
    junta 4 con la fruta en el jardín, se va. Si la cabeza la alcanza antes, son 5 puntos.

    #### El cartel del final
    Cuando la partida termina, el cartel depende del largo: con 15 partes o más, «EL JARDIN FLORECE»; si no, «TE
    ENREDASTE». Centrado como siempre: `320 - letras * 4`.
    ''',
    para_que='''
    Una función que responde una pregunta («¿esta celda está libre?») se usa en todos los juegos de grilla: para
    poner enemigos, premios, piezas del Tetris o fantasmas. Y el Snake completo es tu tercer juego entero: lo vas a
    poder bajar y jugar en tu compu.
    ''',
    errores='''
    **La fruta encima de una maceta.** Sin `libre`, la fruta puede caer debajo de una maceta y nadie la puede comer.

    **`while` en lugar de `do … while`.** Con `while (!libre(fx, fy, …))` se pregunta por la fruta vieja antes de
    elegir la nueva. El `do` elige primero.

    **La fruta dorada eterna.** Si no se vuelve el reloj a 0 al aparecer, la fruta dorada desaparece apenas aparece
    (el reloj ya pasaba de 4).

    **Glitch: chocar macetas invisibles.** Si se chequea el choque con una lista de macetas y se dibuja otra, la
    serpiente choca contra la nada.
    ''',
    misiones=[
        dict(titulo='Las macetas',
             carta='Obstáculos | dibujar MX[m], MY[m] marrones · si la cabeza está en una: PERDISTE',
             personajes='Kira, Gheco, Arcadia, la Serpiente Jardinera',
             escena='''
             —Mi jardín tiene macetas —dice la Serpiente Jardinera, y deja seis en el caminito con la punta de la cola—.
             Mis serpientes las esquivan. La tuya, en cambio, ni las ve.
             ''',
             gheco='''
             Ya están las macetas: `MACETAS` (6) y dos arreglos con la columna (`MX`) y la fila (`MY`) de cada una. Dos
             cosas:
             1. **Dibujarlas**, después de la fruta:
             ```c
             SDL_SetRenderDrawColor(lapiz, 150, 90, 50, 255);   /* marrón maceta */
             for (int m = 0; m < MACETAS; m++) {
                 SDL_FRect maceta = { MX[m] * CELDA, MY[m] * CELDA, CELDA, CELDA };
                 SDL_RenderFillRect(lapiz, &maceta);
             }
             ```
             2. **Chocarlas**, después de ver si se mordió:
             ```c
             for (int m = 0; m < MACETAS; m++) {
                 if (cx[0] == MX[m] && cy[0] == MY[m]) {
                     estado = PERDISTE;
                 }
             }
             ```
             Por ahora el cartel sigue diciendo «TE MORDISTE»: lo cambiamos en la última. El robot va a dejar que la
             serpiente siga derecho: hay una maceta en su fila.
             ''',
             desafio='Dibujá las macetas y hacé que la serpiente pierda si la cabeza choca una.',
             pasos=['Buscá `/* acá: dibujar las macetas, marrones */` y escribí el color y el `for` que las dibuja.',
                    'Buscá `/* acá: si la cabeza choca una maceta, perdiste */` y escribí el `for` del choque.',
                    'Tocá **Jugar**, empezá y dejá que la serpiente siga derecho. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 300', estado='textos',
             superarla='''
             Seis macetas marrones aparecen en el tablero, y la serpiente que no dobla a tiempo se da contra una y se
             queda quieta. La Serpiente Jardinera aplaude con la cola: —Ahora sí ves mis macetas.
             ''',
             imagen=['La Serpiente Jardinera, una serpiente de luz enorme verde y dorada con sombrerito de paja y una regadera colgada de la cola, deja macetas en el caminito.',
                     'En la pantalla de la máquina, la grilla con cuadraditos marrones y la serpiente verde chocando contra uno.',
                     'Kira esquiva macetas con las flechas, concentrada; Arcadia sonríe; Gheco, sobre la máquina, se agarra fuerte.']),
        dict(titulo='Un lugar libre',
             carta='Función y do … while | libre(x, y, …): false si hay serpiente o maceta · do { elegir al azar } while (!libre(…))',
             personajes='Kira, Gheco, Arcadia, la Serpiente Jardinera',
             escena='''
             La fruta nueva aparece justo debajo de una maceta, y la serpiente no la puede comer nunca. La Serpiente
             Jardinera frunce el ceño: —En mi jardín las frutas crecen en la tierra libre, no debajo de las macetas.
             ''',
             gheco='''
             Dos cosas:
             1. **Una función que pregunta** si una celda está libre (va antes del `main`):
             ```c
             static bool libre(int x, int y, int cx[], int cy[], int largo)
             {
                 for (int i = 0; i < largo; i++) {           /* ¿hay una parte de la serpiente? */
                     if (cx[i] == x && cy[i] == y) {
                         return false;
                     }
                 }
                 for (int m = 0; m < MACETAS; m++) {         /* ¿hay una maceta? */
                     if (MX[m] == x && MY[m] == y) {
                         return false;
                     }
                 }
                 return true;                                /* no hay nada: libre */
             }
             ```
             `return` corta la función en el momento: apenas encuentra algo, contesta `false`.
             2. **Probar hasta que salga una libre**, al poner la fruta nueva:
             ```c
             do {
                 fx = SDL_rand(COLS);
                 fy = SDL_rand(FILAS);
             } while (!libre(fx, fy, cx, cy, largo));
             ```
             `do { … } while (…)` hace el bloque una vez y lo repite **mientras** la celda no esté libre.
             ''',
             desafio='Hacé que la fruta nueva aparezca siempre en una celda libre, sin serpiente ni maceta.',
             pasos=['Buscá `/* acá: una función que dice si una celda está libre (sin serpiente ni maceta) */` (antes del `main`) y escribí la función `libre`.',
                    'Buscá `/* acá: elegir lugares al azar hasta encontrar uno libre */` y borrá las dos líneas de abajo.',
                    'En su lugar, escribí el `do … while` de la sugerencia.',
                    'Tocá **Jugar** y comé la primera fruta: la nueva tiene que verse. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 160', estado='buscar #ff465a',
             superarla='''
             La fruta nueva aparece en tierra libre, a la vista. La Serpiente Jardinera asiente despacio. —Así crecen
             las frutas en mi jardín —dice, y riega una flor que se enciende.
             ''',
             imagen=['En la pantalla de la máquina, la fruta roja en una celda libre, lejos de las macetas marrones.',
                     'La Serpiente Jardinera, la serpiente de luz verde y dorada con sombrerito de paja, riega una flor de vidrio que se enciende.',
                     'Kira y Arcadia sonríen; Gheco, en la palma de Kira, huele la flor.']),
        dict(titulo='La fruta dorada',
             carta='Temporizador | relojDorado += dt · a los 8 s aparece en un lugar libre · a los 4 s se va · comerla: 5 puntos',
             personajes='Kira, Gheco, Arcadia, la Serpiente Jardinera',
             escena='''
             La Serpiente Jardinera sacude la cola y cae una fruta de oro que brilla entre las flores. —Mis frutas de oro
             no esperan a nadie —dice—. Aparecen un ratito, y si no llegás, se van.
             ''',
             gheco='''
             Ya están `hayDorada`, la celda `gx`, `gy` y el reloj `relojDorado`. En cada cuadro, mientras se juega:
             ```c
             if (estado == JUGANDO) {
                 relojDorado += dt;
                 if (!hayDorada && relojDorado >= 8) {          /* 8 segundos sin dorada: aparece */
                     do {
                         gx = SDL_rand(COLS);
                         gy = SDL_rand(FILAS);
                     } while (!libre(gx, gy, cx, cy, largo));
                     hayDorada = true;
                     relojDorado = 0;
                 }
                 if (hayDorada && relojDorado >= 4) {           /* 4 segundos con dorada: se va */
                     hayDorada = false;
                     relojDorado = 0;
                 }
                 if (hayDorada && cx[0] == gx && cy[0] == gy) { /* ¡la alcanzaste! */
                     puntos += 5;
                     hayDorada = false;
                     relojDorado = 0;
                 }
             }
             ```
             Y dibujarla dorada, después de la fruta roja:
             ```c
             if (hayDorada) {
                 SDL_FRect dorada = { gx * CELDA, gy * CELDA, CELDA, CELDA };
                 SDL_SetRenderDrawColor(lapiz, 255, 200, 40, 255);
                 SDL_RenderFillRect(lapiz, &dorada);
             }
             ```
             El robot va a empezar, doblar para arriba (ahí no hay macetas) y esperar 9 segundos.
             ''',
             desafio='Hacé que cada 8 segundos aparezca una fruta dorada en un lugar libre, que dure 4 y valga 5 puntos.',
             pasos=['Buscá `/* acá: la fruta dorada: aparece cada 8 segundos, dura 4 y vale 5 puntos */` y escribí el `if (estado == JUGANDO)` de la sugerencia.',
                    'Buscá `/* acá: dibujar la fruta dorada, si hay */` y escribí el `if (hayDorada)` que la dibuja.',
                    'Tocá **Jugar** y esperá: a los 8 segundos tiene que aparecer. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 2\ntecla Arriba\ncuadros 520', estado='buscar #ffc828',
             superarla='''
             Una fruta dorada se enciende en un rincón del tablero. Kira dobla, dobla otra vez… y la alcanza justo antes
             de que se apague. **+5**. La Serpiente Jardinera silba de admiración.
             ''',
             imagen=['En la pantalla de la máquina, una fruta dorada brillante en un rincón de la grilla y la serpiente verde yendo a buscarla.',
                     'La Serpiente Jardinera sacude la cola y cae una fruta de oro entre las flores de vidrio.',
                     'Kira juega a toda velocidad; Arcadia aplaude; Gheco atrapa en el aire una chispa dorada.']),
        dict(titulo='El jardín florece',
             carta='Cartel centrado | al perder: cartel = largo >= 15 ? "EL JARDIN FLORECE" : "TE ENREDASTE" · x = 320 - SDL_strlen(cartel) * 4',
             personajes='Kira, Gheco, Arcadia, la Serpiente Jardinera',
             recompensa='xp 20, monedas 5', item='Escama de Luz',
             escena='''
             —Llegá a quince anillos —dice la Serpiente Jardinera— y, cuando termine la partida, que la máquina lo diga
             bien grande, en el medio: que mi jardín floreció. Y si no llegás, que diga la verdad: que te enredaste.
             ''',
             gheco='''
             En lugar del cartel de antes («TE MORDISTE», corrido a ojo), uno centrado que depende del largo:
             ```c
             if (estado == PERDISTE) {
                 const char *cartel = (largo >= 15) ? "EL JARDIN FLORECE" : "TE ENREDASTE";
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             }
             ```
             - Con 15 partes o más, ganaste el jardín aunque después te hayas enredado.
             - Cada letra mide 8 píxeles: para centrar un texto de `n` letras, empieza en `320 - n * 4` (como los carteles
               del Campeón y del Muro).

             El robot va a dejar que la serpiente choque una maceta enseguida.
             ''',
             desafio='Cambiá el cartel del final por uno centrado: EL JARDIN FLORECE con 15 partes o más, TE ENREDASTE si no.',
             pasos=['Buscá `/* acá: el cartel del final, centrado: con 15 partes o más, el jardín florece */` y borrá el `if` de abajo.',
                    'En su lugar, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 300', estado='textos',
             superarla='''
             Quince anillos. Dieciséis. La serpiente de Kira se enreda por fin y la pantalla dice, en amarillo y en el
             medio, **EL JARDIN FLORECE**. Todas las flores de vidrio se encienden a la vez. La Serpiente Jardinera se ríe
             y riega a Kira, que también se ríe, empapada.

             En la pantalla aparece **otro pedazo del mapa del Vidriero**: una torre altísima hecha de bloques de colores
             que caen del cielo. {mentor} la mira y se pone seria. —La Torre que no para —dice—. Esa es difícil.

             La Serpiente Jardinera se saca una escama que brilla como un vitral y se la da a Kira: la **Escama de Luz**.
             —Para que mi jardín te acompañe —dice.
             ''',
             imagen=['La Serpiente Jardinera, la serpiente de luz verde y dorada con sombrerito de paja, riega a Kira riéndose, con todas las flores de vidrio encendidas.',
                     'En la pantalla de la máquina, un pedazo de mapa antiguo con una torre altísima de bloques de colores.',
                     'Kira, empapada y feliz, sostiene una escama que brilla como un vitral; Arcadia mira el mapa, seria; Gheco abraza la máquina.']),
    ],
)
