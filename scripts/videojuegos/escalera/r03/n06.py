import motor
import n05

PLANTILLA = motor.crecer(motor.full(n05.PLANTILLA), [
    ('''
#define FILAS 5

enum Estado { JUGANDO, PERDISTE, GANASTE };''', '''
#define FILAS 5
//@ n3+
#define NIVELES 2
//@ end

//@ n3: acá: un segundo nivel, con otro dibujo
/* Cada nivel, dibujado con letras: # ladrillo · M metal (dos golpes) · . vacío */
static const char *MAPAS[NIVELES][FILAS] = {
    {
        "#.#.#.#.#.",
        ".#.#.#.#.#",
        "##########",
        "#...##...#",
        "MMMMMMMMMM",
    },
    {
        "..######..",
        ".########.",
        "##..##..##",
        "##########",
        "MM.MMMM.MM",
    },
};
static int nivel = 0;   /* el nivel que se juega: 0 es el primero */
//@ else
/* El nivel, dibujado con letras: # ladrillo · M metal (dos golpes) · . vacío */
static const char *MAPA[FILAS] = {
    "#.#.#.#.#.",
    ".#.#.#.#.#",
    "##########",
    "#...##...#",
    "MMMMMMMMMM",
};
//@ end

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

//@ n1: acá: un estado más, el primero: el menú
enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };
//@ else
enum Estado { JUGANDO, PERDISTE, GANASTE };
//@ end'''),
    ('''
/* Arma los 50 ladrillos enteros, con los de metal abajo */''', '''
/* Arma la pared del nivel */'''),
    ('''
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }''', '''
            //@ n3: acá: la letra sale del mapa del nivel que se juega
            char letra = MAPAS[nivel][f][c];
            //@ else
            char letra = MAPA[f][c];
            //@ end
            //@ n2: acá: con un punto no hay ladrillo; con una M, dos golpes
            pared[i].vivo = letra != '.';
            pared[i].golpes = (letra == 'M') ? 2 : 1;
            //@ else
            pared[i].vivo = true;
            //@ end
            pared[i].fila = f;
        }
    }
    //@ n2: acá: borrá este for: ahora los golpes salen del mapa
    //@ else
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }
    //@ end'''),
    ('''
    SDL_Init(SDL_INIT_VIDEO);''', '''
    //@ n4+
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);
    //@ else
    SDL_Init(SDL_INIT_VIDEO);
    //@ end'''),
    ('''
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);''', '''
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);
    //@ n4+

    SDL_AudioSpec formato = { SDL_AUDIO_F32, 1, 44100 };
    SDL_AudioStream *parlante = SDL_OpenAudioDeviceStream(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, &formato, NULL, NULL);
    SDL_ResumeAudioStreamDevice(parlante);
    //@ end'''),
    ('''
    enum Estado estado = JUGANDO;''', '''
    //@ n1: acá: arrancar en el menú
    enum Estado estado = MENU;
    //@ else
    enum Estado estado = JUGANDO;
    //@ end'''),
    ('''
                vx = 150;
                vy = -300;
            }
        }''', '''
                vx = 150;
                vy = -300;
            }
            //@ n1: acá: en el menú, el espacio empieza la partida
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                estado = JUGANDO;
            }
            //@ end
            //@ n3: acá: en el menú, el 1 y el 2 eligen el nivel
            if (evento.type == SDL_EVENT_KEY_DOWN && estado == MENU && (evento.key.key == SDLK_1 || evento.key.key == SDLK_2)) {
                nivel = (evento.key.key == SDLK_1) ? 0 : 1;
                armarPared(pared);
            }
            //@ end
        }'''),
    ('''
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;''', '''
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
            //@ n4: acá: el toc de la paleta
            pitido(parlante, 440, 0.05f);
            //@ end'''),
    ('''
                puntos += 10 * (FILAS - pared[i].fila);''', '''
                puntos += 10 * (FILAS - pared[i].fila);
                //@ n4: acá: el tic del ladrillo, más agudo
                pitido(parlante, 880, 0.04f);
                //@ end'''),
    ('''
            pegada = true;
            vidas--;''', '''
            pegada = true;
            vidas--;
            //@ n4: acá: el bum de la pelota que se cae
            pitido(parlante, 150, 0.3f);
            //@ end'''),
    ('''
        if (quedan == 0) {
            estado = GANASTE;
        }''', '''
        if (quedan == 0) {
            //@ n3: acá: si hay otro nivel, pasar a ese; si no, ganaste
            if (nivel + 1 < NIVELES) {
                nivel++;
                armarPared(pared);
                pegada = true;
            } else {
                estado = GANASTE;
            }
            //@ else
            estado = GANASTE;
            //@ end
        }'''),
    ('''
        if (estado != JUGANDO) {
            SDL_RenderDebugText(lapiz, 276, 320, "R: OTRA VEZ");
        }''', '''
        //@ n1: acá: la revancha solo al final (en el menú no)
        if (estado == PERDISTE || estado == GANASTE) {
        //@ else
        if (estado != JUGANDO) {
        //@ end
            SDL_RenderDebugText(lapiz, 276, 320, "R: OTRA VEZ");
        }
        //@ n1: acá: el menú: el nombre grande y cómo empezar
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 5, 5);
            SDL_RenderDebugText(lapiz, 36, 50, "EL MURO");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 264, 320, "ESPACIO: JUGAR");
        }
        //@ end
        //@ n3: acá: en el menú, qué nivel está elegido
        if (estado == MENU) {
            SDL_RenderDebugTextFormat(lapiz, 256, 345, "NIVEL %d (1 O 2)", nivel + 1);
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
    codigo='R03-N06', titulo='Menú, niveles y sonido', criatura='glitch', padre='R03-N05',
    lugar='El Muro de Ladrillos',
    usa='juegos.estados, juegos.sonido, col.matrices, prog.cadenas',
    plantilla=PLANTILLA,
    cronica='''
    En la plaza ya hay más chicos que lugar. {mentor} saca de un cajón un cuaderno viejo, con las tapas de
    cartón gastadas. Adentro, en cada hoja, hay un muro dibujado con numerales, puntitos y letras M. —Los niveles
    del Vidriero —dice—. Los dibujaba así, con letras, y la máquina los armaba. Pero la máquina arranca de golpe,
    sin menú, y muda. Un **glitch** pasa las hojas del cuaderno muy rápido, para que nadie pueda leerlas.
    ''',
    objetivos='''
    Que el juego empiece en un **menú**, que la pared salga de un **mapa dibujado con letras**, que haya **dos
    niveles** (para elegir en el menú, y al romper el primero se pasa al segundo) y que suene: el toc de la paleta,
    el tic de los ladrillos y el bum de la pelota que se cae.
    ''',
    antes='''
    R03-N05. Del Pong: el menú (R02-N05) y el sonido con `pitido` (R02-N06). Del curso de C: las cadenas como
    arreglos de `char`.
    ''',
    explicacion='''
    #### El menú
    Un estado más en el `enum`, el primero: `MENU`. El juego arranca ahí; con el espacio pasa a `JUGANDO`. Como en el
    Pong, el título va grande con la escala.

    #### Un nivel dibujado con letras
    Cada fila de la pared es una **cadena** de 10 letras:
    ```c
    "#.#.#.#.#."
    ```
    `#` es un ladrillo, `.` es un hueco y `M` es uno de metal. Cinco cadenas, una por fila, son el dibujo del nivel.
    Una cadena es un arreglo de `char`, así que la letra de la fila `f` y la columna `c` es `MAPA[f][c]`. Al armar
    la pared, cada ladrillo mira su letra: si es un punto, no está vivo; si es una M, tiene dos golpes.

    Así, para hacer un nivel nuevo no hay que tocar el código: alcanza con dibujarlo.

    #### Dos niveles
    `MAPAS[NIVELES][FILAS]` guarda varios dibujos: `MAPAS[0]` es el primero y `MAPAS[1]`, el segundo. Una variable
    `nivel` dice cuál se juega. Es **global** (está afuera de `main`, como `mudo` en el Pong) para que `armarPared`
    la pueda leer sin cambiarle los parámetros. En el menú, el 1 y el 2 lo eligen. Cuando no quedan ladrillos, si
    hay otro nivel, se pasa a ese; si no, ganaste.

    #### El sonido
    La función `pitido` del Pong (R02-N06): un sonido de una frecuencia y una duración. Una nota para cada cosa: 440
    para la paleta, 880 (más agudo) para los ladrillos y 150 (grave y largo) cuando se cae la pelota.
    ''',
    para_que='''
    Los niveles dibujados con letras son la forma más simple de hacer **muchos niveles sin escribir código**: lo
    vas a usar para el laberinto del Pac-Man y para los mapas de un juego de plataformas.
    ''',
    errores='''
    **Una fila más corta.** Si una cadena tiene 9 letras en lugar de 10, la columna 9 lee el `'\\0'` del final (o
    algo peor): cada fila tiene que tener exactamente `COLUMNAS` letras.

    **Comparar con comillas dobles.** `letra == "."` compara con una cadena, no con una letra. Una letra va entre
    comillas simples: `letra == '.'`.

    **Glitch: el espacio que hace dos cosas.** Si el `if` del menú va antes del `if` que saca la pelota, el mismo
    espacio pasa a `JUGANDO` y saca en el mismo momento. Por eso el del menú va después.

    **Pasar de nivel sin armar la pared.** Si se cambia `nivel` pero no se llama a `armarPared`, la pared sigue vacía
    y se gana enseguida.
    ''',
    misiones=[
        dict(titulo='El menú del Muro',
             carta='Menú | enum { MENU, JUGANDO, … } · arrancar en MENU · espacio en el menú: JUGANDO',
             escena='''
             Un chico se acerca y la máquina ya está jugando sola, sin esperarlo. —Las máquinas de verdad te esperan
             con un cartel —dice {mentor}—. El nombre bien grande y cómo empezar.
             ''',
             gheco='''
             Como en el Pong (R02-N05), un estado nuevo, el **primero** del `enum`: `MENU`. Cinco cositas:
             1. El `enum`: `enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };`
             2. Arrancar en el menú: `enum Estado estado = MENU;`
             3. En los eventos, **después** del `if` que saca la pelota:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == MENU) {
                 estado = JUGANDO;
             }
             ```
             Va después para que el mismo espacio no empiece y saque a la vez.
             4. El cartel de la revancha, solo al final: `if (estado == PERDISTE || estado == GANASTE)`.
             5. El menú, al final del dibujo:
             ```c
             if (estado == MENU) {
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_SetRenderScale(lapiz, 5, 5);
                 SDL_RenderDebugText(lapiz, 36, 50, "EL MURO");
                 SDL_SetRenderScale(lapiz, 1, 1);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
                 SDL_RenderDebugText(lapiz, 264, 320, "ESPACIO: JUGAR");
             }
             ```
             ''',
             desafio='Hacé que el juego empiece en un menú con el nombre grande y que el espacio arranque la partida.',
             pasos=['Buscá `/* acá: un estado más, el primero: el menú */` y cambiá el `enum` de abajo por el de la sugerencia.',
                    'Buscá `/* acá: arrancar en el menú */` y cambiá `JUGANDO` por `MENU`.',
                    'Buscá `/* acá: en el menú, el espacio empieza la partida */` y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: la revancha solo al final (en el menú no) */` y cambiá la condición del `if` de abajo.',
                    'Buscá `/* acá: el menú: el nombre grande y cómo empezar */` y escribí el `if (estado == MENU)` con los dos textos.',
                    'Tocá **Jugar**: tiene que esperar en el menú. Después, **Comprobar**.'],
             eventos='cuadros 5', estado='textos',
             superarla='''
             La pantalla se enciende con **EL MURO** en letras amarillas enormes y, abajo, **ESPACIO: JUGAR**. El chico
             aprieta el espacio, sonríe y la partida empieza recién cuando él quiere.
             ''',
             imagen=['La pantalla de la máquina con un título enorme de bloques amarillos arriba y un renglón blanco abajo (sin texto legible), con la pared de colores detrás.',
                     'Un chico del barrio con abrigo cerrado aprieta la barra espaciadora, feliz.',
                     'Kira le muestra cómo; Gheco, arriba de la máquina, levanta los brazos.'], personajes='Kira, Gheco'),
        dict(titulo='El muro dibujado con letras',
             carta='Mapa con letras | letra = MAPA[f][c] · vivo = letra != \'.\' · golpes = letra == \'M\' ? 2 : 1',
             escena='''
             {mentor} abre el cuaderno del Vidriero en la primera hoja: un muro dibujado con numerales y puntitos, como
             un tablero de damas, y una fila de letras M abajo. —Este era su primer nivel —dice—. Que la máquina lo lea.
             ''',
             gheco='''
             Arriba del programa ya está el dibujo del nivel, `MAPA`: cinco cadenas de diez letras. `#` es un ladrillo,
             `.` un hueco y `M` uno de metal. Y en `armarPared` ya está la letra de cada ladrillo:
             `char letra = MAPA[f][c];` (la fila `f`, la letra `c`).

             Falta usarla. En lugar de `pared[i].vivo = true;`:
             ```c
             pared[i].vivo = letra != '.';                 /* con un punto, no hay ladrillo */
             pared[i].golpes = (letra == 'M') ? 2 : 1;     /* con una M, dos golpes */
             ```
             - Una letra va entre comillas **simples**: `'.'`, `'M'`.
             - `letra != '.'` es `true` si la letra **no** es un punto.

             Y como los golpes ahora salen del mapa, el `for` de los golpes de la fila de abajo ya no hace falta:
             borralo.
             ''',
             desafio='Hacé que la pared se arme leyendo el dibujo del nivel: sin ladrillo en los puntos y de metal en las M.',
             pasos=['Buscá `/* acá: con un punto no hay ladrillo; con una M, dos golpes */` y cambiá la línea de abajo por las dos de la sugerencia.',
                    'Buscá `/* acá: borrá este for: ahora los golpes salen del mapa */` y borrá el `for` de abajo.',
                    'Tocá **Jugar**: la pared tiene que verse como el dibujo. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='pixel 110 70\npixel 50 70',
             superarla='''
             La pared aparece igual que la hoja del cuaderno: un tablero de damas arriba, una fila llena, dos agujeros y
             el metal abajo. {mentor} pasa el dedo por la hoja y por la pantalla, comparando. —Idéntico.
             ''',
             imagen=['La pantalla con una pared de ladrillos con forma de tablero de damas arriba y huecos, igual a un dibujo.',
                     'Arcadia sostiene un cuaderno viejo abierto con un dibujo de puntitos y cuadraditos (sin letras), al lado de la pantalla.',
                     'Kira compara el cuaderno con la pantalla; Gheco, en la palma de Kira, señala la hoja.']),
        dict(titulo='Dos niveles',
             carta='Niveles | MAPAS[nivel][f][c] · 1 o 2 en el menú · sin ladrillos: nivel++ y armarPared, o GANASTE',
             escena='''
             —¿Y la segunda hoja? —pregunta Kira, y da vuelta la página: otro muro, con forma de castillo. —Cuando
             rompías el primero, la máquina te ponía este —dice {mentor}—. Y los que ya sabían, lo elegían de entrada.
             ''',
             gheco='''
             Ahora hay **dos** dibujos: `MAPAS[NIVELES][FILAS]` (`MAPAS[0]` y `MAPAS[1]`) y una variable `nivel` que
             dice cuál se juega. Es **global** (afuera de `main`), así `armarPared` la puede leer. Cinco cosas:
             1. Cambiá el `MAPA` de arriba por `MAPAS`, con los dos niveles de la sugerencia de abajo y `nivel`.
             2. En `armarPared`, la letra del nivel que se juega: `char letra = MAPAS[nivel][f][c];`
             3. En el menú, el 1 y el 2 eligen el nivel y arman la pared otra vez:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && estado == MENU && (evento.key.key == SDLK_1 || evento.key.key == SDLK_2)) {
                 nivel = (evento.key.key == SDLK_1) ? 0 : 1;
                 armarPared(pared);
             }
             ```
             4. Cuando no quedan ladrillos, si hay otro nivel, a ese; si no, ganaste:
             ```c
             if (nivel + 1 < NIVELES) {
                 nivel++;
                 armarPared(pared);
                 pegada = true;
             } else {
                 estado = GANASTE;
             }
             ```
             5. En el menú, cuál está elegido:
             `SDL_RenderDebugTextFormat(lapiz, 256, 345, "NIVEL %d (1 O 2)", nivel + 1);` adentro de un
             `if (estado == MENU)`. Se muestra `nivel + 1` porque para las personas el primero es el 1.

             El segundo nivel:
             ```c
             "..######..",
             ".########.",
             "##..##..##",
             "##########",
             "MM.MMMM.MM",
             ```
             ''',
             desafio='Agregá un segundo nivel, que se pueda elegir en el menú y al que se pase al romper el primero.',
             pasos=['Buscá `/* acá: un segundo nivel, con otro dibujo */` y cambiá el `MAPA` de abajo por `MAPAS[NIVELES][FILAS]` con los dos dibujos, y agregá `static int nivel = 0;`.',
                    'Buscá `/* acá: la letra sale del mapa del nivel que se juega */` y cambiá `MAPA[f][c]` por `MAPAS[nivel][f][c]`.',
                    'Buscá `/* acá: en el menú, el 1 y el 2 eligen el nivel */` y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: si hay otro nivel, pasar a ese; si no, ganaste */` y cambiá la línea de abajo por el `if` de la sugerencia.',
                    'Buscá `/* acá: en el menú, qué nivel está elegido */` y escribí el texto del nivel.',
                    'Tocá **Jugar**, apretá el 2 en el menú y mirá la pared. Después, **Comprobar**.'],
             eventos='tecla 2\ncuadros 3', estado='pixel 50 70\ntextos',
             superarla='''
             Kira aprieta el 2 y la pared se transforma: ahora es un castillo, con almenas y ventanas. Los chicos de la
             fila aplauden. —Hay más hojas en el cuaderno —dice {mentor}, y lo guarda con cuidado—. Para otro día.
             ''',
             imagen=['La pantalla con una pared de ladrillos con forma de castillo, con almenas y huecos como ventanas.',
                     'Kira aprieta un botón; los chicos del barrio con abrigos cerrados aplauden detrás.',
                     'Arcadia guarda un cuaderno viejo en el bolsillo del chaleco; Gheco la mira con curiosidad.']),
        dict(titulo='El muro suena',
             carta='Sonido | paleta: pitido 440 · ladrillo: 880 · caída: 150 durante 0.3 s',
             escena='''
             La máquina funciona, pero en silencio. —El Muro sonaba como una lluvia de vidrio —recuerda {mentor}—. Toc
             en la paleta, tic en cada ladrillo, y un bum cuando se te caía la pelota.
             ''',
             gheco='''
             Ya está todo para el sonido: el parlante abierto (`parlante`) y la función `pitido` del Pong (R02-N06):
             `pitido(parlante, frecuencia, segundos)`. A más frecuencia, más agudo. Faltan tres llamadas:
             1. Cuando la paleta devuelve la pelota: `pitido(parlante, 440, 0.05f);`
             2. Cuando la pelota golpea un ladrillo, más agudo: `pitido(parlante, 880, 0.04f);`
             3. Cuando la pelota se cae, grave y más largo: `pitido(parlante, 150, 0.3f);`

             El robot va a empezar, sacar y escuchar si la máquina suena.
             ''',
             desafio='Hacé que suene la paleta, cada ladrillo y la pelota que se cae, cada uno con su nota.',
             pasos=['Buscá `/* acá: el toc de la paleta */` y escribí `pitido(parlante, 440, 0.05f);`.',
                    'Buscá `/* acá: el tic del ladrillo, más agudo */` y escribí `pitido(parlante, 880, 0.04f);`.',
                    'Buscá `/* acá: el bum de la pelota que se cae */` y escribí `pitido(parlante, 150, 0.3f);`.',
                    'Tocá **Jugar** (con el volumen prendido) y escuchá. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 2\ntecla Espacio\ncuadros 80', estado='sonido',
             superarla='''
             *Toc… tic, tic… toc.* La máquina suena como una lluvia de vidrio, y toda la plaza se da vuelta a mirar. El
             glitch que pasaba las hojas del cuaderno se tapa los oídos y se deshace en píxeles.
             ''',
             imagen=['La máquina del Muro con anillos de sonido cian saliendo de la pantalla en cada golpe.',
                     'Un glitch pixelado se tapa los oídos y se deshace en píxeles al costado de la máquina.',
                     'Kira juega sonriendo; Arcadia cierra los ojos para escuchar; Gheco mueve la cabeza al ritmo.']),
    ],
)
