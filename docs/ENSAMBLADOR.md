# Curso de Ensamblador 8086 (D110)

Curso nuevo pedido el 2026-10-18 a partir del material de
`/home/djmov/Programas/Cursos/FullCursos/26-Ensamblador-8086/` (17 lecciones, solo lectura).

**Estado (2026-10-19):** hechos el emulador y el tablero (los 82 programas del material dan la salida de
referencia), el lenguaje autocomprobado con `#### Estado esperado`, las consultas desde micro-misiones para
todos los cursos con la solución al lado, la herramienta libre *Herramientas → Gólem 8086*, la historia de Nova,
**los tres primeros nodos** (Clase 0, La voz del Gólem, Los cajones con nombre: 17 micro-misiones) y todas sus
imágenes en Stitch (Nova, Axón, logo, moneda, fondo, 6 aspectos y 17 escenas). Sigue: el resto del temario
(§ 5), la tienda y las expediciones de Nova, la enciclopedia y la temporada de inglés (lista de ALTA).

## 1. Decisiones tomadas (2026-10-18)

| Tema | Decisión |
|---|---|
| Ejecución | **Ensamblador y emulador 8086 propios**, en JavaScript, en el navegador del alumno: un intérprete que corre por tandas sin trabar la página (no hace falta Web Worker: no ejecuta JavaScript ajeno). El fork `vgath-8086` solo fue referencia visual: no tiene licencia, así que no se copia código. |
| Sintaxis | **MASM, la de la cursada** (`.model small`, `.stack`, `.data`, `.code`, `@data`, `proc`/`endp`, `end main`): lo que el alumno escribe acá corre igual en emu8086. |
| Corrección | **Ninguna**: el curso se completa solo con **micro-misiones** que se comprueban solas (como el de inglés, `Language::isSelfChecked`). Sin prácticas ni entregas. |
| Precio | **Con abono**, como todos los cursos. |
| Protagonista | **Nova**, la chispa del Gólem (§ 6, opción A). Prepara la idea de los nanobots. Kira queda en C y aparece de visita. |
| Moneda | **Chispas** (en el diccionario). Como en inglés, un curso que se comprueba solo no paga monedas (lo del navegador se puede trampear): los nodos se abren gratis al completar el anterior. |
| Herramienta libre | *Herramientas → Gólem 8086*: el tablero suelto, con el abono vigente de un curso de Ensamblador (`CoursePolicy::useAsmTool`). |
| Consultas | El alumno puede **escribirle al docente desde cada micro-misión** (hoy solo se puede desde una práctica). El docente ve el código del alumno **junto a la solución**, como cuando corrige (§ 7). |
| Pedagogía | Cada idea, con su **puente a los otros cursos**: «`cmp` + `jg` es el `if (a > b)` de C», «`loop` es el `for`», «`call`/`ret` es llamar a una función». El objetivo no es ser experto en ensamblador, sino reconocer después qué hay debajo de un `if`, un `for` o una función. |

## 2. La pantalla del alumno (el «tablero del Gólem»)

Inspirada en la captura del fork, pero con la estética del juego. Se abre en cada micro-misión de este curso,
en lugar del editor con consola simple:

```
┌ Editor (CodeMirror, resaltado 8086) ───────┐┌ Palancas (registros) ─────────────────────┐
│ .model small                               ││ AX 1234  BX 00FF  CX 1234  DX FF00        │
│ .data                                      ││ SI 0000  DI 0000  BP 0000  SP 0100        │
│   pociones db 3                            ││ CS ...   DS ...   SS ...   IP 0012        │
│ .code                                      │├ Interruptores (banderas) ─────────────────┤
│ main proc                                  ││ ZF 1  SF 0  CF 0  OF 0  (+ DF IF TF AF PF) │
│ ▶  mov ax, @data       ← línea actual      │├ Pantalla del Gólem (consola 80×25) ───────┤
│    ...                                     ││ Heroina: Kira                              │
└────────────────────────────────────────────┘├ Cajones (memoria) │ Torre de platos (pila)┤
 [▶ Ejecutar] [⏭ Un paso] [⏹ Parar] [↺ Reiniciar]  │ 0200: FF 00 00 ...  │ 0100: 0005          │
                                                 └───────────────────────────────────────────┘
```

- **Paso a paso:** cada paso marca la línea, y lo que cambió se ilumina en amarillo (registro, bandera, cajón),
  como en el fork. Es el «pergamino de la maldición» de la historia: ver qué hace cada orden.
- **Nombres del juego con el nombre real al lado:** «Palancas (registros)», «Interruptores (banderas)»,
  «Cajones (memoria)», «Torre de platos (pila)», «Ojo / pantalla». Se aprende el término técnico sin perder
  la metáfora.
- **Variables con nombre:** la memoria muestra al lado de cada dirección la variable que vive ahí
  (`pociones`, `mochila+1`…), como el botón *vars* de emu8086.
- **En el celular:** editor arriba y el tablero en pestañas (Palancas · Interruptores · Pantalla · Cajones · Pila).
- **Errores del ensamblador en español**, con la criatura del bestiario de `GUION.md` (Slime para la sintaxis,
  Goblin para los tamaños, Esqueleto para el «símbolo no definido», Orco para salirse, Ogro para la lógica
  y Troll para la pila) y el mensaje real entre paréntesis, para que lo reconozca en emu8086.

## 3. El emulador (Fase 1)

`resources/js/runners/asm8086/` (sin dependencias, probado con Vitest o con Node):

- **Ensamblador en dos pasadas:** etiquetas y variables en la primera, código en la segunda. Directivas:
  `.model`, `.stack`, `.data`, `.code`, `db`, `dw`, `dup`, `?`, `equ`, `offset`, `byte ptr`/`word ptr`,
  `proc`/`endp`, `macro`/`endm`/`local`, `end`. Genera un «.EXE» simplificado: segmentos separados de código,
  datos y pila.
- **CPU:** las instrucciones que usa el curso (unas 80): `mov xchg lea push pop pushf popf`, `add adc sub sbb
  inc dec neg mul imul div idiv cmp cbw cwd`, `and or xor not test shl shr sar rol ror rcl rcr`, `jmp call ret
  loop loope loopne jcxz` y todos los `Jcc`, las de cadena (`movsb lodsb stosb cmpsb scasb` con `rep`), `clc stc
  cmc cld std`, `int`. Los 7 modos de direccionamiento de la lección 09.
- **Interrupciones** (las mismas que atiende `herramientas/dos8086.py` del material): `INT 21h` (01h 02h 06h
  07h 08h 09h 0Ah 2Ch 4Ch), `INT 10h` (00h 02h 03h 06h 07h 09h 0Eh, con colores), `INT 16h` (00h), `INT 1Ah`
  (00h, para el azar), `INT 20h`.
- **Entrada:** el teclado de verdad mientras corre (la consola pide la tecla) y, para comprobar, la `#### Entrada`
  de la micro-misión.
- **Límites:** tope de pasos (para el bucle infinito: «el Gólem se quedó dando vueltas») y de tiempo, como el
  timeout de 5 s de Python.
- **Prueba de que anda:** las 17 lecciones y todas sus `soluciones/` del material, con sus `.entrada.txt` y
  `.salida.txt`, tienen que dar la misma salida que en `dos8086.py`. Esa es la prueba de aceptación de la Fase 1.

## 4. Cómo se comprueba una micro-misión

Hoy una micro-misión se aprueba si la salida coincide con la `#### Salida esperada`. En ensamblador muchas
órdenes no imprimen nada (mueven palancas y llenan cajones), así que se suma una segunda forma:

````
#### Estado esperado
AX = 1234h
BL = FFh
ZF = 1
[pociones] = 4
[0200h] = FFh
````

- Se aprueba si **todas** las líneas se cumplen al terminar el programa (y la salida, si también hay
  `Salida esperada`).
- Al fallar, el tablero marca en rojo lo que no coincide («AX quedó en 0012h, se esperaba 1234h»), sin
  mostrar la solución.
- Tipos de micro-misión (todas con el tablero):
  1. **Completar** un `___` en un código casi hecho (la más común al principio).
  2. **Arreglar** un programa con un error (el Slime o el Goblin a la vista).
  3. **Predecir y comprobar:** «¿cuánto vale AX después de estas 3 órdenes?». Se contesta escribiendo una
     orden (`mov resultado, 7`) y el paso a paso le muestra si acertó.
  4. **Escribir** unas pocas órdenes desde cero (al final de cada nodo).
- Una sola idea por micro-misión, con el `#### Gheco sugiere` del formato (concepto mínimo y ejemplo).

## 5. El temario estirado (unas 130 micro-misiones)

Se respeta el orden del material y se estira donde cuesta. Cada nodo tiene entre 4 y 7 micro-misiones cortas
y una `carta:` con el puente a otros lenguajes.

| Rama | Nodos | Puente con los otros cursos |
|---|---|---|
| **R00 Clase 0 (gratis)** | El despertar: qué es una orden, el tablero, el primer `mov` y el paso a paso | «Cada línea de Python o C termina siendo un montón de estas» |
| **R01 Fundamentos** (01–05) | 01 Hola mundo (estructura, `INT 21h` 09h/4Ch) · 02 Palancas (`AX`…`DX`, `AH`/`AL`, hexa) · 03a Cajones con nombre (`db`, `dw`) · 03b Dirección y contenido (`offset`, `lea`, little endian) · 04 El teclado (01h, 0Ah) · 05 Cuentas (`add` `sub` `inc` `dec` `mul` `div`) · **Jefe: el Slime de las Palancas** | variables = cajones con nombre; `x = x + 1` = `inc` |
| **R02 Decisiones y repeticiones** (06–09) | 06a Comparar (`cmp` y los interruptores ZF/SF/CF) · 06b Saltar (`je` `jne` `jmp`) · 06c El if/else completo · 06d Con signo y sin signo (`jg` vs `ja`) · 07a `loop` · 07b mientras y hasta que · 08 Bits y máscaras · 09 Arreglos e índices · **Jefe: el Ogro de las Banderas** | `if`, `else`, `while`, `for`, `arr[i]` |
| **R03 Pila, procedimientos y pantalla** (10–14) | 10 La torre de platos (`push`/`pop`) · 11a `call`/`ret` · 11b Parámetros y registros que se cuidan · 12 El grimorio de números · 13 Macros · 14 El ojo del Gólem (colores, cursor, azar) · **Jefe: el Troll de la Pila** | funciones, parámetros, la pila de llamadas (recursión), `#define` |
| **R04 Proyectos** (15–17) | 15 Calculadora · 16 Oráculo · 17 Combate · **Jefe final: el Dragón del Gólem** | un programa entero, como en cualquier lenguaje |

Los proyectos, que en el material son grandes, se parten en micro-misiones que **arman el programa de a una
pieza** (el menú, después leer el número, después la cuenta…), como en las Sendas.

## 6. La historia: el Corazón del Gólem con protagonista nuevo

Se mantiene el arco de `GUION.md` (Axón, el Gólem de Bronce, debajo de las Forjas; palancas, cajones,
torre de platos, interruptores y ojo; los cuatro jefes) y se **cambia quién lo despierta**. Tres opciones
(nombres libres en el universo):

| Opción | Quién es | Por qué cuadra |
|---|---|---|
| **A · Nova, la chispa del Gólem** (recomendada) | Una IA recién nacida en el núcleo de Axón. No tiene cuerpo: **es** el Gólem aprendiendo a mover su propio cuerpo, palanca por palanca. Aspecto (2026-10-19): una chica con capa oscura de cuello alto con circuitos cian, túnica cerrada y botas con suela cian; ropa opaca y cerrada, apta para la escuela. | El alumno literalmente le enseña a la máquina a pensar. «El lenguaje más potente» es el idioma nativo de Nova. Cada paso a paso es Nova sintiendo cómo cambia por dentro. |
| **B · La doctora Ilse Vatio** | Científica de las Forjas, de unos 30 años, con un exotraje de bronce y cian y un monóculo de lectura de circuitos. Baja al interior del Gólem para repararlo. | Rol científico-futurista clásico; aventura de exploración dentro de la máquina. |
| **C · Sigma** | Un androide explorador de las Forjas, alto y delgado, con el pecho transparente donde se ven sus propios registros. | Mezcla los dos: un cuerpo-máquina que se reconoce en el Gólem. |

Gheco sigue de guía (como en todos los cursos) y Kira puede aparecer de visita (es de las Forjas). La
compañía y las criaturas ya están en `GUION.md`. La historia completa se escribe en
`docs/historias/ensamblador.md` cuando se elija la opción, y se recorre
[ALTA-DE-CURSOS-Y-PERSONAJES.md](ALTA-DE-CURSOS-Y-PERSONAJES.md) entera.

## 7. Consultas desde una micro-misión, con la solución al lado

Hoy las consultas (D63, `PracticeMessenger`, `practice_messages`) cuelgan de una **práctica**. Este curso no
tiene prácticas, y además sirve para todos los cursos que tienen micro-misiones:

- **Alumno:** en cada micro-misión, «Preguntale al profe» abre el mismo chat de siempre. Al enviar, el mensaje
  se guarda con una **foto del código** que tenía en el editor en ese momento (y lo que le dio al ejecutar).
- **Docente/administrador:** en la bandeja de mensajes (y en el aviso en vivo), cada consulta de micro-misión
  muestra en dos columnas **el código del alumno** y **la solución** (`#### Solución`, que nunca llega al
  alumno), con el botón *Ejecutar* para correr los dos. Es la misma idea que cuando corrige una entrega.
- **Permisos:** igual que hoy, `PracticeMessagePolicy` con `TeacherScope` (el docente, solo sus alumnos); la
  solución sigue en `$hidden` y hay test de que no sale en vistas del alumno.
- Técnicamente: `practice_messages` pasa a apuntar a una práctica **o** a una micro-misión (relación
  polimórfica `subject`), más una columna `code_snapshot`. La bandeja agrupa igual por alumno y tema.

## 8. Fases (frenar al final de cada una para que el docente pruebe)

| Fase | Qué | Cómo se prueba |
|---|---|---|
| 1 | Emulador + tablero, en una página de prueba (*Herramientas → Gólem 8086*) | Las 17 lecciones y sus soluciones dan la salida esperada; paso a paso en la compu y el celular |
| 2 | `Language::Asm8086` (autocomprobado), importador con `#### Estado esperado`, el tablero dentro de la micro-misión | Una micro-misión de ejemplo importada y superada |
| 3 | Consultas desde micro-misiones con la solución al lado (§ 7), para todos los cursos | Mandar una consulta y verla como docente |
| 4 | Historia (§ 6) + R00 y R01 escritas en `cursos/ensamblador/` | Cursarlas como alumno |
| 5 | R02, R03 y R04 | `app:simulate-course ensamblador` |
| 6 | Escenas en Stitch, enciclopedia, landing, temporada de inglés (lista de ALTA) | Revisión de la lista |

## 9. Preguntas abiertas (respondidas el 2026-10-18)

1. Protagonista: **Nova**.
2. Herramienta libre: **sí**, con abono.
3. Moneda: **chispas**.
4. Consultas desde micro-misiones: **para todos los cursos**, con todo lo necesario para responder sin salir del chat.
