# Ayuda en las micro-misiones (D123, fase 1 hecha; fase 2 en curso: Pasos de C)

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
| ¿Qué cursos? | Todos los de código. Los **Pasos** (§ 3, ayuda 1) se escriben primero para **los 10 primeros nodos de cada curso** (cambio del docente, 2026-11-15: antes era C entero) y después el resto. Inglés ya tiene sus escalones (D106) y queda afuera. |

## 3. El botón «Necesito ayuda»

Un botón fijo junto al desafío. Abre las ayudas de a una, de la más suave a la más directa; cada una queda abierta al pasar a la siguiente.

1. **«¿Qué me piden?»**: el desafío en **pasos cortos y numerados**, uno por línea, en lenguaje literal, sin historia ni metáforas. Ejemplo: «1. Buscá la línea que dice `int total`. 2. Cambiá `int` por `float`. 3. Ejecutá.» Es contenido nuevo (`#### Pasos` en el .md); mientras una micro-misión no lo tenga, el botón arranca en la ayuda 2.
2. **«¿Dónde toco?»**: se **resaltan en el editor** las líneas que hay que cambiar o completar. Sale sola, comparando el código inicial con la solución en el servidor; al alumno le llegan solo los números de línea.
3. **«Comparemos»**: la salida esperada y la suya **una al lado de la otra**, renglón por renglón, con la primera diferencia marcada (y los espacios o saltos de línea que sobran o faltan, visibles).
4. **«Mostrame una línea»**: muestra **una** de las líneas que cambian respecto del código inicial (la primera que todavía está mal), con su número de renglón en la solución (y su Paso al lado cuando los haya). El alumno la escribe y vuelve a ejecutar. Si sigue fallando, el botón ofrece la siguiente; nunca más de una por intento fallido. Sin botón de copiar ni «pegar todo». La solución entera solo se ve al final de la escalera, línea por línea.
5. **«Preguntale al profe»**: el último escalón, como ahora.

## 4. Gheco ofrece ayuda solo

Si el alumno **falla 2 veces** o pasan **3 minutos sin ejecutar** con el desafío abierto, el botón late y Gheco dice «¿Te doy una mano?». No hace falta que el alumno se dé cuenta de que está trabado ni que se anime a pedir. Se puede cerrar y no vuelve a ofrecer en esa micro-misión.

## 5. Más fácil de leer

- **Leer en voz alta**: un botón junto al desafío (y junto a los Pasos) que lo lee con la voz del navegador (`speechSynthesis`, español). Sin servicios externos; si el navegador no tiene voz, el botón no aparece.
- **Modo enfoque**: el desafío y los Pasos primero, letra un poco más grande, la escena y la carta plegadas. Lo prende el alumno en su perfil o el docente desde la ficha del alumno (sin motivo). Se guarda en el usuario.

## 6. Para el docente

- En el **Recorrido** (D107): al lado de cada micro-misión, qué ayuda pidió («¿Dónde toco?, 2 líneas de la solución»). Se guarda en una tabla aparte, `step_helps` (`kind` = `offer`, `read`, `where`, `compare`, `line` con qué renglón), para no mezclarla con los fallos de las estadísticas. Se borra al reiniciar la cuenta o el curso. El staff y la Clase 0 de prueba no dejan registros.
- Falta (fase 2): sumarlo a *Admin → Estadísticas* y mostrar en la consulta al profe cuántas líneas ya había visto.

## 7. Cómo quedó la fase 1 (2026-11-15)

- **El botón**: «Necesito ayuda» debajo del editor de cada micro-misión de código (`livewire/partials/step-help.blade.php`, `resources/js/step-help.js`). Los pasos van numerados según los que hay: escuchar, ¿Dónde toco?, Comparemos, Mostrame una línea y el profe.
- **¿Dónde toco?**: `App\Services\StepHelper::whereLines` compara el código inicial con la solución (`App\Support\LineDiff`, sin los espacios del final; la sangría cuenta) y el editor marca esos renglones en ámbar. No aparece si el código inicial está vacío (ahí todo es nuevo).
- **Comparemos**: solo con una salida de texto (no en el Gólem ni con el inspector de HTML o JS) y después de un intento que no coincide. Tabla de dos columnas; en los renglones distintos los espacios se ven como «·» y el primero distinto va resaltado.
- **Mostrame una línea**: `StepHelper::revealLine`. La primera, con un intento fallido anotado; cada siguiente, con otro fallo posterior a la última que vio (el mismo código ejecutado dos veces cuenta una vez: hay que cambiar algo). Elige el primer renglón que cambia y que todavía no está en su código; con todos vistos, muestra la solución completa. El texto no se puede seleccionar ni hay botón de copiar.
- **El premio**: `StepCompleter::rewardFor`: con alguna línea vista, la mitad de XP y de oro (para arriba); las monedas del curso (D111) y los ítems no cambian. El panel de «¡Superada!» lo dice sin retar.
- **Gheco ofrece**: tras 2 ejecuciones que no coinciden o 3 minutos sin ejecutar; una vez por micro-misión.
- **Escuchar**: el parlante junto al desafío y «Leémelo» en el panel (`speechSynthesis`, es-AR).
- **Pruebas**: Pest en `tests/Feature/Student/NodeStepsTest.php` y la de Chrome `NODE_URL=/cursos/python/nodos/1 node scripts/ayuda/probar.mjs` (con `php artisan serve --port=8123`).

## 8. Fases

1. ~~**Botón y ayudas 2 a 4** (con la entrega de a una línea), oferta de Gheco, leer en voz alta y registro.~~ Hecho (2026-11-15), a probar con los alumnos.
2. **Pasos de los 10 primeros nodos de cada curso**: el importador lee `#### Pasos`; se escriben (como se hizo con las pistas de Gheco) y se reimporta. Con las ayudas en *Admin → Estadísticas*.
   - Hecho (2026-11-15): `#### Pasos` → `node_steps.guide`; «¿Qué me piden?» es la primera ayuda del panel (botón «Mostrame los pasos», con su parlante) y queda anotada (`guide`) en el Recorrido. Muestra: C R00-N01-P1 a P5, para que el docente ajuste el tono.
   - Cómo se escriben: 2 a 6 pasos numerados, una acción por paso; nombrar la línea como se ve en el editor (`printf(…)`, «el primer `___`»); decir qué escribir y dónde; terminar con «Tocá **Ejecutar**» y qué tiene que salir. Sin historia ni metáforas.
   - Falta: el resto de C (10 nodos), los demás cursos y las ayudas en *Admin → Estadísticas*.
3. **Modo enfoque.**
4. **Pasos del resto de los nodos**, curso por curso.

Se frena al final de cada fase para que el docente lo pruebe con sus alumnos.

## 9. Cómo seguir (traspaso, 2026-11-15)

Estado: fase 1 en producción. Fase 2 arrancada (commit bd27962b, falta `git push` + `scripts/deploy.sh --cursos`).

**Pregunta abierta al docente (esperar respuesta antes de escribir más):** los 5 Pasos de muestra (C R00-N01-P1 a P5, en `cursos/c/00-curso.md`) son muy directos: casi dicen la respuesta («escribí `printf`»). ¿Así, o que guíen sin dar el código exacto («el comando que muestra texto») y dejar la línea exacta a «Mostrame una línea» (medio premio)?

**Después, en orden:**
1. Pasos del resto de los 10 primeros nodos de C: R00-N01 (P6–P8), R01-N01 a R01-N09 (`cursos/c/00-curso.md` y `01-templar-el-metal.md`; ~66 micro-misiones). Va `#### Pasos` justo después de `#### Desafío`, con las reglas de § 8.2. Leer cada código inicial y solución: contar bien los `___`.
2. Revisar e importar: `php artisan app:import-course cursos/c` y luego con `--apply`. Commit por nodo o tanda.
3. Frenar para que el docente pruebe. Luego los demás cursos (10 primeros nodos de cada uno: Python 88, Java 70, PHP 66, Ensamblador 62, C++ 61, JS 59, HTML 56, C# 50 micro-misiones).
4. Las ayudas en *Admin → Estadísticas* (tabla `step_helps`, `StepHelp::KINDS`; hoy solo salen en el Recorrido del alumno, `StudentJourney::helpSummary`).
5. Fase 3: modo enfoque (§ 3).

Prueba en el navegador: `NODE_URL=/cursos/python/nodos/1 node scripts/ayuda/probar.mjs` con `php artisan serve --port=8123`.
