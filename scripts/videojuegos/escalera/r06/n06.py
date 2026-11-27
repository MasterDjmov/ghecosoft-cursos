import motor
import n05

PLANTILLA = motor.crecer(motor.full(n05.PLANTILLA), [
    ('''
enum Estado { MENU, JUGANDO, PERDISTE };''', '''
enum Estado { MENU, JUGANDO, PERDISTE, GANASTE };'''),
    ('''
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */''', '''
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */
    SDL_FRect nodriza = { 220, 40, 200, 60 };   /* la Nave Nodriza: un dirigible enorme */
    float nvx = 100;          /* hacia dónde va de costado */
    int nvida = 20;           /* cuántos golpes aguanta */
    bool hayNodriza = false;  /* ¿ya apareció? */
    float relojNodriza = 0;   /* cuánto falta para que aparezca */
    float relojBombas = 0;    /* cada cuánto tira */'''),
    ('''
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {''', '''
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && (estado == PERDISTE || estado == GANASTE)) {
                nodriza.x = 220;
                nvida = 20;
                hayNodriza = false;
                relojNodriza = 0;
                relojBombas = 0;'''),
    ('''
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */''', '''
        //@ n1: acá: a los 20 segundos aparece la Nodriza, y va y viene de costado
        relojNodriza += dt;
        if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
            hayNodriza = true;
        }
        if (hayNodriza) {
            nodriza.x += nvx * dt;
            if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                nvx = -nvx;
            }
        }
        //@ end
        //@ n2: acá: cada bala que la toca le saca una vida; sin vidas, ganaste
        for (int i = 0; i < BALAS; i++) {
            SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
            if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                balas[i].viva = false;
                nvida--;
                puntos += 5;
                if (nvida <= 0) {
                    hayNodriza = false;
                    estado = GANASTE;
                }
            }
        }
        //@ end
        //@ n3: acá: la Nodriza tira dos bombas de agua, una de cada lado, cada 0,8 segundos
        if (hayNodriza) {
            relojBombas += dt;
        }
        if (relojBombas >= 0.8f) {
            relojBombas -= 0.8f;
            int puestas = 0;
            for (int t = 0; t < TIROS && puestas < 2; t++) {
                if (!tiros[t].viva) {
                    tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
                    tiros[t].y = nodriza.y + nodriza.h;
                    tiros[t].viva = true;
                    puestas++;
                }
            }
        }
        //@ end
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);''', '''
        //@ n1: acá: dibujar la Nodriza, lila
        if (hayNodriza) {
            SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
            SDL_RenderFillRect(lapiz, &nodriza);
        }
        //@ end
        //@ n2: acá: su barra de vida, verde, arriba en el medio
        if (hayNodriza) {
            SDL_FRect barra = { 220, 8, nvida * 10, 8 };
            SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
            SDL_RenderFillRect(lapiz, &barra);
        }
        //@ end
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);'''),
    ('''
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }''', '''
        //@ n4: acá: el cartel del final, centrado: si ganaste, la Nodriza aterriza
        if (estado == PERDISTE || estado == GANASTE) {
            const char *cartel = (estado == GANASTE) ? "LA NODRIZA ATERRIZA" : "TE MOJARON";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ else
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ end'''),
    ('''
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }''', '''
        if (estado == PERDISTE || estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }'''),
])

NODO = dict(
    codigo='R06-N06', titulo='Jefe: La Nave Nodriza', tipo='jefe', criatura='glitch', padre='R06-N05',
    lugar='La Pista de los Biplanos',
    insignia='Sello de la Pista de los Biplanos',
    insignia_descripcion='Hiciste aterrizar a la Nave Nodriza: un juego de naves entero, con el cielo que pasa, las balas y los enemigos en piletas de structs, las oleadas, los tiros, las vidas con parpadeo, el menú, la revancha y un jefe con barra de vida.',
    temas='juegos.estados', usa='juegos.colisiones, col.registros, juegos.ia, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Después de la quinta oleada, el hangar se oscurece: algo enorme tapa el sol en la puerta. Es un dirigible de
    juguete del tamaño de una casa, hecho de retazos de tela de colores, con hélices que zumban y una canasta llena de
    globos rojos colgando abajo. Tiene dos ojos de buzo redondos en la proa y una sonrisa de lona. —¡Por fin un piloto!
    —dice, con voz de altoparlante—. Treinta años soltando globos sin que nadie me los reviente. Yo soy **la Nave
    Nodriza**, la que lleva los globos. Si querés que aterrice, vas a tener que mojarme más de lo que yo te mojo a vos.
    ''',
    objetivos='''
    Terminar el juego de naves contra la Nave Nodriza: que **aparezca** a los 20 segundos y vaya y venga, que las balas
    le saquen **vida** (con su barra), que **tire bombas de agua** de los dos costados y un **cartel final centrado** que
    diga si aterrizó o te mojó.
    ''',
    antes='''
    Toda la rama R06. De R02: el Campeón con su rapidez (N07). De R05: el cartel centrado del jefe (N06).
    ''',
    explicacion='''
    #### Un jefe es un enemigo grande
    La Nodriza es un rectángulo grande, `nodriza`, con su propia velocidad de costado, `nvx`. Cuando llega a un borde, se
    da vuelta (`nvx = -nvx`), como la pelota del Pong. No aparece desde el principio: un reloj, `relojNodriza`, espera 20
    segundos.

    #### La vida del jefe y su barra
    `nvida` empieza en 20. Cada bala viva que toca la Nodriza se apaga y le saca uno. La barra verde de arriba mide
    `nvida * 10` píxeles: empieza en 200 y se achica con cada golpe. Cuando llega a 0, la Nodriza se va y ganaste: un
    estado nuevo, `GANASTE`.

    #### Las bombas de agua
    Cada 0,8 segundos, la Nodriza suelta **dos** tiros: uno de cada costado. Se buscan dos tiros libres en la pileta con
    un contador, `puestas`: el `for` se corta cuando ya puso dos (`puestas < 2` en la condición). El primero sale del
    costado izquierdo y el segundo, del derecho.

    #### El cartel del final
    Si ganaste, «LA NODRIZA ATERRIZA»; si perdiste, «TE MOJARON». Centrado como siempre: `320 - letras * 4`.
    ''',
    para_que='''
    Un jefe con barra de vida está en casi todos los juegos de acción: es un enemigo como los demás, pero más grande, con
    más vida y con sus propios ataques. Y el juego de naves completo es tu quinto juego entero: lo vas a poder bajar y
    jugar en tu compu.
    ''',
    errores='''
    **La barra que no se achica.** Si el ancho es fijo (200), la barra no muestra nada. Tiene que salir de `nvida`.

    **Golpear a la Nodriza antes de que aparezca.** Sin el `hayNodriza` en la condición, las balas chocan contra un
    rectángulo invisible arriba de la pantalla.

    **Poner las dos bombas en el mismo tiro libre.** Sin el contador `puestas`, el `for` usa todos los tiros libres
    (o uno solo, con `break`).

    **Glitch: que la Nodriza se trabe en el borde.** Si al tocar el borde se da vuelta pero no vuelve adentro, en el
    cuadro siguiente se vuelve a dar vuelta y tiembla. Con `dt` chiquito y la vuelta inmediata, alcanza para salir.
    ''',
    misiones=[
        dict(titulo='Algo tapa el sol',
             carta='Jefe | relojNodriza += dt · a los 20 s: hayNodriza = true · si está: nodriza.x += nvx * dt · en un borde: nvx = -nvx',
             personajes='Kira, Gheco, Arcadia, la Nave Nodriza',
             escena='''
             —Cuando un piloto aguantaba veinte segundos —dice la Nave Nodriza—, yo bajaba a saludarlo. Y a mojarlo un
             poquito.
             ''',
             gheco='''
             Ya están la cajita `nodriza`, su velocidad `nvx` y `relojNodriza`. Dos cosas:
             1. **Que aparezca a los 20 segundos y vaya y venga:**
             ```c
             relojNodriza += dt;
             if (!hayNodriza && nvida > 0 && relojNodriza >= 20) {
                 hayNodriza = true;
             }
             if (hayNodriza) {
                 nodriza.x += nvx * dt;
                 if (nodriza.x < 0 || nodriza.x > 640 - nodriza.w) {
                     nvx = -nvx;          /* llegó a un borde: se da vuelta */
                 }
             }
             ```
             2. **Dibujarla**, lila, antes de los tiros:
             ```c
             if (hayNodriza) {
                 SDL_SetRenderDrawColor(lapiz, 170, 120, 220, 255);
                 SDL_RenderFillRect(lapiz, &nodriza);
             }
             ```
             El robot va a despegar, esconder el biplano en una esquina y esperar 21 segundos.
             ''',
             desafio='Hacé que a los 20 segundos aparezca la Nodriza y vaya y venga de costado.',
             pasos=['Buscá `/* acá: a los 20 segundos aparece la Nodriza, y va y viene de costado */` y escribí las líneas de la sugerencia.',
                    'Buscá `/* acá: dibujar la Nodriza, lila */` y escribí el `if` que la dibuja.',
                    'Tocá **Jugar**, despegá y aguantá 20 segundos. Después, **Comprobar**.'],
             eventos='tecla Enter\napretar Izquierda\ncuadros 70\nsoltar Izquierda\ncuadros 1200', estado='buscar #aa78dc',
             superarla='''
             A los veinte segundos, el cielo de la pantalla se oscurece y baja un dirigible lila enorme que va de un lado al
             otro, zumbando. Kira traga saliva. Gheco se esconde detrás del volante.
             ''',
             imagen=['La Nave Nodriza: un dirigible de juguete enorme hecho de retazos de tela de colores, con hélices, dos ojos de buzo redondos en la proa, una sonrisa de lona y una canasta llena de globos rojos, en la puerta del hangar.',
                     'En la pantalla de la máquina, un dirigible lila grande arriba y el biplano amarillo abajo.',
                     'Kira traga saliva, decidida; Arcadia mira la Nodriza con una sonrisa; Gheco se esconde detrás del volante de la máquina.']),
        dict(titulo='La barra de vida',
             carta='Vida del jefe | bala viva que toca la Nodriza: se apaga · nvida-- · puntos += 5 · sin vida: GANASTE · barra de nvida * 10',
             personajes='Kira, Gheco, Arcadia, la Nave Nodriza',
             escena='''
             Kira le dispara a la Nodriza: las burbujas la atraviesan como si fuera una nube. —Je —dice la Nodriza—. Yo
             aguanto veinte burbujas. Y quiero ver cuántas me quedan.
             ''',
             gheco='''
             Ya está `nvida` en 20. Dos cosas:
             1. **Cada bala que la toca le saca una vida:**
             ```c
             for (int i = 0; i < BALAS; i++) {
                 SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                 if (hayNodriza && balas[i].viva && SDL_HasRectIntersectionFloat(&bala, &nodriza)) {
                     balas[i].viva = false;
                     nvida--;
                     puntos += 5;
                     if (nvida <= 0) {
                         hayNodriza = false;     /* ¡se va! */
                         estado = GANASTE;
                     }
                 }
             }
             ```
             2. **La barra**, verde, arriba en el medio:
             ```c
             if (hayNodriza) {
                 SDL_FRect barra = { 220, 8, nvida * 10, 8 };   /* 200 píxeles con 20 vidas */
                 SDL_SetRenderDrawColor(lapiz, 120, 220, 120, 255);
                 SDL_RenderFillRect(lapiz, &barra);
             }
             ```
             El robot va a esconder el biplano en una esquina y esperar a la Nodriza: la barra tiene que aparecer con ella.
             ''',
             desafio='Hacé que cada bala que toca la Nodriza le saque una vida, con su barra verde que se achica.',
             pasos=['Buscá `/* acá: cada bala que la toca le saca una vida; sin vidas, ganaste */` y escribí el `for` de la sugerencia.',
                    'Buscá `/* acá: su barra de vida, verde, arriba en el medio */` y escribí el `if` de la barra.',
                    'Tocá **Jugar**, esperá a la Nodriza y dispárale. Después, **Comprobar**.'],
             eventos='tecla Enter\napretar Izquierda\ncuadros 70\nsoltar Izquierda\ncuadros 1200', estado='buscar #78dc78',
             superarla='''
             Cada burbuja que la toca hace *¡plop!* y la barra verde se achica un poquito. —¡Ay, ay! —se ríe la Nodriza—.
             ¡Me hacés cosquillas!
             ''',
             imagen=['La Nave Nodriza, el dirigible de retazos de tela con ojos de buzo, se ríe mojada mientras burbujas de luz le explotan en la panza.',
                     'En la pantalla de la máquina, el dirigible lila con una barra verde arriba que se achica.',
                     'Kira dispara sin parar; Arcadia aplaude; Gheco cuenta los ¡plop! con los dedos.']),
        dict(titulo='Bombas de agua',
             carta='Dos tiros | relojBombas += dt · a 0,8 s: dos tiros libres (puestas < 2): uno en nodriza.x + 20 y otro en nodriza.x + nodriza.w - 24',
             personajes='Kira, Gheco, Arcadia, la Nave Nodriza',
             escena='''
             —Ahora me toca a mí —dice la Nodriza, y de su canasta asoman dos regaderas, una de cada lado—. ¡Bombas de agua!
             ''',
             gheco='''
             Ya está `relojBombas`. Cada 0,8 segundos (mientras está la Nodriza), dos tiros: uno de cada costado. Se cuentan
             con `puestas`, y el `for` se corta cuando ya puso dos:
             ```c
             if (hayNodriza) {
                 relojBombas += dt;
             }
             if (relojBombas >= 0.8f) {
                 relojBombas -= 0.8f;
                 int puestas = 0;
                 for (int t = 0; t < TIROS && puestas < 2; t++) {
                     if (!tiros[t].viva) {
                         tiros[t].x = (puestas == 0) ? nodriza.x + 20 : nodriza.x + nodriza.w - 24;
                         tiros[t].y = nodriza.y + nodriza.h;
                         tiros[t].viva = true;
                         puestas++;
                     }
                 }
             }
             ```
             - `t < TIROS && puestas < 2`: sigue mientras haya tiros por mirar **y** falte poner alguno.
             - El primero (`puestas == 0`) sale del costado izquierdo; el segundo, del derecho.

             Los tiros ya bajan y mojan solos. El robot va a esconder el biplano en una esquina y esperar a la Nodriza.
             ''',
             desafio='Hacé que la Nodriza tire dos bombas de agua, una de cada costado, cada 0,8 segundos.',
             pasos=['Buscá `/* acá: la Nodriza tira dos bombas de agua, una de cada lado, cada 0,8 segundos */`.',
                    'Debajo, escribí los dos `if` de la sugerencia.',
                    'Tocá **Jugar**, esperá a la Nodriza y esquivá. Después, **Comprobar**.'],
             eventos='tecla Enter\napretar Izquierda\ncuadros 70\nsoltar Izquierda\ncuadros 1300', estado='buscar #ff5a28',
             superarla='''
             La Nodriza riega el cielo con dos chorros de burbujas de agua, uno de cada lado. Kira pasa por el medio,
             esquivando, y le dispara justo debajo de la panza. —¡Bien pensado! —se ríe la Nodriza.
             ''',
             imagen=['La Nave Nodriza, el dirigible de retazos de tela, riega el cielo con dos regaderas colgadas de su canasta, una de cada lado.',
                     'En la pantalla de la máquina, el dirigible lila soltando gotas anaranjadas de los dos costados y el biplano pasando por el medio.',
                     'Kira esquiva concentrada; Arcadia se cubre con la mano riéndose; Gheco abre un paraguitas.']),
        dict(titulo='La Nodriza aterriza',
             carta='Cartel centrado | al terminar: cartel = estado == GANASTE ? "LA NODRIZA ATERRIZA" : "TE MOJARON" · x = 320 - SDL_strlen(cartel) * 4',
             personajes='Kira, Gheco, Arcadia, la Nave Nodriza',
             recompensa='xp 20, monedas 5', item='Hélice de Plata',
             escena='''
             —Si me ganás —dice la Nodriza—, que la máquina lo diga en el medio, bien claro: que aterricé. Y si me ganás yo
             a vos, que diga que te mojé.
             ''',
             gheco='''
             En lugar del cartel de antes («FIN DEL VUELO», corrido a ojo), uno centrado para los dos finales:
             ```c
             if (estado == PERDISTE || estado == GANASTE) {
                 const char *cartel = (estado == GANASTE) ? "LA NODRIZA ATERRIZA" : "TE MOJARON";
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             }
             ```
             Cada letra mide 8 píxeles: un texto de `n` letras, centrado, empieza en `320 - n * 4` (como los carteles del
             Campeón, el Muro, la Serpiente y la Torre). El robot va a dejar que lo mojen hasta perder.
             ''',
             desafio='Cambiá el cartel del final por uno centrado: LA NODRIZA ATERRIZA si ganaste, TE MOJARON si perdiste.',
             pasos=['Buscá `/* acá: el cartel del final, centrado: si ganaste, la Nodriza aterriza */` y borrá el `if` de abajo.',
                    'En su lugar, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 1800', estado='textos',
             superarla='''
             La última burbuja le da justo en la panza. La barra verde se apaga y la pantalla dice, en amarillo y en el
             medio, **LA NODRIZA ATERRIZA**. Afuera del hangar, la Nave Nodriza de verdad baja despacito, apoya la canasta en
             el pasto de la pista y apaga las hélices, empapada y feliz. —Treinta años esperando un piloto así —dice.

             De su hélice más chica se desprende una pieza que brilla como una moneda: la **Hélice de Plata**. —Para que
             nunca te falte viento —dice, y se la da a Kira.

             En la pantalla aparece **otro pedazo del mapa del Vidriero**: un tren viejo que entra en un túnel oscuro, con
             ventanitas que brillan. {mentor} se ríe bajito: —El Tren Fantasma. No te asustes: los fantasmas de ahí son
             muy educados.
             ''',
             imagen=['La Nave Nodriza, el dirigible de retazos de tela con ojos de buzo, aterrizada en el pasto de la pista, empapada y sonriente, con las hélices quietas.',
                     'En la pantalla de la máquina, un pedazo de mapa antiguo con un tren viejo entrando en un túnel oscuro.',
                     'Kira sostiene una hélice chiquita que brilla como la plata; Arcadia mira el mapa, divertida; Gheco se sienta en la hélice.']),
    ],
)
