# Formato de curso para importar (Fase 7)

Un curso completo se escribe en uno o varios archivos **Markdown** y se carga en *Admin → Cursos → Importar* (o con `php artisan app:import-course carpeta/ --apply`).

- Es el mismo formato para **todos los lenguajes** (D39). Lo único que cambia por lenguaje está en el [anexo](#anexo-por-lenguaje).
- Ejemplo completo y probado: [tests/Fixtures/curso-ejemplo.md](../tests/Fixtures/curso-ejemplo.md).
- Primero se **revisa** (no guarda nada y muestra qué pasaría). Si hay un error, no se guarda nada.
- **Reimportar actualiza** por ID: no duplica, no borra y no toca el progreso de los alumnos (aperturas, entregas, monedas, XP). Lo que está en la base y no en el archivo queda como estaba, y el informe lo avisa.

## 1. Reglas generales

1. Los títulos marcan la estructura:

   | Título | Qué es |
   |---|---|
   | `# CURSO` | Datos del curso |
   | `# DICCIONARIO` | Nombres narrativos (tabla) |
   | `## R00-N01 · Título` antes de la primera rama | El **nodo raíz** (Clase 0) |
   | `# RAMA R01 · Título` | Una rama (un acto de la historia) |
   | `## R01-N01 · Título` | Un nodo de esa rama |
   | `### Crónica`, `### Explicación`… | Una sección del nodo |
   | `### Misión R01-N01-M1 · Título` | Una práctica obligatoria (`Encargo` o `Desafío` = optativa) |
   | `#### Consigna`, `#### Criterio de aprobación`… | Una parte de la práctica |
   | `#### ¿Pregunta?` dentro de `### Prueba del sello` | Una pregunta; lo que sigue es la respuesta |

2. **Dentro del texto de una sección**, los subtítulos van con `####` o más (nunca `#`, `##` o `###`, que cortan la sección). Lo que está dentro de un bloque de código nunca cuenta como título.
3. Cada curso, rama, nodo y práctica puede llevar un bloque de datos justo debajo de su título:

   ````
   ```meta
   clave: valor
   ```
   ````

4. Los **IDs son estables**: una vez importado, no se cambian (si cambian, se crea otro nodo). Convención: rama `R01`, nodo `R01-N02`, práctica `R01-N02-M1` (misión) o `R01-N02-E1` (encargo). El raíz suele ser `R00-N01`.
5. Separador del título: `·`, `:` o `-` (`## R01-N01 · Variables`).
6. Valores de sí/no: `si` o `no`.
7. Todo el texto admite markdown. El HTML se muestra escapado.

### Marcadores en los textos

En cualquier texto (crónicas, explicación, consignas, historia del diccionario) se pueden usar:

| Marcador | Se reemplaza por |
|---|---|
| `{heroe}` | El héroe que eligió el alumno (o `hero.name`, "Kira", si todavía no eligió) |
| `{mentor}` | `mentor.name` del curso (por ejemplo, Ofidia) |
| `{mundo}` | `world.name` |
| `{region}` | `world.region` del curso |

Escribí en segunda persona y sin marcar el género del héroe: *"—Bien hecho, {heroe} —dice {mentor}."*

Textos de historia del diccionario que se muestran: `story.course_intro` (bienvenida, en la ficha y el árbol), `story.branch_completed` (al completar una rama), `story.course_completed` (al terminar el curso). El **título** es la columna *singular* y el texto, la columna *historia*.

## 2. `# CURSO`

```meta
slug: python             # obligatorio; minúsculas y guiones; identifica el curso al reimportar
titulo: Python desde cero # obligatorio
lenguaje: python          # obligatorio: python, c, cpp, java, javascript, typescript, php, sql, arduino, other
descripcion_corta: Tu primera lengua: clara y legible.
precio_raiz: 10           # monedas para abrir la Clase 0
dias_abono: 30
nivel: desde_cero         # desde_cero | intermedio | avanzado
destacado: si             # sale en la landing entre los cursos que más se dictan
proximamente: no          # "Próximamente": se ve con su temario pero no se abre (solo si no está publicado)
publicado: no             # solo al crearlo (por defecto, borrador); después se publica desde el admin
```

- `### Descripción`: texto largo de la ficha del curso.
- `### Temario`: una lista corta (un tema por línea, con `-`) que se muestra en las tarjetas del catálogo y de la landing.

## 3. `# DICCIONARIO`

Una tabla con estas columnas (la última es opcional):

```
| clave | singular | plural | género | descripción | historia | ámbito |
```

- **género**: `f` o `m`. **historia**: el texto largo (lore); para saltos de línea usá `<br>`.
- **ámbito**: `curso` o `general`. Si se deja vacío: `world.name`, `hero.name`, `coin.wildcard`, `xp`, `xp.short`, `level`, `level.N`, `companion.*` y `state.*` van a **general** (valen para toda la plataforma); el resto, al **curso**.
- Claves existentes: ver *Admin → Diccionario* o `config/glossary.php`. Se pueden crear claves nuevas (por ejemplo `beast.hydra`, `story.rey_slime_intro`).

## 4. Rama: `# RAMA R01 · Título`

```meta
tipo: tronco      # tronco (por defecto) | extra (nodos optativos sueltos) | senda (especialización optativa)
posicion: 1       # orden en el árbol (por defecto, el orden del archivo)
```

### Sendas

Una Senda es una rama `tipo: senda`. Su primer nodo tiene como `padre` el nodo del tronco del que **brota** (normalmente una `ventana`) y suele cobrarse en `comodin`; los de adentro, en la moneda del curso. Si un tramo necesita un tema más avanzado del tronco, se agrega con `requiere:`. Una Senda puede brotar de otra. En el árbol se dibuja saliendo de su nodo de origen, y **no cuenta** para completar el curso (como los extras).

## 5. Nodo: `## R01-N01 · Título`

```meta
tipo: tema        # raiz | tema | jefe | extra | ventana (nodo corto que hace probar un campo; de ahí brota una Senda)
padre: R00-N01    # obligatorio salvo el raíz: el nodo que hay que completar antes
requiere: R03-N02, R05-N01 # requisitos extra: también hay que completarlos (además del padre)
precio: 10        # el raíz toma precio_raiz del curso
moneda: curso     # curso | comodin (cualquier nodo salvo el raíz; la entrada a una Senda suele ir en comodín)
criatura: slime   # del bestiario: slime, goblin, esqueleto… o la clave completa (beast.hydra)
video: https://www.youtube.com/watch?v=…
ejecutable: no    # el Código de ejemplo se muestra y se copia, sin botón Ejecutar (pygame, hardware, paquetes externos)
insignia: Cazador de slimes            # solo jefes
insignia_descripcion: Venciste al Rey Slime.
publicado: si     # un nodo nuevo se publica por defecto; uno existente cambia solo si se escribe
```

Secciones (todas opcionales; el alumno ve solo las que tienen texto, en este orden):

| Título | Qué es | Quién la presenta |
|---|---|---|
| `### Crónica` | 2 a 4 líneas de historia, en segunda persona | — |
| `### Objetivos` | Lista «Al terminar, vas a poder…» | — |
| `### Antes de empezar` | Qué tiene que saber ya | — |
| `### Explicación` | La teoría | Mia (`companion.theory`) |
| `### Código de ejemplo` | Un bloque de código ejecutable | — |
| `### Entrada de ejemplo` | Lo que se tipea (una línea por lectura) | — |
| `### Salida esperada` | Lo que tiene que mostrar el ejemplo | — |
| `### ¿Para qué sirve?` | Usos reales fuera del juego | Bron (`companion.uses`) |
| `### Errores habituales` | El error típico y cómo leer el traceback | Zed (`companion.errors`) + la criatura |
| `### Prueba del sello` | Preguntas `####` con su respuesta debajo (autoevaluación **sin nota**) | — |
| `### Soluciones` | **Solo el docente**: soluciones, tiempos y dificultades | — |

Lo que va entre paréntesis en el título se ignora: `### Explicación (Mia)` vale.

## 6. Práctica: `### Misión R01-N01-M1 · Título`

**Todo nodo necesita al menos una misión obligatoria**, incluidos el raíz, los jefes, las ventanas, los extras y los nodos narrativos (como la Encrucijada: una misión de reflexión, que puede ser `entrega: ninguna`).


`Misión` o `Práctica` = obligatoria; `Encargo` o `Desafío` = optativa (paga comodines).

```meta
obligatoria: si     # pisa lo que dice el título
entrega: codigo     # codigo | archivo | ambos | ninguna
entorno: navegador  # navegador | local (se resuelve en la compu del alumno)
extensiones: py, zip  # solo con entrega archivo o ambos
monedas: 3          # las obligatorias pagan moneda del curso; las optativas, comodines
xp: 10
```

Partes:

| Título | Qué es |
|---|---|
| `#### Consigna` | Qué hay que hacer, en pasos |
| `#### Criterio de aprobación` | Lista verificable; la ve el alumno («Para aprobar») y el docente al corregir |
| `#### Código inicial` | Bloque de código con el que arranca el editor |
| `#### Entrada de ejemplo` | Lo que se tipea al ejecutar |
| `#### Salida esperada` | Lo que tiene que mostrar |
| `#### Solución de referencia` | **Solo el docente** |

## 7. Qué revisa el importador

- **Errores** (no se guarda nada): un nodo publicado **sin ninguna práctica obligatoria** (todo nodo necesita al menos una; si no está listo, `publicado: no`); falta `slug`, `titulo` o `lenguaje`; no hay exactamente un raíz; IDs repetidos; `padre` o `requiere` que no existen; ciclos (por padre o por requisitos); rama inexistente; valores desconocidos en `tipo`, `entrega` o `entorno`; bloques de código sin cerrar; un nodo que pasa de raíz a otro tipo.
- **Avisos**: secciones o claves desconocidas; obligatorias sin criterio; jefes sin insignia; obligatorias que cambian de tipo con entregas de alumnos; **economía**: si las obligatorias de un nodo pagan menos de lo que cuesta un hijo (en la moneda del curso).

## Anexo por lenguaje

| Lenguaje | Se ejecuta en el navegador | Prácticas |
|---|---|---|
| **Python** | Sí (Pyodide, programas de consola, corte a los 5 s) | `entorno: navegador` para consola; `local` + `entrega: archivo` para pygame, Tkinter, hardware, archivos del disco, red o paquetes externos (numpy, pandas) |
| C, C++, Java, PHP, SQL, Arduino, otros | No (por ahora) | El ejemplo se muestra y se copia, no se ejecuta (el editor colorea C, C++ y Arduino). Las prácticas van `entorno: local` con `entrega: codigo` (pegar el código) o `archivo` (programas de varios archivos, SDL, Qt, sketches de Arduino: `.zip`). La *Entrada de ejemplo* y la *Salida esperada* sirven igual: el alumno compara en su compu, y el súper test compila con `gcc -std=c11` / `g++ -std=c++20` y las verifica |
| JavaScript / TypeScript | No (por ahora; es posible a futuro) | Igual que el anterior |

Detalles del ejecutor de Python (para escribir salidas esperadas que coincidan):

- La salida es la misma que en la terminal con la entrada redirigida: el texto de `input("Nivel: ")` queda en la misma línea que lo que se muestra después, y lo que se "tipea" **no** aparece.
- `if __name__ == "__main__":` funciona, y también `asyncio.run(...)`.
- Los archivos que escribe el programa viven en una memoria temporal: se pueden crear y leer durante la ejecución (conviene borrarlos al final para que cada ejecución arranque igual).
- Las salidas esperadas se comparan tal cual (se respetan los tabuladores); la forma segura de obtenerlas es ejecutar la solución de referencia en una terminal.

Para C y C++ vale lo mismo: la salida esperada es la de la terminal con la entrada redirigida (`./programa < entrada.txt`). Lo que tiene que ser igual en cualquier compu va por la salida estándar; lo que cambia (tiempos medidos) va por `std::cerr`. Con `<random>`, la salida esperada es la de `g++` en Linux: `std::mt19937` es igual en todos lados, pero las distribuciones pueden dar otros números con `clang`.
