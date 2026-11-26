PLANTILLA = r'''
#include <SDL3/SDL.h>

static bool toca(SDL_FRect a, SDL_FRect b)
{
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

//@ n4+
static bool mudo = false;   /* true: la máquina no suena */
//@ end

/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    //@ n4: acá: si está en silencio, salir sin sonar
    if (mudo) {
        return;
    }
    //@ end
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

enum Estado { MENU, JUGANDO, FIN };

int main(void)
{
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

    SDL_Window *ventana = NULL;
    SDL_Renderer *lapiz = NULL;
    SDL_CreateWindowAndRenderer("La Cancha de las Paletas", 640, 480, 0, &ventana, &lapiz);

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);

    SDL_FRect izq = { 20, 200, 12, 80 };
    SDL_FRect der = { 608, 170, 12, 80 };
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;
    enum Estado estado = MENU;
    //@ n3+
    bool pausado = false;
    //@ end
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
                if (estado == MENU && tecla == SDLK_SPACE) estado = JUGANDO;
                if (estado == JUGANDO && tecla == SDLK_ESCAPE) estado = MENU;
                if (estado == FIN && tecla == SDLK_R) {
                    puntosIzq = 0;
                    puntosDer = 0;
                    estado = MENU;
                }
                //@ n3: acá: jugando, la P pausa y despausa
                if (estado == JUGANDO && tecla == SDLK_P) {
                    pausado = !pausado;
                }
                //@ end
                //@ n4: acá: la M prende y apaga el sonido
                if (tecla == SDLK_M) {
                    mudo = !mudo;
                }
                //@ end
            }
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        //@ n3: acá: no mover nada mientras está en pausa
        if (estado == JUGANDO && !pausado) {
        //@ else
        if (estado == JUGANDO) {
        //@ end
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
                //@ n1: acá: el toc de la paleta
                pitido(parlante, 440, 0.05f);
                //@ end
            }
            if (toca(pelota, der) && vx > 0) {
                pelota.x = der.x - pelota.w;
                vx = SDL_clamp(-vx * 1.1f, -600, 600);
                vy = ((pelota.y + pelota.h / 2) - (der.y + der.h / 2)) * 5;
                //@ n1
                pitido(parlante, 440, 0.05f);
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
                //@ n2: acá: el punto suena más grave y más largo
                pitido(parlante, 220, 0.3f);
                //@ end
                pelota.x = 314;
                pelota.y = 234;
                vx = (vx > 0) ? -300 : 300;
                vy = 0;
                espera = 1;
                if (puntosIzq == 5 || puntosDer == 5) {
                    estado = FIN;
                }
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
        //@ n3: acá: el cartel de la pausa
        if (estado == JUGANDO && pausado) {
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
        }
        //@ end
        //@ n4: acá: avisar que está en silencio
        if (mudo) {
            SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
            SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");
        }
        //@ end
        SDL_RenderPresent(lapiz);
        SDL_Delay(16);
    }

    SDL_DestroyAudioStream(parlante);
    SDL_DestroyRenderer(lapiz);
    SDL_DestroyWindow(ventana);
    SDL_Quit();
    return 0;
}
'''

NODO = dict(
    codigo='R02-N06', titulo='Sonido y pausa', criatura='fuga_texturas', padre='R02-N05',
    temas='juegos.sonido', usa='juegos.estados, juegos.entrada',
    plantilla=PLANTILLA,
    cronica='''
    La Cancha está llena, pero algo falta. {mentor} cierra los ojos y escucha: las paletas golpean en silencio,
    los puntos pasan sin que nadie se entere. —Las máquinas de antes hacían *toc* —dice—. Un toc agudo en cada
    golpe y un *bum* grave en cada punto. Con los ojos cerrados sabías cómo iba el partido. —Y además, cuando
    llaman a cenar, hay que poder parar sin perder. En el estante del fondo, una niebla de imágenes repetidas se
    agita: la **Fuga de Texturas** también se come los sonidos que nadie libera.
    ''',
    objetivos='''
    Que la Cancha suene: un pitido corto y agudo en cada golpe de paleta y uno grave y largo en cada punto.
    Además, una pausa con la P y un botón de silencio con la M.
    ''',
    antes='''
    R02-N05 (menú, partido y fin). De R01: el sonido (N09), con la función `pitido`.
    ''',
    explicacion='''
    #### El parlante y el pitido
    Es lo mismo que en R01-N09: se abre el parlante una vez al principio y la función `pitido` arma una onda y
    se la manda. El número de vueltas por segundo (la **frecuencia**) decide si suena agudo o grave: 440 es un
    *la*, agudo y corto para el golpe; 220 es la misma nota una octava más grave, para el punto.

    #### ¿Dónde va cada sonido?
    Exactamente donde pasa la cosa: el toc, adentro de los `if (toca(...))` de las paletas; el bum, adentro del
    `if (punto)`. Así suena en el mismo cuadro en que se ve.

    #### La pausa
    Una variable `bool pausado`. La P le da la vuelta: `pausado = !pausado;` (`!` es «lo contrario»: si era
    `true` pasa a `false`, y al revés). Mientras esté en pausa, no se actualiza nada: se agrega a la condición
    que envuelve todo lo que se mueve, `if (estado == JUGANDO && !pausado)`. El dibujo sigue, así se ve la
    cancha quieta con el cartel.

    #### Silencio
    Otra variable que se da vuelta con una tecla: `mudo`. Esta vez es **global** (afuera de `main`, con
    `static`), porque la usa la función `pitido`: si está en silencio, `return;` sale de la función sin hacer
    nada.
    ''',
    para_que='''
    El sonido dice cosas sin que haya que mirar: un golpe, un punto, un peligro. Y la pausa y el silencio son
    dos cosas que cualquier jugador espera encontrar; se van a repetir en cada juego de la escalera.
    ''',
    errores='''
    **Fuga de Texturas: no liberar la onda.** `pitido` pide memoria con `SDL_malloc` en cada sonido. Si falta el
    `SDL_free`, cada golpe se queda con un pedazo de memoria y la máquina se ahoga de a poco.

    **Sonar en cada cuadro.** Si el pitido va afuera del `if (toca(...))`, suena 60 veces por segundo y se
    amontona en el parlante.

    **Pausar con `estado`.** Si la P cambia el estado a otro y la R o el ESC también, se pierde dónde estaba el
    partido. Una variable aparte, `pausado`, es más simple.

    **Olvidar `!pausado` en la condición.** El cartel dice PAUSA, pero la pelota sigue corriendo.
    ''',
    misiones=[
        dict(titulo='El toc de la paleta',
             carta='Sonar al golpear | pitido(parlante, 440, 0.05f) adentro de cada toca(...)',
             escena='''
             —El toc primero —dice {mentor}—. Cortito y agudo, en cada golpe. Como una pelotita de ping-pong.
             ''',
             gheco='''
             El parlante y la función `pitido` ya están (son los de R01-N09). Falta llamarla **justo cuando una
             paleta devuelve la pelota**, adentro de cada `if (toca(...))`:
             ```c
             pitido(parlante, 440, 0.05f);   /* agudo (440) y cortito (5 centésimas de segundo) */
             ```
             En las **dos** paletas: la izquierda y la derecha.
             ''',
             desafio='Hacé que suene un pitido corto y agudo (440, 0.05 segundos) cada vez que una paleta devuelve la pelota.',
             pasos=['Buscá el comentario `/* acá: el toc de la paleta */` (adentro de la paleta izquierda) y escribí `pitido(parlante, 440, 0.05f);`.',
                    'Escribí la misma línea al final del `if (toca(pelota, der) && vx > 0)`.',
                    'Tocá **Jugar** (con el sonido de la compu prendido) y escuchá los golpes. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla Espacio\ncuadros 120', estado='sonido',
             superarla='''
             *Toc… toc… toc.* Los chicos del barrio se quedan callados para escuchar. Uno cierra los ojos y sigue el
             partido de oído.
             ''',
             imagen=['La máquina de la Cancha con anillos de sonido cian saliendo del borde de la pantalla en cada golpe.',
                     'Un chico del barrio con los ojos cerrados, escuchando; Kira juega.',
                     'Gheco mueve la cabeza al ritmo del toc, con los auriculares gigantes puestos.']),
        dict(titulo='El bum del punto',
             carta='Sonar al hacer un punto | pitido(parlante, 220, 0.3f) adentro del if (punto)',
             escena='''
             —Y el punto, que se note —pide {mentor}—. Más grave y más largo. Que hasta los de la puerta sepan que
             alguien hizo un punto.
             ''',
             gheco='''
             El punto se nota con otro pitido, **más grave** (220 vueltas por segundo, la mitad que el toc) y **más
             largo** (0.3 segundos). Va al principio del `if (punto)`:
             ```c
             pitido(parlante, 220, 0.3f);
             ```

             El robot va a jugar de a dos y va a subir la paleta rosa para que la pelota pase sin tocar ninguna
             paleta: solo va a sonar el punto.
             ''',
             desafio='Hacé que suene un pitido grave y largo (220, 0.3 segundos) cada vez que alguien hace un punto.',
             pasos=['Buscá el comentario `/* acá: el punto suena más grave y más largo */` (adentro del `if (punto)`).',
                    'Debajo, escribí `pitido(parlante, 220, 0.3f);`.',
                    'Tocá **Jugar**, dejá pasar una pelota y escuchá. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla 2\ntecla Espacio\napretar Arriba\ncuadros 40\nsoltar Arriba\ncuadros 40', estado='sonido',
             superarla='''
             *Bum.* Desde la puerta, alguien grita «¡punto!» sin haber visto la pantalla. {mentor} sonríe: así
             sonaba la Cancha cuando estaba llena.
             ''',
             imagen=['Un anillo de sonido grande, violeta y grave, saliendo de la máquina de la Cancha.',
                     'En la puerta del salón, un chico grita con las manos alrededor de la boca.',
                     'Arcadia sonríe con los ojos cerrados; Gheco, sobre la máquina, se tapa los oídos.']),
        dict(titulo='Pausa',
             carta='Pausar | P: pausado = !pausado · si está en pausa, no se mueve nada',
             escena='''
             —¡A cenar! —grita alguien desde la puerta. El chico que va ganando no puede soltar los controles: si se
             va, pierde. —Una pausa —dice Kira—. Las máquinas tienen que poder esperar.
             ''',
             gheco='''
             La variable `pausado` ya existe y arranca en `false`. Hacen falta tres cosas:
             1. Jugando, la **P** le da la vuelta: `pausado = !pausado;` (`!` es «lo contrario»).
             2. Lo que se mueve, solo si **no** está en pausa: la condición grande pasa a ser
                `if (estado == JUGANDO && !pausado) {`.
             3. Un cartel que diga PAUSA:
             ```c
             if (estado == JUGANDO && pausado) {
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
                 SDL_RenderDebugText(lapiz, 300, 236, "PAUSA");
             }
             ```
             El robot va a apretar la P en medio del partido.
             ''',
             desafio='Hacé que jugando, con la P, el partido se pause (nada se mueve y aparece el cartel PAUSA) y se despause.',
             pasos=['Buscá `/* acá: jugando, la P pausa y despausa */` y escribí `if (estado == JUGANDO && tecla == SDLK_P) { pausado = !pausado; }`.',
                    'Buscá `/* acá: no mover nada mientras está en pausa */` y cambiá la línea de abajo por `if (estado == JUGANDO && !pausado) {`.',
                    'Buscá `/* acá: el cartel de la pausa */` y escribí el `if` del cartel de la sugerencia.',
                    'Tocá **Jugar**, apretá la P dos veces y mirá. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla Espacio\ncuadros 20\ntecla P\ncuadros 30', estado='buscar #ffdc00\ntextos',
             superarla='''
             P, y la cancha se congela con un cartel de PAUSA. El chico se va a cenar tranquilo. —Vuelvo en diez
             minutos —avisa—. No me toquen la paleta.
             ''',
             imagen=['La pantalla de la Cancha congelada, con la pelota quieta en el aire y un cartel blanco en el medio (sin texto legible).',
                     'Un chico del barrio se aleja hacia la puerta, mirando para atrás.',
                     'Gheco hace guardia sentado sobre la paleta cian, de brazos cruzados.']),
        dict(titulo='Silencio', criatura='fuga_texturas',
             carta='Silenciar | M: mudo = !mudo · en pitido: if (mudo) return;',
             escena='''
             Es de noche y {mentor} quiere seguir probando la máquina sin despertar a los vecinos de la Cancha. —Un
             botón de silencio —pide—. Que se pueda jugar callado.
             ''',
             gheco='''
             La variable `mudo` ya existe, pero esta vez es **global**: está arriba de todo, afuera de `main`, con
             `static`. Así la puede ver la función `pitido`.
             1. Al principio de `pitido`, si está en silencio, se sale sin hacer nada:
             ```c
             if (mudo) {
                 return;
             }
             ```
             2. Con la **M**, en cualquier estado: `if (tecla == SDLK_M) { mudo = !mudo; }`.
             3. Un aviso abajo, a la derecha, cuando está en silencio: `if (mudo)` con
                `SDL_RenderDebugText(lapiz, 528, 460, "SIN SONIDO");`.

             El robot va a apretar la M antes de jugar: no tiene que sonar nada.
             ''',
             desafio='Hacé que con la M la máquina se quede en silencio (ningún pitido) y vuelva a sonar, con un aviso en pantalla.',
             pasos=['Buscá `/* acá: si está en silencio, salir sin sonar */` (en `pitido`) y escribí el `if (mudo) { return; }`.',
                    'Buscá `/* acá: la M prende y apaga el sonido */` y escribí `if (tecla == SDLK_M) { mudo = !mudo; }`.',
                    'Buscá `/* acá: avisar que está en silencio */` y escribí el `if (mudo)` con el color y el texto «SIN SONIDO».',
                    'Tocá **Jugar**, apretá la M y escuchá. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla M\ntecla Espacio\ncuadros 120', estado='sonido\ntextos',
             superarla='''
             M, y la Cancha juega en silencio, con el cartelito en una esquina. En el estante del fondo, la Fuga de
             Texturas busca sonidos olvidados que comerse… y no encuentra ninguno: cada pitido libera su memoria.
             Se deshace en el aire.
             ''',
             imagen=['La máquina de la Cancha jugando en silencio, con un cartelito violeta en la esquina de la pantalla (sin texto legible).',
                     'En un estante del fondo, una niebla de imágenes repetidas (la Fuga de Texturas) se deshace en el aire.',
                     'Arcadia juega tranquila; Kira, a su lado, se lleva un dedo a la boca; Gheco duerme acurrucado sobre la máquina.']),
    ],
)
