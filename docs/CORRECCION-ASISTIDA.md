# Corrección asistida (D73, diseño a revisar)

Conversado con el docente el 2026-09-30. **Estado:** aprobado por el docente; etapa 1 (el indicio) hecha el 2026-09-30; etapa 2 (pruebas, formato, importador y `app:course-tests`) y etapa 3 (las pruebas de los cinco cursos) hechas el 2026-10-01. Sigue la etapa 4, con el docente.

## Punto de partida

- **La corrección sigue siendo humana.** El docente (o los docentes, D72) mira el esfuerzo: un ejercicio que no salió igual puede aprobarse si se ve el intento, y uno que coincide puede volver a rehacer. **No hay aprobación automática** y «corrección automática» sigue fuera de alcance en CLAUDE.md.
- Lo que se busca es **corregir más rápido**: que al abrir una entrega ya se sepa si el programa hace lo que tiene que hacer, con varias pruebas y no con una sola.
- El código del alumno sigue sin tocar el servidor: las pruebas corren **en el navegador del docente** con los ejecutores que ya existen (Python con Pyodide, C/C++ con Clang en WebAssembly D66, PHP en WebAssembly D68, Java con `scripts/JavaRunner.java` D69).
- **Qué entra:** las entregas de código con salida esperada (620 hoy). **Quedan afuera** las de archivo o zip y los proyectos (213): se siguen corrigiendo a ojo, como hoy.

| Curso | Se pueden probar | Afuera (archivo o zip) | Leen entrada (llevan pruebas extra) |
|---|---|---|---|
| Python | 86 | 21 | 4 |
| C | 119 | 25 | 47 |
| C++ | 160 | 31 | 120 |
| Java | 149 | 38 | 43 |
| PHP | 106 | 98 | 31 |

Las 74 prácticas de código sin salida esperada (sobre todo Java y PHP) se revisan una por una: se les completa la salida o quedan a ojo.

## 1. El indicio, igual en todos los cursos

Hoy la *Entrada de ejemplo* y la *Salida esperada* se muestran distinto según el curso:

- **Python** (corre en el navegador): la salida esperada está escondida en la solapa *Esperada* de la consola, y la entrada, precargada en *Entrada (stdin)*. Es fácil no verla.
- **C, C++, Java y PHP** (se resuelven en la compu): un desplegable *Salida esperada*, pero **la entrada de ejemplo no se muestra**. En C++, 120 prácticas leen entrada y el alumno no sabe con qué datos se obtiene esa salida.

**Propuesta:** un mismo bloque, **«Cómo debería verse»**, en todas las prácticas de todos los cursos, en la tarjeta del nodo y en el modo misión. Va **cerrado** de entrada, como hoy la salida esperada (es un recurso: el alumno lo abre si lo necesita), y muestra:

- **Entrada de ejemplo**, si la práctica la tiene, con la aclaración «lo que se tipea, una línea por lectura».
- **Salida esperada**.

En Python, la consola queda con *Salida* y *Entrada (stdin)* y el «✓ Coincide» (la entrada sigue precargada para ejecutar), pero el bloque se ve igual que en los demás cursos. Lo mismo vale para el ejemplo del nodo (*Código de ejemplo*). Componente único: `<x-expected-io>`. La solapa *Esperada* de la consola de Python se saca para que el indicio esté en un solo lugar.

Las pruebas extra del § 2 **no** salen en este bloque: el alumno ve solo la de ejemplo.

## 2. Varias pruebas por práctica

- Tabla nueva `practice_tests`: `practice_id`, `position`, `input` (puede ir vacía), `expected_output`. La práctica sigue con su `sample_input` y `expected_output`, que es la **prueba 1** (la visible).
- Las pruebas extra son **solo del docente**, como la solución de referencia (D37): no se cargan en las vistas del alumno y hay test que lo verifica.
- Solo tienen sentido en los programas que **leen entrada**: uno sin entrada imprime siempre lo mismo y le alcanza con la salida esperada.
- Cuántas: entre 2 y 4 extra por práctica, pensadas para los casos que el ejemplo no cubre (el borde, el vacío, el dato inválido que la consigna pide manejar).

### En el formato del curso (FORMATO-CURSO.md § 6)

Una parte nueva, `#### Pruebas`, después de la *Salida esperada*. Cada prueba es un `#####` con dos bloques, `entrada` y `salida`:

````markdown
#### Pruebas

##### Sin piezas
```entrada
fin
```
```salida
No hay piezas.
```

##### Cantidad negativa
```entrada
tornillo -3
fin
```
```salida
Cantidad inválida: tornillo
No hay piezas.
```
````

El importador las reemplaza enteras en cada reimportación (no tienen actividad de alumnos colgando). Avisos: una prueba sin `salida`, o pruebas en una práctica de entrega archivo o ninguna.

### Quién las escribe

Las arma Claude en este proyecto, curso por curso: elige las entradas y **saca la salida corriendo la solución de referencia** (python3, gcc/g++, java, php8.3, como ya hace el súper test), así ninguna salida se escribe a mano. Un comando local `app:course-tests {curso} [--fill]` corre la solución de referencia contra todas las pruebas, informa las que no coinciden y, con `--fill`, completa las salidas vacías en los `.md`. El súper test pasa a verificar todas las pruebas, no solo la de ejemplo.

## 3. Al corregir una entrega

En *Admin → Entregas*, en una entrega de código con pruebas:

- Al abrirla, **corren todas las pruebas** en el navegador del docente (en C/C++ se compila una vez y se ejecuta con cada entrada; en Java, `JavaRunner` recibe la lista de entradas y compila una vez).
- Arriba del código: **«3 de 4 pruebas pasan»**. Cada prueba que falla muestra entrada, salida esperada y salida obtenida, con las diferencias marcadas.
- **Comparación:** se ignoran los espacios al final de cada línea y las líneas vacías del principio y del final (no se ven). Los espacios al principio de una línea sí cuentan: son la sangría. Si la única diferencia es lo ignorado, se marca como coincide, con la aclaración «difiere solo en espacios o líneas vacías».
- *Aprobar* y *Pedir que rehaga* quedan igual que hoy: la decisión es del docente.
- En Java, si `JavaRunner` no está abierto, se avisa como hoy y las pruebas no corren.

## 4. En la bandeja

- Botón **Probar pendientes**: corre, una tras otra en el navegador, las pruebas de las entregas pendientes que se ven en la lista y deja una marca en cada una: ✓ pasan todas, ✗ falla alguna (con «2/4»), — sin pruebas.
- El resultado se guarda en la entrega (`submissions.check_result`: pasadas, total, cuándo) para no repetirlo. Es una **ayuda**, no una nota: el alumno no lo ve, y lo manda el navegador del docente (solo quien puede corregir esa entrega, `SubmissionPolicy::review`).
- Filtro y orden por esa marca: se puede empezar por las que pasan, que se confirman rápido.

## 5. Dos ayudas más

- **Comentarios guardados:** cada docente guarda sus devoluciones frecuentes («Bien, pero revisá los nombres de las variables») y las inserta con un clic al corregir. Tabla `review_snippets` (`user_id`, `course_id` opcional, `body`, `position`).
- **Dónde se traban:** en cada curso, las prácticas con más pedidos de rehacer y más intentos promedio, con los alumnos del alcance del docente (`TeacherScope`). Suele señalar consignas poco claras.

## 6. Orden de trabajo (cada etapa se prueba antes de seguir)

1. **Indicio igual en todos los cursos** (§ 1). Chico, se ve enseguida.
2. **Pruebas:** tabla, formato, importador, `app:course-tests` y súper test (§ 2).
3. **Contenido:** escribir las pruebas, empezando por C++ (120), y después C, Java, PHP y Python. Se reimporta con `scripts/deploy.sh --cursos`.
4. **Pantalla de la entrega y bandeja** (§ 3 y § 4).
5. **Comentarios guardados y Dónde se traban** (§ 5).

Tests Pest en cada etapa: el alumno nunca recibe las pruebas extra, solo quien corrige guarda `check_result`, el importador lee y reemplaza las pruebas.

## Etapa 3: cómo quedó (2026-10-01)

| Curso | Prácticas con pruebas | Casos (ejemplo + pruebas) |
|---|---|---|
| Python | 4 | 97 |
| C | 45 | 244 |
| C++ | 116 | 458 |
| Java | 36 | 211 |
| PHP | 24 | 156 |

Todos coinciden con la solución de referencia (`app:course-tests`). Las salidas las escribió `--fill`, no a mano. Notas:

- **Java:** las prácticas con base de datos (JDBC) quedan sin pruebas: no se pueden correr ni en el súper test ni con `JavaRunner`. Lo mismo en PHP con las páginas web y PDO (15 prácticas).
- **Contenido corregido al verificar:** dos salidas esperadas de Python habían perdido la sangría de la primera línea (R02-N02-M1 y R03-N02-M2).
- **A revisar por el docente:** la solución de referencia de PHP R05-N05-E1 (*El monitor de la tienda*) falla con `number_format(null)` si el registro no tiene ningún pedido confirmado. La consigna no dice qué mostrar en ese caso; las pruebas incluyen siempre un pedido.
- **Rendimiento:** C++ R05-N03-M3 mide búsquedas (2000 sobre 200 000 números) y, sin optimizar, tarda cerca de 5 s; el comando y el súper test usan 20 s de margen en los lenguajes compilados (con 5 s, el súper test la rechazaba siempre y los alumnos simulados se trababan ahí). Al corregir en el navegador (Clang en WebAssembly) va a tardar.
- **Súper test de C++ con las pruebas (2026-10-01):** todos los controles en verde; en 90 días terminan valen, cami y lu, y tomi y mateo (los perfiles que más se equivocan y faltan) quedan a mitad de camino, sin ninguna práctica que los trabe.

## Decidido (2026-09-30)

- El bloque «Cómo debería verse» va **cerrado** de entrada.
- Los comentarios guardados son **de cada docente**.
