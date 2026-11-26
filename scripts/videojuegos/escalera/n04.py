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
    SDL_FRect der = { 608, 170, 12, 80 };   /* la máquina (o el jugador 2, con las flechas) */
    SDL_FRect pelota = { 314, 234, 12, 12 };
    float vx = 300;
    float vy = 0;
    int puntosIzq = 0;
    int puntosDer = 0;
    float espera = 0;
    bool contraLaMaquina = true;   /* true: la paleta derecha la mueve la máquina */
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            //@ n4: acá: con la tecla 1, contra la máquina; con la 2, de a dos
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_1) {
                contraLaMaquina = true;
            }
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_2) {
                contraLaMaquina = false;
            }
            //@ end
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        if (teclas[SDL_SCANCODE_W]) izq.y -= 300 * dt;
        if (teclas[SDL_SCANCODE_S]) izq.y += 300 * dt;
        izq.y = SDL_clamp(izq.y, 0, 480 - izq.h);

        if (contraLaMaquina) {
            /* La máquina: mira hacia dónde tiene que ir y se acerca, sin pasar de 240 píxeles por segundo */
            //@ n3: acá: seguir la pelota solo cuando viene; si no, volver al medio (240)
            float objetivo = 240;
            if (vx > 0) {
                objetivo = pelota.y + pelota.h / 2;
            }
            //@ else
            float objetivo = pelota.y + pelota.h / 2;
            //@ end
            float distancia = objetivo - (der.y + der.h / 2);
            //@ n2: acá: si está cerca (a menos de 10 píxeles), no moverse
            if (SDL_fabsf(distancia) < 10) {
                distancia = 0;
            }
            //@ end
            //@ n1: acá: acercar la paleta al objetivo
            if (distancia < 0) der.y -= 240 * dt;
            if (distancia > 0) der.y += 240 * dt;
            //@ end
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
        SDL_SetRenderDrawColor(lapiz, 150, 140, 190, 255);
        SDL_RenderDebugText(lapiz, 200, 460, contraLaMaquina ? "1 JUGADOR: CONTRA LA MAQUINA" : "2 JUGADORES");
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
    codigo='R02-N04', titulo='La máquina juega', criatura='glitch', padre='R02-N03',
    temas='juegos.ia', usa='juegos.colisiones, juegos.entrada, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Es tarde. {mentor} se va a revisar las luces del salón y Kira se queda sola frente a la máquina, con la
    paleta rosa quieta del otro lado. —Si nadie juega de ese lado, no hay partido —dice Gheco. Entonces Kira
    tiene una idea: ¿y si la paleta rosa se moviera sola? Una máquina que juega. Las de antes lo hacían: mirabas
    la pantalla y del otro lado no había nadie, y aun así te devolvían la pelota. Un **glitch** se ríe en la
    pantalla: él sabe cómo hacer temblar a una paleta que piensa demasiado.
    ''',
    objetivos='''
    Programar una paleta que juega sola (una inteligencia artificial muy simple): que mire dónde está la pelota y
    se acerque, con una velocidad máxima para que se le pueda ganar, que no tiemble cuando ya llegó, que vuelva al
    medio mientras la pelota se aleja y que se pueda elegir entre jugar contra la máquina o de a dos.
    ''',
    antes='''
    R02-N03 (la pelota que acelera). De R01: el teclado (N02) y el delta time (N04).
    ''',
    explicacion='''
    #### Una máquina que juega no adivina
    La «inteligencia» de la paleta es una regla chiquita, repetida en cada cuadro:
    1. **¿A dónde tengo que ir?** Al lugar de la pelota (el **objetivo**).
    2. **¿Qué tan lejos estoy?** El objetivo menos el centro de la paleta: la **distancia**.
    3. **Me acerco un poquito**: si la distancia es negativa (el objetivo está más arriba), subo; si es positiva,
       bajo.

    #### Que se le pueda ganar
    Si la paleta fuera directo al objetivo (`der.y = objetivo`), nunca erraría: aburridísimo. Por eso se mueve como
    mucho **240 píxeles por segundo** (`240 * dt` por cuadro), menos que la pelota cuando se acelera. Si la pelota va
    muy rápido o en diagonal, no llega.

    #### Que no tiemble
    Si ya está casi en el lugar, un paso de más la pasa, y en el cuadro siguiente vuelve, y se pasa para el otro
    lado: tiembla. La solución es una **zona muerta**: si está a menos de 10 píxeles, no se mueve.
    `SDL_fabsf(distancia)` es la distancia sin el signo (el valor absoluto: -7 da 7).

    #### Jugar como alguien
    Un buen jugador no persigue la pelota cuando se aleja: vuelve al medio y espera. Si `vx > 0`, la pelota viene
    hacia la paleta derecha: el objetivo es la pelota. Si no, el objetivo es el medio de la cancha (240).

    #### Uno o dos jugadores
    Una variable `bool contraLaMaquina` decide quién mueve la paleta derecha: la máquina o las flechas. Con un
    evento de teclado (de un toque, como en R01-N02) se cambia: la tecla 1 o la 2.
    ''',
    para_que='''
    Los enemigos de casi todos los juegos funcionan así: miran algo (dónde estás vos), deciden a dónde ir y se
    acercan con una velocidad máxima. Los fantasmas del laberinto, las naves enemigas y los robots de los
    plataformas son variaciones de esta misma regla.
    ''',
    errores='''
    **Teletransportar la paleta.** `der.y = pelota.y;` hace una paleta perfecta que nunca pierde. Moverla de a
    `240 * dt` es lo que la hace humana.

    **Glitch: la paleta que tiembla.** Sin la zona muerta, cuando ya llegó se pasa un poquito para un lado y para
    el otro, cuadro a cuadro.

    **Comparar la pelota con el borde de la paleta.** `pelota.y < der.y` compara con el borde de arriba: la paleta
    termina recibiendo con la punta. Se compara con el centro: `der.y + der.h / 2`.

    **Olvidar `SDL_fabsf`.** `if (distancia < 10)` es verdadero para cualquier distancia negativa (la pelota está
    arriba): la paleta nunca sube.
    ''',
    misiones=[
        dict(titulo='La paleta que sigue',
             carta='Acercarse | distancia = objetivo - centro · si < 0, subir · si > 0, bajar (240 * dt)',
             escena='''
             —Empecemos por lo más simple —dice Kira—. La paleta rosa mira dónde está la pelota y va para ahí.
             Gheco se sienta arriba de la paleta, listo para el viaje.
             ''',
             gheco='''
             Ya está calculada la **distancia**: dónde está la pelota (el `objetivo`) menos el centro de la paleta.
             - Si la distancia es **negativa**, la pelota está más arriba: la paleta sube, `der.y -= 240 * dt;`.
             - Si es **positiva**, está más abajo: la paleta baja, `der.y += 240 * dt;`.

             ```c
             if (distancia < 0) der.y -= 240 * dt;
             if (distancia > 0) der.y += 240 * dt;
             ```
             240 píxeles por segundo es la velocidad máxima de la máquina: más lenta que la pelota rápida, para
             que se le pueda ganar.
             ''',
             desafio='Hacé que la paleta derecha se acerque sola a la pelota, a 240 píxeles por segundo.',
             pasos=['Buscá el comentario `/* acá: acercar la paleta al objetivo */`.',
                    'Debajo, escribí `if (distancia < 0) der.y -= 240 * dt;`.',
                    'En la línea siguiente, `if (distancia > 0) der.y += 240 * dt;`.',
                    'Tocá **Jugar**: ahora jugás vos solo con la W y la S contra la máquina. Después, **Comprobar**.'],
             eventos='cuadros 40', estado='buscar #ff3ca0',
             superarla='''
             La paleta rosa se mueve sola y le devuelve la pelota a Kira. Gheco, sentado encima, se agarra fuerte.
             —¡Está viva! —grita—. Bueno… está mirando.
             ''',
             imagen=['La paleta rosa moviéndose sola en la pantalla, con una flecha de movimiento hacia la pelota amarilla.',
                     'Kira juega sola, asombrada, con los dedos en la W y la S.',
                     'Gheco, diminuto, sentado sobre el borde de la máquina del lado rosa, agarrado fuerte.']),
        dict(titulo='Que no tiemble', criatura='glitch',
             carta='Zona muerta | si SDL_fabsf(distancia) < 10, distancia = 0',
             escena='''
             La paleta rosa llega a la altura de la pelota… y se pone a temblar: arriba, abajo, arriba, abajo, como
             si tuviera frío. En la pantalla, un glitch se ríe con cada temblor.
             ''',
             gheco='''
             Cuando la paleta ya está casi en el lugar, un paso de más la pasa. En el cuadro siguiente vuelve, se
             pasa para el otro lado… y así: tiembla.

             La solución es una **zona muerta**: si está a menos de 10 píxeles, la distancia se toma como 0 y la
             paleta no se mueve.
             ```c
             if (SDL_fabsf(distancia) < 10) {
                 distancia = 0;
             }
             ```
             `SDL_fabsf` da el número sin signo (el **valor absoluto**): `SDL_fabsf(-7)` es 7. Así sirve para los
             dos lados.
             ''',
             desafio='Hacé que la paleta de la máquina no se mueva cuando está a menos de 10 píxeles de su objetivo.',
             pasos=['Buscá el comentario `/* acá: si está cerca (a menos de 10 píxeles), no moverse */`.',
                    'Escribí `if (SDL_fabsf(distancia) < 10) {`, adentro `distancia = 0;` y cerrá la llave.',
                    'Tocá **Jugar** y mirá la paleta cuando llega: ya no tiembla. Después, **Comprobar**.'],
             eventos='cuadros 40', estado='buscar #ff3ca0',
             superarla='''
             La paleta llega, frena y espera, quieta y tranquila. El glitch se queda sin temblor del que reírse y
             se apaga con un chasquido.
             ''',
             imagen=['La paleta rosa quieta, alineada con la pelota amarilla, con un halo tranquilo.',
                     'Un glitch pixelado se apaga con chispas al costado de la pantalla.',
                     'Kira sonríe; Gheco aplaude sentado arriba de la máquina.']),
        dict(titulo='Volver al medio',
             carta='Jugar como alguien | si vx > 0 el objetivo es la pelota · si no, el medio (240)',
             escena='''
             La paleta rosa persigue la pelota incluso cuando se va para el otro lado, y después no llega a volver.
             —Un buen jugador no persigue: espera en el medio —dice {mentor}, que volvió con una linterna.
             ''',
             gheco='''
             La pelota **viene** hacia la paleta derecha cuando `vx > 0` (va hacia la derecha). Solo en ese caso
             vale la pena seguirla. Si se aleja, lo mejor es volver al **medio de la cancha**, que está en 240.
             ```c
             float objetivo = 240;
             if (vx > 0) {
                 objetivo = pelota.y + pelota.h / 2;
             }
             ```
             Es decir: el objetivo es el medio, salvo que la pelota venga.
             ''',
             desafio='Hacé que la máquina siga la pelota solo cuando viene hacia ella y, si no, vuelva al medio (240).',
             pasos=['Buscá el comentario `/* acá: seguir la pelota solo cuando viene; si no, volver al medio (240) */`.',
                    'Cambiá la línea de abajo por `float objetivo = 240;`.',
                    'Debajo, escribí `if (vx > 0) {`, adentro `objetivo = pelota.y + pelota.h / 2;` y cerrá la llave.',
                    'Tocá **Jugar** y mirá qué hace la paleta rosa cuando la pelota se aleja. Después, **Comprobar**.'],
             eventos='cuadros 120', estado='buscar #ff3ca0',
             superarla='''
             Ahora la paleta rosa devuelve, vuelve al medio y espera, como un jugador de verdad. {mentor} la mira con
             la linterna en la mano. —Así jugaba él —murmura—. El campeón.
             ''',
             imagen=['La paleta rosa en el medio de su lado, esperando, mientras la pelota amarilla se aleja hacia la paleta cian.',
                     'Arcadia, con una linterna en la mano, mira la pantalla muy seria.',
                     'Kira juega concentrada; Gheco mira a Arcadia con curiosidad.']),
        dict(titulo='Uno o dos jugadores',
             carta='Elegir | evento de la tecla 1: contraLaMaquina = true · tecla 2: false',
             escena='''
             —¿Y si mañana viene alguien a jugar de a dos? —pregunta Kira—. Tiene que poder elegir. {mentor} le
             señala dos botones viejos en el tablero de la máquina: uno con un muñequito y otro con dos.
             ''',
             gheco='''
             La variable `contraLaMaquina` ya decide quién mueve la paleta derecha: si es `true`, la máquina; si es
             `false`, las flechas. Abajo de la pantalla ya se ve el modo.

             Falta cambiarla con el teclado, con un **evento** (un toque, como en R01-N02), adentro del
             `while (SDL_PollEvent(&evento))`:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_1) {
                 contraLaMaquina = true;
             }
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_2) {
                 contraLaMaquina = false;
             }
             ```
             El robot va a apretar el 2 y después la flecha de arriba.
             ''',
             desafio='Hacé que con la tecla 1 se juegue contra la máquina y con la 2, de a dos (la paleta derecha con las flechas).',
             pasos=['Buscá el comentario `/* acá: con la tecla 1, contra la máquina; con la 2, de a dos */`.',
                    'Escribí el `if` de la tecla 1, con `contraLaMaquina = true;` adentro.',
                    'Escribí el `if` de la tecla 2, con `contraLaMaquina = false;` adentro.',
                    'Tocá **Jugar**, probá las dos teclas y mirá el cartelito de abajo. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla 2\napretar Arriba\ncuadros 30\nsoltar Arriba\ncuadros 2', estado='buscar #ff3ca0\ntextos',
             superarla='''
             Con el 1, la máquina juega sola; con el 2, {mentor} agarra las flechas. —Uno contra uno o contra la
             máquina —dice—. Como en los buenos tiempos. —Y mira de reojo la máquina más vieja del salón, tapada con
             una lona, en el fondo.
             ''',
             imagen=['El tablero de la máquina de la Cancha con dos botones viejos: uno con un muñequito y otro con dos.',
                     'Kira aprieta uno de los botones; Arcadia ya tiene las manos en las flechas.',
                     'Al fondo del salón, una máquina grande tapada con una lona; Gheco la mira con sospecha.']),
    ],
)
