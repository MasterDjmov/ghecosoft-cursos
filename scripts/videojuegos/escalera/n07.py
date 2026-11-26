import motor
import n06


def _plantilla():
    code = motor.full(n06.PLANTILLA)
    cambios = [
        ('    bool contraLaMaquina = true;\n',
         '    bool contraLaMaquina = true;\n    //@ n3+\n    bool dificil = false;\n    //@ end\n'),
        ('                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;\n',
         '                if (estado == MENU && tecla == SDLK_2) contraLaMaquina = false;\n'
         '                //@ n3: acá: en el menú, F para fácil y D para difícil\n'
         '                if (estado == MENU && tecla == SDLK_F) dificil = false;\n'
         '                if (estado == MENU && tecla == SDLK_D) dificil = true;\n'
         '                //@ end\n'),
        ('                if (distancia < -10) der.y -= 240 * dt;\n                if (distancia > 10) der.y += 240 * dt;\n',
         '                //@ n3: acá: la rapidez de base según la dificultad: 280 si es difícil, 200 si es fácil\n'
         '                float base = dificil ? 280 : 200;\n'
         '                //@ else\n'
         '                float base = 200;\n'
         '                //@ end\n'
         '                //@ n1: acá: cuantos más puntos le hacés, más rápido se mueve (40 más por punto)\n'
         '                float rapidez = base + 40 * puntosIzq;\n'
         '                //@ else\n'
         '                float rapidez = 240;\n'
         '                //@ end\n'
         '                if (distancia < -10) der.y -= rapidez * dt;\n'
         '                if (distancia > 10) der.y += rapidez * dt;\n'),
        ('                vy = 0;\n                espera = 1;\n',
         '                //@ n2: acá: el saque sale con una inclinación al azar, entre -120 y 120\n'
         '                vy = SDL_rand(241) - 120;\n'
         '                //@ else\n'
         '                vy = 0;\n'
         '                //@ end\n'
         '                espera = 1;\n'),
        ('            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");\n',
         '            SDL_RenderDebugText(lapiz, 228, 320, "1 O 2 PARA CAMBIAR");\n'
         '            //@ n3\n'
         '            SDL_RenderDebugText(lapiz, 236, 340, dificil ? "DIFICIL (F O D)" : "FACIL (F O D)");\n'
         '            //@ end\n'),
        ('            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");\n',
         '            //@ n4: acá: contra la máquina, el cartel del campeón, centrado\n'
         '            const char *cartel = puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2";\n'
         '            if (contraLaMaquina) {\n'
         '                cartel = puntosIzq == 5 ? "LE GANASTE AL CAMPEON" : "EL CAMPEON SIGUE INVICTO";\n'
         '            }\n'
         '            SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);\n'
         '            //@ else\n'
         '            SDL_RenderDebugText(lapiz, 252, 220, puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2");\n'
         '            //@ end\n'),
        ('SDL_CreateWindowAndRenderer("La Cancha de las Paletas"', 'SDL_CreateWindowAndRenderer("El Campeon Invicto"'),
        ('    SDL_FRect der = { 608, 170, 12, 80 };\n', '    SDL_FRect der = { 608, 20, 12, 80 };    /* el Campeón arranca arriba */\n'),
    ]
    for old, new in cambios:
        assert code.count(old) == 1, old
        code = code.replace(old, new)
    return code


PLANTILLA = _plantilla()

NODO = dict(
    codigo='R02-N07', titulo='Jefe: El Campeón Invicto', tipo='jefe', criatura='glitch', padre='R02-N06',
    insignia='Sello de la Cancha de las Paletas',
    insignia_descripcion='Despertaste al Campeón Invicto: un Pong entero, con menú, dos jugadores o contra la máquina, aceleración, sonido, pausa y un fin con revancha.',
    temas='juegos.ia', usa='juegos.estados, juegos.colisiones, juegos.sonido, prog.matematica-azar',
    plantilla=PLANTILLA,
    cronica='''
    Cuando los chicos se van, {mentor} camina hasta el fondo del salón y saca la lona de la máquina más vieja.
    Es enorme, de madera oscura, con dos paletas gastadas y una placa de bronce sin letras. —El **Campeón
    Invicto** —dice—. El Vidriero le enseñó a jugar solo, y nadie le ganó nunca. Ni yo. Cuando él se fue, se
    apagó.

    La máquina tose, parpadea y se enciende a medias: la paleta de la máquina tiembla, el saque sale siempre
    igual, no sabe si jugar fácil o difícil. Un glitch viejo le corre por la pantalla. —Le falta lo último que le
    enseñaste a la Cancha —dice {mentor}—. Y algo más: un campeón de verdad se pone serio cuando le hacés
    puntos.
    ''',
    objetivos='''
    Terminar el Pong completo, con el Campeón Invicto del otro lado: una máquina que se apura cuantos más puntos le
    hacés, un saque con una inclinación al azar, la dificultad para elegir en el menú y un cartel del campeón al
    terminar.
    ''',
    antes='''
    Toda la rama R02. De R01: el azar con `SDL_rand` y centrar un texto (N07 y N10).
    ''',
    explicacion='''
    #### Un rival que se pone serio
    La máquina ya sabe jugar (R02-N04). Para que sea un campeón, su **rapidez** cambia con el partido: arranca en
    una base y suma 40 por cada punto que le hiciste.
    ```c
    float rapidez = base + 40 * puntosIzq;
    ```
    Con 0 puntos va a 200; con 3, a 320. Cuanto mejor jugás, más difícil se pone.

    #### El saque al azar
    Si el saque sale siempre derecho, se aprende de memoria. `SDL_rand(241)` da un número entero entre 0 y 240 (lo
    usaste en R01-N10 para las gemas). Restándole 120 queda entre -120 y 120: a veces sube, a veces baja, a veces
    casi derecho.

    #### Fácil o difícil
    Una variable `bool dificil` que se elige en el menú con dos teclas (F y D). La rapidez de base sale de ahí:
    `dificil ? 280 : 200` («si es difícil, 280; si no, 200»).

    #### El cartel del final, centrado
    Las letras miden 8 de ancho. Un texto de `n` letras mide `n * 8`; para centrarlo en una pantalla de 640, se
    empieza en `320 - n * 4`. `SDL_strlen(cartel)` cuenta las letras.

    #### El juego completo
    Juntando toda la rama: la cancha y la red, dos jugadores o contra la máquina, el rebote y la aceleración con
    tope, el ángulo según dónde pega, el marcador grande, el respiro antes del saque, el menú, el fin a 5, la
    revancha, el sonido, la pausa y el silencio.
    ''',
    para_que='''
    Un rival que se adapta a cómo jugás es la base de la dificultad de casi todos los juegos. Y el Pong completo es
    tu primer juego entero con todo lo que tiene un juego de verdad: lo vas a poder bajar y jugar en tu compu.
    ''',
    errores='''
    **Sumar la rapidez en cada cuadro.** `rapidez += 40;` dentro del bucle la hace crecer sin parar. Se calcula
    de nuevo en cada cuadro a partir de los puntos: `base + 40 * puntosIzq`.

    **`SDL_rand(120)` para los dos lados.** Da entre 0 y 119: el saque siempre baja. Para que también suba, se
    resta la mitad: `SDL_rand(241) - 120`.

    **Centrar sin restar.** `320 + n * 4` corre el texto a la derecha; se empieza a la izquierda del centro.

    **Glitch: el saque que se repite.** Si el azar se pide una sola vez al principio y se guarda, todos los saques
    salen iguales. Se pide de nuevo en cada saque.
    ''',
    misiones=[
        dict(titulo='El campeón se pone serio',
             carta='Rapidez que crece | rapidez = base + 40 * puntosIzq',
             escena='''
             La paleta del Campeón se mueve siempre igual, sin ganas. —Un campeón se pone serio cuando le hacés
             puntos —dice {mentor}—. Cada punto tuyo, un poco más rápido.
             ''',
             gheco='''
             La paleta de la máquina se mueve `rapidez * dt` por cuadro, y hoy la rapidez es siempre 240. Ya hay
             una variable `base` que vale 200: la rapidez del principio.

             Para que suba 40 por cada punto que le hace el jugador 1:
             ```c
             float rapidez = base + 40 * puntosIzq;
             ```
             Con 0 puntos, 200; con 1, 240; con 2, 280… Se calcula de nuevo en cada cuadro, así siempre va con el
             marcador.
             ''',
             desafio='Hacé que la rapidez de la máquina sea la base (200) más 40 por cada punto que le hizo el jugador 1.',
             pasos=['Buscá el comentario `/* acá: cuantos más puntos le hacés, más rápido se mueve (40 más por punto) */`.',
                    'Cambiá la línea de abajo, `float rapidez = 240;`, por `float rapidez = base + 40 * puntosIzq;`.',
                    'Tocá **Jugar**, hacele un punto al Campeón y mirá cómo se apura. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla Espacio\ncuadros 30', estado='buscar #ff3ca0',
             superarla='''
             Le hacés un punto y la paleta del Campeón se tensa; otro, y ya se mueve como un rayo. {mentor} se
             muerde los labios. —Así era. Exactamente así.
             ''',
             imagen=['La máquina del Campeón Invicto: enorme, de madera oscura, con una placa de bronce lisa; en la pantalla, la paleta rosa con líneas de velocidad.',
                     'Kira, concentrada, juega contra la máquina; Arcadia mira detrás de ella, nerviosa.',
                     'Gheco, sobre la máquina, se agarra de la placa de bronce.']),
        dict(titulo='El saque al azar',
             carta='Azar | vy = SDL_rand(241) - 120 en cada saque',
             escena='''
             Kira descubre el truco: el saque del Campeón sale siempre derecho, al mismo lugar. Pone la paleta ahí y
             gana el punto. —Así no vale —se ríe {mentor}—. Un saque tiene que sorprender.
             ''',
             gheco='''
             Después de cada punto la pelota sale con `vy = 0`: siempre derecho. Con el azar (lo usaste en R01-N10
             para las gemas) sale distinto cada vez:
             - `SDL_rand(241)` da un número entero entre 0 y 240;
             - restándole 120, queda entre -120 (para arriba) y 120 (para abajo).
             ```c
             vy = SDL_rand(241) - 120;
             ```
             El robot va a jugar de a dos y va a dejar pasar una pelota para ver el saque.
             ''',
             desafio='Hacé que en cada saque la pelota salga con una inclinación al azar, entre -120 y 120.',
             pasos=['Buscá el comentario `/* acá: el saque sale con una inclinación al azar, entre -120 y 120 */` (adentro del `if (punto)`).',
                    'Cambiá la línea de abajo, `vy = 0;`, por `vy = SDL_rand(241) - 120;`.',
                    'Tocá **Jugar** y mirá varios saques. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla 2\ntecla Espacio\napretar Arriba\ncuadros 40\nsoltar Arriba\ncuadros 110', estado='buscar #ffdc00',
             superarla='''
             El saque sale para arriba, después para abajo, después casi derecho. Kira ya no sabe dónde poner la
             paleta. —Ahora sí —dice {mentor}—. Ahora es un campeón.
             ''',
             imagen=['La pantalla del Campeón con tres recorridos posibles de la pelota saliendo del centro: uno hacia arriba, uno derecho y uno hacia abajo, como abanico.',
                     'Kira duda con la paleta en el aire; Arcadia se ríe.',
                     'Gheco hace un gesto de «no sé» con los brazos.']),
        dict(titulo='Fácil o difícil',
             carta='Dificultad | en el menú F o D: dificil = false o true · base = dificil ? 280 : 200',
             escena='''
             Al día siguiente vuelven los chicos del barrio, y los más chiquitos pierden 5 a 0 contra el Campeón.
             —Que se pueda elegir —pide Kira—. Fácil para empezar, difícil para los que se animan.
             ''',
             gheco='''
             La variable `dificil` ya existe (arranca en `false`). Faltan tres cosas:
             1. En el menú, con la **F**, fácil; con la **D**, difícil (con los otros eventos del menú):
             ```c
             if (estado == MENU && tecla == SDLK_F) dificil = false;
             if (estado == MENU && tecla == SDLK_D) dificil = true;
             ```
             2. La base sale de ahí: `float base = dificil ? 280 : 200;` («si es difícil, 280; si no, 200»).
             3. En el menú ya se ve qué dificultad está elegida.

             El robot va a apretar la D en el menú y después jugar.
             ''',
             desafio='Hacé que en el menú se elija la dificultad (F fácil, D difícil) y que en difícil la máquina arranque a 280 en lugar de 200.',
             pasos=['Buscá `/* acá: en el menú, F para fácil y D para difícil */` y escribí los dos `if` de la sugerencia.',
                    'Buscá `/* acá: la rapidez de base según la dificultad: 280 si es difícil, 200 si es fácil */`.',
                    'Cambiá la línea de abajo, `float base = 200;`, por `float base = dificil ? 280 : 200;`.',
                    'Tocá **Jugar**, probá las dos dificultades y mirá el menú. Después, **Comprobar**.'],
             eventos='cuadros 2\ntecla D\ncuadros 2\ntecla Espacio\ncuadros 40', estado='buscar #ff3ca0',
             superarla='''
             Los chiquitos juegan en fácil y le hacen un punto al Campeón: festejan como si fuera una final. Los
             grandes eligen difícil y se quedan callados, concentrados.
             ''',
             imagen=['Chicos del barrio, con abrigos cerrados, frente a la máquina del Campeón: los más chicos festejan un punto.',
                     'En la pantalla, el menú con un renglón nuevo resaltado (sin texto legible).',
                     'Kira explica algo a un chico chiquito; Gheco, a su lado, le levanta el pulgar.']),
        dict(titulo='El cartel del campeón', criatura='glitch', recompensa='xp 20, monedas 5', item='Paleta del Campeón',
             carta='El final | contra la máquina: «LE GANASTE AL CAMPEON» o «EL CAMPEON SIGUE INVICTO», centrado',
             escena='''
             Llega la hora: Kira contra el Campeón Invicto, en difícil, a 5 puntos. Todo el barrio mira. Pero al
             terminar, la máquina dice lo mismo que una Cancha cualquiera: «gana el jugador». —Un campeón se despide
             con su propio cartel —dice {mentor}.
             ''',
             gheco='''
             Cuando se juega **contra la máquina**, el final tiene que hablar del Campeón:
             ```c
             const char *cartel = puntosIzq == 5 ? "GANA EL JUGADOR 1" : "GANA EL JUGADOR 2";
             if (contraLaMaquina) {
                 cartel = puntosIzq == 5 ? "LE GANASTE AL CAMPEON" : "EL CAMPEON SIGUE INVICTO";
             }
             SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);
             ```
             - `const char *cartel` guarda un texto; se elige primero el de dos jugadores y, si es contra la
               máquina, se cambia.
             - Para **centrarlo**: cada letra mide 8, así que el texto mide `SDL_strlen(cartel) * 8`; empieza la
               mitad antes del centro: `320 - SDL_strlen(cartel) * 4.0f`. (Las letras van sin tilde: la letra
               chiquita de SDL no las tiene.)

             El robot va a jugar contra la máquina hasta el final.
             ''',
             desafio='Hacé que al terminar contra la máquina aparezca, centrado, «LE GANASTE AL CAMPEON» o «EL CAMPEON SIGUE INVICTO».',
             pasos=['Buscá el comentario `/* acá: contra la máquina, el cartel del campeón, centrado */` y borrá la línea de abajo.',
                    'Escribí `const char *cartel = …` con los dos textos de dos jugadores.',
                    'Escribí el `if (contraLaMaquina) { … }` que cambia el cartel.',
                    'Dibujalo centrado con `SDL_RenderDebugText(lapiz, 320 - SDL_strlen(cartel) * 4.0f, 220, cartel);`. Tocá **Jugar** y después **Comprobar**.'],
             eventos='cuadros 2\ntecla Espacio\ncuadros 3000', estado='textos',
             superarla='''
             Cinco a cuatro. La pantalla del Campeón se queda quieta y, por primera vez en treinta años, dice **LE
             GANASTE AL CAMPEON**. El salón entero grita. La máquina zumba, la placa de bronce se calienta y en la
             pantalla aparece un dibujo nuevo: **otro pedazo del mapa del Vidriero**. Este muestra un muro de
             ladrillos de colores, altísimo.

             {mentor} se seca los ojos con la manga. Del costado de la máquina se abre una tapita y cae una paleta
             vieja, de madera, gastada en la punta: la **Paleta del Campeón**. —Te la ganaste —dice—. El Muro de
             Ladrillos nos espera.
             ''',
             imagen=['La máquina del Campeón Invicto encendida a pleno, con luces en los costados; en la pantalla, un pedazo de mapa antiguo con un muro altísimo de ladrillos de colores.',
                     'Una paleta vieja de madera, gastada en la punta, cae de una tapita al costado de la máquina.',
                     'Kira con los brazos en alto; Arcadia se seca los ojos con la manga; Gheco abraza la placa de bronce; detrás, los chicos del barrio festejan.']),
    ],
)
