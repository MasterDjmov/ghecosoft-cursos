# Java con micro-misiones (D111)

Pedido del docente (2026-10-20): probó Ensamblador, que se completa **solo con micro-misiones**, y quedó más que
satisfecho. Quiere probar lo mismo en **Java** y sacarse de encima las prácticas que corrige, sin perder lo que
funciona del curso.

## 1. Punto de partida

- Java está **en producción** con 4 alumnos con abono vigente: 55 entregas (la última, el 2026-10-19), 64
  micro-misiones superadas y 18 nodos abiertos. **Nadie pierde nada** con el cambio.
- El tronco (Clase 0 a R05) tiene **119 misiones obligatorias** y 39 encargos:
  - **99** son de consola, con su *Salida esperada*: se pueden comprobar solas con el ejecutor de Java del alumno
    (D85), igual que las micro-misiones que ya tiene el curso;
  - **20** son proyectos que se entregan en un .zip (Maven, el .jar, JUnit, varias clases): no se comprueban solos.
- Las Sendas (Bóveda, Palacio de las Ventanas, Arcade, Spring) usan bases de datos, ventanas y Spring: tampoco.

## 2. Decisiones (charla con el docente, 2026-10-20)

| Tema | Decisión |
|---|---|
| Sendas | **Quedan como están**: prácticas que corrige el docente. |
| Misiones de consola del tronco (99) | **Pasan a ser micro-misiones**, con la misma lógica: el mismo enunciado, el código inicial, la salida esperada y la solución. Se comprueban solas. |
| Proyectos del tronco (20) | Quedan como **prácticas que corrige el docente** (como las Sendas): no hay forma de comprobarlos solos. |
| Denarios | **Siguen abriendo los nodos**. La micro-misión que viene de una misión paga los **denarios** que pagaba la misión; el resto de las micro-misiones sigue pagando **oro** y XP. |
| Escenas | Cada micro-misión nueva lleva **su escena**, como las demás (Stitch, proyecto de Java). |

| Encargos del tronco (39) | Quedan como prácticas **optativas** que corrige el docente (dan los comodines de las Sendas). Confirmado el 2026-10-20. |
| CV (D64) | Los nodos completos de Java **siguen contando**, aunque lo que se comprueba en la compu del alumno se pueda trampear. Confirmado el 2026-10-20. |

## 3. Cómo funciona (para cualquier curso, no solo Java: D39)

1. **Un ajuste del curso, no del lenguaje.** En el `00-curso.md`: `micromisiones_completan: si`. Hoy «se comprueba solo» depende del lenguaje (inglés, ensamblador); esto lo vuelve una opción de cualquier curso. Inglés y Ensamblador siguen igual (sin monedas).
2. **Cuándo se completa un nodo** en un curso con el ajuste: **todas sus micro-misiones superadas** y, si le quedan prácticas obligatorias (los proyectos), **también aprobadas**.
3. **Micro-misión que paga denarios**: en su `meta`, `recompensa: xp 20, monedas 4` (lo que pagaba la misión). Solo en un curso con el ajuste; se paga una vez, por el `Ledger`, como todo.
4. **Lo que ya estaba completo, sigue completo.** Un nodo que el alumno completó con las misiones aprobadas no vuelve atrás porque ahora tenga micro-misiones nuevas (cuenta el registro de «nodo completado» del libro de XP).
5. **Las misiones convertidas que el alumno ya tenía aprobadas** quedan superadas como micro-misión (sin volver a pagar): no tiene que rehacerlas.
6. **Prácticas retiradas.** Una misión que se convierte se borra del .md. El importador:
   - la **borra** si no tiene entregas;
   - si tiene entregas, la **retira** (`practices.retired_at`): deja de verse y de ser obligatoria, y el docente sigue viendo las entregas viejas.

## 4. Orden de trabajo (cada fase se prueba antes de seguir)

1. **Motor**: el ajuste del curso, la regla de completar, los denarios de las micro-misiones, las prácticas retiradas y lo ya hecho que se conserva. Tests Pest y `app:simulate-course`. **Hecha (2026-10-20):** `courses.steps_complete_nodes` (`micromisiones_completan: si`), `node_steps.coin_reward` (`recompensa: … monedas N`), `practices.retired_at` (global scope `Practice::ACTIVE`; entregas, consultas y pruebas la siguen viendo), `TreeAccess::nodeWorkDone`/`stepsCompleteNodes`, `StepCompleter::creditCoins`, el importador (`antes:`, retirar o borrar) y `tests/Feature/Student/StepsCompleteNodesTest.php`.
2. **Contenido**: las 99 misiones de consola, convertidas en `cursos/java/` (con su escena escrita, «Gheco sugiere» y «Al superarla»), probadas con el ejecutor de Java contra su salida esperada. **Hecha (2026-10-20):** eran **97** (dos de las 99 se entregan como archivo y quedan como proyectos). Las convierte `scripts/java-misiones-a-micro.py` con la historia escrita a mano en `scripts/java-micro/*.json` (lugar, personajes, escena, Gheco sugiere, Al superarla e imagen); el enunciado, la entrada, la salida y la solución son los de la misión. `python3 scripts/java-micro/probar.py cursos/java/0*.md` corre cada solución con `java` y la compara (97 bien). En el tronco quedan 22 misiones que corrige el docente: los proyectos de .zip (Maven, .jar, JUnit, UML, Spring) y «Mirá hacia atrás». `app:simulate-course java`: los 5 alumnos terminan los 64 nodos y los 9 controles dan bien (el simulador juega primero las micro-misiones de los nodos abiertos). Las «Pruebas» extra de 25 misiones no pasan a la micro-misión (se comprueba solo el ejemplo); en producción quedan con la práctica retirada.
3. **Escenas** (en curso, después de la subida): las de las micro-misiones nuevas, en Stitch; 15 de 97 hechas el 2026-10-20 (Stitch cortó por cuota). Ojo: a Java todavía le faltan 153 de sus 229 escenas actuales (ESCENAS.md).
4. **Subida**: reimportar, verificar a los 4 alumnos (nodos, denarios, micro-misiones) y deploy. **Hecha (2026-10-20):** ensayada antes contra una copia de la base de producción y después subida con `deploy.sh --cursos`: los 4 alumnos conservan los mismos nodos abiertos y completos y los mismos denarios; 29 misiones con entregas quedaron retiradas y lo que tenían aprobado pasó como micro-misión superada (43 en el ensayo).
