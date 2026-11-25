# Videojuegos (D126) — propuesta para revisar

Pedido del docente (2026-11-25): un curso de **videojuegos** que arranque con **SDL3** y siga con SFML, Phaser y algo de
OpenGL. Es pedagógico ante todo: que el alumno aprenda a hacer juegos de verdad, de a poco, con juegos simples y
demostrables. En la plataforma el alumno **ve** el juego, lo **edita sí o sí** y lo **juega en la página**, sin bajar
IDEs; como opción, lo **baja y lo corre en su compu** (Linux y Windows), para que le quede.

Nada de esto está programado. Este documento es para revisar y corregir antes de arrancar.

## 1. Decisiones (charla con el docente, 2026-11-25)

| Pregunta | Decisión |
|---|---|
| ¿Curso propio o anexo? | **Curso propio**, «Videojuegos», que se apoya en otro: pide C. SDL3 es el primero; SFML, Phaser y OpenGL vienen después como barrios del mismo mundo (§ 3). |
| ¿Lenguaje? | **C** para SDL3: SDL es una biblioteca de C, se lee más simple y continúa el curso de C. SFML (C++) llega después. |
| ¿Requisito? | Haber completado **C hasta el jefe de la rama R02** («Pasillos numerados»: arrays, strings, structs, punteros, punteros y structs, arrays de structs). Si no, el curso lo dice claro (§ 6). |
| ¿Dónde corre? | **En el navegador**, editable (§ 4). Y el mismo archivo, sin cambios, compila con SDL3 real en la compu (§ 5). |
| ¿Historia? | Sí, unida al universo: **Kira, mejorada**, en **un mundo nuevo, una ciudad de los videojuegos** (§ 2; nombre provisorio Ciudad Arcadia), con **Arcadia** de mentora. |
| ¿Cómo se ve Kira? | Diseño nuevo, «versión videojuegos», del proyecto de Stitch **Kira Game Designer Concept** (https://stitch.google.com/projects/4092585402994005468, creado por el docente para las muestras). **Elegida la segunda imagen (2026-11-25):** mono oscuro con líneas cian, visor, auricular, cinturón de herramientas y un brazal con **un control de juego** del que sale un escudo de luz hexagonal. Ropa cerrada (regla de siempre). Falta su hoja de 8 ángulos. |
| ¿Cómo son los juegos? | **Cada juego claro y completo**: menú, partida, puntaje, vidas o niveles, fin del juego y volver a jugar. Nada a medias. |
| ¿Cameos? | Sí, siempre que sumen al curso: los temas compartidos aparecen en el universo de cursos (*Admin → Universo*, `cursos/temas.md`). |
| ¿Clase 0 sin requisito? | Sí, para que vean de lo que son capaces. Además, **imágenes de referencia** de cada juego (cómo se verá al terminar), para que sepan qué van a hacer y hasta dónde llega. |

## 2. La historia: la ciudad de los videojuegos (un mundo nuevo)

No es un salón: es **otra región del Mundo del Código**, una **ciudad** con su propio mapa, como los demás mundos. La
idea del docente (2026-11-25): algo como un gran centro de entretenimiento, con mucha luz y movimiento, pero en forma
de pueblo o ciudad. **Sin apuestas ni nada de casino** (los alumnos son chicos): es la ciudad de los videojuegos, con
calles de neón, máquinas en cada esquina y atracciones. Cada lugar del mapa es **un desarrollo**: un juego, o una
técnica (una montaña rusa, un cubo que gira en el cielo para OpenGL). El mapa también sirve para las expediciones del
juego, como en los demás cursos.

- **El lugar.** Una ciudad que construyó **el Vidriero**, el que hizo el portal-vitral y desapareció. Se apagó cuando
  él se fue: las máquinas y las atracciones están quietas, y cada una hay que programarla para que vuelva a andar.
  Nombre provisorio: **Ciudad Arcadia** (ver § 8).
- **Kira, Forjadora de Mundos.** La protagonista de las Forjas (C) ya no forja espadas: forja mundos. Llegó al Mundo
  del Código por un portal; ahora aprende a construir los suyos. Es la misma Kira, mejorada (como Nova en Ensamblador
  32/64): por eso el curso pide C.
- **La mentora: Arcadia**, la maquinista de la ciudad (la ciudad lleva su nombre porque es la única que se quedó a cuidarla). Aprendiz de Maese Ferrum, como Tesla y Tesela, pero eligió las
  máquinas que juegan. Overol cerrado lleno de fichas y destornilladores; conoce cada máquina por su ruido.
  Su frase (propuesta): *«Un juego es un bucle que nunca deja de escuchar.»*
- **El hilo con el misterio.** Cada atracción que Kira hace andar muestra, en su pantalla de *Game Over*, un pedazo
  del mapa del Vidriero. La última revela para qué construyó el portal.
- **La moneda: créditos** («INSERT COIN»). Se ganan con las micro-misiones que vienen de misiones y abren los nodos,
  como en los demás cursos.

### 2.1 El mapa: cada lugar es un desarrollo

| Lugar | Qué se aprende ahí |
|---|---|
| **La Boletería** (la entrada de la ciudad) | Clase 0: la ventana y el bucle del juego. Insertá un crédito. |
| **El Banco de Pruebas de Arcadia** | R01, lo básico: teclado, mouse, delta time, colisiones, joystick, texto, sprites, sonido |
| **La Cancha de las Paletas** | Pong |
| **El Muro de Ladrillos** | Arkanoid |
| **El Jardín de la Serpiente** | Snake (un guiño al Valle de Ofidia) |
| **La Torre que no para** | Tetris |
| **La Pista de los Biplanos** | naves tipo 1942 |
| **El Tren Fantasma** | Pac-Man (el laberinto y los cuatro fantasmas) |
| **La Montaña Rusa** | plataformas tipo Megaman: gravedad, salto, subir y caer |
| **El Castillo del Vidriero** (el centro de la ciudad) | el proyecto final y el último pedazo del mapa |
| **La Vuelta al Mundo** (llega de la Ciudadela) | el ala de **SFML** (C++), con Bron: engranajes que giran |
| **Los Puestos de la Kermés** (el borde que toca la Feria) | el ala de **Phaser** (JavaScript), con Nima |
| **El Cubo del Cielo** (flota sobre la ciudad) | el ala de **OpenGL**, con Rigel: un cubo que gira, luces y cámara |

### 2.2 El bestiario de los glitches (los errores típicos de un juego)

| Criatura | Qué error representa |
|---|---|
| **Glitch** | un sprite que aparece corrido o parpadea (dibujar antes de limpiar, coordenadas mal) |
| **Fantasma del Fotograma** | el juego va rápido en una compu y lento en otra (moverse sin *delta time*) |
| **Atraviesaparedes** | la colisión mal calculada: la pelota se mete en el ladrillo |
| **Bucle Eterno** | la ventana no responde (un bucle que no lee los eventos) |
| **Fuga de Texturas** | la memoria que crece porque se cargan texturas en cada cuadro y no se liberan |

- **Los jefes son los juegos clásicos:** el campeón invicto de Pong, la Torre que no para (Tetris), la Nave Nodriza
  (naves), los cuatro fantasmas (Pac-Man) y un robot maestro (plataformas).
- **Cameos que unen cursos** (y temas compartidos en el universo): **Nova** pasa por la ciudad (en Ensamblador 32/64
  hace «Junta las gemas» con SDL desde ensamblador) y **Zed** reconoce las máquinas (en Java vio el Arcade Imperial
  sin botones: eran de acá).

Al sumarlo, recorrer [ALTA-DE-CURSOS-Y-PERSONAJES.md](ALTA-DE-CURSOS-Y-PERSONAJES.md) (Arcadia, Kira mejorada, las
criaturas, la moneda, el mundo y su mapa, su temporada de inglés).

## 3. Los barrios que vienen después de SDL3

| Ala | Lenguaje | Región que la abre | Héroe |
|---|---|---|---|
| **La ciudad: SDL3** | C | las Forjas | Kira |
| **La Vuelta al Mundo: SFML** | C++ | la Ciudadela | Bron, el mecánico de Tesla |
| **Los Puestos de la Kermés: Phaser** | JavaScript | la Feria de las Luces | Nima |
| **El Cubo del Cielo: OpenGL** | C/C++ | el Mirador (el Gran Planisferio proyecta estrellas: OpenGL es proyectar en pantalla) | Rigel |

Cada ala es un curso (o una Senda) que pide el curso de su región. Primero se hace SDL3 entero.

## 4. El temario de SDL3: lo básico y la escalera de juegos

Cada juego suma algo nuevo; cada nodo, con sus micro-misiones (que se comprueban solas, § 4.2), su teoría corta y
muy explicada (regla de sencillez) y un juego que se juega al final.

**R00 · Clase 0 — La máquina que se enciende:** qué es SDL3, la ventana, el bucle del juego (leer eventos → actualizar
→ dibujar), cerrar bien.

**R01 · Lo básico (el banco de pruebas de Arcadia):**
1. Ventana y renderer; limpiar y presentar; colores.
2. Rectángulos y coordenadas (dónde está el 0,0).
3. Eventos y teclado (apretar contra mantener apretado).
4. El mouse.
5. Movimiento y *delta time* (el Fantasma del Fotograma).
6. Colisiones entre rectángulos (el Atraviesaparedes).
7. El joystick y el gamepad.
8. Texto en pantalla y puntaje.
9. Imágenes y sprites (texturas), y liberarlas (la Fuga de Texturas).
10. Sonido.
11. Jefe: «Junta las gemas» chico, con todo lo anterior.

**R02 en adelante · La escalera de juegos** (una rama por máquina; el orden se puede ajustar):

| Máquina | Lo nuevo que enseña |
|---|---|
| **Pong** | dos jugadores, rebote, puntaje, la pelota que acelera; una IA simple |
| **Arkanoid** | grilla de ladrillos (array de structs), rebote según dónde pega, vidas, niveles |
| **Snake** (opcional, corto) | la grilla, la cola como cola de datos, crecer |
| **Tetris** | matrices y rotación, el tablero, líneas completas, la caída que se acelera |
| **Naves (tipo 1942)** | disparos y enemigos en arrays, aparición por oleadas, el fondo que se mueve |
| **Pac-Man** | el laberinto como mapa, los fantasmas con reglas simples de persecución, estados |
| **Plataformas (tipo Megaman)** | gravedad, salto, el mapa de bloques, la cámara que sigue, enemigos con patrón |
| **Proyecto final** | un juego propio, o «El Guardián de las Gemas» de FullCursos |

**Cada juego, claro y completo:** menú, partida, puntaje, vidas o niveles, fin del juego y volver a jugar. Cada rama
arranca con una **imagen de referencia** del juego terminado (para saber qué se hace y hasta dónde llega) y termina con
el juego entero andando.

Material de partida: `FullCursos/06-SDL3` (13 capítulos en C), `07-SDL3-Cpp`, `08-ProyectoFinal` y el SDL2 desde
ensamblador de `28-Ensamblador-32-64` (parte 4). Los juegos de la escalera se escriben nuevos, sencillos y muy
explicados.

### 4.1 Cómo corre en el navegador

- El código del alumno se compila con el **Clang en WebAssembly que ya usa C** (D98), en su navegador.
- Las funciones de SDL3 que usa el curso (`SDL_Init`, `SDL_CreateWindow`, `SDL_CreateRenderer`, `SDL_PollEvent`,
  `SDL_SetRenderDrawColor`, `SDL_RenderFillRect`, `SDL_RenderPresent`, `SDL_GetTicks`, texturas, texto, sonido,
  `SDL_Gamepad`…) las resuelve un **«SDL3 de la plataforma»** en JavaScript, que dibuja en un lienzo de la página.
  Con los mismos nombres y la misma forma de uso que SDL3 real.
- El joystick anda en la web: el navegador lee joysticks y gamepads (USB o de consola).
- Corre en una caja como la de JavaScript: sin red, sin ver la sesión, con un tope para el Bucle Eterno.
- **Por qué no Emscripten:** es el que convierte un juego SDL en página, pero corre en una compu (pesa unos 2 GB, con
  Python y Node); no entra en el navegador del alumno, y en el servidor no se compila código de alumnos.
- Lo que el SDL de la plataforma no tenga, el curso no lo usa. La lista exacta sale del temario.

### 4.2 Micro-misiones que se comprueban solas

El juego corre unos cuadros con **teclas simuladas** y se revisa el resultado (dónde quedó la paleta, cuántos puntos
hay, si la pelota rebotó). Ejemplos: «que la paleta no salga de la pantalla», «sumá un punto al romper un ladrillo».
El docente corrige solo los proyectos.

### 4.3 Assets (gráficos y sonidos)

Referencias que pasó el docente (2026-11-25). **Antes de usar cada uno, revisar su licencia** (que permita usarlo en
un curso, y si pide créditos) y anotarlo en una página de créditos del curso:

- Sonidos: Freesound, por ejemplo https://freesound.org/people/Victor_Natas/sounds/766921/ (cada sonido tiene su
  propia licencia: CC0 o con atribución).
- Personajes y escenarios: KayKit de Kay Lousberg (https://kaylousberg.itch.io/) y Pixel Adventure de Pixel Frog
  (https://pixelfrog-assets.itch.io/pixel-adventure-1).
- Paleta: Resurrect 64 (https://lospec.com/palette-list/resurrect-64), para que todos los juegos de la ciudad compartan
  colores.
- Sprites generados: SpriteCook (https://www.spritecook.ai/), revisando sus términos de uso.

Los assets van a la plataforma (para la web) y adentro del .zip para bajar.

## 5. Bajarlo y correrlo en la compu

- Botón **Bajar** (como en Mis prácticas, D124): un .zip con el juego, SDL3 y un lanzador para **Linux** y otro para
  **Windows** (como el Ejecutor de Java, D85). Doble clic: compila y abre la ventana.
- **El mismo archivo compila igual** en la web y en la compu: esa es la prueba de que el SDL de la plataforma está bien.
- Instrucciones siempre para los dos sistemas (regla de siempre).

## 6. Requisitos entre cursos (sirve para todos)

- Un curso puede **exigir haber completado un nodo de otro curso**.
- Si no lo cumple, el curso lo dice claro: «Para avanzar se requiere **«Arrays de structs»** (el jefe de la rama R02)
  del curso **Las Forjas de Hierro (C)**», con un botón para ir ahí.
- Usos: **Videojuegos** pide C hasta R02-N07; **Ensamblador 32/64** pide el curso de **8086**.
- Falta decidir: ¿bloquea solo inscribirse, o también la Clase 0 de prueba? (propuesta: la Clase 0 se puede probar
  igual, y el cartel aparece al querer inscribirse o abrir el primer nodo).

## 7. Fases (se frena al final de cada una)

1. **Prototipo:** Pong editable y jugable en la página, con teclado y joystick, y el mismo archivo compilando con SDL3
   real en Linux. Si anda, el resto es posible.
2. **Requisitos entre cursos** (§ 6), con Videojuegos y Ensamblador 32/64.
3. **El SDL3 de la plataforma completo** para R00 y R01, y la prueba de que cada ejemplo da lo mismo en la web y en la
   compu.
4. **El curso:** historia, Clase 0 y R01 con micro-misiones; Kira mejorada (hoja de 8 ángulos), Arcadia, las criaturas,
   escenas.
5. **La escalera de juegos**, una máquina por vez.
6. **Bajar y correr en la compu** (el .zip con lanzadores).
7. Después: las alas de SFML, Phaser y OpenGL.

## 8. Para decidir

Respondido el 2026-11-25: la escalera está bien (cada juego claro y completo); los cameos, sí; la Clase 0 se prueba
sin el requisito, con imágenes de referencia; y en vez de un salón, **un mundo nuevo con su mapa** (§ 2).

Después (2026-11-25): el mundo es **una ciudad con mapa** (como un gran centro de entretenimiento, sin apuestas), no un
parque ni un salón.

1. **El nombre de la ciudad.** Propuestas: **Ciudad Arcadia**, **Neón**, **Pixelia**, **Villa Crédito**. ¿Alguna, u otra?
2. **El nombre del curso.** Por ejemplo «Videojuegos: Ciudad Arcadia».
3. ¿Los lugares del mapa (§ 2.1) cuadran? ¿Cambiarías alguno?
