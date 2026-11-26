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
    SDL_FRect der = { 608, 200, 12, 80 };   /* jugador 2: flechas */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 120;
    int puntosIzq = 0;
    int puntosDer = 0;
    //@ n4+
    float espera = 0;   /* segundos que faltan para sacar */
    //@ end
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

        //@ n4: acá: si hay que esperar, descontar el tiempo y no mover la pelota
        if (espera > 0) {
            espera -= dt;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        //@ else
        pelota.x += vx * dt;
        pelota.y += vy * dt;
        //@ end
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
            vx = -vx;
        }
        if (toca(pelota, der) && vx > 0) {
            pelota.x = der.x - pelota.w;
            vx = -vx;
        }

        /* ¿se fue por un costado? */
        bool punto = false;
        if (pelota.x + pelota.w < 0) {   /* por la izquierda: se le pasó al jugador 1 */
            //@ n1: acá: un punto para el jugador 2
            puntosDer++;
            //@ end
            punto = true;
        }
        if (pelota.x > 640) {            /* por la derecha: se le pasó al jugador 2 */
            //@ n1: acá: un punto para el jugador 1
            puntosIzq++;
            //@ end
            punto = true;
        }
        if (punto) {
            pelota.x = 314;
            pelota.y = 234;
            //@ n2: acá: que el saque salga para el otro lado
            vx = -vx;
            //@ end
            //@ n4: acá: un segundo de respiro antes del saque
            espera = 1;
            //@ end
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

        /* el marcador */
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        //@ n3: acá: el marcador cuatro veces más grande
        SDL_SetRenderScale(lapiz, 4, 4);
        SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
        SDL_SetRenderScale(lapiz, 1, 1);
        //@ else
        SDL_RenderDebugTextFormat(lapiz, 280, 20, "%d", puntosIzq);
        SDL_RenderDebugTextFormat(lapiz, 352, 20, "%d", puntosDer);
        //@ end
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
    codigo='R02-N02', titulo='Los puntos', criatura='glitch', padre='R02-N01',
    usa='juegos.colisiones, juegos.bucle, juegos.entrada',
    plantilla=PLANTILLA,
    cronica='''
    Kira y {mentor} juegan diez minutos sin parar. La pelota va, viene, se escapa por un costado, vuelve al
    medio… y nadie sabe quién va ganando. —Así no es un partido —dice {mentor}, cruzada de brazos—. Es pelotear.
    Gheco, sentado arriba de la máquina, levanta una mano por cada pelota que se escapa, pero ya se le acabaron
    los dedos. Sobre la pantalla parpadea un **glitch**: dos números que se pisan y no dicen nada.
    ''',
    objetivos='''
    Que el Pong lleve la cuenta: sumar un punto cuando la pelota se escapa por un costado, sacar desde el medio
    hacia el otro lado, mostrar el marcador grande arriba y dar un segundo de respiro antes de cada saque.
    ''',
    antes='''
    R02-N01 (la cancha, las paletas y el rebote). De R01: el texto en pantalla y la escala (N07) y el delta
    time (N04).
    ''',
    explicacion='''
    #### ¿Cuándo es punto?
    Cuando la pelota sale **entera** por un costado. Por la izquierda, sale cuando su borde derecho pasa el 0:
    `pelota.x + pelota.w < 0`. Por la derecha, cuando su borde izquierdo pasa el ancho de la ventana:
    `pelota.x > 640`. Si se escapa por la izquierda, al jugador 1 se le pasó: el punto es para el jugador 2.

    #### Dos contadores
    Cada jugador tiene su variable entera, que arranca en 0:
    ```c
    int puntosIzq = 0;
    int puntosDer = 0;
    ```
    `puntosDer++;` le suma uno (es lo mismo que `puntosDer = puntosDer + 1;`).

    #### Un aviso: «hubo punto»
    Pase lo que pase, después de un punto se hace lo mismo: la pelota vuelve al medio. Para no escribirlo dos
    veces, se usa una variable `bool punto` que arranca en `false`, se pone en `true` en cualquiera de los dos
    casos y, al final, un solo `if (punto)` acomoda la pelota.

    #### El saque
    Si la pelota vuelve al medio con la misma velocidad, sale siempre para el mismo lado. Dándole la vuelta a
    `vx` (`vx = -vx;`), cada saque va hacia el otro jugador.

    #### El marcador grande
    `SDL_SetRenderScale(lapiz, 4, 4)` hace que todo lo que se dibuje después salga 4 veces más grande, también
    las coordenadas: `(60, 5)` cae en `(240, 20)` de la pantalla. Después hay que volver a `1, 1`, porque si no
    el cuadro siguiente se dibuja todo gigante.

    #### Un respiro
    Una variable `espera` con los segundos que faltan para sacar. Mientras sea mayor que 0, se le resta `dt` y la
    pelota no se mueve. Al hacer un punto se la pone en 1: un segundo de pausa para que los dos se acomoden.
    ''',
    para_que='''
    Contar puntos, volver a sacar y esperar un ratito antes de seguir es lo que hace que un juego tenga
    partidas: lo mismo pasa con las vidas del Arkanoid, las líneas del Tetris o los niveles de las naves.
    ''',
    errores='''
    **Mirar el borde equivocado.** Con `pelota.x < 0` el punto se cuenta cuando la pelota todavía está a medias
    en la pantalla. Para que salga entera, el borde derecho: `pelota.x + pelota.w < 0`.

    **Glitch: el punto que se cuenta cien veces.** Si la pelota no vuelve al medio en el mismo cuadro, en el
    cuadro siguiente sigue afuera y suma otro punto, y otro… El `if (punto)` la saca de ahí enseguida.

    **Olvidar volver la escala a 1.** Todo lo que se dibuja después (y el cuadro siguiente) sale cuatro veces más
    grande y corrido.

    **Restar la espera sin `dt`.** `espera -= 1;` se termina en un solo cuadro. El tiempo se descuenta en
    segundos: `espera -= dt;`.
    ''',
    misiones=[
        dict(titulo='¿Quién hizo el punto?',
             carta='Contar el punto | se fue por la izquierda: puntosDer++ · por la derecha: puntosIzq++',
             escena='''
             —Primero, la cuenta —dice {mentor}—. Si la pelota se le escapa a Kira por la izquierda, el punto es
             mío. Si se me escapa a mí por la derecha, es de ella. La máquina ya ve cuándo se escapa: le falta
             sumar.
             ''',
             gheco='''
             Ya están los dos `if` que ven si la pelota se fue por un costado, y las dos variables del marcador,
             `puntosIzq` y `puntosDer`, que arrancan en 0. Falta sumar:
             - Si se fue **por la izquierda** (`pelota.x + pelota.w < 0`), se le pasó al jugador 1: punto para el
               jugador 2, `puntosDer++;`.
             - Si se fue **por la derecha** (`pelota.x > 640`), punto para el jugador 1: `puntosIzq++;`.

             `++` le suma uno a la variable: `puntosDer++;` es lo mismo que `puntosDer = puntosDer + 1;`. El
             marcador de arriba ya muestra las dos variables, así que se va a ver solo.

             El robot no va a mover las paletas: la pelota se le va a escapar al jugador 2.
             ''',
             desafio='Sumá el punto al jugador que corresponde cada vez que la pelota se escapa por un costado.',
             pasos=['Buscá el comentario `/* acá: un punto para el jugador 2 */` (adentro del `if` de la izquierda) y escribí debajo `puntosDer++;`.',
                    'Buscá `/* acá: un punto para el jugador 1 */` (adentro del `if` de la derecha) y escribí `puntosIzq++;`.',
                    'Tocá **Jugar** y dejá pasar la pelota: el número de arriba tiene que cambiar. Después, **Comprobar**.'],
             eventos='cuadros 100', estado='textos',
             superarla='''
             La pelota se escapa por la derecha y arriba aparece un **1** del lado de Kira. {mentor} resopla:
             —Uno a cero. No te agrandes.
             ''',
             imagen=['La máquina de la Cancha con el marcador encendido arriba: un 1 de un lado y un 0 del otro.',
                     'Kira festeja con el puño; Arcadia, del otro lado, resopla con los brazos cruzados.',
                     'Gheco, sentado arriba de la máquina, levanta un dedo como un árbitro.']),
        dict(titulo='El saque',
             carta='Sacar hacia el otro lado | al volver al medio: vx = -vx',
             escena='''
             Después del punto, la pelota vuelve al medio… y sale otra vez hacia {mentor}, que ni la ve venir.
             —¡Eso es trampa! —se queja—. El saque tiene que ir para el otro lado.
             ''',
             gheco='''
             Después de un punto, el `if (punto)` vuelve a poner la pelota en el medio. Pero `vx` sigue igual:
             si iba hacia la derecha, sale otra vez hacia la derecha.

             Para que el saque salga **para el otro lado**, se le da la vuelta a `vx`, como en un rebote:
             ```c
             vx = -vx;
             ```
             Si valía 300 (hacia la derecha), pasa a valer -300 (hacia la izquierda).
             ''',
             desafio='Hacé que después de cada punto la pelota salga desde el medio hacia el otro lado.',
             pasos=['Buscá el comentario `/* acá: que el saque salga para el otro lado */` adentro del `if (punto)`.',
                    'Debajo, escribí `vx = -vx;`.',
                    'Tocá **Jugar** y mirá qué pasa después del primer punto. Después, **Comprobar**.'],
             eventos='cuadros 100', estado='buscar #ffdc00',
             superarla='''
             Ahora el saque cruza la cancha hacia el que no hizo el punto. {mentor} lo devuelve con un golpe
             seco. —Así sí. Parejo.
             ''',
             imagen=['La pelota amarilla sale del centro de la cancha hacia la paleta rosa, con una estela.',
                     'Arcadia, lista, con la mano sobre los controles; Kira sonríe del otro lado.',
                     'Gheco señala con la cola hacia dónde va la pelota.']),
        dict(titulo='El marcador grande',
             carta='Texto grande | SDL_SetRenderScale(lapiz, 4, 4) · dibujar · volver a 1, 1',
             escena='''
             Los números del marcador son tan chiquitos que Gheco tiene que subirse a la pantalla para leerlos.
             —En una cancha, el marcador se ve desde la puerta —dice {mentor}.
             ''',
             gheco='''
             Las letras de `SDL_RenderDebugText` miden 8 × 8 píxeles. Para agrandarlas, se agranda **todo lo que
             se dibuja después** con la escala (lo viste en R01-N07):
             ```c
             SDL_SetRenderScale(lapiz, 4, 4);   /* todo 4 veces más grande */
             SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
             SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
             SDL_SetRenderScale(lapiz, 1, 1);   /* y de vuelta a lo normal */
             ```
             Con la escala, las coordenadas también se multiplican por 4: `(60, 5)` cae en `(240, 20)` de la
             pantalla, y `(88, 5)` en `(352, 20)`. Por eso se escriben más chicas.
             ''',
             desafio='Dibujá el marcador cuatro veces más grande, a los dos lados de la red.',
             pasos=['Buscá el comentario `/* acá: el marcador cuatro veces más grande */` y borrá las dos líneas de abajo (las de 280 y 352).',
                    'En su lugar, escribí `SDL_SetRenderScale(lapiz, 4, 4);`.',
                    'Dibujá los dos números en `(60, 5)` y `(88, 5)` con `SDL_RenderDebugTextFormat`, como estaban.',
                    'Al final, `SDL_SetRenderScale(lapiz, 1, 1);`. Tocá **Jugar** y después **Comprobar**.'],
             eventos='cuadros 5', estado='buscar #ffffff',
             superarla='''
             Dos números enormes se encienden arriba de la red. Desde la puerta del salón, alguien aplaude: la
             Cancha ya tiene marcador de verdad.
             ''',
             imagen=['La pantalla de la máquina con dos números blancos enormes arriba, a cada lado de la red.',
                     'Kira, de lejos, señala el marcador; Arcadia asiente.',
                     'Gheco, que estaba subido a la pantalla, se baja de un salto.']),
        dict(titulo='Un respiro antes del saque',
             carta='Esperar | espera = 1 al hacer un punto · si espera > 0: espera -= dt y la pelota quieta',
             escena='''
             Apenas hay un punto, la pelota ya está saliendo otra vez. {mentor} no llega ni a acomodar la paleta.
             —Un segundito, por favor —pide—. Las máquinas viejas siempre daban un respiro.
             ''',
             gheco='''
             Se agrega una variable `espera`: los **segundos que faltan** para sacar. Ya está creada y arranca en 0.

             1. Cuando hay un punto, adentro del `if (punto)`: `espera = 1;` (un segundo).
             2. Donde se mueve la pelota, solo se la mueve si no hay que esperar:
             ```c
             if (espera > 0) {
                 espera -= dt;   /* va bajando, en segundos */
             } else {
                 pelota.x += vx * dt;
                 pelota.y += vy * dt;
             }
             ```
             Mientras `espera` sea mayor que 0, la pelota se queda quieta en el medio. Cuando llega a 0, vuelve a
             moverse sola.
             ''',
             desafio='Hacé que después de cada punto la pelota espere un segundo en el medio antes de salir.',
             pasos=['Buscá `/* acá: un segundo de respiro antes del saque */` (en el `if (punto)`) y escribí `espera = 1;`.',
                    'Buscá `/* acá: si hay que esperar, descontar el tiempo y no mover la pelota */`.',
                    'Envolvé las dos líneas que mueven la pelota con el `if (espera > 0) { espera -= dt; } else { … }` de la sugerencia.',
                    'Tocá **Jugar**, dejá pasar una pelota y mirá el respiro. Después, **Comprobar**.'],
             eventos='cuadros 90', estado='buscar #ffdc00',
             superarla='''
             Punto, un segundo de silencio, y el saque. {mentor} acomoda la paleta con calma y sonríe. —Ahora sí
             parece un partido. —El glitch del marcador se ordena: dos números claros que ya no se pisan.
             ''',
             imagen=['La pelota amarilla quieta en el centro de la cancha, con un brillo que late, esperando el saque.',
                     'Arcadia acomoda la paleta tranquila; Kira estira los dedos.',
                     'Un glitch chiquito se desarma en píxeles al lado del marcador; Gheco lo mira irse.']),
    ],
)
