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
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);

    SDL_FRect paleta = { 280, 440, 80, 12 };   /* abajo, en el medio */
    SDL_FRect pelota = { 315, 300, 10, 10 };
    float vx = 150;    /* + derecha, - izquierda */
    float vy = -300;   /* - sube, + baja */
    //@ n4+
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    //@ end
    Uint64 antes = SDL_GetTicks();

    bool jugando = true;
    while (jugando) {
        SDL_Event evento;
        while (SDL_PollEvent(&evento)) {
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            //@ n4: acá: con el espacio, la pelota sale hacia arriba
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                pegada = false;
                vx = 150;
                vy = -300;
            }
            //@ end
        }

        Uint64 ahora = SDL_GetTicks();
        float dt = (ahora - antes) / 1000.0f;
        antes = ahora;

        const bool *teclas = SDL_GetKeyboardState(NULL);
        //@ n1: acá: mover la paleta con las flechas, sin que se salga de la pantalla
        if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;
        if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;
        paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);
        //@ end

        //@ n4: acá: si está pegada, la pelota viaja arriba de la paleta; si no, se mueve sola
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;
            pelota.y = paleta.y - pelota.h;
        } else {
            pelota.x += vx * dt;
            pelota.y += vy * dt;
        }
        //@ else
        pelota.x += vx * dt;
        pelota.y += vy * dt;
        //@ end

        /* las paredes: los dos costados y el techo (abajo no hay pared) */
        //@ n2: acá: rebotar en la pared izquierda, en la derecha y en el techo
        if (pelota.x < 0) {
            pelota.x = 0;
            vx = -vx;
        }
        if (pelota.x + pelota.w > 640) {
            pelota.x = 640 - pelota.w;
            vx = -vx;
        }
        if (pelota.y < 0) {
            pelota.y = 0;
            vy = -vy;
        }
        //@ end

        //@ n3: acá: si la pelota baja y toca la paleta, vuelve a subir
        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }
        //@ end

        /* ¿se cayó por abajo? */
        if (pelota.y > 480) {
            //@ n4: acá: vuelve a quedar pegada a la paleta
            pegada = true;
            //@ else
            pelota.x = 315;
            pelota.y = 300;
            vy = -300;
            //@ end
        }

        SDL_SetRenderDrawColor(lapiz, 20, 12, 40, 255);
        SDL_RenderClear(lapiz);
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);
        SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
        SDL_RenderFillRect(lapiz, &pelota);
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
    codigo='R03-N01', titulo='La paleta y la pelota', criatura='fantasma_fotograma', padre='R02-N07',
    lugar='El Muro de Ladrillos',
    temas='juegos.fisica', usa='juegos.entrada, juegos.colisiones, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    El pedazo de mapa que dejó el Campeón Invicto lleva a una plaza que Kira nunca había visto. En el medio hay un
    paredón altísimo de ladrillos de vidrio, todos apagados, y al pie, una máquina de juegos con la pantalla negra.
    —El Muro de Ladrillos —dice {mentor}, y pasa la mano por la madera—. Acá no hay rival del otro lado: hay una
    pared. Tu paleta abajo, una pelota y todo un muro para romper. Pero primero, lo primero: que la paleta se
    mueva y la pelota rebote. Gheco se trepa a la máquina y, en la pantalla, algo se mueve a los saltos: un
    **Fantasma del Fotograma**, que va rápido o lento según el humor de la compu.
    ''',
    objetivos='''
    Armar la base del Arkanoid con lo que ya sabés del Pong: una **paleta abajo** que se mueve con las flechas
    (sin salirse de la pantalla), una **pelota** que rebota en las **dos paredes y en el techo**, la paleta que la
    **devuelve hacia arriba** y la pelota que **espera arriba de la paleta** hasta que apretás el espacio.
    ''',
    antes='''
    Toda la rama R02 (el Pong): la velocidad `vx` y `vy`, el rebote dando vuelta un signo y la función `toca`.
    De R01: el teclado (N02) y el delta time (N04).
    ''',
    explicacion='''
    #### Qué es el Arkanoid
    Una paleta abajo, una pelota y una pared de ladrillos arriba. La pelota rompe cada ladrillo que toca y rebota.
    Si se te cae por abajo, perdés una vida. Ganás cuando no queda ningún ladrillo. Es el Pong de un solo jugador:
    en vez de un rival, una pared. En este nodo armamos la paleta y la pelota; en el que sigue, los ladrillos.

    #### Lo mismo que el Pong, de costado
    En el Pong las paletas estaban a los costados y se movían para arriba y para abajo. Acá la paleta está
    **abajo** y se mueve para la **izquierda** y la **derecha**: se cambia `y` por `x`, y la W y la S por las flechas
    `SDL_SCANCODE_LEFT` y `SDL_SCANCODE_RIGHT`. Para que no se salga, `SDL_clamp` la deja entre 0 y `640 - paleta.w`.

    #### Tres paredes, no cuatro
    La pelota rebota en la pared de la **izquierda** y en la de la **derecha** (dando vuelta `vx`) y en el **techo**
    (dando vuelta `vy`). Abajo no hay pared: si la pelota pasa el borde de abajo (`pelota.y > 480`), se cayó.

    #### La paleta devuelve
    Si la pelota **viene bajando** (`vy > 0`) y toca la paleta, se la pone justo arriba de la paleta y se le da la
    vuelta a `vy`, para que suba. Preguntar `vy > 0` evita que la paleta la devuelva dos veces seguidas (lo mismo
    que con las paletas del Pong).

    #### La pelota pegada
    Al empezar (y cada vez que se cae), la pelota espera **arriba de la paleta** y viaja con ella. Una variable
    `bool pegada` dice si está esperando. Mientras está pegada, en cada cuadro se la pone en el medio de la paleta;
    cuando apretás el **espacio**, se despega y sale hacia arriba.
    ''',
    para_que='''
    La paleta que se mueve con un tope, la pelota con velocidad y los rebotes en las paredes son la base de un montón
    de juegos. Y la pelota que espera al jugador es una idea de todos los juegos: el juego no arranca solo, espera
    a que estés listo.
    ''',
    errores='''
    **Mover la paleta sin `dt`.** `paleta.x -= 5;` va más rápido en una compu rápida y más lento en una lenta: es
    el Fantasma del Fotograma. Siempre `400 * dt`.

    **Olvidar el tope.** Sin `SDL_clamp`, la paleta se va de la pantalla y no vuelve más.

    **Rebotar en el piso.** Si se pone un rebote abajo, la pelota nunca se cae y el juego no tiene gracia: abajo
    no hay pared.

    **Devolverla aunque suba.** Sin el `vy > 0`, si la pelota sigue tocando la paleta en el cuadro siguiente, se da
    vuelta otra vez y se queda temblando en la paleta.
    ''',
    misiones=[
        dict(titulo='La paleta de abajo',
             carta='Mover de costado | flechas: paleta.x ∓ 400 * dt · SDL_clamp(paleta.x, 0, 640 - paleta.w)',
             criatura='fantasma_fotograma',
             escena='''
             La máquina se enciende con un zumbido. Abajo de la pantalla aparece una rayita celeste: la paleta. Kira
             aprieta las flechas, pero la rayita no se mueve. —Está dormida —dice {mentor}—. Despertala.
             ''',
             gheco='''
             La paleta es un rectángulo, `paleta`, abajo de todo. Como en el Pong, se lee el teclado con
             `SDL_GetKeyboardState`, pero ahora la paleta se mueve **de costado** (cambia su `x`):
             ```c
             if (teclas[SDL_SCANCODE_LEFT]) paleta.x -= 400 * dt;    /* flecha izquierda */
             if (teclas[SDL_SCANCODE_RIGHT]) paleta.x += 400 * dt;   /* flecha derecha */
             paleta.x = SDL_clamp(paleta.x, 0, 640 - paleta.w);      /* que no se salga */
             ```
             - Restar a `x` la lleva a la izquierda; sumar, a la derecha.
             - `400 * dt` son 400 píxeles por segundo, en cualquier compu (el delta time).
             - `SDL_clamp(valor, mínimo, máximo)` deja el valor adentro de los límites: el borde izquierdo de la paleta
               no baja de 0 y no pasa de `640 - paleta.w`, para que no se salga por la derecha.

             El robot va a mantener apretada la flecha izquierda medio segundo.
             ''',
             desafio='Hacé que la paleta se mueva con las flechas izquierda y derecha, sin salirse de la pantalla.',
             pasos=['Buscá el comentario `/* acá: mover la paleta con las flechas, sin que se salga de la pantalla */`.',
                    'Debajo, escribí las dos líneas con `SDL_SCANCODE_LEFT` y `SDL_SCANCODE_RIGHT` de la sugerencia.',
                    'Agregá la línea con `SDL_clamp` para el tope.',
                    'Tocá **Jugar**, hacé clic en el juego y probá las flechas. Después, **Comprobar**.'],
             eventos='apretar Izquierda\ncuadros 30\nsoltar Izquierda\ncuadros 2', estado='buscar #00e5ff',
             superarla='''
             La rayita celeste se desliza de un lado al otro y se frena justo en el borde, sin caerse. El Fantasma
             del Fotograma intenta hacerla saltar, pero con el `dt` la paleta va siempre a la misma velocidad.
             ''',
             imagen=['La máquina del Muro de Ladrillos encendida, con una paleta celeste abajo de la pantalla y una flecha de movimiento.',
                     'Kira aprieta las flechas, concentrada; Arcadia mira por encima de su hombro.',
                     'Un fantasma translúcido que parpadea entre dos posiciones se desvanece al costado de la pantalla; Gheco lo señala.']),
        dict(titulo='Tres paredes',
             carta='Rebotar en tres lados | costados: vx = -vx · techo: vy = -vy · abajo no hay pared',
             escena='''
             La pelota amarilla sale disparada… y se va por arriba de la pantalla, como si no hubiera techo. Gheco
             la busca detrás de la máquina. —En esta máquina hay tres paredes —explica {mentor}—: los dos costados y
             el techo. Abajo no: abajo está tu paleta.
             ''',
             gheco='''
             La pelota ya se mueve sola con `vx` y `vy`. Falta que rebote. Igual que en el Pong, rebotar es poner la
             pelota justo en el borde y dar vuelta un signo:
             ```c
             if (pelota.x < 0) {                    /* pared izquierda */
                 pelota.x = 0;
                 vx = -vx;
             }
             if (pelota.x + pelota.w > 640) {       /* pared derecha */
                 pelota.x = 640 - pelota.w;
                 vx = -vx;
             }
             if (pelota.y < 0) {                    /* techo */
                 pelota.y = 0;
                 vy = -vy;
             }
             ```
             - En los **costados** cambia la dirección de costado: `vx`.
             - En el **techo** cambia la dirección de arriba abajo: `vy`.
             - Para la pared derecha se mira el borde derecho de la pelota, `pelota.x + pelota.w`.
             ''',
             desafio='Hacé que la pelota rebote en la pared izquierda, en la derecha y en el techo.',
             pasos=['Buscá el comentario `/* acá: rebotar en la pared izquierda, en la derecha y en el techo */`.',
                    'Debajo, escribí los tres `if` de la sugerencia.',
                    'Tocá **Jugar** y mirá cómo rebota arriba. Después, **Comprobar**.'],
             eventos='cuadros 70', estado='buscar #ffdc00',
             superarla='''
             La pelota pega en el techo con un brillo y vuelve a bajar. Gheco sale de atrás de la máquina, todavía
             buscándola. —Ahora sí tiene paredes —se ríe Kira.
             ''',
             imagen=['La pantalla de la máquina con la pelota amarilla rebotando en el techo, con una línea punteada de su recorrido.',
                     'Kira señala el rebote; Arcadia asiente con los brazos cruzados.',
                     'Gheco se asoma por detrás de la máquina, buscando la pelota.']),
        dict(titulo='La paleta devuelve',
             carta='Devolver hacia arriba | si toca(pelota, paleta) y vy > 0: arriba de la paleta y vy = -vy',
             escena='''
             La pelota rebota en el techo, baja… y atraviesa la paleta como si fuera de aire. Vuelve a aparecer en el
             medio, como si nada. —Tu paleta todavía no sabe pegarle —dice {mentor}.
             ''',
             gheco='''
             Para saber si la pelota toca la paleta está la función `toca` (la de los dos rectángulos, de R01-N05).
             Si la pelota **viene bajando** (`vy > 0`) y la toca:
             ```c
             if (toca(pelota, paleta) && vy > 0) {
                 pelota.y = paleta.y - pelota.h;   /* justo arriba de la paleta */
                 vy = -vy;                         /* y para arriba */
             }
             ```
             - Se la pone arriba de la paleta para que no quede metida adentro.
             - `vy > 0` hace que solo la devuelva cuando baja: si en el cuadro siguiente sigue tocándola, ya va
               subiendo y no se da vuelta otra vez.

             El robot va a llevar la paleta hacia la derecha, para ponerla donde cae la pelota.
             ''',
             desafio='Hacé que la paleta devuelva la pelota hacia arriba cuando la toca al bajar.',
             pasos=['Buscá el comentario `/* acá: si la pelota baja y toca la paleta, vuelve a subir */`.',
                    'Debajo, escribí el `if` con `toca(pelota, paleta) && vy > 0` de la sugerencia.',
                    'Tocá **Jugar** y poné la paleta debajo de la pelota. Después, **Comprobar**.'],
             eventos='apretar Derecha\ncuadros 40\nsoltar Derecha\ncuadros 120', estado='buscar #ffdc00',
             superarla='''
             *¡Toc!* La pelota pega en la paleta y vuelve a subir. Kira la persigue de un lado al otro. —¡La tengo!
             —grita, y {mentor} sonríe: así empieza cada partida en el Muro.
             ''',
             imagen=['La pelota amarilla rebota hacia arriba desde la paleta celeste, con una chispa.',
                     'Kira mueve la paleta con decisión; Arcadia festeja con un puño.',
                     'Gheco, sentado arriba de la máquina, sigue la pelota con la cabeza.']),
        dict(titulo='La pelota espera',
             carta='Pelota pegada | bool pegada · si pegada: arriba de la paleta · espacio: pegada = false',
             escena='''
             Cada vez que la pelota se cae, vuelve a salir sola desde el medio, y Kira no llega nunca. —En esta
             máquina la pelota te espera —dice {mentor}—. Se queda arriba de tu paleta hasta que vos digas.
             ''',
             gheco='''
             Ya está la variable `bool pegada`, que arranca en `true`. Se usa en tres lugares:
             1. **Al mover la pelota:** si está pegada, se la pone en el medio de la paleta; si no, se mueve sola:
             ```c
             if (pegada) {
                 pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;   /* el medio de la paleta */
                 pelota.y = paleta.y - pelota.h;                      /* apoyada arriba */
             } else {
                 pelota.x += vx * dt;
                 pelota.y += vy * dt;
             }
             ```
             2. **Con el espacio**, en los eventos (como en R01-N02, una sola vez por apretada):
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
                 pegada = false;
                 vx = 150;
                 vy = -300;    /* sale hacia arriba */
             }
             ```
             3. **Cuando se cae**, en lugar de volver al medio: `pegada = true;`.
             ''',
             desafio='Hacé que la pelota espere arriba de la paleta y salga recién cuando se aprieta el espacio.',
             pasos=['Buscá `/* acá: si está pegada, la pelota viaja arriba de la paleta; si no, se mueve sola */`, borrá las dos líneas de abajo y escribí el `if (pegada) { … } else { … }`.',
                    'Buscá `/* acá: con el espacio, la pelota sale hacia arriba */` (en los eventos) y escribí el `if` con `SDLK_SPACE`.',
                    'Buscá `/* acá: vuelve a quedar pegada a la paleta */`, borrá las tres líneas de abajo y escribí `pegada = true;`.',
                    'Tocá **Jugar**: la pelota espera. Apretá el espacio para sacar. Después, **Comprobar**.'],
             eventos='apretar Izquierda\ncuadros 20\nsoltar Izquierda\ncuadros 2', estado='buscar #ffdc00',
             superarla='''
             La pelota se queda quieta arriba de la paleta y la acompaña de un lado al otro. Kira elige el lugar,
             aprieta el espacio y la pelota sale disparada. En el paredón, un ladrillo de vidrio parpadea, como si
             se despertara.
             ''',
             imagen=['La pelota amarilla quieta, apoyada en el medio de la paleta celeste, con un brillo que late.',
                     'Kira, con el dedo sobre la barra espaciadora, elige el momento; Arcadia espera, divertida.',
                     'Al fondo, el paredón de ladrillos de vidrio apagados; un ladrillo se enciende. Gheco lo mira asombrado.']),
    ],
)
