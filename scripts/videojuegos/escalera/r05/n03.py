import motor
import n02

PLANTILLA = motor.crecer(motor.full(n02.PLANTILLA), [
    ('''
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */
''', '''
#define OX 200      /* dónde empieza el pozo: (640 - 240) / 2, en el medio */
//@ n3+

/* Las siete piezas, cada una en su cajita de 4 × 4: I, O, T, S, Z, J y L */
static const int PIEZAS[7][4][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 1, 1 }, { 0, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 0: I, el palo */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 1: O, el cuadrado */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 2: T */
    { { 0, 0, 0, 0 }, { 0, 1, 1, 0 }, { 1, 1, 0, 0 }, { 0, 0, 0, 0 } },   /* 3: S */
    { { 0, 0, 0, 0 }, { 1, 1, 0, 0 }, { 0, 1, 1, 0 }, { 0, 0, 0, 0 } },   /* 4: Z */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 0, 0, 1, 0 }, { 0, 0, 0, 0 } },   /* 5: J */
    { { 0, 0, 0, 0 }, { 1, 1, 1, 0 }, { 1, 0, 0, 0 }, { 0, 0, 0, 0 } },   /* 6: L */
};

/* Los colores: el 0 es la casilla vacía; del 1 al 7, el de cada pieza (la pieza 0 usa el 1, la 1 el 2…) */
static const Uint8 COLORES[8][3] = {
    { 28, 28, 44 },      /* vacía */
    { 0, 220, 255 },     /* I: celeste */
    { 255, 220, 0 },     /* O: amarillo */
    { 170, 80, 255 },    /* T: violeta */
    { 80, 220, 100 },    /* S: verde */
    { 255, 70, 90 },     /* Z: rojo */
    { 60, 110, 255 },    /* J: azul */
    { 255, 150, 40 },    /* L: naranja */
};
//@ end
'''),
    ('''
    return true;
}
''', '''
    return true;
}

/* Gira la pieza un cuarto de vuelta, como las agujas del reloj */
static void girar(int pieza[4][4])
{
    //@ n1: acá: armar la pieza girada en otra cajita y copiarla de vuelta
    int girada[4][4];
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            girada[f][c] = pieza[3 - c][f];
        }
    }
    for (int f = 0; f < 4; f++) {
        for (int c = 0; c < 4; c++) {
            pieza[f][c] = girada[f][c];
        }
    }
    //@ end
}
'''),
    ('''
    int px = 3;   /* dónde''', '''
    //@ n3+
    int tipo = 2;   /* qué pieza es: la 2 es la T */
    //@ end
    int px = 3;   /* dónde'''),
    ('''
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }''', '''
                if (evento.key.key == SDLK_RIGHT && cabe(pieza, tablero, px + 1, py)) {
                    px++;
                }
                if (evento.key.key == SDLK_UP) {   /* la flecha de arriba gira la pieza */
                    girar(pieza);
                    //@ n2: acá: si girada no cabe, girarla tres veces más para que vuelva como estaba
                    if (!cabe(pieza, tablero, px, py)) {
                        girar(pieza);
                        girar(pieza);
                        girar(pieza);
                    }
                    //@ end
                }'''),
    ('''
                            tablero[py + f][px + c] = 1;''', '''
                            //@ n4: acá: guardar en el pozo el color de la pieza (tipo + 1) en lugar de un 1
                            tablero[py + f][px + c] = tipo + 1;
                            //@ else
                            tablero[py + f][px + c] = 1;
                            //@ end'''),
    ('''
                px = 3;
                py = 0;''', '''
                //@ n3: acá: la pieza nueva, una de las siete al azar
                tipo = SDL_rand(7);
                for (int f = 0; f < 4; f++) {
                    for (int c = 0; c < 4; c++) {
                        pieza[f][c] = PIEZAS[tipo][f][c];
                    }
                }
                //@ end
                px = 3;
                py = 0;'''),
    ('''
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }''', '''
                //@ n4: acá: cada casilla con su color, sacado de la tabla COLORES
                int t = tablero[f][c];   /* 0: vacía; del 1 al 7: el color que dejó ahí una pieza */
                SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
                //@ else
                if (tablero[f][c] == 0) {
                    SDL_SetRenderDrawColor(lapiz, 28, 28, 44, 255);    /* vacía: casi negra */
                } else {
                    SDL_SetRenderDrawColor(lapiz, 0, 220, 255, 255);   /* ocupada: celeste */
                }
                //@ end'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */''', '''
        //@ n3: acá: el color de la pieza que cae, según su tipo
        SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
        //@ else
        SDL_SetRenderDrawColor(lapiz, 170, 80, 255, 255);   /* violeta */
        //@ end'''),
])

NODO = dict(
    codigo='R05-N03', titulo='Girar y las siete piezas', criatura='glitch', padre='R05-N02',
    lugar='La Torre que no para',
    temas='col.matrices', usa='prog.funciones, prog.matematica-azar, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    Las T se apilan, una arriba de la otra, y enseguida queda una torrecita torcida, llena de huecos. —Así no encaja
    nada —dice {mentor}—. En la Torre de verdad caen siete piezas distintas, y cada una se puede girar. Por la pantalla
    pasa un parpadeo: un gatito pixelado se mete entre las piezas y las deja medio corridas. Es el **Glitch**.
    ''',
    objetivos='''
    **Girar** la pieza un cuarto de vuelta armando otra matriz, girarla solo si **cabe**, sacar **una de las siete
    piezas al azar** de una tabla y dibujar cada una (y lo que queda en el pozo) **con su color**.
    ''',
    antes='''
    El nodo anterior. De R04: elegir al azar con `SDL_rand` (N03). De R03: los colores de cada fila de la pared (N03).
    ''',
    explicacion='''
    #### Girar una matriz
    Girar la pieza es girar su cajita de 4 × 4 un cuarto de vuelta, como las agujas del reloj. La fila de arriba pasa a
    ser la columna de la derecha; la columna de la izquierda pasa a ser la fila de arriba. En cuentas: el lugar
    `(f, c)` de la pieza girada sale del lugar `(3 - c, f)` de la de antes. Se arma en **otra** cajita, `girada`,
    porque si se escribiera encima de la misma se pisarían los números que todavía no se leyeron. Al final se copia de
    vuelta.

    #### Girar solo si cabe
    Al lado de una pared, la pieza girada puede quedar medio afuera. Se gira, se pregunta con `cabe` y, si no cabe, se
    gira **tres veces más**: cuatro cuartos de vuelta son una vuelta entera, y queda como estaba.

    #### Las siete piezas: una tabla de matrices
    `PIEZAS[7][4][4]` son siete cajitas de 4 × 4, una por pieza: la I (el palo), la O (el cuadrado), la T, la S, la Z,
    la J y la L. `tipo` dice cuál es la que cae (del 0 al 6). Para sacar una nueva, se elige `tipo = SDL_rand(7)` y se
    copia su cajita en `pieza`, casilla por casilla.

    #### Los colores en una tabla
    `COLORES[8][3]` tiene el rojo, el verde y el azul de cada color. El 0 es el de la casilla vacía, y del 1 al 7, el
    de cada pieza: la pieza `tipo` usa el color `tipo + 1`. Así, cuando una pieza se queda en el pozo, guarda
    `tipo + 1` en sus casillas, y el pozo se dibuja con un solo renglón: el color de la casilla `t` es
    `COLORES[t]`.
    ''',
    para_que='''
    Girar matrices sirve para girar mapas, imágenes y tableros. Y guardar los datos en tablas (las piezas, los colores)
    en lugar de llenar el código de `if` hace que sumar una pieza nueva sea agregar un renglón.
    ''',
    errores='''
    **Girar en la misma cajita.** Si se hace `pieza[f][c] = pieza[3 - c][f]` sin `girada`, se pisan los números que
    todavía no se leyeron y la pieza queda rota: es el Glitch.

    **Girar sin preguntar.** Al lado de la pared, la pieza girada queda con un bloque afuera del pozo.

    **`tipo` en lugar de `tipo + 1`.** El color 0 es el de vacía: si la I guarda `tipo` (0), se vuelve invisible al
    quedarse en el pozo.

    **`SDL_rand(6)`.** Da del 0 al 5: la L no sale nunca. Para siete piezas, `SDL_rand(7)`.
    ''',
    misiones=[
        dict(titulo='Un cuarto de vuelta',
             carta='Girar | girada[f][c] = pieza[3 - c][f] (en otra cajita) · después copiar girada en pieza',
             escena='''
             Kira aprieta la flecha de arriba: la T debería girar, pero se queda igual. —Girar es lo que hace interesante a
             la Torre —dice {mentor}—. La cajita entera da un cuarto de vuelta, como las agujas del reloj.
             ''',
             gheco='''
             La flecha de arriba ya llama a `girar(pieza)`, pero la función está vacía. Adentro, la pieza girada se arma
             en **otra** cajita y después se copia de vuelta:
             ```c
             int girada[4][4];
             for (int f = 0; f < 4; f++) {
                 for (int c = 0; c < 4; c++) {
                     girada[f][c] = pieza[3 - c][f];   /* la fila de arriba pasa a la columna de la derecha */
                 }
             }
             for (int f = 0; f < 4; f++) {
                 for (int c = 0; c < 4; c++) {
                     pieza[f][c] = girada[f][c];       /* se copia de vuelta */
                 }
             }
             ```
             ¿Por qué otra cajita? Si se escribiera en la misma, al llegar a un lugar ya se habría pisado el número que
             había que leer. El robot va a apretar la flecha de arriba.
             ''',
             desafio='Hacé que la flecha de arriba gire la pieza un cuarto de vuelta.',
             pasos=['Buscá `/* acá: armar la pieza girada en otra cajita y copiarla de vuelta */` (en la función `girar`).',
                    'Debajo, escribí `girada` y los dos pares de `for` de la sugerencia.',
                    'Tocá **Jugar** y apretá la flecha de arriba. Después, **Comprobar**.'],
             eventos='tecla Arriba\ncuadros 2', estado='buscar #aa50ff',
             superarla='''
             Kira aprieta la flecha y la T gira: ahora apunta para la izquierda. Otra vez: para arriba. Cuatro veces, y
             vuelve a ser la de siempre. Gheco gira sobre sí mismo para imitarla y se marea.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta en T girada un cuarto de vuelta, con una flecha curva.',
                     'Kira aprieta la flecha de arriba; Arcadia gira las manos para mostrar el cuarto de vuelta.',
                     'Gheco gira sobre sí mismo arriba de la máquina, mareado.']),
        dict(titulo='Girar sin salirse',
             carta='Deshacer | girar · si no cabe: girar tres veces más (cuatro cuartos = una vuelta entera)',
             escena='''
             Kira lleva la T contra la pared derecha y la gira dos veces: un bloque queda **afuera** del pozo, flotando en
             la nada. —Girar también tiene que respetar las paredes —dice {mentor}.
             ''',
             gheco='''
             Después de girar, se pregunta si la pieza cabe ahí. Si no cabe, se la deja como estaba. ¿Cómo? Girándola tres
             veces más: cuatro cuartos de vuelta son una vuelta entera.
             ```c
             girar(pieza);
             if (!cabe(pieza, tablero, px, py)) {
                 girar(pieza);      /* dos cuartos… */
                 girar(pieza);      /* tres… */
                 girar(pieza);      /* cuatro: una vuelta entera, como estaba */
             }
             ```
             El robot va a llevar la T contra la pared derecha y la va a girar dos veces.
             ''',
             desafio='Hacé que la pieza gire solo si girada cabe en el pozo.',
             pasos=['Buscá `/* acá: si girada no cabe, girarla tres veces más para que vuelva como estaba */` (abajo del `girar(pieza);` de la flecha de arriba).',
                    'Debajo, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar**, llevá la T contra una pared y girala. Después, **Comprobar**.'],
             eventos='tecla Derecha\ntecla Derecha\ntecla Derecha\ntecla Derecha\ntecla Arriba\ntecla Arriba\ncuadros 2',
             estado='buscar #aa50ff',
             superarla='''
             Contra la pared, la T intenta girar… y no gira: se queda como estaba, con todos sus bloques adentro. Kira la
             aleja un paso de la pared y ahí sí, gira tranquila.
             ''',
             imagen=['La pantalla de la máquina con la pieza violeta pegada a la pared derecha del pozo, sin salirse.',
                     'Kira aprieta la flecha de arriba, pensativa; Arcadia asiente.',
                     'Gheco, con las patas contra la pared del pozo, la empuja para que la pieza no salga.']),
        dict(titulo='Siete piezas',
             carta='Al azar | tipo = SDL_rand(7) · copiar PIEZAS[tipo] en pieza · color COLORES[tipo + 1]',
             criatura='glitch',
             escena='''
             Desde lo alto de la torre caen piezas de todas las formas: un palo largo, un cuadrado, unas como escalones,
             unas como ganchos. Pero en la pantalla sale siempre la T. El Glitch se ríe, sentado arriba del pozo.
             ''',
             gheco='''
             Ya están las tablas `PIEZAS` (las siete cajitas) y `COLORES` (un color por pieza), y `tipo` (qué pieza es).
             Dos cosas:
             1. **La pieza nueva, al azar** (donde sale otra arriba):
             ```c
             tipo = SDL_rand(7);                          /* del 0 al 6 */
             for (int f = 0; f < 4; f++) {
                 for (int c = 0; c < 4; c++) {
                     pieza[f][c] = PIEZAS[tipo][f][c];    /* se copia su cajita */
                 }
             }
             ```
             2. **Su color**, en lugar del violeta fijo:
             ```c
             SDL_SetRenderDrawColor(lapiz, COLORES[tipo + 1][0], COLORES[tipo + 1][1], COLORES[tipo + 1][2], 255);
             ```
             `COLORES[tipo + 1]` es una fila de la tabla: `[0]` el rojo, `[1]` el verde, `[2]` el azul. El robot va a
             esperar a que salga la segunda pieza.
             ''',
             desafio='Hacé que cada pieza nueva sea una de las siete al azar, dibujada con su color.',
             pasos=['Buscá `/* acá: la pieza nueva, una de las siete al azar */` y escribí el `tipo = SDL_rand(7);` y los dos `for` de la sugerencia.',
                    'Buscá `/* acá: el color de la pieza que cae, según su tipo */` y cambiá el color violeta por el de la sugerencia.',
                    'Tocá **Jugar** y esperá varias piezas. Después, **Comprobar**.'],
             eventos='cuadros 600', estado='buscar #ffdc00',
             superarla='''
             La segunda pieza no es una T: es otra, de otro color. La tercera, otra más. El Glitch intenta corrérselas,
             pero cada pieza sale entera, con su forma y su color.
             ''',
             imagen=['La pantalla de la máquina con piezas de varias formas y colores: un palo celeste, un cuadrado amarillo, una ese verde.',
                     'Un gatito pixelado que parpadea mira, sorprendido, sentado arriba de la máquina.',
                     'Kira y Arcadia sonríen; Gheco sostiene en la mano una pieza de colores de verdad.']),
        dict(titulo='Cada una con su color',
             carta='Pozo de colores | al fijar: tablero[…] = tipo + 1 · al dibujar: color COLORES[tablero[f][c]]',
             escena='''
             Las piezas bajan de colores, pero apenas tocan el fondo se vuelven todas celestes, como si se despintaran.
             —En la Torre cada bloque se queda con su color —dice {mentor}—. Si no, no se sabe qué pieza era cuál.
             ''',
             gheco='''
             El pozo tiene que guardar **el color** y no solo un 1. Dos cosas:
             1. **Al fijar**, en lugar de `1`:
             ```c
             tablero[py + f][px + c] = tipo + 1;   /* del 1 al 7: el color de esta pieza */
             ```
             2. **Al dibujar el pozo**, en lugar del `if` con dos colores:
             ```c
             int t = tablero[f][c];
             SDL_SetRenderDrawColor(lapiz, COLORES[t][0], COLORES[t][1], COLORES[t][2], 255);
             ```
             Como `COLORES[0]` es el casi negro de las vacías, un solo renglón sirve para todas las casillas. El robot va
             a esperar a que se quede la primera T.
             ''',
             desafio='Hacé que cada bloque se quede en el pozo con el color de su pieza.',
             pasos=['Buscá `/* acá: guardar en el pozo el color de la pieza (tipo + 1) en lugar de un 1 */` y cambiá el `1` por `tipo + 1`.',
                    'Buscá `/* acá: cada casilla con su color, sacado de la tabla COLORES */` y borrá el `if` de abajo.',
                    'En su lugar, escribí las dos líneas de la sugerencia.',
                    'Tocá **Jugar** y dejá que se apilen piezas. Después, **Comprobar**.'],
             eventos='cuadros 600', estado='pixel 306 466',
             superarla='''
             La T toca el fondo y se queda violeta; arriba, un palo celeste, y al lado un cuadrado amarillo. La torrecita
             parece un vitral. Desde lo alto de la Torre de verdad cae un bloque de cada color.
             ''',
             imagen=['La pantalla de la máquina con el fondo del pozo lleno de bloques de muchos colores, como un vitral.',
                     'Desde lo alto de la torre caen bloques de colores, brillando.',
                     'Kira y Arcadia miran admiradas; Gheco apoya la cara contra la pantalla.']),
    ],
)
