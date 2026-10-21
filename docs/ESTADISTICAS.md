# Estadísticas de avance (D107)

Pedido del docente (2026-10-15): elegir alumnos y saber **qué vieron, dónde fallaron y en qué capítulo se traban**, en todos los cursos, también en las Crónicas en Inglés (que hasta ahora no dejaban ninguna métrica).

## 1. El problema

Hasta D107 la plataforma solo guardaba los **aciertos** de las micro-misiones (`node_step_completions`), las entregas y los nodos abiertos. Los **fallos** se quedaban en el navegador (la criatura de `english.js`, el «Todavía no» del ejecutor) y nadie sabía qué nodo **miró** un alumno. Sin eso no se puede ver dónde se traban.

## 2. Decisiones (charla con el docente, 2026-10-15)

| Pregunta | Decisión |
|---|---|
| ¿Qué se registra? | Cada **intento** de una micro-misión (acierto o fallo, con el tipo de error) y cada **visita** a un nodo (una fila por alumno, nodo y día, con cuántas veces entró). |
| ¿Se guarda la respuesta equivocada? | **Sí, recortada a 500 caracteres**: es lo más útil (en inglés se ve que todos escriben «He go»). Los intentos de más de **6 meses** se borran solos. |
| ¿Se ejecuta algo en el servidor? | **No.** Se anota lo que ya pasó en el navegador del alumno; el servidor no vuelve a comprobar un fallo. |
| ¿Y el staff? | Sus pruebas no se registran. |
| ¿Dónde se ve? | En el **árbol del alumno** (*Alumnos → alumno → curso*), una sección «Recorrido»; y un panel nuevo ***Admin → Estadísticas*** con filtros. El Inicio queda con un resumen chico y el enlace al panel. |
| ¿Quién lo ve? | El administrador todo; el **docente, solo los alumnos de sus comisiones** (`TeacherScope`, como el resto). |
| ¿Desde cuándo hay datos? | Desde que se sube D107. Lo anterior no se reconstruye, salvo los aciertos y las entregas que ya estaban. |

## 3. Qué se guarda

- **`step_attempts`**: alumno, micro-misión, nodo y curso (repetidos para contar rápido), `passed`, `kind` y `answer` (≤ 500), `created_at`.
  - `kind`: en inglés, lo que dice `english.js` (`almost` = le falta o sobra una letra, `bad`, y los propios de cada misión); en código, `output` (la salida no coincide) o `checks` (el inspector no encontró lo pedido).
  - En código, `answer` es la salida que obtuvo (recortada) y, desde el 2026-10-21, **`code`** guarda el código de cada fallo (≤ 20.000; el mismo error con otro código cuenta aparte); el código del acierto queda en la completion.
  - Un acierto que ya estaba superado (repasar) también cuenta como intento.
- **`node_visits`**: alumno, nodo, día, `views`, primera y última hora. Se anota al abrir el nodo (`NodeView`), no en cada click.
- Límite de pedidos como el de `completeStep`: un alumno no puede llenar la base apretando «Ejecutar».

## 4. Qué se muestra

### 4.1 Recorrido del alumno (en su árbol, por curso) — fase 1
Capítulo por capítulo (nodo por nodo, en el orden del árbol):
- cuándo lo vio por primera y última vez y cuántos días entró;
- micro-misiones superadas / total, y **intentos por micro-misión** (los fallos antes del acierto);
- **«Trabado»**: una micro-misión con 3 o más fallos y sin acierto, o un nodo abierto sin avanzar hace 7 días o más;
- sus **últimas respuestas equivocadas** (con la micro-misión y la fecha). Al tocar una se despliega lo necesario para corroborar la comparación: lo que obtuvo, **lo esperado** (y el inspector, si tiene), **su código** de ese intento y **la solución**, los dos con «Ejecutar» (Java con el ejecutor de la compu del docente). Los intentos anteriores al 2026-10-21 no tienen código: se muestra el del acierto si después la superó.

### 4.2 Panel *Admin → Estadísticas* — fase 2
Filtros: curso, comisión, período y alumnos (uno, varios o todos).
- **Embudo por capítulo**: cuántos alumnos vieron cada nodo y cuántos lo terminaron; dónde se cae la gente.
- **Micro-misiones más difíciles**: intentos por acierto, alumnos que fallaron y no volvieron, y las **respuestas equivocadas más repetidas**.
- **Alumnos trabados**: quién lleva X días sin avanzar o muchos fallos seguidos, con el enlace a su recorrido.
- Los números de entregas que hoy están en el Inicio (`PracticeStats`) se mudan acá; el Inicio queda con el resumen.

## 5. Fases
1. **Registro + Recorrido del alumno** (`ActivityLog`, las dos tablas, los avisos de fallo desde el navegador). Frenar para que el docente pruebe. **Hecha (2026-10-15):** `App\Services\ActivityLog`, `StepAttempt`, `NodeVisit`, `NodeView::failStep` (lo llaman el pie del ejecutor de la micro-misión y `english.js`), `Support\StudentJourney` y la sección «Recorrido» en *Alumnos → árbol del alumno*.
2. **Panel de Estadísticas** y resumen en el Inicio. **Hecha (2026-10-20):** *Admin → Estadísticas* (`Livewire\Admin\Statistics`, `Support\ProgressStats`; `PracticeStats` filtra por alumnos y cursos para el docente) con filtros de curso, comisión, período y alumno; resumen, **desde dónde entran** (celular, tablet o compu, D109), embudo por capítulo, micro-misiones más difíciles con las respuestas equivocadas más repetidas, alumnos trabados (enlace a Demorados y al recorrido de cada uno) y las prácticas que estaban en el Inicio. El Inicio queda con el resumen de 30 días. El Recorrido y el embudo van en el orden de los códigos (R00, R01-N01…, S01).
