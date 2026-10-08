# C++ · Análisis (borrador 0, a revisar antes de escribir)

El curso de C++, **«La Ciudadela de los Artífices»**, con **Bron** como protagonista y **Tesla** como mentor. Este borrador solo compara lo que hay con lo que piden las cátedras; el arco de Bron y las micro-misiones se escriben después del OK del docente, con el mismo molde que C (docs/historias/c.md).

## 1. Qué piden las cátedras

- **UNLaR (Programación I, apunte de Camargo, pp. 70–88):** clases, niveles de acceso (`public`, `private`, `protected`), funciones `inline`, constructores y destructores, `new` y `delete`, herencia (simple y múltiple, con la **tabla de accesos** de la herencia `public` y `private`), el puntero `this`, sobrecarga de funciones, **sobrecarga de operadores** (miembro y **`friend`**, con la clase `complejo`), `operator<<`. Los alumnos de la UNLaR llegan **hasta clases** (R02).
- **UTN (Programación II):** C++ + **STL** (unidad 2: contenedores de secuencia, asociativos, no ordenados y adaptadores; categorías de iteradores, `rbegin`/`cbegin`; algoritmos `sort`, `find`, `count`, `binary_search`, `reverse`, `unique`, `remove_if`, `transform`, `accumulate`, `for_each`, `copy`; functores y lambdas; errores comunes: índices fuera de rango, **invalidar iteradores**, olvidar `<numeric>`; buenas prácticas) + **Qt** (unidad 3, con Qt Creator; todavía no la pasaron). En los parciales de C++ toman **archivos con clases y herencia**.
- **Decidido (2026-10-08):** STL y Qt van **obligatorias** en el camino; los de la UNLaR llegan hasta clases y los de la UTN siguen.

## 2. Lo que hay contra lo que falta

| Tema | Hoy | Qué hacer |
|---|---|---|
| Clases, constructores, encapsulamiento, operadores, composición, herencia, polimorfismo, varios archivos | R02 (Los Planos), completo | Mantener |
| **`friend`** (funciones y operadores amigos, como `operator==` y `operator<<` de `complejo`) | no aparece | Sumar a R02-N04 (operadores) |
| **Herencia `private` y `protected`** y la tabla de accesos del apunte | solo `protected` como nivel de acceso | Sumar a R02-N06 (herencia) |
| **`new` y `delete`** a mano (y por qué después se usan punteros inteligentes) | casi no aparecen (el curso salta a `unique_ptr`) | Sección en R02-N02 (constructores y destructores): el destructor que libera |
| **Archivos con clases** (guardar y cargar objetos, como en los parciales) | `fstream` en R03-N06 (archivos y carpetas) | Un encargo en R03-N06 o en el jefe: guardar y cargar una lista de objetos con herencia |
| STL: `forward_list`, el idiom **erase-remove**, **invalidar iteradores** | casi nada | Sumar a R04-N02 (iteradores) y R04-N05 (algoritmos) |
| STL: el resto de la unidad 2 de la UTN | R04 (La Gran Biblioteca), completo | Mantener |
| **Qt** | Senda S02 (Los Vitrales) | **Pasa al camino obligatorio** (por ejemplo, R06), con su jefe; la Senda del juego (S01, SFML/SDL) queda optativa |

## 3. La historia (a definir con el docente)

- **Bron** es el protagonista (PERSONAJES.md: mecánico y guerrero, viejo amigo de Ferrum). Hoy los ejemplos de C++ usan a **Kira** como compañía (≈ 470 menciones) y a Bron (≈ 70): Kira es la protagonista de C, así que pasa a gente de la Ciudadela, como se hizo en Java y en C. Hace falta definir esa gente (un compañero o compañera de Bron y dos o tres secundarios) y sus fichas.
- **Tesla**, el Artífice Mayor, fue aprendiz de Ferrum junto con Tesela: el hilo del Vidriero puede pasar por un **engranaje** del portal (el balcón de los cuatro portales tiene una espiral, un engranaje, un vitral y un arco de fuego).
- Igual que en C: Linux y Windows en cada «Cómo compilarlo» (la UTN usa **VS Code** y **Qt Creator**), crónicas en tercera persona, micro-misiones que corren en el navegador (C++ para el alumno, como D98 con C) y un jefe final que sea el **simulacro del parcial** (archivos con clases y herencia).

## 4. Preguntas para el docente

1. ¿Qt pasa al camino obligatorio como rama nueva (R06) después de la Gran Biblioteca, o reemplaza al Taller del Juego (R05)?
2. ¿Tenés algún parcial de C++ de la UTN o de la UNLaR, como los de C, para armar el simulacro?
3. ¿Habilitamos C++ en el navegador del alumno para las micro-misiones (el mismo Clang de D98, con el encabezado precompilado de ~14 MB más)?
