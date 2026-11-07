# D119 · El curso de C#: el Conservatorio de Do Sostenido (demostración de 5 nodos, 2026-11-04)

Pedido del docente: después de que Ensamblador les gustó a los alumnos, le pidieron C#, y va con prioridad sobre las escenas de JS. Material: `FullCursos/27-CSharp` (solo lectura). Historia: [historias/csharp.md](historias/csharp.md).

## 1. Dónde corre: en el navegador, emulado

C# **no se ejecuta en el servidor** y el alumno **no instala nada**: el compilador oficial (Roslyn) y el runtime de .NET corren en WebAssembly, en un Web Worker.

| Qué | Cómo |
|---|---|
| Armado | `scripts/build-csharp-toolchain.sh` (`scripts/csharp-runner/`) deja `public/toolchains/csharp/`: unos 16 MB comprimidos, que se bajan una sola vez y quedan en caché. Necesita el SDK de .NET 10 solo en la compu del docente. |
| Conector | `resources/js/runners/csharp.js`, `csharp-errors.js` y `workers/csharp.worker.js`. |
| Velocidad | Carga en unos 4 s la primera vez; después compila y ejecuta en decenas de milisegundos. |
| Consola y teclado | De mentira: la salida queda en memoria (con tope, por los bucles que imprimen sin parar) y `ReadLine` lee la Entrada. |
| Archivos | Cada ejecución tiene una carpeta vacía, en memoria, que se borra al final. |
| Red | No sale: `HttpClient` no llega a ningún lado. |
| Tope | 5 s para el programa; si se pasa, se tira el worker. |
| Idioma | Los errores del compilador salen en español, con la explicación y la criatura (`csharp-errors.js`). Los números, como en una compu de acá (`es-AR`: `7,5`). |
| Pruebas | `node scripts/csharp-micro/probar-ejecutor.mjs` (20 casos) y `node scripts/csharp-micro/probar.mjs cursos/csharp` (cada solución y ejemplo). |

**Lo que no anda acá, y hay que tener en cuenta al seguir el curso:** al haber un solo hilo, `Task.Wait()`, `.Result` y `Thread.Sleep` bloqueantes no funcionan (`await` sí). Los temas 21 a 24 (hilos, xUnit, SQLite, API web) van a necesitar su propia emulación, como el Puerto simulado de JS, o proyectos en la compu.

## 2. La regla del curso (pedido del docente)

**Sencillo, pedagógico y explicativo, aunque sumen capítulos.** Es lo que más les gustó a los alumnos en Ensamblador. Por eso:
- una sola idea nueva por micro-misión, explicada antes de pedirla, con un ejemplo distinto a la respuesta;
- un tema del material se parte en varios nodos si hace falta (el 02 del material ya quedó repartido entre R01-N01 y R01-N02);
- `Código inicial` listo para completar: nada de pantalla en blanco salvo en la primera.

## 2 bis. El plan del curso entero (aprobado por el docente el 2026-11-07)

El docente pidió que el curso llegue a unos 30 nodos o más, como los demás, y que se vincule con otros lenguajes. Con la regla de sencillez, el tronco queda en **unos 50 nodos**:

| Acto | Material | Nodos | Jefe | Estado |
|---|---|---|---|---|
| I · La Sala de Ensayo | 01–08 | R01-N01 a R01-N14 + el jefe R01-N15 | el Slime Desafinado | **hecho (2026-11-07)** |
| II · El Taller de Instrumentos | 09–14 | unos 9: clases, constructores, propiedades y `static`, `struct`/`enum`/`record`, `null`, herencia, polimorfismo, interfaces, composición (y la **sobrecarga**, que en un programa suelto no se puede) | la Quimera de las Mil Partituras | falta |
| III · El Archivo y la batuta | 15–18 | unos 9: `List`, `Dictionary`, `HashSet`/`Queue`/`Stack`, genéricos, `yield`, delegados y lambdas, eventos, LINQ (dos nodos) | la Hidra del Coro | falta |
| IV · El Archivo Mudo | 19–20 | unos 5: excepciones, propias y `when`, archivos, CSV, JSON | el Liche del Archivo Mudo | falta |
| V · El mundo real | 21–24 | unos 6, con un mundo simulado como el Puerto de JS (SQLite: el de SQL en el navegador) | la Sirena de la Red | falta |
| Proyectos | 25–27 | la Arena, Junta las Gemas y el Gremio | el Dragón del Conservatorio | falta |

**Los vínculos con otros lenguajes:** los encargos siguen llegando de otras regiones, y al terminar el tronco van **Sendas cruzadas**: el Teatro (con JS: Ceci y Hilván), el Gólem (con Ensamblador: qué hay debajo de C#), el Puerto (con PHP: una API en C# que habla con la de Elefa) y el Arcade (a la manera de Unity o Godot).

**Por fases, frenando en cada una:** 1) el Acto I completo; 2) el juego del Conservatorio (un **luthier nuevo** atiende la tienda, ítems, una **montura musical nueva** para Ceci, el mapa y sus lugares); 3) los actos II a V, los proyectos y las Sendas.

### El Acto I (fase 1, 2026-11-07)

- 10 nodos nuevos (R01-N05 a R01-N14) y el jefe (R01-N15): textos; cortar, partir y dar formato; leer y validar; `Math` y azar; decidir (`if`, `switch`); repetir y el menú; arreglos; matrices y referencias; métodos; tuplas, `ref`/`out` y recursión. 55 micro-misiones y 11 encargos (con Pruebas en los que leen entrada).
- `node scripts/csharp-micro/probar.mjs cursos/csharp`: 112 de 112 (ahora también le pasa la «Entrada de ejemplo» a los ejemplos y encargos).
- **Lo que no se puede en un programa suelto:** los métodos son funciones locales, que no admiten sobrecarga. Por eso la sobrecarga pasó al Acto II.
- El jefe, **el Slime Desafinado**: ficha, retrato, cuerpo (`652d3237…`) y hoja (`d0581643…`) en el proyecto de la Feria; insignia «Oído Afinado».
- Las 55 escenas, con las hojas de Ceci, Clave, Bemol, Gheco, Don Tano, el Slime y las criaturas de la Feria (el ogro, el troll chiquito y el Orco del Desborde).

## 3. Lo que hay hoy

5 nodos (Clase 0, Variables, Tipos, Cuentas y Comparar), 25 micro-misiones con su escena y 5 encargos de otras regiones. `micromisiones_completan: si`, como Java y PHP. Moneda: **corcheas**. `app:simulate-course csharp`: los 5 alumnos terminan y los 9 controles dan bien.

Personajes: **Ceci** (protagonista, 6 aspectos), **Clave** (líder) y **Bemol**, en [historias/PERSONAJES.md](historias/PERSONAJES.md). Referencias de Stitch en `scripts/escenas/pendientes.py`, en el proyecto de la Feria (donde ya están Gheco, Nilo, Nima y Bruno).

## 4. La guía de alta ([ALTA-DE-CURSOS-Y-PERSONAJES.md](ALTA-DE-CURSOS-Y-PERSONAJES.md))

| Punto | Estado |
|---|---|
| Lenguaje, contenido, temas, ejecutores, seeder, deploy, universo, enciclopedia | hecho |
| Logo y moneda | hecho (`php artisan app:course-brand csharp cursos/csharp/marca`, también en producción) |
| Retrato de Clave y fondo del mundo | hecho (`php artisan app:glossary-portraits cursos/csharp/marca --apply`, también en producción) |
| Historia, fichas, novela gráfica, Mis Crónicas (`story.portal_piece`) | hecho (borrador, a revisar por el docente) |
| Protagonista y 6 aspectos | hecho |
| Simulación | hecho |
| Tienda de Ceci | **pendiente**: hace falta el vendedor y su imagen |
| Expediciones y mapa | **pendiente**: el mapa y sus lugares |
| Monturas e ítems del Conservatorio | **pendiente** |
| Jefe del bloque (Slime Desafinado) y el resto de los nodos | Acto I **hecho** (2026-11-07); siguen los actos II a V (§ 2 bis) |
| Temporada en las Crónicas en Inglés | **pendiente**: cuando el curso esté más avanzado |
| Copia de las imágenes en `publicidad/logos cursos/personajes/` | **pendiente** |
