# Material existente — análisis para llevarlo a la plataforma

> Origen: `/home/djmov/Programas/Cursos/FullCursos/` (relevado el 2026-09-26).
> Objetivo: decidir **cómo se arma cada curso en la plataforma** (curso → unidades → clases → tarea) a partir de lo que ya está escrito.
> No se modificó nada en esa carpeta.

---

## 1. Qué hay en la carpeta

- **23 capítulos** (`01-C` … `23-TypeScript`) con **~291 carpetas de ejemplo** hoy. Los índices nuevos de C, Python y Java suman más (30 + 47 + 42).
- Documentos generales:
  - `README.md`: la progresión completa.
  - `ROADMAP.md`: la checklist por tema. Está **desactualizado** respecto de las reconstrucciones.
  - `INSTALACIONES.md`: las dependencias.
  - `GUION.md`: la historia común.
  - `AUDITORIA-CURRICULAR.md`: el método para rehacer cada capítulo.
- `external/` (1,2 GB): SDL3, emsdk, Maven, driver JDBC. Son herramientas del entorno local, **no son contenido**: no se suben a la plataforma.
- Cada ejemplo es **una carpeta autocontenida**: `README.md` + código + `Makefile`/`build.sh`/`CMakeLists.txt`.
- Los capítulos ya reconstruidos traen además:
  - `*.salida.txt`: la salida esperada;
  - `*.entrada.txt`: lo que se "tipea";
  - `soluciones/`.
- Hay un `verificar.sh` por capítulo que compila, ejecuta y compara salidas.

### La historia común: "Las Crónicas del Código" (`GUION.md`)

Todos los cursos comparten una historia:

- **Kira** cruza a **Codexia**, un mundo donde la magia se escribe.
- **Cada lenguaje es una región**, con su propio mentor.
- **Los errores son monstruos**: slime = sintaxis, goblin = tipos, esqueleto = nombres, orco = índices, ogro = lógica, troll = estado compartido.
- **Cada bloque cierra con un jefe.**

| Región | Capítulos | Mentor | Estado |
|---|---|---|---|
| Las Forjas de Hierro | 01–02 C | Maese Ferrum | definida |
| El Valle de la Serpiente | 17 Python | Ofidia | definida |
| El Imperio de las Clases | 18–20 Java | Kaffa | definida |
| La Ciudadela de los Artífices | 03–11 C++ | a definir | — |
| El Puerto de los Mensajeros / La Feria de las Luces | 21 PHP / 22–23 JS-TS | a definir | — |

> Dato a tener en cuenta para [DISENO.md](DISENO.md): la **idea 2 (CodeQuest)** tiene el mismo tono que este guion:
> - "misiones";
> - rutas por bloque;
> - un jefe al final;
> - el "Mapa de misiones".
>
> Encajan sin sumar puntos ni rankings (la gamificación queda fuera de alcance): se puede tomar la **estética narrativa**.

---

## 2. Dos formatos de ejemplo conviviendo

### Formato nuevo (capítulos reconstruidos) — listo para una clase de la plataforma

README de 150–260 líneas con estas secciones fijas:

```
# NN - Tema
> Crónica (2–4 líneas de historia)
## Objetivo · ## Antes de empezar · ## Explicación · ## Código · ## Salida esperada
## Errores habituales (el bestiario) · ## Misiones (3) · ## Encargo del Gremio
## Prueba del sello (autoevaluación) · ## Soluciones
<details><summary>Si venís de C</summary> … </details>
```

Más `soluciones/` (4–6 archivos por ejemplo), `*.salida.txt` y `*.entrada.txt`.

### Formato viejo (resto de los capítulos) — sirve de borrador, no de clase

README de ~30–45 líneas: *Qué se aprende · Conceptos · Cómo compilar · Qué deberías observar · Ejercicios*.

- No tiene historia, salida esperada ni soluciones.
- Muchos están escritos como "delta sobre C", con el cambio que trae cada tema, y contradicen la regla nueva de que **cada capítulo arranca de cero**.

### Estado real por capítulo

Columnas:
- **Ej.**: carpetas de ejemplo.
- **Nuevo**: ejemplos con el formato nuevo (tienen `soluciones/`).
- **En navegador**: si el código puede correr con el runner de la plataforma.

| Cap. | Tema | Ej. | Nuevo | En navegador | Estado |
|---|---|---|---|---|---|
| 01 | C (Forjas, parte 1) | 16 | **16** | ❌ (C) | ✅ reconstruido completo |
| 02 | C intermedio (Forjas, parte 2) | 7 | 0 | ❌ | 🔄 bloques 3–5 y proyectos por hacer (índice: 17–30) |
| 03 | C++ | 12 | 0 | ❌ | formato viejo; se rehace desde cero junto con 04 y 11 |
| 04 | C++ moderno / STL | 14 | 0 | ❌ | formato viejo |
| 05 | C++ videojuegos (consola) | 7 | 0 | ❌ | formato viejo |
| 06 | SDL3 en C | 13 | 0 | ❌ (ventana gráfica) | formato viejo |
| 07 | SDL3 en C++ | 9 | 0 | ❌ | formato viejo |
| 08 | Proyecto final "Guardián de las Gemas" | 1 proyecto | — | ❌ | proyecto único (~1200 líneas, con assets) |
| 09 | SFML | 8 | 0 | ❌ | ⏳ falta `libsfml-dev` |
| 10 | OpenGL | 10 | 0 | ❌ | formato viejo |
| 11 | STL a fondo | 10 | 0 | ❌ | formato viejo |
| 12 | Qt GUI | 7 + 46 mini apps (`Lab-Qt6`) | 0 | ❌ | formato viejo |
| 13 | WebAssembly | 6 | 0 | ⚠️ el **resultado** corre en el navegador | formato viejo |
| 14 | PostgreSQL (libpq) | 6 | 0 | ❌ | ⏳ falta `libpq-dev` |
| 15 | Arduino | 7 | 0 | ❌ (hardware) | formato viejo |
| 16 | Phaser | 13 | 0 | ⚠️ son páginas HTML jugables | formato viejo |
| 17 | **Python** | 28 (índice: 47) | **11** | ✅ Pyodide (ver § 5) | 🔄 bloque 1 listo (01–11); sigue 12–19 |
| 18 | **Java** (Paradigmas III, UNLaR) | 26 (índice: 42) | **8** | ❌ | 🔄 bloque 1 listo (01–08); sigue 09–18 |
| 19 | Java avanzado | 13 | 0 | ❌ | pendiente: bloque 0 de repaso |
| 20 | Spring Boot + Lombok | 12 | 0 | ❌ | pendiente: bloque 0 de repaso |
| 21 | PHP | 23 | 0 | ❌ hoy (posible con php-wasm) | formato viejo |
| 22 | JS Vanilla | 22 | 0 | ⚠️ JS corre nativo en el navegador | formato viejo |
| 23 | TypeScript | 22 | 0 | ⚠️ ídem, compilando TS en el cliente | formato viejo |

**Conclusión:** para un primer curso real en la plataforma, lo que está listo es:
- **C bloques 1–2** (16 clases);
- **Python bloque 1** (11 clases);
- **Java bloque 1** (8 clases).

El resto necesita la reconstrucción que ya está planificada en cada `AUDITORIA.md`.

---

## 3. Cómo se traduce una carpeta a la plataforma

| En `FullCursos` | En la plataforma | Comentario |
|---|---|---|
| Capítulo / región | **Curso** (`courses`) | C = 01 + 02 juntos (una región, numeración continua). C++ = 03 + 04 + 11 (así lo propone la auditoría) |
| Bloque ("Bloque 1 · Fundamentos — *templar el metal*") | **Unidad** (`units`) | El jefe del bloque puede ir en el título o en la descripción |
| Ejemplo `NN-Tema` | **Clase** (`lessons`) | Ver pregunta C1: ¿1 ejemplo = 1 clase? |
| Crónica | Primer bloque de la explicación, como recuadro destacado | |
| Objetivo · Antes de empezar · Explicación · Errores habituales · Prueba del sello | `lessons.content` (markdown) | Los "Antes de empezar" que nombran otro ejemplo pueden ser links a esa clase |
| Código (`main.c`, `hola.py`, `saludo.py`…) | **Ejemplo resuelto** (`example_code`) | ⚠️ Muchos ejemplos tienen **más de un archivo**. Ver C3 |
| `*.salida.txt` | Salida esperada, debajo del ejemplo | Hoy no está en el modelo de datos |
| `*.entrada.txt` | Texto inicial del campo *entrada estándar* | Encaja justo con el textarea de stdin de Pyodide |
| Misiones (3) + Encargo del Gremio | **Tarea** (`assignments`) | ⚠️ Son **4 ejercicios por ejemplo**; la spec dice "una tarea por clase". Ver C2 |
| `soluciones/` | Material **solo del docente** | Ver C4: ¿se publican después del vencimiento? |
| Makefile / build.sh / CMakeLists / assets | **Recurso descargable** (zip del ejemplo) | Para compilar en la máquina del alumno |
| `INSTALACIONES.md` (sección del lenguaje) | "Clase 0 — Prepará tu entorno" de cada curso | |
| `<details>Si venís de C…</details>` | Bloque plegable en la explicación | ⚠️ Es HTML dentro del markdown; ver § 6 |
| `MisPracticas/`, `pendiente-*`, `herramientas/`, `verificar.sh` | **No se importan** | Material interno del docente |

---

## 4. Tamaño de los cursos frente al ritmo de las comisiones

- Con **1 o 2 clases por semana**, un cuatrimestre da ~16–32 encuentros.
- Python tiene **47 ejemplos** planificados, Java 42 y C 30.
- Si 1 ejemplo = 1 clase de la plataforma, un curso completo no entra en un cuatrimestre. Hay tres salidas:
  - **a)** dividir en varios cursos, por ejemplo "Python I: Fundamentos" (bloques 1–3) y "Python II" (4–8);
  - **b)** que una clase de la plataforma agrupe 2–3 ejemplos, como el encuentro semanal real;
  - **c)** mantener 1 ejemplo = 1 clase y que la comisión libere varias por semana.

  La grilla de liberación ya lo permite con "Liberar toda la unidad".

---

## 5. Qué se puede ejecutar en el navegador (Pyodide)

Python es el único lenguaje con "Ejecutar" en el alcance actual. Por bloque del cap. 17:

| Bloque | Temas | ¿Corre en Pyodide? |
|---|---|---|
| 1 Fundamentos (01–11) | print, input, tipos, control, colecciones, funciones, módulos | ✅ (el 11 usa **varios archivos**: el runner tiene que poder escribir módulos al sistema de archivos virtual) |
| 2 Objetos (12–15) | clases, dataclass, herencia, Protocol | ✅ |
| 3 Errores y persistencia (16–19) | excepciones, archivos, JSON/CSV, **sqlite3** | ✅ (archivos en memoria; sqlite3 hay que cargarlo como paquete) |
| 4 Iteración (20–23) | iteradores, generadores, itertools, decoradores | ✅ |
| 5 Calidad (24–28) | type hints, venv/pip, pytest, logging, ruff | ⚠️ parcial: lo conceptual sí; venv/pip/mypy/ruff son de terminal |
| 6 Concurrencia (29–31) | threading, asyncio, timeit/cProfile | ⚠️ sin hilos reales; asyncio con limitaciones; los tiempos medidos no son representativos |
| 7 pygame (32–35) | ventana, input, sprites | ❌ (ventana gráfica: se descarga y se corre local) |
| 8 Aplicado (36–42) | os/subprocess, regex, HTTP, Tkinter, numpy/pandas/matplotlib, IA, serial | mixto: regex, IA y numpy/pandas ✅ (matplotlib necesita mostrar la imagen); subprocess, HTTP, Tkinter y serial ❌ |

> ⚠️ Todo lo de esta tabla está **a verificar en la Fase 4**: depende de la versión de Pyodide.

**Otros lenguajes, a futuro** (sin cambiar el alcance actual):
- **JS y TS** (caps. 22–23) son los más baratos de sumar: corren nativos en un Worker o iframe aislado, y TS se compila en el cliente.
- **PHP** podría correr con php-wasm.
- **C, C++ y Java** necesitan el servicio externo (Piston o Judge0) detrás de `CodeRunner`.
- **Phaser (16) y WebAssembly (13)** generan páginas jugables: podrían mostrarse como **demo embebida** (un tipo de recurso "demo").

---

## 6. Impacto en el plan técnico ([PLAN.md](PLAN.md))

1. **Markdown con HTML acotado.** Los README usan `<details><summary>`, tablas GFM y comentarios `<!-- salida: … -->`.
   - Escapar todo el HTML (decisión D10) rompe los recuadros "Si venís de C".
   - Propuesta: GFM + lista blanca de etiquetas (`details`, `summary`, `kbd`, `br`), y el resto se escapa.
2. **Varios archivos por ejemplo.** Opciones:
   - tabla `lesson_files` (nombre, lenguaje, contenido, orden, `is_runnable`), con el ejemplo mostrado **en pestañas**;
   - o seguir con `example_code` único y dejar los demás archivos como zip descargable.
3. **Salida esperada y entrada.** Sumar `expected_output` y `sample_input` al ejemplo (o por archivo).
4. **Tarea con varios ejercicios.** Ver C2.
5. **Soluciones.** Campo o archivo privado, con opción de publicarlas (ver C4).
6. **Lenguajes.** El enum de la spec (`python|c|cpp|java|otro`) se queda corto. Propuesta: sumar `javascript`, `typescript`, `php`, `sql` y `arduino`, porque definen el resaltado y la extensión de las entregas.
7. **Importador.** Comando `php artisan app:import-course <carpeta>`:
   - lee el README del capítulo (tablas de índice) y cada carpeta `NN-Tema/`;
   - crea unidades, clases, ejemplo, salida esperada, tarea y zip de recursos;
   - las clases quedan **en borrador** para revisarlas antes de liberar.

   Con ~300 ejemplos, cargarlos a mano no es viable. Iría al final de la **Fase 2**.
8. **Etiquetas de unidad de cátedra.** Java 18 marca cada ejemplo con la unidad del programa de UNLaR ("U1…U6"). Se podría guardar como etiqueta de la clase, para poder estudiar por unidad del programa.

---

## 7. Preguntas para definir cómo querés los cursos

| # | Pregunta | Mi recomendación |
|---|---|---|
| C1 | ¿**1 ejemplo = 1 clase** de la plataforma, o una clase agrupa varios ejemplos (el encuentro semanal)? | 1 ejemplo = 1 clase (el material ya está cortado así); la comisión libera 2–3 por semana |
| C2 | Misiones + Encargo del Gremio (4 ejercicios): ¿**una sola entrega** con todos, o **una entrega por ejercicio**? | Una tarea por clase con los 4 ejercicios en la consigna, entrega en zip o en varios archivos. Si querés corregir cada uno por separado, hay que cambiar el modelo (`assignments` pasa a ser 1:N) |
| C3 | Ejemplos con varios archivos: ¿pestañas en la clase o zip descargable? | Pestañas para ver el código + zip para compilar localmente |
| C4 | `soluciones/`: ¿nunca se muestran, se publican tras el vencimiento de la comisión, o las liberás a mano? | Liberación manual por comisión (como las clases) |
| C5 | ¿Cómo se agrupan los capítulos en **cursos del catálogo**? | Ver la propuesta de abajo |
| C6 | ¿El guion (Kira, regiones, bestiario) se ve en la plataforma: portada del curso, crónica destacada, íconos de monstruos en "Errores habituales"? | Sí, como estética narrativa sin puntos: se conecta con la idea 2 |
| C7 | Los capítulos con formato viejo, ¿se publican igual como "versión preliminar" o recién después de reconstruirlos? | Solo después de reconstruirlos; primero C, Python y Java |
| C8 | ¿Querés el importador (§ 6.7) o preferís cargar las clases a mano con el editor? | Importador, con revisión manual |

### Propuesta de catálogo (para discutir en C5)

| Curso en la plataforma | Capítulos de origen | Unidades |
|---|---|---|
| **Python desde cero** | 17 | bloques 1–8 + proyectos (o partido en I y II) |
| **C desde cero** | 01 + 02 | bloques 1–5 + proyectos |
| **Java: POO, escritorio y bases de datos** (Paradigmas III) | 18 | bloques 1–7 + proyectos |
| **C++ desde cero** | 03 + 04 + 11 (a reconstruir) | a definir |
| **Videojuegos 2D en C/C++** | 05 + 06 + 07 + 08 (+ 09 SFML, 10 OpenGL como optativas) | por etapa |
| **Java avanzado y Spring** | 19 + 20 | bloque 0 de repaso + cada capítulo como unidad |
| **Desarrollo web: PHP, JS y TypeScript** | 21, 22, 23 (juntos o separados) | uno por capítulo |
| **Juegos web con Phaser** | 16 | — |
| Talleres cortos | 12 Qt, 13 WebAssembly, 14 PostgreSQL, 15 Arduino | uno por taller |
