import motor
import n01

PLANTILLA = motor.crecer(motor.full(n01.PLANTILLA), [
    ('''
#define NUBES 6     /* cuántas nubes pasan por el cielo */
''', '''
#define NUBES 6     /* cuántas nubes pasan por el cielo */
#define BALAS 5     /* cuántas balas puede haber en el aire a la vez */

/* Una bala: dónde está y si está volando (viva) o guardada, libre para disparar */
struct Bala {
    float x;
    float y;
    bool viva;
};
'''),
    ('''
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };''', '''
    float ny[NUBES] = { 40, 120, 200, 300, 380, 440 };
    struct Bala balas[BALAS] = { 0 };          /* todas empiezan guardadas: viva = false */'''),
    ('''
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }''', '''
            if (evento.type == SDL_EVENT_QUIT) {
                jugando = false;
            }
            //@ n1: acá: con el espacio, buscar una bala libre y dispararla desde el biplano
            if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                for (int i = 0; i < BALAS; i++) {
                    if (!balas[i].viva) {
                        balas[i].x = avion.x + 18;
                        balas[i].y = avion.y - 10;
                        balas[i].viva = true;
                        break;   /* una sola por apretada */
                    }
                }
            }
            //@ end'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */''', '''
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                //@ n2: acá: la bala sube rápido
                balas[i].y -= 500 * dt;
                //@ end
                //@ n3: acá: si salió por arriba, se apaga y queda libre para otro disparo
                if (balas[i].y < -10) {
                    balas[i].viva = false;
                }
                //@ end
            }
        }

        SDL_SetRenderDrawColor(lapiz, 40, 90, 160, 255);   /* el cielo */'''),
    ('''
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */''', '''
        SDL_SetRenderDrawColor(lapiz, 255, 255, 120, 255);  /* las balas que vuelan */
        for (int i = 0; i < BALAS; i++) {
            if (balas[i].viva) {
                SDL_FRect bala = { balas[i].x, balas[i].y, 4, 10 };
                SDL_RenderFillRect(lapiz, &bala);
            }
        }
        //@ n4: acá: el cargador: un cuadradito naranja abajo por cada bala libre
        SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
        for (int i = 0; i < BALAS; i++) {
            if (!balas[i].viva) {
                SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                SDL_RenderFillRect(lapiz, &libre);
            }
        }
        //@ end
        SDL_SetRenderDrawColor(lapiz, 255, 200, 60, 255);   /* el biplano: un cuerpo y un ala */'''),
])

NODO = dict(
    codigo='R06-N02', titulo='Las balas', criatura='fuga_texturas', padre='R06-N01',
    lugar='La Pista de los Biplanos',
    temas='col.registros', usa='col.arrays, juegos.entrada, prog.bucles',
    plantilla=PLANTILLA,
    cronica='''
    Kira vuela por el cielo de la máquina, pero en el panel hay un botón rojo que dice, en letras gastadas, algo que
    nadie se acuerda. Lo aprieta: nada. —Los biplanos de la máquina disparaban burbujas de luz —dice {mentor}—. Pero
    no infinitas: la máquina tenía lugar para cinco. Si cada disparo fuera una burbuja nueva, la memoria se llenaría.
    Desde atrás del panel, algo se infla como un globo: la **Fuga de Texturas**, que vive de lo que nadie libera.
    ''',
    objetivos='''
    Guardar las balas en un **arreglo de structs** (cada una con su `x`, su `y` y si está **viva**), disparar buscando
    una **libre**, hacerlas subir, **apagarlas** cuando salen de la pantalla para poder reusarlas y mostrar cuántas
    quedan en el cargador.
    ''',
    antes='''
    El nodo anterior. De R03: el arreglo de `struct Ladrillo` con su `viva` (N02) y el `break` (N02).
    ''',
    explicacion='''
    #### Muchas cosas iguales: un arreglo de structs
    Una bala tiene tres datos: `x`, `y` y `viva` (si está volando). Se juntan en un `struct Bala`, como los ladrillos del
    Arkanoid, y se arma un arreglo de cinco: `struct Bala balas[BALAS]`. Con `= { 0 }` todas empiezan en cero: guardadas,
    sin volar.

    #### Disparar: buscar una libre
    No se crea una bala nueva: se busca en el arreglo una que **no** esté viva (`!balas[i].viva`), se la pone en la punta
    del biplano y se la marca viva. El `break` corta el `for` apenas encuentra una: si no, con una apretada saldrían las
    cinco juntas. Si están todas volando, no sale nada.

    #### Volar y apagarse
    En cada cuadro, cada bala viva sube `500 * dt`. Cuando pasa el borde de arriba, se marca `viva = false`: vuelve al
    cargador, lista para otro disparo. Es la misma idea que las nubes que vuelven arriba: **reusar** en lugar de crear.

    #### El cargador
    Un cuadradito naranja abajo a la izquierda por cada bala libre. Se ve cómo se gastan al disparar y cómo vuelven
    cuando salen de la pantalla.
    ''',
    para_que='''
    Un arreglo de structs con un `viva` (lo que se llama una «pileta» de objetos) se usa para todo lo que aparece y
    desaparece muchas veces: balas, enemigos, explosiones, chispas, monedas. Es rápido y la memoria no crece nunca.
    ''',
    errores='''
    **Olvidarse del `break`.** Con una apretada se disparan todas las balas libres juntas, encimadas.

    **Mover las balas muertas.** Si se mueve sin mirar `viva`, las guardadas también suben y, al dispararlas, aparecen
    lejos.

    **Fuga de Texturas: no apagarlas.** Si la bala que sale de la pantalla sigue viva, después de cinco disparos el
    cargador queda vacío para siempre: las balas siguen «volando» afuera, donde nadie las ve.

    **`balas[i] = 0`.** Un struct no se pone en cero así: se cambia el campo, `balas[i].viva = false`.
    ''',
    misiones=[
        dict(titulo='Fuego',
             carta='Disparar | espacio: for i hasta BALAS · si !balas[i].viva: x = avion.x + 18, y = avion.y - 10, viva = true · break',
             escena='''
             Kira aprieta el espacio y el botón rojo del panel se enciende, pero del biplano no sale nada. —Hay cinco
             burbujas guardadas —dice {mentor}—. Al disparar, buscás una que esté libre y la soltás.
             ''',
             gheco='''
             Ya está el arreglo `balas` (cinco `struct Bala`, todas guardadas). Con el espacio, se busca la primera libre:
             ```c
             if (evento.type == SDL_EVENT_KEY_DOWN && evento.key.key == SDLK_SPACE) {
                 for (int i = 0; i < BALAS; i++) {
                     if (!balas[i].viva) {               /* ¿está guardada? */
                         balas[i].x = avion.x + 18;      /* en la punta del biplano */
                         balas[i].y = avion.y - 10;
                         balas[i].viva = true;           /* ¡a volar! */
                         break;                          /* una sola por apretada */
                     }
                 }
             }
             ```
             `balas[i].x` es el campo `x` de la bala número `i`. Las balas vivas ya se dibujan. El robot va a apretar el
             espacio.
             ''',
             desafio='Hacé que con el espacio salga una bala libre desde la punta del biplano.',
             pasos=['Buscá `/* acá: con el espacio, buscar una bala libre y dispararla desde el biplano */` (en los eventos).',
                    'Debajo, escribí el `if` del espacio con el `for` de la sugerencia.',
                    'Tocá **Jugar**, hacé clic en el juego y apretá el espacio. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 2', estado='buscar #ffff78',
             superarla='''
             Kira aprieta el espacio y en la punta del biplano aparece una burbuja de luz amarilla. Se queda ahí, flotando,
             esperando. —Ya salió —dice Arcadia—. Ahora tiene que volar.
             ''',
             imagen=['La pantalla de la máquina con el biplano amarillo y una burbuja de luz amarilla en la punta.',
                     'Kira aprieta un botón rojo grande del panel de la máquina; Arcadia señala la pantalla.',
                     'Gheco, sobre la máquina, se tapa las orejas esperando un estruendo.']),
        dict(titulo='Para arriba',
             carta='Volar | para cada bala viva: balas[i].y -= 500 * dt',
             escena='''
             Las burbujas salen del biplano y se quedan flotando, quietas, donde salieron. —Una burbuja de luz es rápida
             —dice {mentor}—. Mucho más que el avión.
             ''',
             gheco='''
             Ya está el `for` que pasa por las balas y el `if` que mira solo las vivas. Adentro, que suban:
             ```c
             balas[i].y -= 500 * dt;   /* 500 píxeles por segundo, hacia arriba */
             ```
             Solo las vivas se mueven: las guardadas esperan en el cargador. El robot va a disparar y esperar medio
             segundo.
             ''',
             desafio='Hacé que las balas vivas suban 500 píxeles por segundo.',
             pasos=['Buscá `/* acá: la bala sube rápido */` (adentro del `if (balas[i].viva)`).',
                    'Debajo, escribí la línea de la sugerencia.',
                    'Tocá **Jugar** y dispará. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 30', estado='buscar #ffff78',
             superarla='''
             *¡Fiuuu!* La burbuja sale disparada hacia arriba y se pierde en el cielo. Kira dispara otra, y otra. Gheco
             trata de seguirlas con la vista y se marea.
             ''',
             imagen=['La pantalla de la máquina con el biplano amarillo disparando burbujas de luz que suben rápido, con estelas.',
                     'Kira dispara con el botón rojo, entusiasmada; Arcadia sonríe.',
                     'Gheco sigue las burbujas con la vista y se marea, sentado arriba de la máquina.']),
        dict(titulo='El cargador no se vacía',
             carta='Reusar | si balas[i].y < -10: balas[i].viva = false (vuelve a estar libre)',
             criatura='fuga_texturas',
             escena='''
             Kira dispara cinco veces… y la sexta, nada. Ni la séptima. Las cinco burbujas se fueron por arriba, pero la
             máquina cree que siguen volando. La Fuga de Texturas se infla, feliz, detrás del panel.
             ''',
             gheco='''
             Cuando una bala sale por arriba, hay que **guardarla** otra vez, así queda libre para otro disparo. Adentro del
             mismo `if`, después de moverla:
             ```c
             if (balas[i].y < -10) {     /* la bala mide 10: ya salió entera */
                 balas[i].viva = false;   /* vuelve al cargador */
             }
             ```
             El robot va a disparar cinco veces, esperar a que salgan, y disparar una sexta.
             ''',
             desafio='Hacé que la bala que sale por arriba se apague y quede libre para otro disparo.',
             pasos=['Buscá `/* acá: si salió por arriba, se apaga y queda libre para otro disparo */`.',
                    'Debajo, escribí el `if` de la sugerencia.',
                    'Tocá **Jugar** y dispará muchas veces. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 60\ntecla Espacio\ncuadros 60\ntecla Espacio\ncuadros 60\ntecla Espacio\ncuadros 60\ntecla Espacio\ncuadros 60\ntecla Espacio\ncuadros 2',
             estado='buscar #ffff78',
             superarla='''
             Las burbujas que salen por arriba vuelven al cargador, y Kira puede disparar todo lo que quiera. La Fuga de
             Texturas se desinfla con un silbido y se va volando por la puerta del hangar.
             ''',
             imagen=['La pantalla de la máquina con el biplano disparando una fila larga de burbujas de luz que nunca se acaban.',
                     'Una criatura como una nube que se desinfla con un silbido sale volando por la puerta del hangar.',
                     'Kira dispara sin parar; Arcadia aplaude; Gheco persigue la nube desinflada.']),
        dict(titulo='El cargador',
             carta='Contar libres | for i hasta BALAS · si !balas[i].viva: un cuadradito naranja en (10 + i * 12, 456)',
             escena='''
             —Los pilotos de la máquina sabían cuántas burbujas les quedaban —dice {mentor}—. Abajo, en un costado,
             había una fila de lucecitas: una por cada burbuja guardada.
             ''',
             gheco='''
             Un cuadradito naranja por cada bala **libre**, abajo a la izquierda:
             ```c
             SDL_SetRenderDrawColor(lapiz, 255, 160, 60, 255);
             for (int i = 0; i < BALAS; i++) {
                 if (!balas[i].viva) {                           /* guardada: se muestra */
                     SDL_FRect libre = { 10 + i * 12, 456, 8, 14 };
                     SDL_RenderFillRect(lapiz, &libre);
                 }
             }
             ```
             `10 + i * 12`: cada lucecita, 12 píxeles más a la derecha que la anterior. Al disparar se apaga una; cuando la
             bala sale de la pantalla, vuelve. El robot va a disparar una vez.
             ''',
             desafio='Mostrá abajo a la izquierda un cuadradito naranja por cada bala libre.',
             pasos=['Buscá `/* acá: el cargador: un cuadradito naranja abajo por cada bala libre */`.',
                    'Debajo, escribí el color y el `for` de la sugerencia.',
                    'Tocá **Jugar** y dispará: mirá cómo se apagan y vuelven. Después, **Comprobar**.'],
             eventos='tecla Espacio\ncuadros 2', estado='buscar #ffa03c',
             superarla='''
             Abajo a la izquierda aparecen cinco lucecitas naranjas. Kira dispara dos: quedan tres. Las burbujas salen por
             arriba y, *plin, plin*, las lucecitas vuelven. —Cinco que van y vuelven —dice Kira—. Nunca se terminan.
             ''',
             imagen=['La pantalla de la máquina con el biplano y, abajo a la izquierda, una fila de lucecitas naranjas.',
                     'Kira cuenta las lucecitas con el dedo; Arcadia asiente.',
                     'Gheco sostiene una lucecita naranja de verdad, como una linterna, arriba de la máquina.']),
    ],
)
