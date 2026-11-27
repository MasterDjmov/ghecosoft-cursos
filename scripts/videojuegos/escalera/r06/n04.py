import motor
import n03

PLANTILLA = motor.crecer(motor.full(n03.PLANTILLA), [
    ('''
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
''', '''
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
#define POR_OLEADA 5   /* cuántos enemigos trae cada oleada */
#define TIROS 6        /* cuántos tiros de los enemigos puede haber a la vez */
'''),
    ('''
    int puntos = 0;''', '''
    int puntos = 0;
    int oleada = 1;           /* qué oleada viene */
    int salidos = 0;          /* cuántos enemigos de esta oleada ya salieron */
    float descanso = 0;       /* el respiro entre oleadas */
    //@ n4+
    struct Bala tiros[TIROS] = { 0 };   /* los tiros de los enemigos: también son balas */
    float relojTiro = 0;
    //@ end'''),
    ('''
        relojEnemigo += dt;
        if (relojEnemigo >= 1) {''', '''
        //@ n2: acá: mientras falten enemigos de esta oleada, corre el reloj; si no, un respiro de 3 segundos y la oleada siguiente
        if (salidos < POR_OLEADA) {
            relojEnemigo += dt;
        } else {
            descanso += dt;
            if (descanso >= 3) {
                descanso = 0;
                salidos = 0;
                oleada++;
            }
        }
        //@ else
        relojEnemigo += dt;
        //@ end
        if (relojEnemigo >= 1) {'''),
    ('''
                    enemigos[e].vivo = true;
                    break;''', '''
                    enemigos[e].vivo = true;
                    //@ n2: acá: contar el que salió
                    salidos++;
                    //@ end
                    break;'''),
    ('''
                enemigos[e].y += 120 * dt;''', '''
                //@ n3: acá: cada oleada baja más rápido
                enemigos[e].y += (100 + 40 * oleada) * dt;
                //@ else
                enemigos[e].y += 120 * dt;
                //@ end
                //@ n1: acá: y se mueve de costado, de un lado a otro, como un zigzag
                enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
                //@ end'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */''', '''
        //@ n4: acá: cada segundo y medio, el primer enemigo vivo tira; los tiros bajan y se apagan al salir
        relojTiro += dt;
        if (relojTiro >= 1.5f) {
            relojTiro -= 1.5f;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (enemigos[e].vivo) {
                    for (int t = 0; t < TIROS; t++) {
                        if (!tiros[t].viva) {
                            tiros[t].x = enemigos[e].x + 18;
                            tiros[t].y = enemigos[e].y + 30;
                            tiros[t].viva = true;
                            break;
                        }
                    }
                    break;
                }
            }
        }
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                tiros[t].y += 250 * dt;
                if (tiros[t].y > 480) {
                    tiros[t].viva = false;
                }
            }
        }
        //@ end

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */''', '''
        //@ n4: acá: dibujar los tiros de los enemigos, rojo anaranjado
        SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
        for (int t = 0; t < TIROS; t++) {
            if (tiros[t].viva) {
                SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &tiro);
            }
        }
        //@ end
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */'''),
    ('''
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);''', '''
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        //@ n2: acá: mostrar la oleada abajo de los puntos
        SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
        //@ end'''),
])

NODO = dict(
    codigo='R06-N04', titulo='Oleadas', criatura='glitch', padre='R06-N03',
    lugar='La Pista de los Biplanos',
    temas='juegos.ia', usa='col.registros, prog.matematica-azar, juegos.bucle',
    plantilla=PLANTILLA,
    cronica='''
    Kira revienta globos sin parar, y se aburre: todos bajan derecho, de a uno, siempre igual. —En la máquina venían
    en **oleadas** —dice {mentor}—: cinco, un respiro, cinco más rápidos. Y bailaban de costado. Y los más pícaros
    tiraban burbujitas de agua. En la pantalla, un globo parpadea y aparece corrido, medio adentro de otro: un gatito
    pixelado se ríe en un rincón. Es el **Glitch**.
    ''',
    objetivos='''
    Hacer que los enemigos se muevan en **zigzag** con el seno, que vengan en **oleadas** de cinco con un respiro entre
    una y otra, que cada oleada sea **más rápida** y que los enemigos **tiren** (otra pileta de balas, que bajan).
    ''',
    antes='''
    El nodo anterior. De R01: el pitido con el seno (N09). De R02: la pelota que acelera (N03).
    ''',
    explicacion='''
    #### El zigzag: el seno
    `SDL_sinf(número)` da un valor entre -1 y 1 que sube y baja, una y otra vez, a medida que el número crece: es una ola.
    Si a la `x` del enemigo se le suma `SDL_sinf(y / 40) * 120 * dt`, mientras baja va de un lado al otro, suave. El `40`
    dice qué tan largas son las curvas, y el `120`, qué tan anchas.

    #### Oleadas
    `salidos` cuenta cuántos enemigos de la oleada ya salieron. Mientras sean menos de cinco, corre el reloj de los
    enemigos; cuando salieron los cinco, corre el `descanso`. A los tres segundos de respiro, `salidos` vuelve a 0 y
    `oleada` sube: empieza la siguiente.

    #### Cada vez más rápido
    La velocidad depende de la oleada: `100 + 40 * oleada`. En la primera son 140 píxeles por segundo; en la segunda,
    180; en la tercera, 220.

    #### Los enemigos tiran
    Los tiros son **balas**: el mismo `struct Bala`, en otra pileta, `tiros`. Cada segundo y medio, el primer enemigo vivo
    suelta un tiro desde abajo suyo. Los tiros bajan y se apagan al salir. (Que le peguen al biplano es el nodo que
    viene.)
    ''',
    para_que='''
    Las oleadas (con su respiro y su dificultad que sube) son la forma de armar el ritmo de casi todos los juegos de
    acción. Y el seno sirve para todo lo que va y viene: enemigos que flotan, plataformas que suben y bajan, una moneda
    que brilla.
    ''',
    errores='''
    **El seno en grados.** `SDL_sinf` usa radianes: con `SDL_sinf(y)` sola, el enemigo tiembla rapidísimo. Dividiendo por
    40, la curva se estira.

    **Olvidarse de contar.** Sin `salidos++`, la oleada nunca termina.

    **Volver `descanso` a 0 al empezar.** Si no, la segunda oleada termina el respiro en un instante.

    **Glitch: dos `break` confundidos.** El de adentro corta la búsqueda de un tiro libre; el de afuera hace que tire **un
    solo** enemigo. Sin el de afuera, tiran todos juntos.
    ''',
    misiones=[
        dict(titulo='Zigzag',
             carta='Seno | enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt',
             criatura='glitch',
             escena='''
             Los globos bajan derecho como plomadas. —Los globos de verdad bailan con el viento —dice {mentor}, y sopla uno
             que se va de costado, de acá para allá.
             ''',
             gheco='''
             `SDL_sinf` da un número que sube y baja entre -1 y 1, como una ola. Abajo de la línea que lo hace bajar:
             ```c
             enemigos[e].x += SDL_sinf(enemigos[e].y / 40) * 120 * dt;
             ```
             - Mientras el globo baja, `y / 40` crece y el seno va y viene: el globo se corre a un lado y al otro.
             - `* 120` es qué tan rápido se corre de costado; `* dt`, para que sea igual en todas las compus.

             El robot va a esperar dos segundos.
             ''',
             desafio='Hacé que los enemigos se muevan de costado, de un lado a otro, mientras bajan.',
             pasos=['Buscá `/* acá: y se mueve de costado, de un lado a otro, como un zigzag */`.',
                    'Debajo, escribí la línea con `SDL_sinf` de la sugerencia.',
                    'Tocá **Jugar** y mirá bailar los globos. Después, **Comprobar**.'],
             eventos='cuadros 120', estado='buscar #dc3c3c',
             superarla='''
             Los globos bajan bailando, de un lado al otro, como hojas en el viento. Ahora apuntar cuesta. El Glitch intenta
             hacerlos parpadear, pero el seno es parejo y no lo deja.
             ''',
             imagen=['La pantalla de la máquina con globos rojos bajando en zigzag, con líneas curvas de movimiento.',
                     'Un gatito pixelado que parpadea mira enojado desde un rincón de la pantalla.',
                     'Arcadia sopla un globo de verdad que se va de costado; Kira lo sigue con la vista; Gheco lo persigue.']),
        dict(titulo='Cinco y un respiro',
             carta='Oleadas | si salidos < POR_OLEADA: relojEnemigo += dt · si no: descanso += dt, a los 3 s: salidos = 0, oleada++ · al soltar uno: salidos++',
             escena='''
             Los globos salen sin parar, uno por segundo, para siempre. —Así nadie respira —dice {mentor}—. En la máquina
             venían de a cinco. Después, un ratito de calma. Y otra oleada.
             ''',
             gheco='''
             Ya están `oleada` (en 1), `salidos` y `descanso`. Tres cosas:
             1. **El reloj corre solo si faltan salir**, en lugar de `relojEnemigo += dt;`:
             ```c
             if (salidos < POR_OLEADA) {
                 relojEnemigo += dt;
             } else {
                 descanso += dt;                /* ya salieron los cinco: respiro */
                 if (descanso >= 3) {
                     descanso = 0;
                     salidos = 0;
                     oleada++;                  /* ¡la que sigue! */
                 }
             }
             ```
             2. **Contar** cada enemigo que sale, antes del `break`: `salidos++;`
             3. **Mostrar la oleada**, abajo de los puntos:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 10, 26, "OLEADA %d", oleada);
             ```
             El robot va a esperar nueve segundos: cinco globos, el respiro y la oleada 2.
             ''',
             desafio='Hacé que los enemigos vengan de a cinco, con 3 segundos de respiro entre oleadas, y mostrá la oleada.',
             pasos=['Buscá `/* acá: mientras falten enemigos de esta oleada, corre el reloj; si no, un respiro de 3 segundos y la oleada siguiente */`, borrá el `relojEnemigo += dt;` de abajo y escribí el `if` de la sugerencia.',
                    'Buscá `/* acá: contar el que salió */` y escribí `salidos++;`.',
                    'Buscá `/* acá: mostrar la oleada abajo de los puntos */` y escribí el texto.',
                    'Tocá **Jugar** y esperá el respiro. Después, **Comprobar**.'],
             eventos='cuadros 540', estado='textos',
             superarla='''
             Cinco globos… calma… y arriba a la izquierda, **OLEADA 2**. Kira aprovecha el respiro para estirar los dedos.
             Gheco se toma un sorbito de la gaseosa de la Boletería.
             ''',
             imagen=['La pantalla de la máquina con el cielo vacío entre dos oleadas y un cartelito blanco arriba (sin letras legibles).',
                     'Kira estira los dedos, sonriendo; Arcadia le pasa una gaseosa.',
                     'Gheco toma un sorbito de una botellita de gaseosa, arriba de la máquina.']),
        dict(titulo='Más rápidos',
             carta='Dificultad | enemigos[e].y += (100 + 40 * oleada) * dt',
             escena='''
             La segunda oleada baja igual de lenta que la primera. —Cada oleada era más brava —dice {mentor}—. Si no, a la
             décima uno se duerme.
             ''',
             gheco='''
             En lugar de `120`, una velocidad que crece con la oleada:
             ```c
             enemigos[e].y += (100 + 40 * oleada) * dt;
             ```
             | oleada | velocidad |
             |---|---|
             | 1 | 140 |
             | 2 | 180 |
             | 3 | 220 |

             Los paréntesis hacen que primero se calcule la velocidad y después se multiplique por `dt`. El robot va a
             esperar dos segundos.
             ''',
             desafio='Hacé que cada oleada baje más rápido: 100 + 40 por la oleada.',
             pasos=['Buscá `/* acá: cada oleada baja más rápido */` y borrá la línea de abajo.',
                    'En su lugar, escribí la línea de la sugerencia.',
                    'Tocá **Jugar** y aguantá varias oleadas. Después, **Comprobar**.'],
             eventos='cuadros 120', estado='buscar #dc3c3c',
             superarla='''
             La tercera oleada baja como lluvia. Kira dispara rápido, mueve el biplano, vuelve a disparar. Arcadia silba: —Ya
             parecés piloto de verdad.
             ''',
             imagen=['La pantalla de la máquina con una oleada de globos rojos bajando rápido, con rayas de velocidad.',
                     'Kira juega a toda velocidad; Arcadia silba admirada.',
                     'Gheco se pone unas antiparras de piloto más grandes que él, arriba de la máquina.']),
        dict(titulo='Burbujitas de agua',
             carta='Tiros | relojTiro += dt · a 1,5 s: el primer enemigo vivo suelta un tiro libre · cada tiro: y += 250 * dt, si y > 480: viva = false',
             escena='''
             —Los globos más pícaros tiraban burbujitas de agua para abajo —dice {mentor}—. Si te mojaban, perdías una vida.
             Primero, que tiren.
             ''',
             gheco='''
             Los tiros son balas: ya está la pileta `tiros` (el mismo `struct Bala`) y `relojTiro`. Dos cosas:
             1. **Tirar y mover**, antes de dibujar:
             ```c
             relojTiro += dt;
             if (relojTiro >= 1.5f) {
                 relojTiro -= 1.5f;
                 for (int e = 0; e < ENEMIGOS; e++) {
                     if (enemigos[e].vivo) {                     /* el primer enemigo vivo… */
                         for (int t = 0; t < TIROS; t++) {
                             if (!tiros[t].viva) {               /* …usa un tiro libre */
                                 tiros[t].x = enemigos[e].x + 18;
                                 tiros[t].y = enemigos[e].y + 30;
                                 tiros[t].viva = true;
                                 break;
                             }
                         }
                         break;                                  /* tira uno solo */
                     }
                 }
             }
             for (int t = 0; t < TIROS; t++) {
                 if (tiros[t].viva) {
                     tiros[t].y += 250 * dt;                     /* bajan */
                     if (tiros[t].y > 480) {
                         tiros[t].viva = false;
                     }
                 }
             }
             ```
             2. **Dibujarlos**, rojo anaranjado:
             ```c
             SDL_SetRenderDrawColor(lapiz, 255, 90, 40, 255);
             for (int t = 0; t < TIROS; t++) {
                 if (tiros[t].viva) {
                     SDL_FRect tiro = { tiros[t].x, tiros[t].y, 4, 10 };
                     SDL_RenderFillRect(lapiz, &tiro);
                 }
             }
             ```
             El robot va a esperar dos segundos.
             ''',
             desafio='Hacé que cada segundo y medio el primer enemigo vivo tire, y que los tiros bajen y se apaguen al salir.',
             pasos=['Buscá `/* acá: cada segundo y medio, el primer enemigo vivo tira; los tiros bajan y se apagan al salir */` y escribí el temporizador y el `for` que los mueve.',
                    'Buscá `/* acá: dibujar los tiros de los enemigos, rojo anaranjado */` y escribí el color y el `for` que los dibuja.',
                    'Tocá **Jugar** y esquivá las burbujitas. Después, **Comprobar**.'],
             eventos='cuadros 120', estado='buscar #ff5a28',
             superarla='''
             Los globos empiezan a tirar burbujitas de agua que caen como gotas. Por ahora atraviesan el biplano sin
             mojarlo. —Por ahora —dice {mentor}, y le guiña un ojo a Kira.
             ''',
             imagen=['La pantalla de la máquina con globos rojos tirando gotitas anaranjadas hacia abajo, cerca del biplano.',
                     'Arcadia le guiña un ojo a Kira; Kira esquiva concentrada.',
                     'Gheco abre un paraguitas diminuto arriba de la máquina.']),
    ],
)
