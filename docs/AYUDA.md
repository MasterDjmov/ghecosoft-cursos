# Ayuda en las micro-misiones (D123, aprobada, se programa después de las Sendas de C#)

Pedido del docente (2026-11-15): que nadie se **frustre** ni se **estanque** en una micro-misión. Hay alumnos a los que les cuesta leer un enunciado largo (un alumno con TEA que cursa C, personas de más de 50 que recién empiezan). En la clase presencial el docente los destraba; en casa se quedan esperando el mensaje del profe. Lo que quieren es **ver cómo se resuelve**, sin volverse locos; el oro y la XP no les importan.

## 1. Qué hay hoy y qué falta

- Hay: la pista de Gheco («Gheco sugiere»), el «Todavía no» con la línea donde difiere la salida, «Preguntale al profe» (D110) y el registro de cada intento (D107).
- Falta: un camino entre «me trabé» y «le pregunto al profe». Y el enunciado sigue siendo un párrafo; en C se notan los más densos (por ejemplo, el tablero de puntajes pide cuatro cosas en un solo párrafo).

## 2. Decisiones (charla con el docente, 2026-11-15)

| Pregunta | Decisión |
|---|---|
| ¿Para quién? | **Para todos los alumnos**, sin activar nada. No se guarda ningún motivo ni diagnóstico. |
| ¿Cuesta premio? | Las ayudas 1 a 3 son **gratis**. Si se mostró **alguna línea** de la solución (ayuda 4), la micro-misión paga **la mitad del oro y de la XP**, solo para que el ranking siga siendo justo con quien la hizo sola (a quien no le importa el premio no le cambia nada). Aprobado. |
| ¿Se muestra la solución entera? | **No de golpe:** se entrega **de a una línea**, a medida que falla. La primera línea, después del primer intento fallido; cada línea siguiente, después de **otro intento fallido** con la anterior ya a la vista. Recién cuando se mostraron todas queda la solución completa. |
| ¿Cambia alguna regla? | **Sí:** FORMATO-CURSO dice que la solución de una micro-misión «nunca llega al alumno». Pasa a llegar **de a una línea** cuando la pide con «Mostrame una línea», desde el servidor (que controla los intentos), y queda anotado. Las soluciones de las **prácticas** y de los nodos (`reference_solution`, `teacher_solutions`) siguen ocultas como siempre. |
| ¿Qué cursos? | Todos los de código. Los **Pasos** (§ 3, ayuda 1) se escriben primero para **C** (254 micro-misiones) y después curso por curso. Inglés ya tiene sus escalones (D106) y queda afuera. |

## 3. El botón «Necesito ayuda»

Un botón fijo junto al desafío. Abre las ayudas de a una, de la más suave a la más directa; cada una queda abierta al pasar a la siguiente.

1. **«¿Qué me piden?»**: el desafío en **pasos cortos y numerados**, uno por línea, en lenguaje literal, sin historia ni metáforas. Ejemplo: «1. Buscá la línea que dice `int total`. 2. Cambiá `int` por `float`. 3. Ejecutá.» Es contenido nuevo (`#### Pasos` en el .md); mientras una micro-misión no lo tenga, el botón arranca en la ayuda 2.
2. **«¿Dónde toco?»**: se **resaltan en el editor** las líneas que hay que cambiar o completar. Sale sola, comparando el código inicial con la solución en el servidor; al alumno le llegan solo los números de línea.
3. **«Comparemos»**: la salida esperada y la suya **una al lado de la otra**, renglón por renglón, con la primera diferencia marcada (y los espacios o saltos de línea que sobran o faltan, visibles).
4. **«Mostrame una línea»**: muestra **una** de las líneas que cambian respecto del código inicial (la primera que todavía está mal), en su lugar del editor como fantasma y con su Paso al lado si lo hay. El alumno la escribe y vuelve a ejecutar. Si sigue fallando, el botón ofrece la siguiente; nunca más de una por intento fallido. Sin botón de copiar ni «pegar todo». La solución entera solo se ve al final de la escalera, línea por línea.
5. **«Preguntale al profe»**: el último escalón, como ahora.

## 4. Gheco ofrece ayuda solo

Si el alumno **falla 2 veces** o pasan **3 minutos sin ejecutar** con el desafío abierto, el botón late y Gheco dice «¿Te doy una mano?». No hace falta que el alumno se dé cuenta de que está trabado ni que se anime a pedir. Se puede cerrar y no vuelve a ofrecer en esa micro-misión.

## 5. Más fácil de leer

- **Leer en voz alta**: un botón junto al desafío (y junto a los Pasos) que lo lee con la voz del navegador (`speechSynthesis`, español). Sin servicios externos; si el navegador no tiene voz, el botón no aparece.
- **Modo enfoque**: el desafío y los Pasos primero, letra un poco más grande, la escena y la carta plegadas. Lo prende el alumno en su perfil o el docente desde la ficha del alumno (sin motivo). Se guarda en el usuario.

## 6. Para el docente

- En el **Recorrido** (D107) y en *Admin → Estadísticas*: qué ayuda usó cada alumno y en qué micro-misión (`step_attempts` con `kind` = `help_steps`, `help_where`, `help_compare`, `help_line` (con qué línea), `help_offer`). Así se ve dónde se traba la clase y qué enunciados conviene reescribir.
- La consulta al profe desde una micro-misión muestra cuántas líneas de la solución ya había visto.

## 7. Fases

1. **Botón y ayudas 2 a 4** (con la entrega de a una línea), oferta de Gheco, leer en voz alta y registro. Solo programación, sirve desde el día uno para las 3170 micro-misiones de código.
2. **Pasos de C**: el importador lee `#### Pasos`; se escriben las 254 de C (como se hizo con las pistas de Gheco) y se reimporta.
3. **Modo enfoque.**
4. **Pasos del resto de los cursos**, de a uno.

Se frena al final de cada fase para que el docente lo pruebe con sus alumnos.
