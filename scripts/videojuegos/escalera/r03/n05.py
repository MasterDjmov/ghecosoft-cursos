import motor
import n04

ARMAR = '''    for (int f = 0; f < FILAS; f++) {
        for (int c = 0; c < COLUMNAS; c++) {
            int i = f * COLUMNAS + c;   /* el número de ladrillo */
            pared[i].caja = (SDL_FRect){ 22 + c * 60, 60 + f * 24, 56, 20 };
            pared[i].vivo = true;
            pared[i].fila = f;
        }
    }
    for (int i = 0; i < FILAS * COLUMNAS; i++) {
        pared[i].golpes = (pared[i].fila == FILAS - 1) ? 2 : 1;
    }'''

PLANTILLA = motor.crecer(motor.full(n04.PLANTILLA), [
    ('\n' + ARMAR, '''
    //@ n4: acá: armar la pared con la función
    armarPared(pared);
    //@ else
''' + ARMAR + '''
    //@ end'''),
    ('''
#define FILAS 5

int main(void)
{''', '''
#define FILAS 5

enum Estado { JUGANDO, PERDISTE, GANASTE };

//@ n4: acá: una función que arma la pared (los mismos for de antes, para usarlos dos veces)
/* Arma los 50 ladrillos enteros, con los de metal abajo */
static void armarPared(Ladrillo pared[])
{
''' + ARMAR + '''
}
//@ end

int main(void)
{'''),
    ('''
    int puntos = 0;''', '''
    int puntos = 0;
    //@ n1+
    int vidas = 3;
    //@ end
    //@ n2+
    enum Estado estado = JUGANDO;
    //@ end'''),
    ('''
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {''', '''
            //@ n4: acá: con la R, otra partida: la pared entera, 3 vidas y 0 puntos
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado != JUGANDO) {
                armarPared(pared);
                vidas = 3;
                puntos = 0;
                pegada = true;
                estado = JUGANDO;
            }
            //@ end
            //@ n2: acá: solo se saca si se está jugando
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada && estado == JUGANDO) {
            //@ else
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE && pegada) {
            //@ end'''),
    ('''
        if (pelota.y > 480) {
            pegada = true;
        }''', '''
        if (pelota.y > 480) {
            pegada = true;
            //@ n1: acá: una vida menos
            vidas--;
            //@ end
            //@ n2: acá: sin vidas, perdiste
            if (vidas == 0) {
                estado = PERDISTE;
            }
            //@ end
        }

        //@ n3: acá: contar los ladrillos que quedan; si no queda ninguno, ganaste
        int quedan = 0;
        for (int i = 0; i < FILAS * COLUMNAS; i++) {
            if (pared[i].vivo) {
                quedan++;
            }
        }
        if (quedan == 0) {
            estado = GANASTE;
        }
        //@ end'''),
    ('''
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);''', '''
        SDL_RenderDebugTextFormat(lapiz, 10, 10, "PUNTOS %d", puntos);
        //@ n1: acá: las vidas arriba a la derecha
        SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
        //@ end
        //@ n3: acá: cuántos quedan, arriba en el medio, y el cartel si ganaste
        SDL_RenderDebugTextFormat(lapiz, 272, 10, "QUEDAN %d", quedan);
        if (estado == GANASTE) {
            SDL_RenderDebugText(lapiz, 280, 300, "PARED ROTA");
        }
        //@ end
        //@ n2: acá: el cartel de perdiste
        if (estado == PERDISTE) {
            SDL_RenderDebugText(lapiz, 288, 300, "PERDISTE");
        }
        //@ end
        //@ n4: acá: cómo volver a jugar
        if (estado != JUGANDO) {
            SDL_RenderDebugText(lapiz, 276, 320, "R: OTRA VEZ");
        }
        //@ end'''),
])

PERDER = 'tecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 30'

NODO = dict(
    codigo='R03-N05', titulo='Vidas, fin y revancha', criatura='bucle_eterno', padre='R03-N04',
    lugar='El Muro de Ladrillos',
    temas='juegos.estados', usa='prog.funciones, col.arrays',
    plantilla=PLANTILLA,
    cronica='''
    Los chicos del barrio ya hacen fila para jugar al Muro. Pero hay un problema: la pelota se cae, vuelve, se cae,
    vuelve… y el juego no termina nunca. Un chico juega media hora sin parar y se va aburrido. Debajo de la máquina
    se enrosca una serpiente de luz violeta que se muerde la cola: el **Bucle Eterno**. —Un juego sin final no es un
    juego —dice {mentor}—. Hacen falta vidas, un cartel de fin y una forma de volver a empezar.
    ''',
    objetivos='''
    Darle **tres vidas** al jugador, **perder** cuando se terminan, **contar los ladrillos que quedan** para saber
    cuándo **ganaste** y armar una **función** que arme la pared, para usarla al empezar y en la **revancha** con la R.
    ''',
    antes='''
    R03-N04. Del Pong: los estados con `enum` (R02-N05). Del curso de C: las funciones y pasar un arreglo a una
    función.
    ''',
    explicacion='''
    #### Las vidas
    Una variable `int vidas = 3;`. Cada vez que la pelota se cae por abajo, `vidas--;` (una menos). Se muestra
    arriba a la derecha.

    #### Los estados del juego
    Como en el Pong (R02-N05), un `enum` le pone nombre a cada momento del juego: `JUGANDO`, `PERDISTE` y
    `GANASTE`. Cuando las vidas llegan a 0, el estado pasa a `PERDISTE`, y mientras no se esté jugando, el espacio no
    saca la pelota.

    #### ¿Cuántos quedan?
    En cada cuadro, un `for` cuenta los ladrillos que siguen vivos. Si no queda ninguno, ganaste. Contar en cada
    cuadro es rapidísimo para la compu: son solo 50.

    #### Una función para armar la pared
    Los `for` que arman la pared hacen falta **dos veces**: al empezar y en la revancha. En lugar de copiarlos, se
    los pone en una **función**:
    ```c
    static void armarPared(Ladrillo pared[])
    {
        /* … los mismos for de antes … */
    }
    ```
    `Ladrillo pared[]` dice que recibe un arreglo de ladrillos. Un arreglo que se pasa a una función **no se
    copia**: la función trabaja sobre el mismo arreglo, así que lo que arma queda armado en `main`.

    #### La revancha
    Con la R, si no se está jugando: la pared entera (`armarPared`), 3 vidas, 0 puntos, la pelota pegada y otra vez
    `JUGANDO`.
    ''',
    para_que='''
    Vidas, fin y volver a empezar son lo que hace que una partida sea una partida. Y una función que deja todo como
    al principio es lo que usan todos los juegos para «empezar de nuevo» o «pasar al nivel siguiente».
    ''',
    errores='''
    **Bucle Eterno: el juego que no termina.** Sin un estado de fin, las vidas siguen bajando (2, 1, 0, -1…) y la
    partida no termina nunca.

    **Restar vidas en cada cuadro.** Si `vidas--` queda afuera del `if` de la caída, se pierden 60 vidas por
    segundo.

    **Contar sin volver a cero.** Si `int quedan = 0;` queda afuera del bucle del juego, cada cuadro suma 50 más.

    **Revancha a medias.** Si la R arma la pared pero no devuelve las vidas, la partida nueva empieza perdida.
    ''',
    misiones=[
        dict(titulo='Tres vidas',
             carta='Vidas | int vidas = 3 · al caerse: vidas-- · VIDAS %d arriba a la derecha',
             escena='''
             La pelota se cae por quinta vez y vuelve como si nada. —En el Muro había tres vidas —dice {mentor}, y
             dibuja tres paletitas con el dedo en el vidrio empañado—. Cada pelota que se te cae, una menos.
             ''',
             gheco='''
             Ya está la variable `int vidas = 3;`. Dos cosas:
             1. Cuando la pelota se cae (adentro del `if (pelota.y > 480)`): `vidas--;` (es `vidas = vidas - 1;`).
             2. Mostrarlas arriba a la derecha, al lado del puntaje:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 560, 10, "VIDAS %d", vidas);
             ```
             El robot va a sacar una vez y dejar que la pelota se caiga.
             ''',
             desafio='Restá una vida cada vez que la pelota se cae y mostrá las vidas arriba a la derecha.',
             pasos=['Buscá `/* acá: una vida menos */` (adentro del `if` de la caída) y escribí `vidas--;`.',
                    'Buscá `/* acá: las vidas arriba a la derecha */` y escribí la línea de `VIDAS`.',
                    'Tocá **Jugar**, dejá caer la pelota y mirá las vidas. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 150', estado='textos',
             superarla='''
             Arriba a la derecha aparece **VIDAS 3**, y cuando la pelota se cae, **VIDAS 2**. Kira se pone seria: ahora
             cada pelota cuenta.
             ''',
             imagen=['La pantalla con el texto de las vidas arriba a la derecha y la pelota cayendo por abajo de la paleta.',
                     'Arcadia dibuja tres paletitas con el dedo en el vidrio de la máquina; Kira mira atenta.',
                     'Gheco, sentado arriba de la máquina, levanta tres dedos.']),
        dict(titulo='Perdiste',
             carta='Fin | enum Estado { JUGANDO, PERDISTE, GANASTE } · vidas == 0: estado = PERDISTE · sacar solo si JUGANDO',
             criatura='bucle_eterno',
             escena='''
             Las vidas llegan a 0… y después a -1, -2, -3. El Bucle Eterno se ríe, enroscado debajo de la máquina. —El
             juego no sabe terminar —dice {mentor}—. Cuando se acaban las vidas, se acabó.
             ''',
             gheco='''
             Ya están el `enum Estado { JUGANDO, PERDISTE, GANASTE };` (como en el Pong, R02-N05) y la variable
             `estado`, que arranca en `JUGANDO`. Tres cosas:
             1. Cuando se cae la pelota, después de restar la vida:
             ```c
             if (vidas == 0) {
                 estado = PERDISTE;
             }
             ```
             2. Que el espacio saque **solo si se está jugando**: agregale `&& estado == JUGANDO` al `if` del espacio.
             3. El cartel, después del puntaje:
             ```c
             if (estado == PERDISTE) {
                 SDL_RenderDebugText(lapiz, 288, 300, "PERDISTE");
             }
             ```
             El robot va a sacar cuatro veces y dejar que se caiga.
             ''',
             desafio='Hacé que con 0 vidas el juego termine, con el cartel PERDISTE y sin poder sacar más.',
             pasos=['Buscá `/* acá: sin vidas, perdiste */` (en la caída) y escribí el `if (vidas == 0)`.',
                    'Buscá `/* acá: solo se saca si se está jugando */` y agregale `&& estado == JUGANDO` a la condición del `if` de abajo.',
                    'Buscá `/* acá: el cartel de perdiste */` y escribí el `if` con `PERDISTE`.',
                    'Tocá **Jugar** y perdé las tres vidas. Después, **Comprobar**.'],
             eventos=PERDER, estado='textos',
             superarla='''
             La tercera pelota se cae y la pantalla dice **PERDISTE**. Se queda quieta, esperando. El Bucle Eterno suelta
             su cola, confundido: el juego ya sabe terminar.
             ''',
             imagen=['La pantalla de la máquina quieta, con un cartel blanco en el medio (sin texto legible) y la pelota quieta sobre la paleta.',
                     'Una serpiente de luz violeta suelta su propia cola, confundida, debajo de la máquina.',
                     'Kira suspira con una sonrisa; Gheco le da una palmadita en el hombro.']),
        dict(titulo='¿Cuántos quedan?',
             carta='Contar | quedan = 0 · for: si vivo, quedan++ · quedan == 0: GANASTE',
             escena='''
             —¿Y cuándo se gana? —pregunta un chico de la fila. Kira mira la pared: le faltan un montón. —Cuando no
             queda ninguno —dice {mentor}—. Pero la máquina tiene que saber contarlos.
             ''',
             gheco='''
             En cada cuadro, después de la caída, se cuentan los ladrillos vivos:
             ```c
             int quedan = 0;
             for (int i = 0; i < FILAS * COLUMNAS; i++) {
                 if (pared[i].vivo) {
                     quedan++;
                 }
             }
             if (quedan == 0) {
                 estado = GANASTE;
             }
             ```
             `quedan` arranca en 0 **en cada cuadro** y suma uno por cada ladrillo vivo. Y para que se vea, arriba en
             el medio, con el cartel si ganaste:
             ```c
             SDL_RenderDebugTextFormat(lapiz, 272, 10, "QUEDAN %d", quedan);
             if (estado == GANASTE) {
                 SDL_RenderDebugText(lapiz, 280, 300, "PARED ROTA");
             }
             ```
             ''',
             desafio='Contá los ladrillos que quedan, mostralos arriba y hacé que ganes cuando no queda ninguno.',
             pasos=['Buscá `/* acá: contar los ladrillos que quedan; si no queda ninguno, ganaste */` y escribí el `for` y el `if` de la sugerencia.',
                    'Buscá `/* acá: cuántos quedan, arriba en el medio, y el cartel si ganaste */` y escribí las líneas de `QUEDAN` y `PARED ROTA`.',
                    'Tocá **Jugar** y rompé uno: el número tiene que bajar. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 150\ntecla Espacio\ncuadros 100', estado='textos',
             superarla='''
             Arriba aparece **QUEDAN 50** y baja con cada ladrillo roto. Los chicos de la fila cuentan en voz alta junto
             con la pantalla: —¡Cuarenta y nueve! ¡Cuarenta y ocho!
             ''',
             imagen=['La pantalla con el contador blanco arriba en el medio y la pared de colores con varios huecos.',
                     'Chicos del barrio con abrigos cerrados cuentan en voz alta, señalando la pantalla.',
                     'Kira juega concentrada; Gheco, sobre la máquina, cuenta con la cola.']),
        dict(titulo='Revancha',
             carta='Función y revancha | static void armarPared(Ladrillo pared[]) · R: armarPared, 3 vidas, 0 puntos, JUGANDO',
             escena='''
             El chico pierde y se queda mirando el cartel. —¿Y ahora? —pregunta. Para volver a jugar hay que apagar la
             máquina y prenderla otra vez. —Una revancha —dice {mentor}—. Con la R.
             ''',
             gheco='''
             Para la revancha hay que volver a armar la pared, y esos `for` ya están al principio. En lugar de copiarlos,
             van a una **función** (antes del `main`):
             ```c
             static void armarPared(Ladrillo pared[])
             {
                 /* acá van los mismos for de antes: cortalos de main y pegalos acá */
             }
             ```
             `Ladrillo pared[]` recibe el arreglo. Un arreglo **no se copia** al pasarlo: la función arma el mismo de
             `main`. En `main`, donde estaban los `for`, queda solo `armarPared(pared);`.

             Y en los eventos, con la R, si no se está jugando:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_R && estado != JUGANDO) {
                 armarPared(pared);
                 vidas = 3;
                 puntos = 0;
                 pegada = true;
                 estado = JUGANDO;
             }
             ```
             Y un cartelito que avise: `R: OTRA VEZ`, cuando no se está jugando.
             ''',
             desafio='Pasá el armado de la pared a una función y usala para volver a jugar con la R.',
             pasos=['Buscá `/* acá: una función que arma la pared … */` (antes del `main`) y escribí la función `armarPared` con los mismos `for`.',
                    'Buscá `/* acá: armar la pared con la función */` (en `main`), borrá los `for` de abajo y escribí `armarPared(pared);`.',
                    'Buscá `/* acá: con la R, otra partida … */` (en los eventos) y escribí el `if` con `SDLK_R`.',
                    'Buscá `/* acá: cómo volver a jugar */` y escribí el cartel `R: OTRA VEZ` cuando `estado != JUGANDO`.',
                    'Tocá **Jugar**, perdé y apretá la R. Después, **Comprobar**.'],
             eventos=PERDER + '\ntecla R\ncuadros 5', estado='textos',
             superarla='''
             El chico aprieta la R y la pared se arma entera de nuevo, con sus tres vidas. Se ríe y juega otra vez. Detrás
             de él, la fila es cada vez más larga. Debajo de la máquina, el Bucle Eterno se escurre y desaparece.
             ''',
             imagen=['La máquina del Muro encendida, con la pared de colores entera otra vez en la pantalla.',
                     'Un chico del barrio con abrigo cerrado aprieta un botón, feliz; detrás, una fila de chicos espera.',
                     'Kira y Arcadia chocan los cinco; Gheco, arriba de la máquina, saluda a los chicos.']),
    ],
)
