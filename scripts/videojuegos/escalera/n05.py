PLANTILLA = r'''
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

/* Los momentos del juego, con nombre */
enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;   /* arranca en el menú */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && !evento.key.repeat) {
                SDL_Keycode tecla = evento.key.key;
                if (estado == MENU && tecla == SDLK_1) contraLaMaquina = true;
                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;
                //@ n1: acá: en el menú, con la barra espaciadora empieza el partido
                if (estado == MENU && tecla == SDLK_SPACE) {
                    estado = JUGANDO;
                }
                //@ end
                //@ n3: acá: en el fin, con la R el marcador vuelve a 0 y se vuelve al menú
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                //@ end
                //@ n4: acá: jugando, con ESC se vuelve al menú
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) {
                    estado = MENU;
                }
                //@ end
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        /* Todo lo que se mueve, solo mientras se juega */
        if (estado == JUGANDO) {
            const bool *teclas = SDL_GetKeyboardState(NULL);
            if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
            if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
            izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);
            if (contraLaMaquina) {
                float objetivo = (vx > 0) ? pelota.y + pelota.h / 2 : 240;
                float distancia = objetivo - (der.y + der.h / 2);
                if (distancia < -10) der.y -= 240 * dt;
                if (distancia > 10) der.y += 240 * dt;
            } else {
                if (teclas[SDL_SCANCODE_UP]) der.y -= 300 * dt;
                if (teclas[SDL_SCANCODE_DOWN]) der.y += 300 * dt;
            }
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
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (izq.y + izq.h / 2)) * 5;
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
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
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                //@ n2: acá: si alguien llegó a 5, se terminó el partido
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
                //@ end
            }
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

        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 6, 6);
            SDL_RenderDebugText(lapiz, 37, 20, "PONG");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 248, 260, "ESPACIO: JUGAR");
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 200, 300, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");
        } else {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderFillRect(lapiz, &pelota);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugTextFormat(lapiz, 60, 5, "%d", puntosIzq);
            SDL_RenderDebugTextFormat(lapiz, 88, 5, "%d", puntosDer);
            SDL_SetRenderScale(lapiz, 1, 1);
        }
        if (estado == FIN) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 244, "R: REVANCHA");
        }
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
    codigo='R02-N05', titulo='Menú, partido y fin', criatura='bucle_eterno', padre='R02-N04',
    temas='juegos.estados', usa='juegos.entrada, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    A la mañana siguiente llega gente nueva a la Cancha: chicos del barrio que vieron las luces encendidas. Se
    paran frente a la máquina y no saben qué hacer: la pelota ya está corriendo, no hay cartel de bienvenida, y
    el partido no termina nunca. —Un juego de verdad tiene un principio y un final —dice {mentor}—. Un menú para
    elegir, el partido, y alguien que gana. Si no, es un **Bucle Eterno**. —Y en el borde de la pantalla, la
    serpiente de luz se muerde la cola, contenta.
    ''',
    objetivos='''
    Ordenar el juego en **estados** (momentos): el menú, el partido y el fin. Empezar con la barra espaciadora,
    terminar cuando alguien llega a 5, jugar la revancha con la R y volver al menú con ESC.
    ''',
    antes='''
    R02-N04 (la máquina juega). De R01: el evento de una tecla (N02) y el jefe «Junta las gemas» (N10), que ya
    tenía un fin y una revancha.
    ''',
    explicacion='''
    #### Los momentos de un juego
    Casi todos los juegos pasan por los mismos momentos: un **menú** donde se elige, el **partido** y el **fin**
    con el resultado. A cada uno se le dice **estado**. En cada cuadro el juego pregunta en qué estado está y
    hace lo que corresponde: en el menú no se mueve nada, en el partido se mueve todo, en el fin se muestra quién
    ganó.

    #### Ponerles nombre: `enum`
    Se podría usar un número (0 el menú, 1 el partido, 2 el fin), pero es fácil confundirse. Un `enum` le pone
    nombre a esos números:
    ```c
    enum Estado { MENU, JUGANDO, FIN };   /* MENU vale 0, JUGANDO 1, FIN 2 */
    enum Estado estado = MENU;
    ```
    Después se pregunta `if (estado == JUGANDO)`, que se lee solo.

    #### Pasar de un estado a otro
    Cada cambio tiene su motivo, y casi siempre es un evento:
    - en el **menú**, la barra espaciadora → **jugando**;
    - **jugando**, alguien llega a 5 → **fin**;
    - en el **fin**, la R → el marcador a 0 y otra vez al **menú**;
    - **jugando**, ESC → **menú** (para cambiar entre uno y dos jugadores).

    Siempre se pregunta en qué estado está **y** qué tecla se apretó: la R solo hace algo en el fin; el espacio,
    solo en el menú.

    #### Todo lo que se mueve, adentro de `if (estado == JUGANDO)`
    Las paletas, la pelota y los puntos se actualizan solo mientras se juega. Por eso en el menú y en el fin
    queda todo quieto, aunque el bucle siga dando vueltas.
    ''',
    para_que='''
    Todos los juegos de la escalera tienen estados: el Arkanoid (menú, jugando, nivel superado, fin), el Tetris,
    las naves… Y muchos programas que no son juegos también: un cajero automático o un formulario de varios
    pasos son estados con sus cambios.
    ''',
    errores='''
    **Bucle Eterno: un juego sin fin.** Sin el estado `FIN`, el partido sigue para siempre y nadie gana.

    **No preguntar el estado antes de la tecla.** Si la R reinicia sin preguntar `estado == FIN`, en medio del
    partido cualquier R borra el marcador.

    **Cambiar de estado y seguir moviendo.** Si la actualización no está adentro de `if (estado == JUGANDO)`, la
    pelota sigue corriendo detrás del menú.

    **Comparar con `=` en lugar de `==`.** `if (estado = FIN)` no pregunta: cambia el estado a `FIN` y siempre es
    verdadero.
    ''',
    misiones=[
        dict(titulo='El menú',
             carta='Empezar | en el menú, evento de la barra espaciadora: estado = JUGANDO',
             escena='''
             Los chicos del barrio miran el cartel **PONG** que ahora brilla en la pantalla. —¿Y ahora? —pregunta
             uno. Kira aprieta la barra espaciadora… y no pasa nada. El menú no deja empezar.
             ''',
             gheco='''
             El juego ya arranca en el estado `MENU` y muestra el cartel. Falta la salida: cuando se aprieta la
             barra espaciadora **estando en el menú**, el estado pasa a `JUGANDO`.

             Va adentro del `if (evento.type == SDL_EVENT_KEY_DOWN …)`, donde ya está guardada la tecla en la
             variable `tecla`:
             ```c
             if (estado == MENU && tecla == SDLK_SPACE) {
                 estado = JUGANDO;
             }
             ```
             `&&` quiere decir «y»: las dos cosas tienen que ser ciertas.
             ''',
             desafio='Hacé que en el menú, con la barra espaciadora, empiece el partido.',
             pasos=['Buscá el comentario `/* acá: en el menú, con la barra espaciadora empieza el partido */`.',
                    'Escribí `if (estado == MENU && tecla == SDLK_SPACE) {`.',
                    'Adentro, `estado = JUGANDO;`, y cerrá la llave.',
                    'Tocá **Jugar**, hacé clic en el juego y apretá la barra espaciadora. Después, **Comprobar**.'],
             eventos='cuadros 5\ntecla Espacio\ncuadros 30', estado='textos',
             superarla='''
             Espacio, y la pelota sale. Los chicos gritan. Uno ya está pidiendo el turno.
             ''',
             imagen=['La pantalla de la Cancha con un cartel enorme amarillo de bloques de luz arriba y dos renglones blancos abajo (sin texto legible).',
                     'Un grupo de chicos del barrio, con abrigos cerrados, rodea la máquina mirando con curiosidad.',
                     'Kira aprieta la barra espaciadora; Gheco, sobre la máquina, levanta los brazos.']),
        dict(titulo='Gana el que llega a 5', criatura='bucle_eterno',
             carta='El fin | después de un punto: si alguno llegó a 5, estado = FIN',
             escena='''
             Los chicos juegan y juegan: 8 a 6, 12 a 9, 20 a 18… —¿Cuándo termina? —pregunta uno, cansado. En la
             pantalla, el Bucle Eterno da vueltas y vueltas, feliz.
             ''',
             gheco='''
             El partido tiene que terminar cuando alguno llega a **5 puntos**. Lo mejor es preguntarlo justo después
             de un punto, adentro del `if (punto)`:
             ```c
             if (puntosIzq == 5 || puntosDer == 5) {
                 estado = FIN;
             }
             ```
             `||` quiere decir «o»: alcanza con que uno de los dos llegue. En el estado `FIN` la pantalla ya
             muestra quién ganó.

             El robot va a jugar un partido de a dos sin mover las paletas, hasta que alguien llegue a 5.
             ''',
             desafio='Hacé que el partido termine cuando alguno de los dos llega a 5 puntos.',
             pasos=['Buscá el comentario `/* acá: si alguien llegó a 5, se terminó el partido */` (adentro del `if (punto)`).',
                    'Escribí `if (puntosIzq == 5 || puntosDer == 5) {`.',
                    'Adentro, `estado = FIN;`, y cerrá la llave.',
                    'Tocá **Jugar** y jugá hasta 5. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla 2\ntecla Espacio\ncuadros 1500', estado='textos',
             superarla='''
             5 a 3. La pantalla se queda quieta y aparece el cartel del ganador. El Bucle Eterno se suelta la cola,
             confundido: el juego terminó, y él no sabe dar vueltas sin fin.
             ''',
             imagen=['La pantalla de la Cancha quieta, con el marcador grande arriba y un cartel amarillo de ganador en el medio (sin texto legible).',
                     'Una serpiente de luz violeta, el Bucle Eterno, suelta su cola confundida en el borde de la pantalla.',
                     'Los chicos festejan; Kira aplaude; Gheco levanta la mano de un ganador imaginario.']),
        dict(titulo='Revancha',
             carta='La revancha | en el fin, la R: puntos a 0 y estado = MENU',
             escena='''
             —¡Revancha! —pide el que perdió. Pero la pantalla se quedó congelada en el fin y no hay forma de
             volver a empezar sin apagar la máquina.
             ''',
             gheco='''
             En el estado `FIN`, la R tiene que dejar todo listo para otro partido: el marcador en 0 y de vuelta al
             menú (así se puede elegir otra vez uno o dos jugadores).
             ```c
             if (estado == FIN && tecla == SDLK_R) {
                 puntosIzq = 0;
                 puntosDer = 0;
                 estado = MENU;
             }
             ```
             Va con los demás eventos de teclado. La pelota no hace falta acomodarla: después del último punto ya
             quedó en el medio.
             ''',
             desafio='Hacé que en el fin, con la R, el marcador vuelva a 0 y se vuelva al menú.',
             pasos=['Buscá el comentario `/* acá: en el fin, con la R el marcador vuelve a 0 y se vuelve al menú */`.',
                    'Escribí `if (estado == FIN && tecla == SDLK_R) {`.',
                    'Adentro, `puntosIzq = 0;`, `puntosDer = 0;` y `estado = MENU;`. Cerrá la llave.',
                    'Tocá **Jugar**, terminá un partido y apretá la R. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla 2\ntecla Espacio\ncuadros 1500\ntecla R\ncuadros 5', estado='textos',
             superarla='''
             R, y el cartel de **PONG** vuelve a brillar. Los chicos hacen fila para la revancha. {mentor} sonríe
             desde la puerta: hacía años que no había fila en la Cancha.
             ''',
             imagen=['Una fila de chicos del barrio, con abrigos cerrados, esperando turno frente a la máquina de la Cancha.',
                     'En la pantalla, otra vez el cartel amarillo enorme del menú.',
                     'Arcadia, desde la puerta, sonríe; Kira y Gheco ordenan la fila.']),
        dict(titulo='Volver al menú',
             carta='Salir al menú | jugando, ESC: estado = MENU',
             escena='''
             A mitad de un partido, una chica quiere cambiar a jugar contra la máquina. Pero el 1 y el 2 solo
             funcionan en el menú, y al menú no se puede volver.
             ''',
             gheco='''
             En la Clase 0, ESC cerraba el juego. Acá, **jugando**, ESC vuelve al **menú**, como en casi todos los
             juegos:
             ```c
             if (estado == JUGANDO && tecla == SDLK_ESCAPE) {
                 estado = MENU;
             }
             ```
             El marcador no se borra: si vuelve a apretar espacio, sigue el mismo partido.
             ''',
             desafio='Hacé que jugando, con ESC, se vuelva al menú.',
             pasos=['Buscá el comentario `/* acá: jugando, con ESC se vuelve al menú */`.',
                    'Escribí `if (estado == JUGANDO && tecla == SDLK_ESCAPE) {`.',
                    'Adentro, `estado = MENU;`, y cerrá la llave.',
                    'Tocá **Jugar**: empezá, apretá ESC, cambiá con el 1 o el 2 y seguí. Después, **Comprobar**.'],
             eventos='cuadros 5\ntecla Espacio\ncuadros 30\ntecla Escape\ncuadros 5', estado='textos',
             superarla='''
             Menú, partido, fin, revancha y vuelta al menú: la máquina de la Cancha ya es un juego completo. Los
             chicos no se quieren ir. El Bucle Eterno, sin vueltas que dar, se escurre por debajo de la máquina.
             ''',
             imagen=['La máquina de la Cancha encendida a pleno, con chicos jugando y otros mirando alrededor.',
                     'Una serpiente de luz violeta se escurre por debajo del gabinete.',
                     'Kira y Arcadia chocan los cinco; Gheco, arriba de la máquina, saluda a los chicos.']),
    ],
)
