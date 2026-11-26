import motor
import n06

PLANTILLA = motor.crecer(motor.full(n06.PLANTILLA), [
    ('''
    SDL_CreateWindowAndRenderer("El Muro de Ladrillos", 640, 480, 0, &ventana, &lapiz);''', '''
    SDL_CreateWindowAndRenderer("El Muro Grunon", 640, 480, 0, &ventana, &lapiz);'''),
    ('''
    enum Estado estado = MENU;''', '''
    enum Estado estado = MENU;
    //@ n1+
    float reloj = 8;          /* segundos que faltan para que el muro baje */
    //@ end
    //@ n2+
    SDL_FRect capsula = { 0, 0, 24, 10 };
    bool cayendo = false;     /* true: hay una cápsula cayendo */
    //@ end
    //@ n3+
    int record = 0;           /* el mejor puntaje desde que se prendió la máquina */
    //@ end'''),
    ('''
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                }''', '''
                if (pared[i].golpes == 0) {
                    pared[i].vivo = false;
                    //@ n2: acá: a veces, del ladrillo roto cae una cápsula
                    if (!cayendo && SDL_rand(3) == 0) {
                        cayendo = true;
                        capsula.x = pared[i].caja.x + 16;
                        capsula.y = pared[i].caja.y;
                    }
                    //@ end
                }'''),
    ('''
        int quedan = 0;''', '''
        //@ n2: acá: la cápsula cae; si la paleta la agarra, la paleta crece
        if (cayendo) {
            capsula.y += 120 * dt;
            if (toca(capsula, paleta)) {
                cayendo = false;
                paleta.w = 120;
            }
            if (capsula.y > 480) {
                cayendo = false;
            }
        }
        //@ end

        //@ n1: acá: cada 8 segundos, el muro baja un escalón; si llega a la paleta, perdiste
        if (estado == JUGANDO) {
            reloj -= dt;
            if (reloj <= 0) {
                reloj = 8;
                for (int i = 0; i < FILAS * COLUMNAS; i++) {
                    pared[i].caja.y += 12;
                    if (pared[i].vivo && pared[i].caja.y + pared[i].caja.h >= paleta.y) {
                        estado = PERDISTE;
                    }
                }
            }
        }
        //@ end

        //@ n3: acá: si hiciste más puntos que el récord, hay récord nuevo
        if (puntos > record) {
            record = puntos;
        }
        //@ end

        int quedan = 0;'''),
    ('''
        if (estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 280, 300, "PARED ROTA");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 288, 300, "PERDISTE");
        }''', '''
        //@ n3: acá: el récord, debajo de los puntos
        SDL_RenderDebugTextFormat(lapiz, 10, 24, "RECORD %d", record);
        //@ end
        //@ n4: acá: el cartel del Muro, centrado
        if (estado == PERDISTE || estado == GANASTE) {
            const char *cartel = (estado == GANASTE) ? "EL MURO SE RINDE" : "EL MURO SIGUE EN PIE";
            SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 300, cartel);
            SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        }
        //@ else
        if (estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 280, 300, "PARED ROTA");
        }
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 288, 300, "PERDISTE");
        }
        //@ end'''),
    ('''
        SDL_RenderFillRect(lapiz, &pelota);''', '''
        SDL_RenderFillRect(lapiz, &pelota);
        //@ n2: acá: dibujar la cápsula, verde
        if (cayendo) {
            SDL_SetRenderDrawColor(lapiz, 80, 255, 150, 255);
            SDL_RenderFillRect(lapiz, &capsula);
        }
        //@ end'''),
])

PERDER = 'tecla Espacio\ncuadros 2\ntecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 30'

NODO = dict(
    codigo='R03-N07', titulo='Jefe: El Muro Gruñón', tipo='jefe', criatura='atraviesaparedes', padre='R03-N06',
    lugar='El Muro de Ladrillos',
    insignia='Sello del Muro de Ladrillos',
    insignia_descripcion='Venciste al Muro Gruñón: un Arkanoid entero, con una pared de struct dibujada con letras, rebotes de costado, vidas, niveles, menú, sonido, cápsulas, récord y un muro que baja.',
    temas='juegos.guardado', usa='juegos.estados, juegos.colisiones, prog.matematica-azar, col.registros',
    plantilla=PLANTILLA,
    cronica='''
    Es de noche y la plaza está llena. Kira rompe el último ladrillo del segundo nivel y, en vez del cartel, se
    escucha un ruido como de piedras que se acomodan. El paredón de la plaza **abre dos ojos de vidrio** y frunce
    unas cejas de ladrillo. —¡Por fin alguien que juega en serio! —gruñe, con una voz de escalera vieja—. Treinta
    años esperando. Pero conmigo no alcanza con romper: yo **bajo**. Y cuando llegue a tu paleta, se terminó. Es
    **El Muro Gruñón**, el jefe del Muro de Ladrillos. {mentor} se ríe bajito: —Está contento. Se le nota.
    ''',
    objetivos='''
    Terminar el Arkanoid completo contra El Muro Gruñón: un muro que **baja** cada 8 segundos (y si llega a la
    paleta, perdiste), **cápsulas** que caen a veces de los ladrillos rotos y agrandan la paleta, un **récord** que
    se guarda entre partidas y un **cartel del Muro** centrado al terminar.
    ''',
    antes='''
    Toda la rama R03. Del Pong: la espera con un temporizador (R02-N02) y el cartel centrado (R02-N07). De R01: el azar
    con `SDL_rand` (N10).
    ''',
    explicacion='''
    #### Un temporizador
    Como la espera antes del saque en el Pong (R02-N02): una variable `reloj` con los segundos que faltan. En cada
    cuadro se le resta `dt`; cuando llega a 0, pasa algo (el muro baja) y vuelve a 8.

    #### Mover todos los ladrillos
    Para que el muro baje, un `for` le suma 12 a la `y` de la caja de cada ladrillo. En el mismo `for` se pregunta si
    algún ladrillo vivo ya llegó a la altura de la paleta: si llegó, perdiste.

    #### La cápsula
    Una sola cápsula a la vez: un rectángulo y un `bool cayendo`. Cuando se rompe un ladrillo, `SDL_rand(3)` da un
    número del 0 al 2: si sale 0 (una vez cada tres, más o menos) y no hay otra cayendo, aparece donde estaba el
    ladrillo. Cae sola a 120 píxeles por segundo; si toca la paleta, la paleta pasa a medir 120 de ancho.

    #### El récord
    Una variable que **no** se pone en 0 en la revancha: `record`. En cada cuadro, si los puntos la pasan, ese es el
    récord nuevo. Como solo vuelven a 0 los puntos, el récord queda de una partida a la otra (mientras la máquina
    esté prendida; guardarlo en un archivo es para más adelante).

    #### El cartel centrado
    Como en el Pong (R02-N07): cada letra mide 8 píxeles, así que un texto de `n` letras mide `n * 8`. Para que quede
    en el medio, empieza en `320 - n * 4`. `SDL_strlen(cartel)` cuenta las letras. El cartel cambia según cómo
    terminó la partida, con `condición ? a : b`.
    ''',
    para_que='''
    Un temporizador que hace que pasen cosas, los premios que caen y el récord están en casi todos los juegos de
    acción. Y el Arkanoid completo es tu segundo juego entero: lo vas a poder bajar y jugar en tu compu.
    ''',
    errores='''
    **El muro que baja de golpe.** Sin volver `reloj` a 8, el muro baja en todos los cuadros y llega a la paleta en un
    segundo.

    **Bajar solo los vivos.** Si se bajan solo los ladrillos vivos, cuando se rompe uno y vuelve a armarse la pared,
    quedan desparejos. Se bajan todos: los rotos no se ven igual.

    **Muchas cápsulas a la vez.** Sin el `!cayendo`, una cápsula nueva pisa a la que venía cayendo.

    **Perder el récord.** Si `record = 0;` va en la revancha, el récord se borra en cada partida.
    ''',
    misiones=[
        dict(titulo='El muro baja',
             carta='Temporizador | reloj -= dt · si reloj <= 0: reloj = 8 y todos los ladrillos y += 12 · si llega a la paleta: PERDISTE',
             personajes='Kira, Gheco, Arcadia, el Muro Gruñón',
             escena='''
             —¡Ahí voy! —gruñe El Muro, y da un paso para abajo. La pared de la pantalla, en cambio, se queda quieta. El
             Muro se ofende: —¿No me ves bajar? ¡Hacé que la máquina baje conmigo!
             ''',
             gheco='''
             Ya está la variable `float reloj = 8;`: los segundos que faltan para que el muro baje. Como la espera del
             Pong (R02-N02), en cada cuadro se le resta el tiempo que pasó:
             ```c
             if (estado == JUGANDO) {
                 reloj -= dt;
                 if (reloj <= 0) {
                     reloj = 8;                                   /* otros 8 segundos */
                     for (int i = 0; i < FILAS * COLUMNAS; i++) {
                         pared[i].caja.y += 12;                   /* un escalón más abajo */
                         if (pared[i].vivo && pared[i].caja.y + pared[i].caja.h >= paleta.y) {
                             estado = PERDISTE;                   /* llegó a la paleta */
                         }
                     }
                 }
             }
             ```
             - Solo corre mientras se juega: en el menú el muro espera.
             - `caja.y + caja.h` es el borde de abajo del ladrillo: si llega a la `y` de la paleta, te alcanzó.

             El robot va a empezar y esperar 9 segundos, sin sacar.
             ''',
             desafio='Hacé que cada 8 segundos el muro baje un escalón, y que pierdas si llega a la paleta.',
             pasos=['Buscá `/* acá: cada 8 segundos, el muro baja un escalón; si llega a la paleta, perdiste */`.',
                    'Debajo, escribí el `if (estado == JUGANDO)` de la sugerencia, con el `for` adentro.',
                    'Tocá **Jugar**, empezá y esperá: a los 8 segundos la pared tiene que bajar. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 540', estado='buscar #50dc64',
             superarla='''
             La pared de la pantalla baja un escalón justo cuando El Muro da su paso en la plaza: *¡pum!* Las dos al mismo
             tiempo. —¡Eso! —gruñe El Muro, contentísimo—. Ahora tenés que apurarte.
             ''',
             imagen=['El Muro Gruñón, un paredón vivo de ladrillos de vidrio de colores con ojos y cejas, da un paso hacia abajo en la plaza.',
                     'En la máquina, la pared de la pantalla baja un escalón con una flecha.',
                     'Kira, decidida, con las manos en los controles; Arcadia sonríe; Gheco se agarra de la máquina.']),
        dict(titulo='La cápsula',
             carta='Premio al azar | al romper: si !cayendo y SDL_rand(3) == 0, cae una cápsula · si toca la paleta: paleta.w = 120',
             personajes='Kira, Gheco, Arcadia, el Muro Gruñón',
             escena='''
             De un ladrillo roto cae una chispa verde y rueda por el piso de la plaza. Gheco la levanta: es una cápsula
             tibia. —El Vidriero escondía premios adentro del muro —dice {mentor}—. Si la agarrabas con la paleta, la
             paleta crecía.
             ''',
             gheco='''
             Ya están la `capsula` (un rectángulo de 24 × 10) y `bool cayendo`. Tres cosas:
             1. **Cuando se rompe un ladrillo** (adentro del `if (pared[i].golpes == 0)`), a veces aparece:
             ```c
             if (!cayendo && SDL_rand(3) == 0) {
                 cayendo = true;
                 capsula.x = pared[i].caja.x + 16;   /* en el medio del ladrillo */
                 capsula.y = pared[i].caja.y;
             }
             ```
             `SDL_rand(3)` da 0, 1 o 2: que salga 0 pasa una vez cada tres, más o menos.
             2. **En cada cuadro**, si está cayendo, baja; si la paleta la agarra, la paleta crece; si se va por
             abajo, se pierde:
             ```c
             if (cayendo) {
                 capsula.y += 120 * dt;
                 if (toca(capsula, paleta)) {
                     cayendo = false;
                     paleta.w = 120;
                 }
                 if (capsula.y > 480) {
                     cayendo = false;
                 }
             }
             ```
             3. **Dibujarla** en verde, después de la pelota:
             ```c
             if (cayendo) {
                 SDL_SetRenderDrawColor(lapiz, 80, 255, 150, 255);
                 SDL_RenderFillRect(lapiz, &capsula);
             }
             ```
             ''',
             desafio='Hacé que a veces caiga una cápsula de un ladrillo roto y que la paleta crezca si la agarra.',
             pasos=['Buscá `/* acá: a veces, del ladrillo roto cae una cápsula */` y escribí el primer `if` de la sugerencia.',
                    'Buscá `/* acá: la cápsula cae; si la paleta la agarra, la paleta crece */` y escribí el `if (cayendo)`.',
                    'Buscá `/* acá: dibujar la cápsula, verde */` y escribí el dibujo.',
                    'Tocá **Jugar**, rompé ladrillos y tratá de agarrar una cápsula. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 2\ntecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 100',
             estado='buscar #50ff96',
             superarla='''
             Una cápsula verde cae haciendo zigzag y Kira la atrapa con la punta de la paleta. La paleta se estira con un
             brillo. —¡Eh, eso es trampa! —gruñe El Muro, pero se le escapa una sonrisa de ladrillo.
             ''',
             imagen=['Una cápsula verde brillante cae de un ladrillo roto hacia la paleta celeste, en la pantalla de la máquina.',
                     'Gheco sostiene en la palma una cápsula verde tibia de verdad, asombrado; Arcadia se ríe.',
                     'El Muro Gruñón, el paredón vivo de ladrillos de colores, frunce las cejas de costado.']),
        dict(titulo='El récord',
             carta='Récord | int record = 0 (no vuelve a 0) · si puntos > record: record = puntos · RECORD %d',
             personajes='Kira, Gheco, Arcadia, el Muro Gruñón',
             escena='''
             Un chico pierde con 80 puntos, aprieta la R… y sus 80 puntos desaparecen. —¿Y cómo sabe el que viene cuánto
             hay que pasar? —pregunta. {mentor} asiente: —Un récord. El número que todos quieren pasar.
             ''',
             gheco='''
             Ya está la variable `int record = 0;`, afuera del bucle. La revancha pone `puntos` en 0, pero a `record`
             no lo toca: por eso queda de una partida a la otra. Dos cosas:
             1. En cada cuadro, si los puntos pasaron el récord, hay récord nuevo:
             ```c
             if (puntos > record) {
                 record = puntos;
             }
             ```
             2. Mostrarlo debajo de los puntos:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 10, 24, "RECORD %d", record);
             ```
             El robot va a perder las tres vidas y apretar la R: los puntos vuelven a 0, el récord no.
             ''',
             desafio='Guardá el mejor puntaje en un récord que no se borre en la revancha, y mostralo debajo de los puntos.',
             pasos=['Buscá `/* acá: si hiciste más puntos que el récord, hay récord nuevo */` y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: el récord, debajo de los puntos */` y escribí la línea de `RECORD`.',
                    'Tocá **Jugar**, hacé puntos, perdé y apretá la R. Después, **Comprobar**.'],
             eventos=PERDER + '\ntecla R\ncuadros 5', estado='textos',
             superarla='''
             Los puntos vuelven a 0, pero arriba queda **RECORD** con el número del chico. El que sigue en la fila lo lee
             en voz alta y se arremanga. El Muro Gruñón resopla: —Récords… En mi época éramos menos competitivos.
             ''',
             imagen=['La pantalla con dos renglones blancos arriba a la izquierda (sin texto legible) y la pared de colores.',
                     'Chicos del barrio con abrigos cerrados señalan la pantalla, entusiasmados; uno se arremanga.',
                     'Kira y Gheco sonríen; al fondo, El Muro Gruñón resopla polvo de ladrillo.']),
        dict(titulo='El cartel del Muro',
             carta='Cartel centrado | cartel = GANASTE ? "EL MURO SE RINDE" : "EL MURO SIGUE EN PIE" · x = 320 - SDL_strlen(cartel) * 4',
             personajes='Kira, Gheco, Arcadia, el Muro Gruñón',
             recompensa='xp 20, monedas 5', item='Ladrillo Arcoíris',
             escena='''
             —Cuando alguien me gane —dice El Muro—, quiero que la máquina lo diga bien claro, en el medio. Y si me ganás
             vos a mí, que se sepa que sigo en pie. —Se acomoda las cejas—. Tengo una reputación.
             ''',
             gheco='''
             En lugar de los dos carteles de antes (`PARED ROTA` y `PERDISTE`, corridos a ojo), uno solo, centrado, que
             cambia según cómo terminó:
             ```c
             if (estado == PERDISTE || estado == GANASTE) {
                 const char *cartel = (estado == GANASTE) ? "EL MURO SE RINDE" : "EL MURO SIGUE EN PIE";
                 SDL_SetRenderDrawColor(lapiz, 255, 220, 0, 255);
                 SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 300, cartel);
                 SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             }
             ```
             - `const char *cartel` guarda una cadena; con `? :` elige cuál.
             - Cada letra mide 8 píxeles: un texto de `n` letras mide `n * 8`, y para que quede en el medio empieza en
               `320 - n * 4` (como el cartel del Campeón, R02-N07).
             - Se pinta amarillo y después se vuelve al blanco, para que lo que se dibuja abajo no salga amarillo.

             El robot va a perder las tres vidas.
             ''',
             desafio='Cambiá los dos carteles del final por uno solo del Muro, centrado, que diga cómo terminó.',
             pasos=['Buscá `/* acá: el cartel del Muro, centrado */` y borrá los dos `if` de abajo (los de `PARED ROTA` y `PERDISTE`).',
                    'En su lugar, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y jugá hasta el final. Después, **Comprobar**.'],
             eventos=PERDER, estado='textos',
             superarla='''
             La última fila cae y la pantalla dice, en el medio y en amarillo, **EL MURO SE RINDE**. En la plaza, El Muro
             Gruñón se sienta en el piso con un ruido de cascotes y se ríe por primera vez en treinta años. —Bien jugado,
             Forjadora.

             Los ladrillos de vidrio del paredón se encienden todos juntos y, en la pantalla, aparece un dibujo nuevo:
             **otro pedazo del mapa del Vidriero**. Este muestra un jardín con una serpiente de luz enroscada entre las
             flores. {mentor} lo mira mucho rato. —El Jardín de la Serpiente —dice—. Ahí vamos.

             El Muro se saca de la frente un ladrillo que brilla con todos los colores y se lo da a Kira: el **Ladrillo
             Arcoíris**. —Para que te acuerdes de mí —gruñe, ya sin bronca.
             ''',
             imagen=['El Muro Gruñón, el paredón vivo de ladrillos de vidrio de colores, sentado en el piso de la plaza, riéndose, con todos sus ladrillos encendidos.',
                     'En la pantalla de la máquina, un pedazo de mapa antiguo con un jardín y una serpiente de luz enroscada entre flores.',
                     'Kira recibe un ladrillo que brilla con todos los colores; Arcadia aplaude; Gheco abraza la máquina; detrás, los chicos del barrio festejan.']),
    ],
)
