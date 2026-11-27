import motor
import n04

PLANTILLA = motor.crecer(motor.full(n04.PLANTILLA), [
    ('''
/* Una bala:''', '''
enum Estado { MENU, JUGANDO, PERDISTE };

/* Una bala:'''),
    ('''
    float relojTiro = 0;''', '''
    float relojTiro = 0;
    enum Estado estado = MENU;
    int vidas = 3;
    float invulnerable = 0;   /* cuánto le queda al biplano sin que lo mojen, después de un golpe */'''),
    ('''
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {''', '''
            //@ n1: acá: en el menú, el Enter empieza la partida
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                estado = JUGANDO;
            }
            //@ end
            //@ n4: acá: después de perder, la R deja todo como al principio
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                for (int i = 0; i < BALAS; i++) {
                    balas[i].viva = false;
                }
                for (int e = 0; e < ENEMIGOS; e++) {
                    enemigos[e].vivo = false;
                }
                for (int t = 0; t < TIROS; t++) {
                    tiros[t].viva = false;
                }
                avion.x = 300;
                avion.y = 400;
                puntos = 0;
                vidas = 3;
                oleada = 1;
                salidos = 0;
                descanso = 0;
                relojEnemigo = 0;
                relojTiro = 0;
                invulnerable = 0;
                estado = JUGANDO;
            }
            //@ end
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && estado == JUGANDO) {'''),
    ('''
        antes = ahora;
''', '''
        antes = ahora;
        //@ n1: acá: si no se está jugando, el tiempo no pasa: todo queda quieto
        if (estado != JUGANDO) {
            dt = 0;
        }
        //@ end
'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */''', '''
        bool golpe = false;   /* ¿mojaron al biplano en este cuadro? */
        //@ n2: acá: si un enemigo o un tiro toca el biplano, se apaga y es un golpe
        for (int e = 0; e < ENEMIGOS; e++) {
            SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
            if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                enemigos[e].vivo = false;
                golpe = true;
            }
        }
        for (int t = 0; t < TIROS; t++) {
            SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
            if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                tiros[t].viva = false;
                golpe = true;
            }
        }
        //@ end
        //@ n3: acá: después de un golpe, dos segundos en que nada lo moja
        invulnerable -= dt;
        if (invulnerable > 0) {
            golpe = false;
        }
        //@ end
        //@ n2: acá: un golpe es una vida menos; sin vidas, se terminó
        if (golpe) {
            vidas--;
            invulnerable = 2;
            if (vidas <= 0) {
                estado = PERDISTE;
            }
        }
        //@ end

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */'''),
    ('''
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);''', '''
        SDL_FRect cuerpo = { avion.x + 15, avion.y, 10, 40 };
        SDL_FRect ala = { avion.x, avion.y + 12, 40, 10 };
        //@ n3: acá: mientras dura, el biplano parpadea: se dibuja un décimo de segundo sí y otro no
        if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
            SDL_RenderFillRect(lapiz, &cuerpo);
            SDL_RenderFillRect(lapiz, &ala);
        }
        //@ else
        SDL_RenderFillRect(lapiz, &cuerpo);
        SDL_RenderFillRect(lapiz, &ala);
        //@ end'''),
    ('''
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);''', '''
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        //@ n2: acá: las vidas arriba a la derecha y el cartel del final
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        if (estado == PERDISTE) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ end
        //@ n4: acá: avisar que con la R se vuela otra vez
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
        }
        //@ end
        //@ n1: acá: el menú: el nombre grande y cómo se empieza
        if (estado == MENU) {
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_SetRenderScale(lapiz, 4, 4);
            SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
            SDL_SetRenderScale(lapiz, 1, 1);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
            SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
        }
        //@ end'''),
])

NODO = dict(
    codigo='R06-N05', titulo='Vidas, menú y revancha', criatura='bucle_eterno', padre='R06-N04',
    lugar='La Pista de los Biplanos',
    temas='juegos.estados', usa='juegos.colisiones, col.registros, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Las burbujitas de agua atraviesan el biplano sin mojarlo, y los globos que chocan contra el ala pasan de largo.
    Kira juega y juega, y la partida no termina nunca: ni empieza, en realidad, porque los globos ya bajan apenas se
    prende la máquina. —El **Bucle Eterno** —dice {mentor}—. Un juego tiene que saber cuándo empieza, cuándo te
    mojaron, cuándo se terminó y cómo se vuelve a empezar.
    ''',
    objetivos='''
    Ordenar el juego con **estados** (menú, jugando, perdiste) congelando el tiempo fuera de la partida, darle al biplano
    **tres vidas** que se pierden al chocar un globo o un tiro, unos segundos de **parpadeo** sin que lo mojen después de
    cada golpe, y la **revancha** con la R.
    ''',
    antes='''
    El nodo anterior. De R05: el menú con Enter y la revancha (N05). De R03: las vidas (N05).
    ''',
    explicacion='''
    #### Congelar el tiempo
    En este juego casi todo se mueve con `dt`: el biplano, las nubes, los globos, los relojes. Un truco: si no se está
    jugando, se pone `dt = 0`. Todo lo que se multiplica por `dt` se queda quieto, y todos los relojes se frenan. Con una
    sola línea, el menú y el fin congelan el juego entero.

    #### Un golpe
    Cada globo y cada tiro vivo se prueba contra la cajita del biplano. Si lo toca, se apaga y se anota que hubo un
    `golpe`. Después, **una sola vez** por cuadro: si hubo golpe, una vida menos (aunque lo hayan tocado dos cosas a la
    vez). Sin vidas, el juego termina.

    #### Unos segundos de respiro
    Después de un golpe, `invulnerable` vale 2 y va bajando con `dt`. Mientras sea mayor que 0, los golpes no cuentan (las
    cosas que lo tocan se rompen igual). Para que se note, el biplano **parpadea**: `(int)(invulnerable * 10) % 2` vale 0 y
    1 alternados cada décimo de segundo, y solo se dibuja cuando vale 0.

    #### La revancha
    Con la R se apagan las tres piletas (balas, enemigos y tiros), el biplano vuelve a su lugar, y los puntos, las vidas,
    la oleada y los relojes vuelven a empezar.
    ''',
    para_que='''
    Congelar el tiempo con `dt = 0` sirve para la pausa de cualquier juego. Y el parpadeo de invulnerabilidad está en casi
    todos los juegos de acción: es la manera de avisar «te salvaste por un ratito».
    ''',
    errores='''
    **Restar una vida por cada cosa que toca.** Si un globo y un tiro lo tocan en el mismo cuadro, se irían dos vidas
    juntas. Por eso primero se junta en `golpe` y después se resta una sola.

    **Olvidarse de `invulnerable = 2`.** Un globo grande toca el biplano varios cuadros seguidos: sin el respiro, se van
    las tres vidas en un instante.

    **La revancha que no apaga las piletas.** Los globos de la partida anterior siguen ahí y mojan al biplano apenas
    arranca.

    **Bucle Eterno: el juego que no termina.** Si al llegar a 0 vidas no se cambia el estado, las vidas siguen bajando:
    -1, -2, -3…
    ''',
    misiones=[
        dict(titulo='Antes de despegar',
             carta='Estados | si estado != JUGANDO: dt = 0 · Enter en el MENU: JUGANDO · cartel LOS BIPLANOS',
             escena='''
             La máquina se prende y los globos ya están bajando, sin aviso. —Primero el nombre bien grande —dice {mentor}—,
             y que nada se mueva hasta que el piloto diga «despego».
             ''',
             gheco='''
             Ya están el `enum` (`MENU`, `JUGANDO`, `PERDISTE`) y `estado` en `MENU`; el espacio dispara solo jugando. Tres
             cosas:
             1. **Congelar el tiempo**, justo después de calcular `dt`:
             ```c
             if (estado != JUGANDO) {
                 dt = 0;       /* todo lo que se mueve con dt se queda quieto */
             }
             ```
             2. **El Enter despega**, en los eventos:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_RETURN && estado == MENU) {
                 estado = JUGANDO;
             }
             ```
             3. **El cartel del menú**, al final del dibujo:
             ```c
             if (estado == MENU) {
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_SetRenderScale(lapiz, 4, 4);
                 SDL_RenderDebugText(lapiz, 32, 40, "LOS BIPLANOS");
                 SDL_SetRenderScale(lapiz, 1, 1);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
                 SDL_RenderDebugText(lapiz, 260, 260, "ENTER: DESPEGAR");
             }
             ```
             El robot va a esperar un segundo en el menú y después apretar el Enter: el primer globo tiene que salir recién un segundo después de despegar.
             ''',
             desafio='Hacé el menú: el juego quieto y el cartel hasta que se apriete el Enter.',
             pasos=['Buscá `/* acá: si no se está jugando, el tiempo no pasa: todo queda quieto */` y escribí el `if` del `dt = 0`.',
                    'Buscá `/* acá: en el menú, el Enter empieza la partida */` y escribí el `if` del Enter.',
                    'Buscá `/* acá: el menú: el nombre grande y cómo se empieza */` y escribí el `if (estado == MENU)` del cartel.',
                    'Tocá **Jugar**, mirá el menú y apretá el Enter. Después, **Comprobar**.'],
             eventos='cuadros 60\ntecla Enter\ncuadros 30', estado='buscar #dc3c3c',
             superarla='''
             La pantalla se prende con **LOS BIPLANOS** en letras amarillas, y todo espera, quieto, hasta las nubes. Kira
             aprieta el Enter: las nubes empiezan a pasar y el primer globo asoma arriba.
             ''',
             imagen=['La pantalla de la máquina con un cartel amarillo enorme sobre el cielo quieto (sin letras legibles).',
                     'Kira se pone unas antiparras de piloto, lista; Arcadia sonríe.',
                     'Gheco hace la cuenta regresiva con los dedos arriba de la máquina.']),
        dict(titulo='Tres vidas',
             carta='Golpe | enemigo o tiro vivo que toca el avión: se apaga, golpe = true · si golpe: vidas--, invulnerable = 2 · sin vidas: PERDISTE',
             criatura='bucle_eterno',
             escena='''
             Un globo choca contra el ala del biplano y pasa de largo, como si nada. Las burbujitas de agua lo atraviesan.
             El Bucle Eterno da vueltas alrededor de la máquina: el juego no termina nunca.
             ''',
             gheco='''
             Ya están `vidas` (3), `invulnerable` y `golpe`. Tres cosas:
             1. **¿Algo tocó el biplano?** Cada enemigo y cada tiro vivo contra la cajita del avión:
             ```c
             for (int e = 0; e < ENEMIGOS; e++) {
                 SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                 if (enemigos[e].vivo && SDL_HasRectIntersectionFloat(&enemigo, &avion)) {
                     enemigos[e].vivo = false;
                     golpe = true;
                 }
             }
             for (int t = 0; t < TIROS; t++) {
                 SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                 if (tiros[t].viva && SDL_HasRectIntersectionFloat(&tiro, &avion)) {
                     tiros[t].viva = false;
                     golpe = true;
                 }
             }
             ```
             2. **Una vida menos** (una sola, aunque lo toquen dos cosas):
             ```c
             if (golpe) {
                 vidas--;
                 invulnerable = 2;      /* lo usamos en la que viene */
                 if (vidas <= 0) {
                     estado = PERDISTE;
                 }
             }
             ```
             3. **Las vidas y el cartel**, abajo de la oleada:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
             if (estado == PERDISTE) {
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_RenderDebugText(lapiz, 268, 220, "FIN DEL VUELO");
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             }
             ```
             El robot va a despegar y poner el biplano debajo del primer globo.
             ''',
             desafio='Hacé que chocar un globo o un tiro cueste una vida, y que sin vidas se termine el vuelo.',
             pasos=['Buscá `/* acá: si un enemigo o un tiro toca el biplano, se apaga y es un golpe */` y escribí los dos `for`.',
                    'Buscá `/* acá: un golpe es una vida menos; sin vidas, se terminó */` y escribí el `if (golpe)`.',
                    'Buscá `/* acá: las vidas arriba a la derecha y el cartel del final */` y escribí el texto y el cartel.',
                    'Tocá **Jugar** y dejate mojar. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 300', estado='textos',
             superarla='''
             Un globo choca contra el ala: *¡plaf!*, revienta y arriba a la derecha queda **VIDAS 2**. Kira se seca la cara
             como si la hubieran mojado de verdad. El Bucle Eterno se frena, mareado, y se va.
             ''',
             imagen=['La pantalla de la máquina con un globo rojo reventando contra el ala del biplano amarillo, en una salpicadura de agua.',
                     'Una criatura que es un aro de luz girando se frena, mareada, y se va caminando en zigzag.',
                     'Kira se seca la cara riéndose; Arcadia le alcanza un pañuelo; Gheco, empapado, se sacude como un perrito.']),
        dict(titulo='Un ratito a salvo',
             carta='Invulnerable | invulnerable -= dt · si invulnerable > 0: golpe = false · dibujar solo si invulnerable <= 0 o (int)(invulnerable * 10) % 2 == 0',
             escena='''
             Un globo grande toca el ala… y se van las tres vidas de golpe, una por cuadro. —Después de un golpe, el piloto
             tiene un ratito a salvo —dice {mentor}—. Y el avión parpadea, para que se sepa.
             ''',
             gheco='''
             Dos cosas:
             1. **El ratito a salvo**, entre los choques y la resta de la vida:
             ```c
             invulnerable -= dt;
             if (invulnerable > 0) {
                 golpe = false;      /* este golpe no cuenta */
             }
             ```
             2. **El parpadeo**, en lugar de dibujar el cuerpo y el ala siempre:
             ```c
             if (invulnerable <= 0 || (int)(invulnerable * 10) % 2 == 0) {
                 SDL_RenderFillRect(lapiz, &cuerpo);
                 SDL_RenderFillRect(lapiz, &ala);
             }
             ```
             `invulnerable * 10` cuenta décimos de segundo; `% 2` da 0 y 1 alternados: un décimo se ve y otro no. El robot va
             a dejar el biplano quieto debajo de los globos un buen rato.
             ''',
             desafio='Hacé que después de un golpe el biplano tenga dos segundos sin que lo mojen, y que parpadee mientras tanto.',
             pasos=['Buscá `/* acá: después de un golpe, dos segundos en que nada lo moja */` y escribí las líneas de la sugerencia.',
                    'Buscá `/* acá: mientras dura, el biplano parpadea: se dibuja un décimo de segundo sí y otro no */` y borrá las dos líneas de abajo.',
                    'En su lugar, escribí el `if` del parpadeo.',
                    'Tocá **Jugar** y dejate mojar. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 600', estado='textos',
             superarla='''
             El globo toca el ala, el biplano parpadea y, por dos segundos, las burbujitas lo atraviesan sin mojarlo. Kira
             aprovecha para escaparse. —Como un escudo de luz —dice, y mira su brazal.
             ''',
             imagen=['La pantalla de la máquina con el biplano amarillo parpadeando, semitransparente, entre gotitas que lo atraviesan.',
                     'Kira mira su brazal de control, pensativa; Arcadia asiente.',
                     'Gheco se tapa y destapa los ojos al ritmo del parpadeo, arriba de la máquina.']),
        dict(titulo='Otra vez al aire',
             carta='Revancha | R en PERDISTE: apagar balas, enemigos y tiros · avión a (300, 400) · puntos, vidas, oleada y relojes como al principio · JUGANDO',
             escena='''
             Se terminó el vuelo y ahí se quedó. Kira aprieta todas las teclas: nada. —Otra vez —pide—. —Todo como al
             principio —dice {mentor}—: el cielo vacío, el avión en la pista y tres vidas.
             ''',
             gheco='''
             Con la R, después de perder, se apagan las tres piletas y todo vuelve a empezar:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado == PERDISTE) {
                 for (int i = 0; i < BALAS; i++) {
                     balas[i].viva = false;
                 }
                 for (int e = 0; e < ENEMIGOS; e++) {
                     enemigos[e].vivo = false;
                 }
                 for (int t = 0; t < TIROS; t++) {
                     tiros[t].viva = false;
                 }
                 avion.x = 300;
                 avion.y = 400;
                 puntos = 0;
                 vidas = 3;
                 oleada = 1;
                 salidos = 0;
                 descanso = 0;
                 relojEnemigo = 0;
                 relojTiro = 0;
                 invulnerable = 0;
                 estado = JUGANDO;
             }
             ```
             Y avisarlo, abajo del cartel:
             ```c
             if (estado == PERDISTE) {
                 SDL_RenderDebugText(lapiz, 276, 244, "R: OTRA VEZ");
             }
             ```
             ''',
             desafio='Hacé que con la R, después de perder, todo vuelva a empezar.',
             pasos=['Buscá `/* acá: después de perder, la R deja todo como al principio */` y escribí el `if` de la R.',
                    'Buscá `/* acá: avisar que con la R se vuela otra vez */` y escribí el `if` del aviso.',
                    'Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.'],
             eventos='tecla Enter\ncuadros 1800\ntecla R\ncuadros 3', estado='textos',
             superarla='''
             Kira aprieta la R: el cielo se vacía, el biplano vuelve a la pista y arriba dice **VIDAS 3**. —Ahora sí —dice, y
             despega de nuevo.
             ''',
             imagen=['La pantalla de la máquina con el cielo vacío, el biplano amarillo abajo en su lugar y nubes pasando.',
                     'Kira, decidida, se acomoda el brazal; Arcadia le guiña un ojo.',
                     'Gheco hace la señal de despegue con dos banderitas arriba de la máquina.']),
    ],
)
