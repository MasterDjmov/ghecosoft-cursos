import motor
import n03

PLANTILLA = motor.crecer(motor.full(n03.PLANTILLA), [
    ('''
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {''', '''
            //@ n4: acá: la paleta sigue al mouse
            if (evento.type == SDL_EVENT_MOUSE_MOTION) {
                paleta.x = evento.motion.x - paleta.w / 2;
            }
            //@ end
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {'''),
    ('''
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;''', '''
        //@ n2: acá: guardar dónde estaba la pelota antes de moverse
        SDL_FRect previa = pelota;
        //@ end
        if (pegada) {
            pelota.x = paleta.x + paleta.w / 2 - pelota.w / 2;'''),
    ('''
        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
        }''', '''
        if (toca(pelota, paleta) && vy > 0) {
            pelota.y = paleta.y - pelota.h;
            vy = -vy;
            //@ n1: acá: el costado depende de dónde pegó en la paleta
            vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
            //@ end
        }'''),
    ('''
                    pared[i].vivo = false;
                }
                vy = -vy;''', '''
                    pared[i].vivo = false;
                }
                //@ n2: acá: si antes de moverse ya estaba a la altura del ladrillo, entró por un costado
                SDL_FRect caja = pared[i].caja;
                bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
                if (aLaAltura) {
                    vx = -vx;
                } else {
                    vy = -vy;
                }
                //@ else
                vy = -vy;
                //@ end
                //@ n3: acá: cada ladrillo roto, la pelota un poco más rápida (con un tope)
                vy = SDL_clamp(vy * 1.03f, -480, 480);
                //@ end'''),
])

NODO = dict(
    codigo='R03-N04', titulo='Rebote según dónde pega', criatura='atraviesaparedes', padre='R03-N03',
    lugar='El Muro de Ladrillos',
    usa='juegos.colisiones, juegos.fisica, juegos.entrada',
    plantilla=PLANTILLA,
    cronica='''
    Kira juega diez minutos y se da cuenta de algo: la pelota hace siempre el mismo dibujo. Sube, rompe, baja, y
    otra vez por el mismo lado. —Así el muro se rompe solo de un costado —dice {mentor}—. En la máquina de verdad,
    vos elegías para dónde salía la pelota según dónde le pegabas con la paleta. Y cuidado con los costados de los
    ladrillos: ahí se esconde el **Atraviesaparedes**.
    ''',
    objetivos='''
    Que la pelota salga **para un lado o para el otro según dónde pega en la paleta**, que rebote bien cuando pega
    en el **costado** de un ladrillo, que se **apure** un poco con cada ladrillo (sin pasarse de un tope) y que la
    paleta también se mueva con el **mouse**.
    ''',
    antes='''
    R03-N03 (la pared). Del Pong: el ángulo según dónde pega (R02-N03). De R01: el mouse (N03).
    ''',
    explicacion='''
    #### El ángulo de la paleta
    Igual que en el Pong, la distancia entre el **centro de la pelota** y el **centro de la paleta** decide para
    dónde sale: si pega a la izquierda del centro, la distancia es negativa y sale hacia la izquierda; si pega a la
    derecha, sale hacia la derecha; en el medio, casi derecho para arriba. Multiplicada por 6, la pelota sale con
    un `vx` de entre -270 y 270.

    #### ¿Por dónde entró?
    Hasta ahora, al tocar un ladrillo siempre se daba vuelta `vy`. Pero si la pelota pega en el **costado** de un
    ladrillo, lo que tiene que cambiar es `vx`. ¿Cómo saberlo? Mirando **dónde estaba la pelota un cuadro antes**,
    antes de moverse (se guarda en `previa`):
    - Si **ya estaba a la altura del ladrillo** (su borde de abajo más abajo que el techo del ladrillo y su borde de
      arriba más arriba que el piso del ladrillo), no pudo haber entrado ni por arriba ni por abajo: entró por un
      **costado**. Se da vuelta `vx`.
    - Si no, entró por arriba o por abajo: se da vuelta `vy`.

    Es como mirar la foto del cuadro anterior para saber de dónde vino.

    #### Más rápido, con un tope
    Con cada ladrillo, `vy` se multiplica por 1,03 (un 3 % más rápido). `SDL_clamp` la deja entre -480 y 480: más
    rápida que eso, la pelota avanzaría en un cuadro más que el alto de un ladrillo y lo atravesaría (otra vez el
    Atraviesaparedes, como en el Pong).

    #### La paleta con el mouse
    Cuando el mouse se mueve llega un evento `SDL_EVENT_MOUSE_MOTION`, con la posición en `evento.motion.x` y
    `evento.motion.y`. Se pone la paleta centrada en el mouse: `evento.motion.x - paleta.w / 2`. El `SDL_clamp` que
    ya estaba la sigue frenando en los bordes.
    ''',
    para_que='''
    Elegir la dirección con la paleta es lo que hace que el Arkanoid sea un juego de puntería y no de suerte. Y
    saber **de qué lado** chocaron dos cosas es lo que vas a usar para caminar sobre plataformas sin atravesarlas.
    ''',
    errores='''
    **Restar al revés.** `paleta - pelota` en lugar de `pelota - paleta` hace que, al pegar a la izquierda, salga
    hacia la derecha.

    **Atraviesaparedes: siempre `vy`.** Si pega en el costado y se da vuelta `vy`, la pelota se mete en el ladrillo
    y sigue de largo rompiendo los de al lado.

    **Sin tope.** Si se multiplica la velocidad sin `SDL_clamp`, después de muchos ladrillos la pelota va tan
    rápido que atraviesa la paleta.

    **El mouse sin centrar.** `paleta.x = evento.motion.x;` deja el mouse en la punta izquierda de la paleta, no en
    el medio.
    ''',
    misiones=[
        dict(titulo='El ángulo de la paleta',
             carta='Salir según dónde pega | vx = ((centro de la pelota) - (centro de la paleta)) * 6',
             escena='''
             —Pegale con la punta —le dice {mentor} a Kira—. En esta máquina, si le pegás con la punta izquierda, la
             pelota sale para la izquierda. Por ahora la paleta es una tabla lisa: devuelve todo igual.
             ''',
             gheco='''
             Cuando la paleta devuelve la pelota, además de dar vuelta `vy`, el `vx` depende de **dónde pegó**:
             ```c
             vx = ((pelota.x + pelota.w / 2) - (paleta.x + paleta.w / 2)) * 6;
             ```
             - `pelota.x + pelota.w / 2` es el centro de la pelota; `paleta.x + paleta.w / 2`, el de la paleta.
             - La resta da negativo si pegó a la izquierda del centro (sale para la izquierda) y positivo si pegó a la
               derecha. En el medio, cerca de 0: sale casi derecho.
             - Por 6, para que salga con ganas: va de -270 a 270.

             El robot va a sacar y a correr la paleta hacia la derecha para recibir la pelota cuando baja.
             ''',
             desafio='Hacé que la pelota salga para un lado o para el otro según dónde pega en la paleta.',
             pasos=['Buscá `/* acá: el costado depende de dónde pegó en la paleta */` (adentro del `if` de la paleta).',
                    'Debajo, escribí la línea de `vx` de la sugerencia.',
                    'Tocá **Jugar** y probá pegarle con las puntas y con el medio. Después, **Comprobar**.'],
             eventos='tecla Espacio\napretar Derecha\ncuadros 42\nsoltar Derecha\ncuadros 100', estado='buscar #ffdc00',
             superarla='''
             Kira le pega con la punta izquierda y la pelota sale en diagonal, directo a un rincón del muro que nadie
             había tocado. —¡Puntería! —grita Gheco desde la máquina.
             ''',
             imagen=['La pelota amarilla sale en diagonal desde la punta izquierda de la paleta celeste, con una línea punteada.',
                     'Kira, concentrada, mueve la paleta para pegarle con la punta; Arcadia mira con una sonrisa pícara.',
                     'Gheco sigue la diagonal con el dedo, sentado arriba de la máquina.']),
        dict(titulo='El golpe de costado',
             carta='¿Por dónde entró? | previa = pelota antes de moverse · si ya estaba a la altura del ladrillo: vx = -vx · si no: vy = -vy',
             criatura='atraviesaparedes',
             escena='''
             La pelota pega en el costado de un ladrillo verde… y en vez de rebotar hacia el costado, se mete adentro de
             la pared y rompe tres de un saque. Una criatura gomosa se ríe desde adentro del muro: el Atraviesaparedes.
             ''',
             gheco='''
             Si la pelota entra por el **costado** de un ladrillo, lo que tiene que cambiar es `vx`, no `vy`. Para
             saber por dónde entró, se mira dónde estaba **un cuadro antes**. Dos cosas:
             1. **Antes de mover la pelota**, guardar dónde estaba:
             ```c
             SDL_FRect previa = pelota;   /* una copia: la pelota de antes */
             ```
             2. **Al chocar con un ladrillo**, en lugar de dar vuelta siempre `vy`:
             ```c
             SDL_FRect caja = pared[i].caja;
             bool aLaAltura = previa.y + previa.h > caja.y && previa.y < caja.y + caja.h;
             if (aLaAltura) {
                 vx = -vx;   /* ya estaba a su altura: entró por un costado */
             } else {
                 vy = -vy;   /* venía de arriba o de abajo */
             }
             ```
             - `previa.y + previa.h > caja.y`: el borde de abajo de la pelota estaba más abajo que el techo del ladrillo.
             - `previa.y < caja.y + caja.h`: el borde de arriba estaba más arriba que el piso del ladrillo.
             - Si pasan las dos, la pelota ya estaba **a la altura** del ladrillo antes de tocarlo: solo pudo llegar de
               costado.

             El robot va a sacar desde un lugar donde la pelota pega de costado en un ladrillo.
             ''',
             desafio='Hacé que la pelota rebote hacia el costado cuando pega en el costado de un ladrillo.',
             pasos=['Buscá `/* acá: guardar dónde estaba la pelota antes de moverse */` y escribí `SDL_FRect previa = pelota;`.',
                    'Buscá `/* acá: si antes de moverse ya estaba a la altura del ladrillo, entró por un costado */` y borrá la línea `vy = -vy;` de abajo.',
                    'En su lugar, escribí las líneas de `caja` y `aLaAltura`, y el `if` de la sugerencia.',
                    'Tocá **Jugar** y mirá cómo rebota en los costados. Después, **Comprobar**.'],
             eventos='apretar Derecha\ncuadros 30\nsoltar Derecha\ntecla Espacio\ncuadros 300', estado='buscar #ffdc00',
             superarla='''
             La pelota pega en el costado del ladrillo verde y sale rebotada hacia el costado, como tiene que ser. El
             Atraviesaparedes queda afuera de la pared, aplastado contra el vidrio, con cara de no entender nada.
             ''',
             imagen=['La pelota amarilla rebota hacia el costado al pegar en el borde lateral de un ladrillo verde, con una flecha.',
                     'Una criatura gomosa y translúcida queda aplastada contra la pared de ladrillos, desde afuera.',
                     'Kira y Arcadia se ríen; Gheco, sentado arriba de la máquina, señala el rebote.']),
        dict(titulo='Cada vez más rápido',
             carta='Apurar con tope | vy = SDL_clamp(vy * 1.03f, -480, 480)',
             escena='''
             Con media pared rota, el juego se pone aburrido: la pelota va siempre igual de lenta. —El Muro original se
             apuraba —recuerda {mentor}—. Cada ladrillo que rompías, la pelota volvía con más bronca.
             ''',
             gheco='''
             Cada vez que se rompe (o se golpea) un ladrillo, la pelota va un 3 % más rápido de arriba abajo:
             ```c
             vy = SDL_clamp(vy * 1.03f, -480, 480);
             ```
             - `vy * 1.03f` es `vy` más un 3 %. La `f` dice que es un `float`.
             - `SDL_clamp` la frena en 480 para arriba o para abajo: más rápido que eso, en un cuadro avanzaría más
               que el alto de un ladrillo y lo podría atravesar (lo viste en el Pong, R02-N03).

             Va justo después del rebote en el ladrillo.
             ''',
             desafio='Hacé que la pelota se apure un 3 % con cada ladrillo, sin pasarse de 480.',
             pasos=['Buscá `/* acá: cada ladrillo roto, la pelota un poco más rápida (con un tope) */`.',
                    'Debajo, escribí la línea con `SDL_clamp` de la sugerencia.',
                    'Tocá **Jugar** y rompé varios ladrillos. Después, **Comprobar**.'],
             eventos='tecla Espacio\napretar Derecha\ncuadros 42\nsoltar Derecha\ncuadros 100', estado='buscar #ffdc00',
             superarla='''
             La pelota vuelve cada vez con más ganas. Kira ya no se ríe: juega con la lengua afuera, concentrada. —Así
             era —dice {mentor}—. Al final, la pelota parecía una chispa.
             ''',
             imagen=['La pelota amarilla con una estela larga, cada vez más rápida, entre la paleta y la pared de colores.',
                     'Kira juega muy concentrada, con la lengua afuera; Arcadia la mira con orgullo.',
                     'Gheco, arriba de la máquina, mueve la cabeza de un lado al otro cada vez más rápido.']),
        dict(titulo='La paleta con el mouse',
             carta='Seguir al mouse | SDL_EVENT_MOUSE_MOTION: paleta.x = evento.motion.x - paleta.w / 2',
             escena='''
             Un chico del barrio se acerca a la máquina y agarra… el mouse que está al costado del tablero. Lo mueve y no
             pasa nada. —Las máquinas viejas del Muro tenían una perilla —dice {mentor}—. Esto es lo más parecido.
             ''',
             gheco='''
             Cuando se mueve el mouse llega un evento `SDL_EVENT_MOUSE_MOTION` (lo viste en R01-N03), con la posición
             en `evento.motion.x` y `evento.motion.y`. En el `while` de los eventos:
             ```c
             if (evento.type == SDL_EVENT_MOUSE_MOTION) {
                 paleta.x = evento.motion.x - paleta.w / 2;   /* el mouse, en el medio de la paleta */
             }
             ```
             Restar la mitad del ancho deja el mouse en el **medio** de la paleta y no en la punta. No hace falta
             frenarla en los bordes: el `SDL_clamp` de después ya lo hace en cada cuadro.

             El robot va a llevar el mouse a la izquierda de la ventana.
             ''',
             desafio='Hacé que la paleta siga al mouse, centrada en él.',
             pasos=['Buscá `/* acá: la paleta sigue al mouse */` (en el `while` de los eventos).',
                    'Debajo, escribí el `if` con `SDL_EVENT_MOUSE_MOTION` de la sugerencia.',
                    'Tocá **Jugar** y mové el mouse adentro del juego. Después, **Comprobar**.'],
             eventos='mouse 120 300\ncuadros 3', estado='buscar #00e5ff',
             superarla='''
             El chico mueve el mouse y la paleta lo sigue como una sombra. Rompe un ladrillo verde y grita. Detrás de él
             ya hay otros dos esperando para probar.
             ''',
             imagen=['Un chico del barrio con abrigo cerrado mueve un mouse al costado de la máquina, con cara de asombro.',
                     'En la pantalla, la paleta celeste sigue al mouse; Kira le explica algo al chico.',
                     'Gheco, sentado arriba de la máquina, levanta el pulgar.'], personajes='Kira, Gheco'),
    ],
)
