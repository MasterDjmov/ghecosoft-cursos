PLANTILLA = r'''
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };    /* jugador 1: W y S */
    SDL_FRect der = { 608, 170, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;       /* el saque sale derecho */
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
        if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
        der.y = SDL_clamp(der.y, 0, 480 - der.h);

        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        if (pelota.y + pelota.h > 480) {
            pelota.y = 480 - pelota.h;
            vy = -vy;
        }

        if (toca(pelota, izq) && vx < 0) {
            pelota.x = izq.x + izq.w;
            //@ n1: acá: devolverla un 10 % más rápido
            vx = -vx * 1.1f;
            //@ else
            vx = -vx;
            //@ end
            //@ n2: acá: que no pase del tope
            vx = SDL_clamp(vx, -600, 600);
            //@ end
            //@ n4: acá: que salga para arriba o para abajo según dónde pegó
            vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            //@ end
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            //@ n1
            vx = -vx * 1.1f;
            //@ else
            vx = -vx;
            //@ end
            //@ n2
            vx = SDL_clamp(vx, -600, 600);
            //@ end
            //@ n3: acá: que salga para arriba o para abajo según dónde pegó
            vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
            //@ end
        }

        bool punto = false;
        if (pelota.x + pelota.w < 0) {
            puntosDer++;
            punto = true;
        }
        if (pelota.x > 640) {
            puntosIzq++;
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            vx = (vx > 0) ? -300 : 300;   /* el saque, para el otro lado y con la velocidad de antes */
            vy = 0;
            espera = 1;
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 90, 80, 130, 255);
        for (int y = 0; y < 480; y += 40) {
            SDL_FRect raya = { 318, (float)y, 4, 20 };
            SDL_RenderFillRect(lapiz, &raya);
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &izq);
        SDL_SetRenderDrawColor(lapiz, 255, 60, 160, 255);
        SDL_RenderFillRect(lapiz, &der);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);

        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
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
    codigo='R02-N03', titulo='La pelota que acelera', criatura='atraviesaparedes', padre='R02-N02',
    temas='juegos.fisica', usa='juegos.colisiones, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Los partidos ya tienen marcador, pero son eternos: la pelota va y viene siempre igual de lenta y siempre
    derecho, como un péndulo. Gheco bosteza. —En la Cancha de verdad, cada golpe la apuraba un poco —cuenta
    {mentor}—. Y el campeón sabía pegarle con la punta de la paleta para mandarla en diagonal. —En la pared,
    un **Atraviesaparedes** se frota las manos: si la pelota va demasiado rápido, él sabe cómo hacerla pasar
    a través de la paleta.
    ''',
    objetivos='''
    Que la pelota se acelere con cada golpe (multiplicando su velocidad), que tenga un tope para que nunca
    atraviese la paleta, y que salga para arriba o para abajo según dónde pegó en la paleta.
    ''',
    antes='''
    R02-N02 (los puntos y el saque). De R01: el delta time (N04) y las colisiones (N05).
    ''',
    explicacion='''
    #### Acelerar es multiplicar
    Para que cada golpe la apure un 10 %, al devolverla se multiplica la velocidad por `1.1`:
    ```c
    vx = -vx * 1.1f;   /* dar la vuelta y un 10 % más */
    ```
    300 pasa a 330, después a 363, después a 399… La `f` de `1.1f` dice que es un `float`, como `vx`.

    #### Un tope
    Si nunca para de crecer, llega un momento en que la pelota avanza más de 12 píxeles por cuadro: en un cuadro
    está antes de la paleta y en el siguiente, del otro lado, **sin haberla tocado nunca**. Ese es el truco del
    Atraviesaparedes. Con un tope de 600 píxeles por segundo avanza unos 10 por cuadro, menos que el ancho de la
    paleta. `SDL_clamp(valor, mínimo, máximo)` lo deja adentro:
    ```c
    vx = SDL_clamp(vx, -600, 600);
    ```
    El mínimo es -600 porque la pelota también puede ir hacia la izquierda (velocidad negativa).

    #### Pegarle con la punta
    Se mide **cuánto se corrió la pelota del medio de la paleta**: el centro de la pelota menos el centro de la
    paleta.
    ```c
    float diferencia = (pelota.y + pelota.h / 2) - (der.y + der.h / 2);
    ```
    Si pegó en el medio, da 0 y la pelota sale derecho. Si pegó abajo, da positivo (sale para abajo); si pegó
    arriba, negativo (sale para arriba). Multiplicado por 5, es la nueva `vy`: cuanto más en la punta, más
    inclinada sale.

    #### El saque vuelve a empezar
    Después de un punto, la pelota vuelve al medio con la velocidad del principio (300) y derecho (`vy = 0`). Eso
    ya está escrito en el `if (punto)`: `(vx > 0) ? -300 : 300` quiere decir «si iba para la derecha, -300; si
    no, 300».
    ''',
    para_que='''
    Que un juego se ponga más difícil de a poco es lo que lo hace entretenido: la pelota del Arkanoid, las
    piezas del Tetris y las naves enemigas también se aceleran. Y el tope es la regla de oro para que lo rápido
    no atraviese lo que tiene que chocar.
    ''',
    errores='''
    **Multiplicar por 10 en lugar de 1.1.** `vx * 10` la vuelve diez veces más rápida de un golpe. Un 10 % más
    es `vx * 1.1f`.

    **Atraviesaparedes: sin tope.** Después de muchos golpes la pelota va tan rápido que salta la paleta de un
    cuadro al otro y es punto aunque la paleta estaba ahí.

    **Tope solo para un lado.** `SDL_clamp(vx, 0, 600)` deja en 0 cualquier velocidad hacia la izquierda: la
    pelota se queda quieta. El mínimo tiene que ser -600.

    **Restar al revés.** `(der.y + der.h / 2) - (pelota.y + …)` da el signo contrario: la pelota que pega abajo
    sale para arriba.
    ''',
    misiones=[
        dict(titulo='Cada golpe, más rápido',
             carta='Acelerar | al devolverla: vx = -vx * 1.1f',
             escena='''
             —Primero, que se apure —dice {mentor}—. Cada vez que una paleta la devuelve, un poquito más rápido.
             Así el partido empieza tranquilo y termina a los gritos.
             ''',
             gheco='''
             Cuando una paleta devuelve la pelota, hoy se le da la vuelta a `vx`: `vx = -vx;`. Para que además vaya
             **un 10 % más rápido**, se multiplica por `1.1`:
             ```c
             vx = -vx * 1.1f;
             ```
             Si venía a 300 hacia la derecha, vuelve a 330 hacia la izquierda. La `f` dice que `1.1` es un
             `float`, como `vx`.

             Hay que cambiarlo en las **dos** paletas: en la de la izquierda y en la de la derecha.
             ''',
             desafio='Hacé que cada vez que una paleta devuelve la pelota, la pelota salga un 10 % más rápido.',
             pasos=['Buscá el comentario `/* acá: devolverla un 10 % más rápido */` (en la paleta izquierda).',
                    'Cambiá la línea de abajo, `vx = -vx;`, por `vx = -vx * 1.1f;`.',
                    'Hacé lo mismo en la paleta derecha (es la otra línea `vx = -vx;` que está adentro de `toca(pelota, der)`).',
                    'Tocá **Jugar** y mirá cómo se apura. Después, **Comprobar**.'],
             eventos='cuadros 90', estado='buscar #ffdc00',
             superarla='''
             Golpe, golpe, golpe: cada uno más rápido que el anterior. Gheco ya no bosteza; ahora mueve la cabeza
             de un lado al otro, cada vez más ligero.
             ''',
             imagen=['La pelota amarilla con una estela cada vez más larga, rebotando entre la paleta cian y la rosa.',
                     'Kira y Arcadia juegan concentradas, inclinadas sobre los controles.',
                     'Gheco, sobre la máquina, mueve la cabeza de un lado al otro, cada vez más rápido.']),
        dict(titulo='Con un tope', criatura='atraviesaparedes',
             carta='El tope | vx = SDL_clamp(vx, -600, 600) · menos que el ancho de la paleta por cuadro',
             escena='''
             La pelota ya va tan rápido que, de golpe, pasa **a través** de la paleta de {mentor} sin tocarla. En
             la pared, el Atraviesaparedes aplaude. —¡Eso no vale! —grita {mentor}—. La tocó. Bueno… no la tocó.
             La saltó.
             ''',
             gheco='''
             Cada cuadro la pelota avanza `vx * dt`. Si va demasiado rápido, en un cuadro está **antes** de la
             paleta y en el siguiente ya está **del otro lado**: nunca se pisaron, así que `toca` nunca da `true`.

             La paleta mide 12 de ancho. A 600 píxeles por segundo, la pelota avanza unos 10 por cuadro: nunca la
             puede saltar. Por eso, después de acelerarla, se le pone un **tope**:
             ```c
             vx = SDL_clamp(vx, -600, 600);
             ```
             `SDL_clamp` deja el número entre -600 y 600 (negativo es hacia la izquierda). Va en las **dos**
             paletas, justo después de `vx = -vx * 1.1f;`.

             El robot va a dejar que la pelota rebote muchas veces, hasta que llegue al tope.
             ''',
             desafio='Ponele un tope de 600 píxeles por segundo a la velocidad de la pelota, en las dos paletas.',
             pasos=['Buscá `/* acá: que no pase del tope */` (en la paleta izquierda) y escribí debajo `vx = SDL_clamp(vx, -600, 600);`.',
                    'En la paleta derecha, después de `vx = -vx * 1.1f;`, escribí la misma línea.',
                    'Tocá **Jugar** y dejá que rebote mucho rato. Después, **Comprobar**.'],
             eventos='cuadros 700', estado='buscar #ffdc00',
             superarla='''
             Por más rápido que vaya, la pelota siempre choca con la paleta. El Atraviesaparedes empuja, empuja… y
             se da la cabeza contra el borde. Se va refunfuñando por una rendija.
             ''',
             imagen=['La pelota amarilla muy rápida, con una estela larga, chocando contra la paleta rosa con una chispa.',
                     'Un Atraviesaparedes, criatura gomosa y translúcida, se golpea la cabeza contra el borde de la pantalla, enojado.',
                     'Arcadia festeja haber devuelto la pelota; Kira se ríe; Gheco se tapa los ojos.']),
        dict(titulo='Pegarle con la punta',
             carta='El ángulo | vy = (centro de la pelota - centro de la paleta) * 5',
             escena='''
             —Ahora, el secreto del campeón —dice {mentor}, y baja la voz—. Si le pegás con la punta de abajo, la
             pelota sale para abajo. Con la de arriba, para arriba. En el medio, derecho. Probalo con mi paleta.
             ''',
             gheco='''
             Para saber dónde pegó, se compara el **centro de la pelota** con el **centro de la paleta**:
             - el centro de la pelota (en altura) es `pelota.y + pelota.h / 2`;
             - el centro de la paleta derecha es `der.y + der.h / 2`.

             La resta dice cuánto se corrió del medio: 0 si pegó justo en el medio, positivo si pegó más abajo,
             negativo si pegó más arriba. Multiplicada por 5 es la nueva velocidad hacia abajo:
             ```c
             vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
             ```
             Si pegó 30 píxeles abajo del medio, sale a 150 hacia abajo. En esta micro-misión, solo la paleta
             derecha.
             ''',
             desafio='Hacé que la pelota salga de la paleta derecha para arriba o para abajo según dónde pegó.',
             pasos=['Buscá el comentario `/* acá: que salga para arriba o para abajo según dónde pegó */` adentro de `toca(pelota, der)`.',
                    'Debajo, escribí `vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;`.',
                    'Tocá **Jugar** y pegale con la punta de la paleta rosa (las flechas). Después, **Comprobar**.'],
             eventos='cuadros 90', estado='buscar #ffdc00',
             superarla='''
             La pelota pega en la punta de la paleta rosa y sale en diagonal, rebota en el techo y cruza la cancha.
             Kira silba. —Eso sí que no lo vi venir.
             ''',
             imagen=['La pelota amarilla sale en diagonal desde la punta de la paleta rosa, con una línea de recorrido que rebota en el borde de arriba.',
                     'Arcadia, con una sonrisa pícara, acaba de mover la paleta; Kira abre grandes los ojos.',
                     'Gheco sigue la diagonal con el dedo.']),
        dict(titulo='Las dos paletas',
             carta='El ángulo en las dos | el mismo cálculo con izq.y + izq.h / 2',
             escena='''
             —¡Ahora yo también! —pide Kira—. Si {mentor} puede pegarle con la punta, la paleta cian también tiene
             que poder.
             ''',
             gheco='''
             Es la misma cuenta que en la paleta derecha, pero con la paleta izquierda:
             ```c
             vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
             ```
             Va adentro de `toca(pelota, izq)`, después del tope.

             El robot va a bajar la paleta cian con la S para que la pelota le pegue cerca de la punta de arriba.
             ''',
             desafio='Hacé que la paleta izquierda también mande la pelota para arriba o para abajo según dónde pegó.',
             pasos=['Buscá el comentario `/* acá: que salga para arriba o para abajo según dónde pegó */` adentro de `toca(pelota, izq)`.',
                    'Debajo, escribí `vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;`.',
                    'Tocá **Jugar** y jugá un partido con las dos puntas. Después, **Comprobar**.'],
             eventos='cuadros 60\napretar S\ncuadros 42\nsoltar S\ncuadros 80', estado='buscar #ffdc00\ntextos',
             superarla='''
             Diagonales, rebotes en el techo, golpes con la punta: ahora el partido es de verdad. {mentor} se ríe a
             carcajadas. —¡Así jugaba el campeón! —dice. Y se queda callada, mirando la máquina más vieja, como si
             se acordara de algo.
             ''',
             imagen=['La pantalla de la Cancha con el recorrido de la pelota en zigzag, rebotando en las dos paletas y en los bordes.',
                     'Kira y Arcadia juegan riéndose a carcajadas.',
                     'Gheco, de árbitro, señala una diagonal con los dos brazos.']),
    ],
)
