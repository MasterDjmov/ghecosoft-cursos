import motor
import n01

PLANTILLA = motor.crecer(motor.full(n01.PLANTILLA), [
    ('''
int main(void)
{''', '''
/* Un ladrillo: dónde está y si sigue entero */
typedef struct {
    SDL_FRect caja;
    bool vivo;
} Ladrillo;

#define COLUMNAS 10

int main(void)
{'''),
    ('''
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */''', '''
    bool pegada = true;   /* true: la pelota espera arriba de la paleta */
    //@ n3+
    int puntos = 0;
    //@ end

    Ladrillo pared[COLUMNAS] = { 0 };   /* todo en cero: ninguno vivo todavía */
    //@ n1: acá: armar la fila: diez ladrillos, uno al lado del otro
    for (int c = 0; c < COLUMNAS; c++) {
        pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
        pared[c].vivo = true;
    }
    //@ end'''),
    ('''
        /* ¿se cayó por abajo? */''', '''
        /* los ladrillos: ¿la pelota toca alguno? */
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                //@ n2: acá: el ladrillo se rompe y la pelota rebota
                pared[i].vivo = false;
                vy = -vy;
                //@ end
                //@ n3: acá: diez puntos por ladrillo
                puntos += 10;
                //@ end
                //@ n4: acá: uno solo por golpe: salir del for
                break;
                //@ end
            }
        }

        /* ¿se cayó por abajo? */'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);''', '''
        SDL_SetRenderDrawColor(lapiz, 255, 60, 100, 255);
        for (int i = 0; i < COLUMNAS; i++) {
            if (pared[i].vivo) {
                SDL_RenderFillRect(lapiz, &pared[i].caja);
            }
        }
        SDL_SetRenderDrawColor(lapiz, 0, 229, 255, 255);
        SDL_RenderFillRect(lapiz, &paleta);'''),
    ('''
        SDL_RenderFillRect(lapiz, &pelota);
        SDL_RenderPresent(lapiz);''', '''
        SDL_RenderFillRect(lapiz, &pelota);
        //@ n3: acá: el puntaje arriba a la izquierda
        SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        //@ end
        SDL_RenderPresent(lapiz);'''),
])

NODO = dict(
    codigo='R03-N02', titulo='Una fila de ladrillos', criatura='atraviesaparedes', padre='R03-N01',
    lugar='El Muro de Ladrillos',
    temas='col.registros, col.arrays', usa='juegos.colisiones, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    La pelota ya va y viene, pero arriba no hay nada que romper. {mentor} abre una tapa de la máquina: adentro hay
    una caja con diez ladrillos de vidrio rosado, todos iguales, esperando su lugar. —Diez ladrillos son diez cosas
    con lo mismo adentro —dice—: un lugar en la pantalla y si siguen enteros. No vamos a escribir diez variables.
    Mientras tanto, una criatura gomosa se mete en la pared como si fuera de gelatina: el **Atraviesaparedes**.
    ''',
    objetivos='''
    Guardar los ladrillos en un **arreglo de `struct`**: cada ladrillo con su caja y si está vivo. Armar una fila de
    diez con un `for`, que la pelota **rompa** el ladrillo que toca y rebote, **sumar puntos** y romper **uno solo
    por golpe** con `break`.
    ''',
    antes='''
    R03-N01 (la paleta y la pelota). Del curso de C: los arreglos, el `for` y los `struct`. De R01: el texto en
    pantalla (N07).
    ''',
    explicacion='''
    #### Un `struct`: varias cosas juntas
    Cada ladrillo tiene dos datos: **dónde está** (un rectángulo) y **si sigue entero**. Un `struct` los junta en un
    tipo nuevo:
    ```c
    typedef struct {
        SDL_FRect caja;   /* dónde está y cuánto mide */
        bool vivo;        /* true: entero · false: roto */
    } Ladrillo;
    ```
    Desde ahí, `Ladrillo` es un tipo como `int` o `float`. Para llegar a un dato de adentro se usa el punto:
    `pared[3].vivo`, `pared[3].caja.x`.

    #### Un arreglo de ladrillos
    `Ladrillo pared[COLUMNAS];` son diez ladrillos seguidos, del `pared[0]` al `pared[9]`. `COLUMNAS` es un
    `#define`: un nombre para el número 10, así si mañana querés doce, lo cambiás en un solo lugar. Con `= { 0 }`
    todo arranca en cero, así que ninguno está vivo hasta que los armemos.

    #### Armar la fila con un `for`
    El ladrillo número `c` va en `x = 22 + c * 60`: el primero en 22, el segundo en 82, el tercero en 142… Miden 56
    de ancho, así que entre uno y otro quedan 4 píxeles de junta. `(SDL_FRect){ x, y, ancho, alto }` arma un
    rectángulo en una sola línea.

    #### Romper y rebotar
    En cada cuadro, un `for` pregunta por cada ladrillo: ¿está vivo y la pelota lo toca? Si sí, se rompe
    (`vivo = false`) y la pelota rebota (`vy = -vy`). Los rotos no se dibujan ni chocan más.

    #### Uno solo por golpe: `break`
    `break` corta el `for` en el momento. Si la pelota pega justo en la junta, entre dos ladrillos, sin `break`
    rompería los dos y daría vuelta `vy` **dos veces**: quedaría para el mismo lado y seguiría de largo, metiéndose
    en la pared (es el Atraviesaparedes).
    ''',
    para_que='''
    Un arreglo de `struct` es la forma de guardar **muchas cosas iguales** en un juego: los ladrillos, los
    enemigos, los disparos, las gemas. Los vas a usar en todos los juegos que siguen.
    ''',
    errores='''
    **Pasarse del arreglo.** Con `c <= COLUMNAS` el `for` llega a `pared[10]`, que no existe: el programa escribe
    donde no debe. El último es `pared[COLUMNAS - 1]`; por eso va `c < COLUMNAS`.

    **Chocar con los rotos.** Si se olvida preguntar `pared[i].vivo`, la pelota sigue rebotando en ladrillos que
    ya no se ven.

    **Atraviesaparedes: rebotar dos veces.** Sin `break`, si la pelota toca dos ladrillos a la vez, da vuelta `vy`
    dos veces y sigue de largo por adentro de la pared.

    **Olvidar el punto.** `pared.vivo` no existe: hay que decir cuál, `pared[i].vivo`.
    ''',
    misiones=[
        dict(titulo='Diez ladrillos en fila',
             carta='Armar con un for | pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 } · pared[c].vivo = true',
             escena='''
             {mentor} saca los diez ladrillos de vidrio rosado y los deja en el piso, desordenados. —Cada uno tiene su
             lugar arriba, en fila —dice—. Uno al lado del otro, con una juntita. Vos decile a la máquina dónde va
             cada uno.
             ''',
             gheco='''
             Ya está el tipo `Ladrillo` (un `struct` con `caja` y `vivo`) y el arreglo `pared` con diez, todos en
             cero. También ya está el código que **dibuja** los que estén vivos. Falta armarlos con un `for`:
             ```c
             for (int c = 0; c < COLUMNAS; c++) {
                 pared[c].caja = (SDL_FRect){ 22 + c * 60, 80, 56, 20 };
                 pared[c].vivo = true;
             }
             ```
             - `c` va de 0 a 9: es el número de ladrillo.
             - `22 + c * 60` es su `x`: cada uno, 60 píxeles más a la derecha que el anterior.
             - `(SDL_FRect){ x, y, ancho, alto }` arma el rectángulo de una vez: `y` 80, 56 de ancho y 20 de alto.
             - `pared[c].vivo = true;` lo deja entero.
             ''',
             desafio='Armá la fila de diez ladrillos con un for, al principio del programa.',
             pasos=['Buscá el comentario `/* acá: armar la fila: diez ladrillos, uno al lado del otro */` (antes del bucle del juego).',
                    'Debajo, escribí el `for` de la sugerencia.',
                    'Tocá **Jugar**: arriba tiene que aparecer la fila rosada. Después, **Comprobar**.'],
             eventos='cuadros 3', estado='buscar #ff3c64',
             superarla='''
             Diez ladrillos rosados se encienden en fila arriba de la pantalla, parejitos, con su junta oscura.
             En el paredón de la plaza, una hilera entera de vidrio se ilumina.
             ''',
             imagen=['La pantalla de la máquina con una fila de diez ladrillos rosados brillantes, parejos, con juntas oscuras.',
                     'Arcadia acomoda un ladrillo de vidrio rosado de verdad en su lugar; Kira cuenta con los dedos.',
                     'Gheco, sentado arriba de la máquina, sostiene un ladrillo de vidrio chiquito entre las manos.']),
        dict(titulo='El ladrillo se rompe',
             carta='Romper y rebotar | si vivo y toca: vivo = false · vy = -vy',
             escena='''
             Kira saca y la pelota sube… y pasa a través de la fila como si los ladrillos fueran dibujados. —Están,
             pero no estorban —dice {mentor}—. Que la pelota los sienta.
             ''',
             gheco='''
             Ya está el `for` que recorre los ladrillos y pregunta, para cada uno, si está vivo y la pelota lo toca:
             ```c
             if (pared[i].vivo && toca(pelota, pared[i].caja)) {
             ```
             Adentro falta lo que pasa cuando lo toca:
             ```c
             pared[i].vivo = false;   /* se rompe: no se dibuja ni choca más */
             vy = -vy;                /* y la pelota rebota */
             ```
             El robot va a sacar enseguida con el espacio y a esperar a que la pelota llegue a la fila.
             ''',
             desafio='Hacé que el ladrillo que toca la pelota se rompa y que la pelota rebote.',
             pasos=['Buscá el comentario `/* acá: el ladrillo se rompe y la pelota rebota */` (adentro del `if` de los ladrillos).',
                    'Debajo, escribí `pared[i].vivo = false;` y `vy = -vy;`.',
                    'Tocá **Jugar**, sacá con el espacio y mirá la fila. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 80', estado='pixel 470 90',
             superarla='''
             *¡Crac!* Un ladrillo rosado desaparece y la pelota vuelve a bajar. Kira la devuelve y rompe otro. El
             Atraviesaparedes, que estaba metido en la fila, sale despedido con cara de ofendido.
             ''',
             imagen=['La pelota amarilla rompe un ladrillo rosado de la fila, que estalla en pedacitos de luz.',
                     'Kira festeja; Arcadia se tapa los oídos sonriendo.',
                     'Una criatura gomosa y translúcida sale despedida de la fila de ladrillos; Gheco se agacha para esquivarla.']),
        dict(titulo='Diez puntos por ladrillo',
             carta='Sumar puntos | puntos += 10 · SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos)',
             escena='''
             Kira rompe tres ladrillos seguidos y se da vuelta, orgullosa. —¿Cuántos puntos hice? —Ni idea —dice
             {mentor}—. La máquina no lleva la cuenta.
             ''',
             gheco='''
             Ya está la variable `int puntos = 0;`. Dos cosas:
             1. Cuando se rompe un ladrillo, adentro del mismo `if`: `puntos += 10;` (es `puntos = puntos + 10;`).
             2. Mostrarlo arriba a la izquierda, después de dibujar la pelota:
             ```c
             SDL_SetRenderDrawColor(lapiz, 255, 255, 255, 255);   /* blanco */
             SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
             ```
             `%d` es el lugar donde va el número (lo viste en R01-N07).
             ''',
             desafio='Sumá diez puntos por cada ladrillo roto y mostrá el puntaje arriba a la izquierda.',
             pasos=['Buscá `/* acá: diez puntos por ladrillo */` y escribí `puntos += 10;`.',
                    'Buscá `/* acá: el puntaje arriba a la izquierda */` y escribí las dos líneas de la sugerencia.',
                    'Tocá **Jugar**, rompé un ladrillo y mirá el puntaje. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 80', estado='textos',
             superarla='''
             Arriba a la izquierda se enciende **PUNTOS 10**. Kira rompe otro: **20**. Gheco anota en el aire con la
             cola, como un árbitro.
             ''',
             imagen=['La pantalla con el puntaje blanco arriba a la izquierda y la fila rosada con un hueco.',
                     'Kira señala el puntaje, contenta; Arcadia aplaude.',
                     'Gheco hace la cuenta con los dedos arriba de la máquina.']),
        dict(titulo='Uno solo por golpe',
             carta='Cortar el for | break: rompe un ladrillo por golpe y no rebota dos veces',
             criatura='atraviesaparedes',
             escena='''
             Kira saca desde un poquito más a la derecha. La pelota pega justo en la junta entre dos ladrillos, rompe
             los dos… y sigue de largo hacia arriba, como si nada. —Ese es el Atraviesaparedes —dice {mentor}—: dio la
             vuelta dos veces y quedó como estaba.
             ''',
             gheco='''
             Si la pelota toca **dos** ladrillos en el mismo cuadro, el `for` rompe el primero (`vy = -vy`, ahora
             baja) y después el segundo (`vy = -vy` otra vez: ¡vuelve a subir!). Dos vueltas son ninguna: la pelota
             sigue para el mismo lado, metiéndose en la pared.

             La solución es romper **uno solo por golpe**: apenas se rompe uno, se corta el `for` con `break`:
             ```c
             if (pared[i].vivo && toca(pelota, pared[i].caja)) {
                 pared[i].vivo = false;
                 vy = -vy;
                 puntos += 10;
                 break;   /* listo: no mira los demás */
             }
             ```
             `break` sale del `for` en el momento, sin mirar los ladrillos que faltan. El robot va a sacar desde un
             lugar donde la pelota pega en la junta.
             ''',
             desafio='Hacé que la pelota rompa un solo ladrillo por golpe, cortando el for con break.',
             pasos=['Buscá `/* acá: uno solo por golpe: salir del for */` (al final del `if` de los ladrillos).',
                    'Debajo, escribí `break;`.',
                    'Tocá **Jugar** y probá sacar desde distintos lugares. Después, **Comprobar**.'],
             eventos='apretar Derecha\ncuadros 3\nsoltar Derecha\ntecla Espacio\ncuadros 90', estado='pixel 470 90\npixel 530 90',
             superarla='''
             La pelota pega en la junta, rompe uno solo y vuelve a bajar, obediente. El Atraviesaparedes rebota contra
             la fila y ya no puede entrar. —Una cosa por vez —dice {mentor}—. Así se rompe un muro.
             ''',
             imagen=['La pelota amarilla pega en la junta entre dos ladrillos rosados: uno se rompe y el otro queda entero.',
                     'Una criatura gomosa y translúcida rebota contra la fila de ladrillos, enojada.',
                     'Kira choca los cinco con Arcadia; Gheco levanta un dedo: uno solo.']),
    ],
)
