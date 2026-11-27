PLANTILLA = r'''
#include <SDL3/SDL.h>

#define NUBES 6     /* cuántas nubes pasan por el cielo */

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Pista de los Biplanos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect avion = { 300, 400, 40, 40 };   /* la cajita del biplano: dónde está y cuánto mide */
    float velocidad = 300;                    /* píxeles por segundo */
    /* las nubes: la x y la y de cada una */
    float nx[NUBES] = { 60, 200, 420, 540, 120, 330 };
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
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

        //@ n1: acá: las flechas, mientras están apretadas, mueven el biplano
        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_LEFT]) {
            avion.x -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_RIGHT]) {
            avion.x += velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_UP]) {
            avion.y -= velocidad * dt;
        }
        if (teclas[SDL_SCANCODE_DOWN]) {
            avion.y += velocidad * dt;
        }
        //@ end
        //@ n2: acá: que el biplano no se salga de la ventana
        avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);
        avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);
        //@ end

        for (int n = 0; n < NUBES; n++) {
            //@ n3: acá: cada nube baja, así parece que el biplano avanza
            ny[n] += 80 * dt;
            //@ end
            //@ n4: acá: si una nube sale por abajo, vuelve a aparecer arriba, en otro lugar
            if (ny[n] > 480) {
                ny[n] = -30;
                nx[n] = SDL_rand(560);
            }
            //@ end
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 200, 220, 255, 255);  /* las nubes */
        for (int n = 0; n < NUBES; n++) {
            SDL_FRect nube = { nx[n], ny[n], 80, 30 };
            SDL_RenderFillRect(lapiz, &nube);
        }
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
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
    codigo='R06-N01', titulo='El biplano y el cielo', criatura='fantasma_fotograma', padre='R05-N06',
    lugar='La Pista de los Biplanos',
    temas='juegos.fisica', usa='juegos.entrada, col.arrays, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    El sexto pedazo de mapa lleva a las afueras de Ciudad Arcadia: una pista larga de pasto, un hangar de madera y,
    colgados del techo, biplanos de juguete con las alas de tela. En el medio del hangar hay una máquina alta con un
    volante de avión en lugar de botones. —La Pista de los Biplanos —dice {mentor}, y sopla el polvo del volante—. Acá
    se vuela: vos manejás el avión, y el cielo pasa por debajo. En la pantalla, unas nubes se mueven a saltitos, unas
    veces rápido y otras lento: el **Fantasma del Fotograma** se metió en el cielo.
    ''',
    objetivos='''
    Mover el **biplano** con las flechas mantenidas (en las cuatro direcciones), que **no se salga** de la ventana, y
    hacer que el **cielo se mueva**: nubes en un arreglo que bajan y, cuando salen por abajo, vuelven a aparecer
    arriba en otro lugar.
    ''',
    antes='''
    Toda la escalera hasta acá. De R02: las paletas con las teclas mantenidas y `SDL_clamp` (N01). De R01: el delta
    time (N04).
    ''',
    explicacion='''
    #### Qué es un juego de naves
    Un avión que vuela hacia arriba de la pantalla, dispara y esquiva a los enemigos que bajan. En realidad el avión
    casi no avanza: lo que se mueve es **el cielo**, que pasa hacia abajo, y eso hace parecer que el avión vuela.

    #### Moverse en cuatro direcciones
    Como las paletas del Pong, pero con las cuatro flechas: `SDL_GetKeyboardState` dice qué teclas están apretadas
    **ahora**, y cada una mueve el avión `velocidad * dt` píxeles. Si se aprietan dos (arriba y a la derecha), se
    mueve en diagonal.

    #### No salirse
    `SDL_clamp(valor, mínimo, máximo)` deja el valor adentro de los límites: la `x` entre 0 y `640 - avion.w`, la `y`
    entre 0 y `480 - avion.h`.

    #### El cielo que pasa
    Las nubes están en dos arreglos, `nx` y `ny`. En cada cuadro, todas bajan `80 * dt`. Cuando una pasa el borde de
    abajo, se la sube arriba de todo (un poquito afuera, en -30) y se le da otra `x` al azar: así el cielo no se
    termina nunca, con las mismas seis nubes.
    ''',
    para_que='''
    El fondo que se mueve es la base de todos los juegos que avanzan: naves, autitos de carrera, corredores sin fin.
    Reusar las mismas nubes en lugar de crear nuevas es un truco que vas a usar con balas, enemigos y partículas.
    ''',
    errores='''
    **Mover con los eventos.** `SDL_EVENT_KEY_DOWN` llega una vez por apretada: el avión saltaría y se quedaría quieto.
    Para moverse mientras la tecla está apretada, `SDL_GetKeyboardState`.

    **Olvidarse del `dt`.** Sin multiplicar por `dt`, el avión vuela distinto en cada compu: es el Fantasma del
    Fotograma.

    **Volver la nube a 0.** Si vuelve en `y = 0`, aparece de golpe, entera, arriba de la pantalla. En -30 entra de a poco.

    **Clamp con `640`.** La `x` es la esquina izquierda del avión: el máximo es `640 - avion.w`, si no, se sale el ala.
    ''',
    misiones=[
        dict(titulo='Despegar',
             carta='Flechas mantenidas | teclas = SDL_GetKeyboardState(NULL) · si teclas[SDL_SCANCODE_LEFT]: avion.x -= velocidad * dt (y las otras tres)',
             escena='''
             {mentor} enciende la máquina: en la pantalla hay un cielo azul y un biplano amarillo, quieto en el medio, con
             la hélice girando. Kira agarra el volante y lo mueve para todos lados. El avión ni se entera.
             ''',
             gheco='''
             Mientras una flecha está apretada, el avión se mueve `velocidad * dt` píxeles para ese lado. Como las paletas:
             ```c
             const bool *teclas = SDL_GetKeyboardState(NULL);   /* qué teclas están apretadas ahora */
             if (teclas[SDL_SCANCODE_LEFT]) {
                 avion.x -= velocidad * dt;
             }
             if (teclas[SDL_SCANCODE_RIGHT]) {
                 avion.x += velocidad * dt;
             }
             if (teclas[SDL_SCANCODE_UP]) {
                 avion.y -= velocidad * dt;     /* para arriba, la y baja */
             }
             if (teclas[SDL_SCANCODE_DOWN]) {
                 avion.y += velocidad * dt;
             }
             ```
             Son cuatro `if` separados (no `else`): así, con dos flechas a la vez, va en diagonal. El robot va a mantener
             apretada la flecha de la izquierda medio segundo.
             ''',
             desafio='Hacé que las cuatro flechas, mientras están apretadas, muevan el biplano.',
             pasos=['Buscá `/* acá: las flechas, mientras están apretadas, mueven el biplano */`.',
                    'Debajo, escribí `teclas` y los cuatro `if` de la sugerencia.',
                    'Tocá **Jugar**, hacé clic en el juego y volá con las flechas. Después, **Comprobar**.'],
             eventos='apretar Izquierda\ncuadros 30\nsoltar Izquierda\ncuadros 2', estado='buscar #ffc83c',
             superarla='''
             El biplano se inclina y vuela a la izquierda, después arriba, después en diagonal. Kira se ríe: el volante de
             la máquina se mueve solo con sus flechas. Gheco, colgado de un biplano de juguete del techo, hace *brrrr*.
             ''',
             imagen=['La pantalla de la máquina con un cielo azul y un biplano amarillo volando en diagonal, con rayitas de movimiento.',
                     'Kira maneja un volante de avión enorme en la máquina, feliz; Arcadia sopla el polvo del volante.',
                     'Gheco cuelga de un biplano de juguete con alas de tela, colgado del techo del hangar, haciendo brrrr.']),
        dict(titulo='Sin salirse del cielo',
             carta='Tope | avion.x = SDL_clamp(avion.x, 0, 640 - avion.w) · avion.y = SDL_clamp(avion.y, 0, 480 - avion.h)',
             escena='''
             Kira vuela a la izquierda… y el biplano se va de la pantalla y no vuelve. —El cielo de la máquina tiene bordes
             —dice {mentor}—. El avión no se puede ir.
             ''',
             gheco='''
             `SDL_clamp(valor, mínimo, máximo)` deja el valor entre los dos límites. Después de mover:
             ```c
             avion.x = SDL_clamp(avion.x, 0, 640 - avion.w);   /* ni más a la izquierda que 0, ni más a la derecha que 600 */
             avion.y = SDL_clamp(avion.y, 0, 480 - avion.h);
             ```
             La `x` es la esquina izquierda del avión: para que el ala derecha no se salga, el máximo es `640 - avion.w`.
             El robot va a mantener la flecha de la izquierda dos segundos.
             ''',
             desafio='Hacé que el biplano no se salga de la ventana por ningún borde.',
             pasos=['Buscá `/* acá: que el biplano no se salga de la ventana */`.',
                    'Debajo, escribí los dos `SDL_clamp` de la sugerencia.',
                    'Tocá **Jugar** y llevá el avión contra un borde. Después, **Comprobar**.'],
             eventos='apretar Izquierda\ncuadros 120\nsoltar Izquierda\ncuadros 2', estado='buscar #ffc83c',
             superarla='''
             El biplano llega al borde y se queda ahí, apoyado en el aire, como contra un vidrio. Kira lo pasea por los
             cuatro costados: no se escapa por ninguno.
             ''',
             imagen=['La pantalla de la máquina con el biplano amarillo pegado al borde izquierdo del cielo, sin salirse.',
                     'Kira gira el volante hasta el tope; Arcadia asiente.',
                     'Gheco, colgado del techo, se balancea de un biplano de juguete a otro.']),
        dict(titulo='El cielo pasa',
             carta='Fondo | para cada nube n: ny[n] += 80 * dt',
             criatura='fantasma_fotograma',
             escena='''
             El biplano vuela, pero las nubes están clavadas en el cielo, como pintadas: parece que el avión no avanza.
             Las nubes de la pantalla de al lado, en cambio, saltan rápido y lento. —El Fantasma del Fotograma —dice
             {mentor}—. Las nubes tienen que bajar, siempre igual, con el `dt`.
             ''',
             gheco='''
             Ya está el `for` que pasa por las seis nubes. Adentro, que cada una baje:
             ```c
             ny[n] += 80 * dt;     /* 80 píxeles por segundo, hacia abajo */
             ```
             El avión casi no se mueve, pero las nubes pasan por debajo: eso hace parecer que vuela hacia arriba. El robot
             va a esperar un segundo.
             ''',
             desafio='Hacé que las nubes bajen 80 píxeles por segundo, para que parezca que el biplano vuela.',
             pasos=['Buscá `/* acá: cada nube baja, así parece que el biplano avanza */` (adentro del `for` de las nubes).',
                    'Debajo, escribí la línea de la sugerencia.',
                    'Tocá **Jugar**: las nubes tienen que pasar. Después, **Comprobar**.'],
             eventos='cuadros 60', estado='buscar #c8dcff',
             superarla='''
             Las nubes empiezan a pasar, parejitas, y de golpe el biplano parece volar de verdad. El Fantasma del Fotograma
             trata de apurar una nube, pero el `dt` no lo deja, y se va volando, ofendido.
             ''',
             imagen=['La pantalla de la máquina con el biplano amarillo y nubes blancas pasando hacia abajo, con rayitas de velocidad.',
                     'Un fantasma redondo y translúcido, borroso, se aleja volando entre las nubes de la pantalla, ofendido.',
                     'Kira maneja sonriendo; Arcadia mira por la puerta del hangar la pista de pasto; Gheco siente el viento en la cara.']),
        dict(titulo='Un cielo sin fin',
             carta='Volver arriba | si ny[n] > 480: ny[n] = -30 · nx[n] = SDL_rand(560)',
             escena='''
             Las nubes pasan… y se terminan. Al rato el cielo queda vacío, azul y aburrido. —No hacen falta más nubes
             —dice {mentor}—. Las que salen por abajo, que vuelvan a entrar por arriba.
             ''',
             gheco='''
             Adentro del mismo `for`, después de bajarla:
             ```c
             if (ny[n] > 480) {          /* ¿ya salió por abajo? */
                 ny[n] = -30;            /* vuelve arriba, un poquito afuera */
                 nx[n] = SDL_rand(560);  /* en otro lugar, para que no se note */
             }
             ```
             - En -30 la nube (que mide 30 de alto) queda justo arriba del borde y entra de a poco.
             - `SDL_rand(560)` da un número del 0 al 559: la nube mide 80, así que nunca se sale por la derecha.

             El robot va a esperar cinco segundos.
             ''',
             desafio='Hacé que la nube que sale por abajo vuelva a entrar por arriba, en otro lugar.',
             pasos=['Buscá `/* acá: si una nube sale por abajo, vuelve a aparecer arriba, en otro lugar */`.',
                    'Debajo, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y esperá: el cielo no se tiene que vaciar. Después, **Comprobar**.'],
             eventos='cuadros 300', estado='buscar #c8dcff',
             superarla='''
             Las nubes que se van por abajo vuelven a asomar por arriba, cada vez en otro lugar. El cielo no se termina
             nunca. Gheco se queda mirando, hipnotizado, y cuenta: son solo seis.
             ''',
             imagen=['La pantalla de la máquina con nubes entrando por arriba y saliendo por abajo, con flechas curvas que las unen.',
                     'Kira vuela tranquila; Arcadia sonríe, con los brazos cruzados.',
                     'Gheco cuenta seis nubes con los dedos, hipnotizado, arriba de la máquina.']),
    ],
)
