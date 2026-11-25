# Videojuegos (D126) — propuesta para revisar

Pedido del docente (2026-11-25): un curso de **videojuegos** que arranque con **SDL3** y siga con SFML, Phaser y algo de
OpenGL. Es pedagógico ante todo: que el alumno aprenda a hacer juegos de verdad, de a poco, con juegos simples y
demostrables. En la plataforma el alumno **ve** el juego, lo **edita sí o sí** y lo **juega en la página**, sin bajar
IDEs; como opción, lo **baja y lo corre en su compu** (Linux y Windows), para que le quede.

Nada de esto está programado. Este documento es para revisar y corregir antes de arrancar.

## 1. Decisiones (charla con el docente, 2026-11-25)

| Pregunta | Decisión |
|---|---|
| ¿Curso propio o anexo? | **Curso propio**, «Videojuegos», que se apoya en otro: pide C. SDL3 es el primero; SFML, Phaser y OpenGL vienen después como alas del mismo salón (§ 3). |
| ¿Lenguaje? | **C** para SDL3: SDL es una biblioteca de C, se lee más simple y continúa el curso de C. SFML (C++) llega después. |
| ¿Requisito? | Haber completado **C hasta el jefe de la rama R02** («Pasillos numerados»: arrays, strings, structs, punteros, punteros y structs, arrays de structs). Si no, el curso lo dice claro (§ 6). |
| ¿Dónde corre? | **En el navegador**, editable (§ 4). Y el mismo archivo, sin cambios, compila con SDL3 real en la compu (§ 5). |
| ¿Historia? | Sí, unida al universo: **Kira, mejorada**, en **el Salón Arcade del Vidriero**, con **Arcadia** de mentora (§ 2). |
| ¿Cómo se ve Kira? | Diseño nuevo, «versión videojuegos»: el del proyecto de Stitch **Kira Game Designer Concept** (https://stitch.google.com/projects/4092585402994005468): mono oscuro con líneas cian, visor, auricular, cinturón de herramientas y un brazal-control del que sale un escudo de luz hexagonal. Ropa cerrada (regla de siempre). Falta su hoja de 8 ángulos. |

## 2. La historia: el Salón Arcade del Vidriero

- **Kira, Forjadora de Mundos.** La protagonista de las Forjas (C) ya no forja espadas: forja mundos. Llegó al Mundo
  del Código por un portal; ahora aprende a construir los suyos. Es la misma Kira, mejorada (como Nova en Ensamblador
  32/64): por eso el curso pide C.
- **El lugar.** Un **salón de máquinas arcade abandonado** que construyó **el Vidriero**, el que hizo el portal-vitral y
  desapareció. Cada máquina (Pong, Arkanoid, Tetris, naves, Pac-Man, plataformas) está apagada o rota.
- **La mentora: Arcadia**, la maquinista del salón. Aprendiz de Maese Ferrum, como Tesla y Tesela, pero eligió las
  máquinas que juegan. Overol cerrado lleno de fichas y destornilladores; conoce cada máquina por su ruido.
  Su frase (propuesta): *«Un juego es un bucle que nunca deja de escuchar.»*
- **El hilo con el misterio.** Cada juego que Kira arma **revive una máquina**, y cada máquina revivida muestra en su
  pantalla de *Game Over* un pedazo del mapa del Vidriero. El último juego revela para qué construyó el portal.
- **La moneda: créditos** («INSERT COIN»). Se ganan con las micro-misiones que vienen de misiones y abren los nodos,
  como en los demás cursos.
- **El bestiario de los glitches** (los errores típicos de un juego):

| Criatura | Qué error representa |
|---|---|
| **Glitch** | un sprite que aparece corrido o parpadea (dibujar antes de limpiar, coordenadas mal) |
| **Fantasma del Fotograma** | el juego va rápido en una compu y lento en otra (moverse sin *delta time*) |
| **Atraviesaparedes** | la colisión mal calculada: la pelota se mete en el ladrillo |
| **Bucle Eterno** | la ventana no responde (un bucle que no lee los eventos) |
| **Fuga de Texturas** | la memoria que crece porque se cargan texturas en cada cuadro y no se liberan |

- **Los jefes son los juegos clásicos:** el campeón invicto de Pong, la Torre que no para (Tetris), la Nave Nodriza
  (naves), los cuatro fantasmas (Pac-Man) y un robot maestro (plataformas).
- **Cameos que unen cursos:** **Nova** pasa por el salón (en Ensamblador 32/64 hace «Junta las gemas» con SDL desde
  ensamblador) y **Zed** reconoce las máquinas (en Java vio el Arcade Imperial sin botones: eran de acá).

Al sumarlo, recorrer [ALTA-DE-CURSOS-Y-PERSONAJES.md](ALTA-DE-CURSOS-Y-PERSONAJES.md) (Arcadia, Kira mejorada, las
criaturas, la moneda, el mundo, su temporada de inglés).

## 3. Las alas del salón (lo que viene después de SDL3)

| Ala | Lenguaje | Región que la abre | Héroe |
|---|---|---|---|
| **El salón principal: SDL3** | C | las Forjas | Kira |
| **El taller de SFML** | C++ | la Ciudadela | Bron, el mecánico de Tesla |
| **Los puestos de Phaser** | JavaScript | la Feria de las Luces | Nima |
| **El proyector de OpenGL** | C/C++ | el Mirador (el Gran Planisferio proyecta estrellas: OpenGL es proyectar en pantalla) | Rigel |

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

1. ¿El orden de la escalera de juegos está bien? ¿Sacar o sumar alguno (Snake, Space Invaders, Asteroids)?
2. ¿Los cameos de Nova y Zed, sí?
3. ¿La Clase 0 de prueba se puede hacer sin cumplir el requisito (§ 6)?
4. El nombre del curso: ¿«El Salón Arcade»? ¿«Videojuegos: el Salón Arcade del Vidriero»?
