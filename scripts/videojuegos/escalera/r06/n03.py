import motor
import n02

PLANTILLA = motor.crecer(motor.full(n02.PLANTILLA), [
    ('''
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
''', '''
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */
#define ENEMIGOS 8  /* cuántos enemigos puede haber a la vez */
'''),
    ('''
    bool viva;
};
''', '''
    bool viva;
};

/* Un enemigo: un globo de juguete que baja; vivo dice si está en el cielo */
struct Enemigo {
    float x;
    float y;
    bool vivo;
};
'''),
    ('''
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */''', '''
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */
    struct Enemigo enemigos[ENEMIGOS] = { 0 };  /* también empiezan guardados */
    float relojEnemigo = 0;                    /* cuánto pasó desde que salió el último */
    int puntos = 0;'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */''', '''
        //@ n1: acá: cada un segundo, sale un enemigo arriba, en una x al azar
        relojEnemigo += dt;
        if (relojEnemigo >= 1) {
            relojEnemigo -= 1;
            for (int e = 0; e < ENEMIGOS; e++) {
                if (!enemigos[e].vivo) {
                    enemigos[e].x = SDL_rand(600);
                    enemigos[e].y = 0;
                    enemigos[e].vivo = true;
                    break;
                }
            }
        }
        //@ end
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                //@ n2: acá: el enemigo baja y, si sale por abajo, se apaga
                enemigos[e].y += 120 * dt;
                if (enemigos[e].y > 480) {
                    enemigos[e].vivo = false;
                }
                //@ end
            }
        }

        //@ n3: acá: si una bala toca un enemigo, los dos se apagan y suman 10 puntos
        for (int i = 0; i < BALAS; i++) {
            for (int e = 0; e < ENEMIGOS; e++) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                    balas[i].viva = false;
                    enemigos[e].vivo = false;
                    puntos += 10;
                }
            }
        }
        //@ end

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */''', '''
        SDL_SetRenderDrawColor(lapiz, 220, 60, 60, 255);    /* los enemigos vivos: globos rojos */
        for (int e = 0; e < ENEMIGOS; e++) {
            if (enemigos[e].vivo) {
                SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                SDL_RenderFillRect(lapiz, &enemigo);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */'''),
    ('''
        SDL_RenderPresent(lapiz);''', '''
        //@ n4: acá: mostrar los puntos arriba a la izquierda
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        //@ end
        SDL_RenderPresent(lapiz);'''),
])

NODO = dict(
    codigo='R06-N03', titulo='Los enemigos', criatura='atraviesaparedes', padre='R06-N02',
    lugar='La Pista de los Biplanos',
    temas='juegos.colisiones', usa='col.registros, col.arrays, prog.matematica-azar',
    plantilla=PLANTILLA,
    cronica='''
    El biplano dispara burbujas a un cielo vacío. —Falta a qué apuntarle —dice {mentor}, y abre un cajón lleno de
    globos rojos de juguete, desinflados—. En la máquina bajaban globos, uno por segundo, y había que reventarlos antes
    de que se escaparan. Nadie se lastima: son globos. Pero en la pantalla las burbujas atraviesan los globos sin
    reventarlos, y desde adentro del vidrio se ríe el **Atraviesaparedes**.
    ''',
    objetivos='''
    Hacer **aparecer** un enemigo por segundo con un temporizador, en una pileta de structs como las balas, que **bajen**
    y se apaguen al salir, que las **balas los revienten** (dos `for`, uno adentro del otro, y la colisión de
    rectángulos) y mostrar los **puntos**.
    ''',
    antes='''
    El nodo anterior. De R01: la colisión entre rectángulos (N06). De R03: el temporizador (N07).
    ''',
    explicacion='''
    #### Los enemigos: otra pileta
    Igual que las balas: un `struct Enemigo` con `x`, `y` y `vivo`, y un arreglo de ocho. Un temporizador,
    `relojEnemigo`, junta el tiempo y cada un segundo busca un enemigo libre y lo pone arriba de todo, en una `x` al
    azar. Si los ocho están en el cielo, ese segundo no sale ninguno.

    #### Bajar y escaparse
    Cada enemigo vivo baja `120 * dt`. Si pasa el borde de abajo, se apaga: se escapó y queda libre para salir otra vez.

    #### Cada bala contra cada enemigo
    Para saber si alguna bala tocó algún enemigo hay que probar **todas las parejas**: un `for` por las balas y, adentro,
    otro por los enemigos. Con 5 balas y 8 enemigos son 40 preguntas por cuadro, y la compu las hace en un instante. Para
    cada pareja se arman las dos cajitas y se pregunta con `SDL_HasRectIntersectionFloat`, pero solo si **los dos están
    vivos** (si no, una bala guardada podría reventar un globo).

    #### Reventar
    Si se tocan, los dos se apagan (vuelven a sus piletas) y se suman 10 puntos.
    ''',
    para_que='''
    «Cada uno contra cada uno» con dos `for` es la manera más simple de chocar dos grupos de cosas: disparos contra
    enemigos, el jugador contra las monedas, los fantasmas contra el Pac-Man.
    ''',
    errores='''
    **No mirar si están vivos.** Una bala guardada (con su `x` e `y` viejas) puede «reventar» un globo que pasa por
    ahí: es el Atraviesaparedes al revés.

    **Apagar solo la bala.** Si el enemigo no se apaga, la bala siguiente lo vuelve a reventar y suma puntos sin parar.

    **El `break` al soltar el enemigo.** Sin él, en un segundo salen los ocho juntos, encimados.

    **Atraviesaparedes: balas muy rápidas.** Si la bala avanzara más que lo que mide el globo en un solo cuadro, podría
    saltarlo sin tocarlo. A 500 por segundo avanza 8 píxeles por cuadro y el globo mide 30: no pasa.
    ''',
    misiones=[
        dict(titulo='Globos a la vista',
             carta='Temporizador | relojEnemigo += dt · a 1 s: buscar un enemigo libre · x = SDL_rand(600), y = 0, vivo = true · break',
             escena='''
             {mentor} infla un globo rojo y lo suelta: sube hasta el techo del hangar. En la pantalla, en cambio, el cielo
             sigue vacío. —En la máquina salía uno por segundo —dice—, cada vez en otro lugar.
             ''',
             gheco='''
             Ya están el arreglo `enemigos` (ocho, guardados) y `relojEnemigo`. Cada un segundo, buscar uno libre y
             soltarlo arriba, en una `x` al azar:
             ```c
             relojEnemigo += dt;
             if (relojEnemigo >= 1) {
                 relojEnemigo -= 1;
                 for (int e = 0; e < ENEMIGOS; e++) {
                     if (!enemigos[e].vivo) {
                         enemigos[e].x = SDL_rand(600);    /* el globo mide 40: de 0 a 599 */
                         enemigos[e].y = 0;                /* arriba de todo */
                         enemigos[e].vivo = true;
                         break;                            /* uno solo por segundo */
                     }
                 }
             }
             ```
             Es lo mismo que disparar una bala, pero lo dispara el reloj. Los vivos ya se dibujan. El robot va a esperar
             un segundo y un poquito.
             ''',
             desafio='Hacé que cada un segundo salga un enemigo arriba, en una x al azar.',
             pasos=['Buscá `/* acá: cada un segundo, sale un enemigo arriba, en una x al azar */`.',
                    'Debajo, escribí el temporizador con el `for` que busca uno libre.',
                    'Tocá **Jugar** y esperá: tienen que ir apareciendo globos arriba. Después, **Comprobar**.'],
             eventos='cuadros 70', estado='buscar #dc3c3c',
             superarla='''
             Arriba de la pantalla aparece un globo rojo, después otro, y otro, cada uno en un lugar distinto. Se quedan
             ahí, colgados del borde. Gheco infla un globo de verdad y casi sale volando con él.
             ''',
             imagen=['La pantalla de la máquina con el biplano amarillo abajo y varios globos rojos arriba, en distintos lugares.',
                     'Arcadia infla un globo rojo de juguete; Kira mira la pantalla.',
                     'Gheco, agarrado de un globo rojo, se eleva un poquito sobre la máquina, asustado y feliz.']),
        dict(titulo='Bajan y se escapan',
             carta='Bajar | enemigos[e].y += 120 * dt · si y > 480: vivo = false',
             escena='''
             Los globos se amontonan arriba, quietos, hasta que salen los ocho y no sale ninguno más. —Tienen que bajar
             —dice {mentor}—, despacito. Y si llegan abajo, se escapan.
             ''',
             gheco='''
             Ya está el `for` que mira los enemigos vivos. Adentro, que bajen y, si salen por abajo, se apaguen:
             ```c
             enemigos[e].y += 120 * dt;       /* 120 píxeles por segundo */
             if (enemigos[e].y > 480) {       /* ¿se escapó por abajo? */
                 enemigos[e].vivo = false;    /* vuelve a la pileta */
             }
             ```
             Al apagarse, el reloj lo puede volver a soltar arriba. El robot va a esperar tres segundos.
             ''',
             desafio='Hacé que los enemigos bajen 120 píxeles por segundo y se apaguen al salir por abajo.',
             pasos=['Buscá `/* acá: el enemigo baja y, si sale por abajo, se apaga */`.',
                    'Debajo, escribí las líneas de la sugerencia.',
                    'Tocá **Jugar** y mirá bajar los globos. Después, **Comprobar**.'],
             eventos='cuadros 180', estado='buscar #dc3c3c',
             superarla='''
             Los globos bajan despacito, como hojas, y los que llegan abajo se escapan por el borde. Arriba siempre sale otro.
             Kira ya tiene el dedo en el botón rojo.
             ''',
             imagen=['La pantalla de la máquina con globos rojos bajando despacio hacia el biplano amarillo, con rayitas de movimiento.',
                     'Kira, con el dedo listo sobre el botón rojo del panel; Arcadia sonríe.',
                     'Gheco mira bajar un globo de verdad que se le escapó a Arcadia en el hangar.']),
        dict(titulo='¡Pum!',
             carta='Colisión | for cada bala · for cada enemigo · si los dos vivos y SDL_HasRectIntersectionFloat: apagar los dos · puntos += 10',
             criatura='atraviesaparedes',
             escena='''
             Kira apunta, dispara… y la burbuja atraviesa el globo como si fuera de humo. Otra, y otra. Dentro del vidrio de
             la pantalla, el Atraviesaparedes se ríe con la boca llena de burbujas.
             ''',
             gheco='''
             Cada bala contra cada enemigo: dos `for`, uno adentro del otro. Para cada pareja, las dos cajitas y la pregunta:
             ```c
             for (int i = 0; i < BALAS; i++) {
                 for (int e = 0; e < ENEMIGOS; e++) {
                     SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                     SDL_FRect enemigo = { enemigos[e].x, enemigos[e].y, 40, 30 };
                     if (balas[i].viva && enemigos[e].vivo && SDL_HasRectIntersectionFloat(&bala, &enemigo)) {
                         balas[i].viva = false;     /* la burbuja se gasta */
                         enemigos[e].vivo = false;  /* y el globo revienta */
                         puntos += 10;
                     }
                 }
             }
             ```
             Solo cuenta si **los dos** están vivos. El robot va a llevar el biplano debajo del primer globo y disparar.
             ''',
             desafio='Hacé que una bala que toca un enemigo apague a los dos y sume 10 puntos.',
             pasos=['Buscá `/* acá: si una bala toca un enemigo, los dos se apagan y suman 10 puntos */`.',
                    'Debajo, escribí los dos `for` con la colisión de la sugerencia.',
                    'Tocá **Jugar**, apuntá a un globo y dispará. Después, **Comprobar**.'],
             eventos='apretar Izquierda\ncuadros 20\nsoltar Izquierda\ncuadros 45\ntecla Espacio\ncuadros 45', estado='buscar #dc3c3c',
             superarla='''
             *¡Pum!* La burbuja toca el globo y los dos desaparecen en una lluvia de chispitas. Kira revienta otro, y otro.
             El Atraviesaparedes se queda sin lugar por donde pasar y se escurre fuera del vidrio.
             ''',
             imagen=['La pantalla de la máquina con una burbuja de luz reventando un globo rojo en una lluvia de chispitas.',
                     'Una criatura de gelatina translúcida se escurre fuera del vidrio de la pantalla, derrotada.',
                     'Kira festeja con el puño; Arcadia aplaude; Gheco se tapa las orejas por el ¡pum!']),
        dict(titulo='Los puntos',
             carta='Marcador | SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos)',
             escena='''
             Los globos revientan uno tras otro, pero la máquina no cuenta nada. —Diez puntos por globo —dice {mentor}—.
             Y que se vea arriba, a la izquierda, como en todas las máquinas.
             ''',
             gheco='''
             Los puntos ya se suman al reventar. Falta mostrarlos, al final del dibujo:
             ```c
             SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
             SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
             ```
             `%d` se reemplaza por el número de `puntos`. El robot va a esperar un ratito.
             ''',
             desafio='Mostrá los puntos arriba a la izquierda.',
             pasos=['Buscá `/* acá: mostrar los puntos arriba a la izquierda */`.',
                    'Debajo, escribí el color y el texto de la sugerencia.',
                    'Tocá **Jugar** y reventá globos. Después, **Comprobar**.'],
             eventos='cuadros 10', estado='textos',
             superarla='''
             Arriba a la izquierda aparece **PUNTOS 0**, y con cada globo sube de a diez. Kira ya va por cien. Gheco anota
             el récord con la cola en el polvo de la máquina.
             ''',
             imagen=['La pantalla de la máquina con globos rojos, el biplano y un marcador blanco arriba a la izquierda (sin letras legibles).',
                     'Kira juega concentrada; Arcadia mira el marcador, contenta.',
                     'Gheco escribe con la cola en el polvo de la máquina.']),
    ],
)
