import motor
import n03

MORDER = 'tecla Arriba\ncuadros 10\ntecla Izquierda\ncuadros 10\ntecla Abajo\ncuadros 30'

PLANTILLA = motor.crecer(motor.full(n03.PLANTILLA), [
    ('''
int main(void)
{
    SDL_Init(SDL_INIT_VIDEO);''', '''
//@ n4+
/* Un pitido de «frecuencia» vueltas por segundo durante «segundos» (el de R01-N09) */
static void pitido(SDL_AudioStream *parlante, float frecuencia, float segundos)
{
    int muestras = (int)(44100 * segundos);
    float *onda = SDL_malloc(muestras * sizeof(float));
    for (int i = 0; i < muestras; i++) {
        onda[i] = 0.2f * SDL_sinf(2 * SDL_PI_F * frecuencia * i / 44100);
    }
    SDL_PutAudioStreamData(parlante, onda, muestras * sizeof(float));
    SDL_free(onda);
}

//@ end
//@ n2: acá: un estado más, el primero: el menú
enum Estado { MENU, JUGANDO, PERDISTE };
//@ else
enum Estado { JUGANDO, PERDISTE };
//@ end

int main(void)
{
    //@ n4+
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);
    //@ else
    SDL_Init(SDL_INIT_VIDEO);
    //@ end'''),
    ('''
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);''', '''
    SDL_CreateWindowAndRenderer("El Jardin de la Serpiente", 640, 480, 0, &ventana, &lapiz);
    //@ n4+

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);
    //@ end'''),
    ('''
    int puntos = 0;''', '''
    int puntos = 0;
    //@ n2: acá: arrancar en el menú
    enum Estado estado = MENU;
    //@ else
    enum Estado estado = JUGANDO;
    //@ end'''),
    ('''
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP''', '''
            //@ n4: acá: un tin al empezar (el espacio en el menú)
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                pitido(parlante, 440, 0.08f);
            }
            //@ end
            //@ n2: acá: en el menú, el espacio empieza la partida
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            //@ end
            //@ n3: acá: con la R, todo como al principio
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                largo = 5;
                for (int i = 0; i < largo; i++) {
                    cx[i] = 5 - i;
                    cy[i] = 12;
                }
                dx = 1;
                dy = 0;
                puntos = 0;
                paso = 0.15f;
                fx = 20;
                fy = 12;
                estado = JUGANDO;
            }
            //@ end
            if (evento.type == SDL_EVENT_KEY_DOWN) {
                if (evento.key.key == SDLK_UP'''),
    ('''
        reloj += dt;''', '''
        //@ n1: acá: el reloj solo corre mientras se juega
        if (estado == JUGANDO) {
            reloj += dt;
        }
        //@ else
        reloj += dt;
        //@ end'''),
    ('''
        /* ¿la cabeza llegó a la fruta? */''', '''
        //@ n1: acá: si la cabeza pisa una parte de su cuerpo, perdiste
        for (int i = 1; i < largo; i++) {
            if (cx[i] == cx[0] && cy[i] == cy[0]) {
                estado = PERDISTE;
            }
        }
        //@ end

        /* ¿la cabeza llegó a la fruta? */'''),
    ('''
            paso = SDL_max(0.06f, paso * 0.9f);''', '''
            paso = SDL_max(0.06f, paso * 0.9f);
            //@ n4: acá: el ñam de la fruta
            pitido(parlante, 660, 0.06f);
            //@ end'''),
    ('''
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);''', '''
        SDL_RenderDebugTextFormat(lapiz, 8, 6, "PUNTOS %d", puntos);
        //@ n1: acá: el cartel si te mordiste
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 220, "TE MORDISTE");
        }
        //@ end
        //@ n3: acá: cómo volver a jugar
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        //@ end
        //@ n2: acá: el menú: el nombre grande y cómo empezar
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
        }
        //@ end'''),
    ('''
    SDL_DestroyRenderer(lapiz);''', '''
    //@ n4+
    SDL_DestroyAudioStream(parlante);
    //@ end
    SDL_DestroyRenderer(lapiz);'''),
])

NODO = dict(
    codigo='R04-N04', titulo='Morderse, menú y revancha', criatura='bucle_eterno', padre='R04-N03',
    lugar='El Jardín de la Serpiente',
    temas='juegos.estados', usa='juegos.sonido, col.arrays',
    plantilla=PLANTILLA,
    cronica='''
    La serpiente ya es larguísima y Kira la enrosca por todo el jardín. En una curva cerrada, la cabeza pasa por
    encima de su propia cola… y no pasa nada: sigue como si fuera un fantasma. Debajo de la máquina, una serpiente de
    luz violeta se muerde la cola y da vueltas sin parar: el **Bucle Eterno**. —Así no se pierde nunca —dice
    {mentor}—. Y un juego en el que no se puede perder se termina aburriendo.
    ''',
    objetivos='''
    Que la serpiente **pierda si se muerde** (y se quede quieta con un cartel), que el juego arranque en un **menú**,
    que se pueda **volver a jugar** con la R dejando todo como al principio y que **suene** al empezar y al comer.
    ''',
    antes='''
    R04-N03. De R03: los estados con `enum` y la revancha (N05) y el sonido con `pitido` (N06).
    ''',
    explicacion='''
    #### Morderse
    La serpiente se muerde cuando la cabeza está en la misma celda que **alguna otra parte** de su cuerpo. Un `for`
    recorre las partes de la 1 en adelante (la 0 es la propia cabeza) y compara: si alguna coincide, perdiste.

    #### Estados
    Como en el Arkanoid: un `enum` con `MENU`, `JUGANDO` y `PERDISTE`. El reloj solo junta tiempo mientras se juega:
    en el menú y después de perder, la serpiente se queda quieta.

    #### La revancha
    Con la R, si perdiste, todo vuelve a como empezó: cinco partes en fila, para la derecha, 0 puntos, la velocidad
    del principio y la fruta en su lugar. Es el mismo código del comienzo, copiado en el `if` de la R.

    #### El sonido
    La función `pitido` de siempre: un *tin* al empezar la partida y un *ñam* agudo cada vez que come.
    ''',
    para_que='''
    Detectar que algo choca contra sí mismo (una cola, un rastro, una fila) aparece en muchos juegos: el Tron, los
    trenes, las carreras de motos de luz. Y el menú, el fin y la revancha ya son el esqueleto de todos tus juegos.
    ''',
    errores='''
    **Compararse con la cabeza.** Si el `for` empieza en 0, la cabeza siempre «coincide» consigo misma y se pierde
    al instante.

    **Bucle Eterno: no poder perder.** Sin el chequeo, la serpiente pasa por encima de sí misma para siempre.

    **Seguir moviéndose después de perder.** Si el reloj no mira el estado, la serpiente sigue avanzando con el
    cartel puesto.

    **Revancha a medias.** Si la R no devuelve la velocidad, la partida nueva arranca rapidísima.
    ''',
    misiones=[
        dict(titulo='Te mordiste',
             carta='Morderse | for i desde 1: si cx[i] == cx[0] y cy[i] == cy[0]: PERDISTE · el reloj solo corre si JUGANDO',
             criatura='bucle_eterno',
             escena='''
             La cabeza pasa por encima de la cola como si nada. El Bucle Eterno se ríe, enroscado debajo de la máquina.
             —Una serpiente que se muerde, se enreda —dice {mentor}—. Y ahí termina la partida.
             ''',
             gheco='''
             Ya están el `enum Estado { JUGANDO, PERDISTE };` y la variable `estado`. Tres cosas:
             1. **Morderse:** después de mover, un `for` compara la cabeza con cada parte del cuerpo:
             ```c
             for (int i = 1; i < largo; i++) {          /* desde la 1: la 0 es la cabeza */
                 if (cx[i] == cx[0] && cy[i] == cy[0]) {
                     estado = PERDISTE;
                 }
             }
             ```
             2. **Quedarse quieta:** el reloj solo junta tiempo si se está jugando:
             ```c
             if (estado == JUGANDO) {
                 reloj += dt;
             }
             ```
             3. **El cartel:** `if (estado == PERDISTE)`, el texto `TE MORDISTE` en `(276, 220)`.

             El robot va a doblar arriba, izquierda y abajo, bien cerrado, para que se muerda.
             ''',
             desafio='Hacé que la serpiente pierda si la cabeza pisa su cuerpo, que se quede quieta y que aparezca el cartel.',
             pasos=['Buscá `/* acá: si la cabeza pisa una parte de su cuerpo, perdiste */` y escribí el `for` de la sugerencia.',
                    'Buscá `/* acá: el reloj solo corre mientras se juega */` y envolvé `reloj += dt;` con el `if (estado == JUGANDO)`.',
                    'Buscá `/* acá: el cartel si te mordiste */` y escribí el `if` con `TE MORDISTE`.',
                    'Tocá **Jugar** y hacé una vuelta bien cerrada. Después, **Comprobar**.'],
             eventos=MORDER, estado='textos',
             superarla='''
             La cabeza se choca con la cola, la serpiente se queda quieta y aparece **TE MORDISTE**. El Bucle Eterno suelta
             su propia cola, mareado, y se escurre entre las flores.
             ''',
             imagen=['La pantalla con la serpiente verde enroscada, la cabeza tocando su propio cuerpo, quieta, con un cartel blanco en el medio (sin texto legible).',
                     'Una serpiente de luz violeta suelta su propia cola, mareada, debajo de la máquina.',
                     'Kira se tapa la cara riéndose; Gheco, sobre la máquina, se enreda la cola a propósito.']),
        dict(titulo='El menú del jardín',
             carta='Menú | enum { MENU, JUGANDO, PERDISTE } · arrancar en MENU · espacio en el menú: JUGANDO',
             personajes='Kira, Gheco',
             escena='''
             La serpiente arranca apenas se prende la máquina, antes de que nadie agarre el teclado. Un chico del barrio
             llega corriendo y ya perdió. —Que espere —dice Kira—. Con un cartel, como el Muro.
             ''',
             gheco='''
             Como en el Arkanoid: un estado nuevo, el **primero** del `enum`. Cuatro cosas:
             1. El `enum`: `enum Estado { MENU, JUGANDO, PERDISTE };`
             2. Arrancar en el menú: `enum Estado estado = MENU;`
             3. En los eventos, el espacio empieza:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                 estado = JUGANDO;
             }
             ```
             4. El menú, al final del dibujo:
             ```c
             if (estado == MENU) {
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_SetRenderScale(lapiz, 5, 5);
                 SDL_RenderDebugText(lapiz, 28, 30, "EL JARDIN");
                 SDL_SetRenderScale(lapiz, 1, 1);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
                 SDL_RenderDebugText(lapiz, 264, 300, "ESPACIO: JUGAR");
             }
             ```
             Como el reloj solo corre jugando, en el menú la serpiente espera sola.
             ''',
             desafio='Hacé que el juego empiece en un menú y que el espacio arranque la partida.',
             pasos=['Buscá `/* acá: un estado más, el primero: el menú */` y cambiá el `enum` de abajo.',
                    'Buscá `/* acá: arrancar en el menú */` y cambiá `JUGANDO` por `MENU`.',
                    'Buscá `/* acá: en el menú, el espacio empieza la partida */` y escribí el `if` del espacio.',
                    'Buscá `/* acá: el menú: el nombre grande y cómo empezar */` y escribí el `if (estado == MENU)`.',
                    'Tocá **Jugar**: tiene que esperar en el menú. Después, **Comprobar**.'],
             eventos='cuadros 5', estado='textos',
             superarla='''
             La pantalla se enciende con **EL JARDIN** en letras amarillas y la serpiente quieta abajo, esperando. El chico
             aprieta el espacio cuando está listo y sonríe.
             ''',
             imagen=['La pantalla de la máquina del jardín con un título enorme de bloques amarillos (sin texto legible) y la serpiente quieta abajo.',
                     'Un chico del barrio con abrigo cerrado, listo, con el dedo sobre la barra espaciadora.',
                     'Kira le muestra cómo; Gheco, arriba de la máquina, levanta los brazos.']),
        dict(titulo='Otra vuelta',
             carta='Revancha | R si PERDISTE: largo = 5 y en fila · dx = 1, dy = 0 · puntos = 0 · paso = 0.15f · fruta en (20, 12) · JUGANDO',
             escena='''
             El chico se muerde y se queda mirando el cartel. —¿Y ahora? —pregunta. Hay que apagar la máquina para volver
             a jugar. —Una vuelta más —dice {mentor}—. Con la R, como en el Muro.
             ''',
             gheco='''
             Con la R, si perdiste, todo vuelve a como empezó. Es el mismo código del principio, en un `if`:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                 largo = 5;
                 for (int i = 0; i < largo; i++) {   /* otra vez en fila */
                     cx[i] = 5 - i;
                     cy[i] = 12;
                 }
                 dx = 1;          /* para la derecha */
                 dy = 0;
                 puntos = 0;
                 paso = 0.15f;    /* la velocidad del principio */
                 fx = 20;         /* la fruta en su lugar */
                 fy = 12;
                 estado = JUGANDO;
             }
             ```
             Y un cartelito que avise, `R: OTRA VEZ` en `(276, 244)`, cuando `estado == PERDISTE`.
             ''',
             desafio='Hacé que con la R se vuelva a jugar con todo como al principio.',
             pasos=['Buscá `/* acá: con la R, todo como al principio */` (en los eventos) y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: cómo volver a jugar */` y escribí el cartel `R: OTRA VEZ`.',
                    'Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.'],
             eventos='tecla Espacio\n' + MORDER + '\ntecla R\ncuadros 5', estado='textos',
             superarla='''
             El chico aprieta la R y la serpiente vuelve a aparecer cortita, en fila, lista. Juega otra vez, y otra, y
             otra. Detrás de él ya se armó una fila.
             ''',
             imagen=['La máquina del jardín con la serpiente cortita otra vez en fila en la pantalla.',
                     'Un chico del barrio con abrigo cerrado aprieta una tecla, feliz; detrás, una fila de chicos espera.',
                     'Kira y Arcadia chocan los cinco; Gheco, arriba de la máquina, saluda a los chicos.']),
        dict(titulo='Ñam',
             carta='Sonido | al empezar: pitido 440 · al comer: pitido 660',
             escena='''
             La máquina funciona, pero en silencio. —En el jardín se escuchaba un *ñam* cada vez que la serpiente comía
             —recuerda {mentor}—. Los chicos lo imitaban.
             ''',
             gheco='''
             Ya está todo para el sonido: el parlante abierto y la función `pitido` de siempre. Faltan dos llamadas:
             1. Al empezar la partida: un `if` igual al del menú, que va **antes** que él (después ya no está en el
                menú):
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                 pitido(parlante, 440, 0.08f);
             }
             ```
             2. Al comer, adentro del `if` de la fruta: `pitido(parlante, 660, 0.06f);` (más agudo).

             El robot va a apretar el espacio y escuchar.
             ''',
             desafio='Hacé que suene un tin al empezar y un ñam agudo cada vez que la serpiente come.',
             pasos=['Buscá `/* acá: un tin al empezar (el espacio en el menú) */` y escribí el `if` con el `pitido` de la sugerencia.',
                    'Buscá `/* acá: el ñam de la fruta */` y escribí `pitido(parlante, 660, 0.06f);`.',
                    'Tocá **Jugar** (con el volumen prendido) y escuchá. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 5', estado='sonido',
             superarla='''
             *Tin*… y después *ñam, ñam, ñam*. Los chicos de la fila hacen *ñam* cada vez que la serpiente come, y se
             ríen. Hasta Arcadia lo hace.
             ''',
             imagen=['La máquina del jardín con anillos de sonido saliendo de la pantalla mientras la serpiente se come una fruta.',
                     'Chicos del barrio con abrigos cerrados hacen como que mastican, riéndose.',
                     'Kira juega; Arcadia se ríe; Gheco, sobre la máquina, abre grande la boca.']),
    ],
)
