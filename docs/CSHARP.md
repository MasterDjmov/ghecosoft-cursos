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
| II · El Taller de Instrumentos | 09–14 | R02-N01 a R02-N10 + el jefe R02-N11: clases, objetos que trabajan juntos y **sobrecarga**, propiedades, constructores y `static`, `struct`/`enum`, `record`/`null`, herencia, polimorfismo y `abstract`, interfaces, composición | la Quimera de las Mil Partituras | **texto hecho (2026-11-08)**, escenas en curso |
| III · El Archivo y la batuta | 15–18 | R03-N01 a R03-N09 + el jefe R03-N10: `List`, `Dictionary`, `HashSet`/`Queue`/`Stack`, genéricos, `yield`, delegados y lambdas, eventos, LINQ (dos nodos, con `GroupBy`, `MaxBy` y extensiones) | la Hidra del Coro | **texto hecho (2026-11-10)**, sin escenas |
| IV · El Archivo Mudo | 19–20 | R04-N01 a R04-N06 + el jefe R04-N07: `try`/`catch`/`finally`, `throw`, excepciones propias y `when`, archivos de texto, `using` con `StreamWriter`/`StreamReader`, CSV con `InvariantCulture`, JSON | el Liche del Archivo Mudo | **hecho** (2026-11-11): 35/35 escenas |
| V · El mundo real | 21–24 | unos 6, con un mundo simulado como el Puerto de JS (SQLite: el de SQL en el navegador) | la Sirena de la Red | falta |
| Proyectos | 25–27 | la Arena, Junta las Gemas y el Gremio | el Dragón del Conservatorio | falta |

**Los vínculos con otros lenguajes:** los encargos siguen llegando de otras regiones, y al terminar el tronco van **Sendas cruzadas**: el Teatro (con JS: Ceci y Hilván), el Gólem (con Ensamblador: qué hay debajo de C#), el Puerto (con PHP: una API en C# que habla con la de Elefa) y el Arcade (a la manera de Unity o Godot).

**Por fases, frenando en cada una:** 1) el Acto I completo; 2) el juego del Conservatorio (**hecho, 2026-11-08**) (un **luthier nuevo** atiende la tienda, ítems, una **montura musical nueva** para Ceci, el mapa y sus lugares); 3) los actos II a V, los proyectos y las Sendas.

### El Acto I (fase 1, 2026-11-07)

- 10 nodos nuevos (R01-N05 a R01-N14) y el jefe (R01-N15): textos; cortar, partir y dar formato; leer y validar; `Math` y azar; decidir (`if`, `switch`); repetir y el menú; arreglos; matrices y referencias; métodos; tuplas, `ref`/`out` y recursión. 55 micro-misiones y 11 encargos (con Pruebas en los que leen entrada).
- `node scripts/csharp-micro/probar.mjs cursos/csharp`: 112 de 112 (ahora también le pasa la «Entrada de ejemplo» a los ejemplos y encargos).
- **Lo que no se puede en un programa suelto:** los métodos son funciones locales, que no admiten sobrecarga. Por eso la sobrecarga pasó al Acto II.
- El jefe, **el Slime Desafinado**: ficha, retrato, cuerpo (`652d3237…`) y hoja (`d0581643…`) en el proyecto de la Feria; insignia «Oído Afinado».
- Las 55 escenas, con las hojas de Ceci, Clave, Bemol, Gheco, Don Tano, el Slime y las criaturas de la Feria (el ogro, el troll chiquito y el Orco del Desborde).

### El Acto II (2026-11-08)

- `cursos/csharp/02-el-taller-de-instrumentos.md`: 11 nodos, 55 micro-misiones y 11 encargos (de otras regiones: Lucio, Nilo, Bruno, el Flaco Ruiz, el guardia de la calesita, Elefa, Doña Mirta, el Gremio, Baldo y Kira). Don Cedro aparece en el Taller.
- Las clases van **abajo de todo**, después de las órdenes y de los métodos sueltos; adentro de una clase sí hay sobrecarga.
- `probar.mjs`: 77 de 77.
- El jefe, **la Quimera de las Mil Partituras**: ficha, retrato, cuerpo (`e6b99aa8…`) y hoja (`6d20041d…`); insignia «Maestro Luthier» y la **Cuerda de la Quimera** (ítem épico).
- Escenas: Stitch se cortaba por tiempo el 2026-11-08 (con dos pedidos en paralelo, y después también de a uno); el modelo liviano con las dos hojas como referencia anduvo a ratos.

### El Acto III (2026-11-10)

- `cursos/csharp/03-el-archivo-y-la-batuta.md`: 10 nodos, 50 micro-misiones y 10 encargos (Doña Mirta, Nilo, la Posada, Hulda, la Torre, Ofidia, Baldo, la Maestra de Moldes, el Flaco Ruiz y el Gremio). `probar.mjs`: 70 de 70.
- El jefe, **la Hidra del Coro** (cuerpo de tubos de órgano, cinco cabezas que cantan): ficha, retrato, cuerpo (`aa188968…`) y hoja (`4da49cc7…`); insignia «Directora del Archivo» y la **Partitura del Coro** (otra parte de la melodía del Vidriero).
- Sin personajes nuevos: Ceci, Clave, Bemol, Don Cedro y Gheco.

### El Acto IV (2026-11-11)

- `cursos/csharp/04-el-archivo-mudo.md`: 7 nodos, 35 micro-misiones y 7 encargos (Hilván, Elefa, Tizón, Zed, Baldo, Nima y el Gremio). `probar.mjs`: 49 de 49.
- Lo que se probó en el ejecutor antes de escribir: `System.Text.Json` anda (las tildes salen como `\u00ED`: el acto usa datos sin tilde en los JSON y lo avisa en «Errores habituales»), los mensajes de las excepciones de .NET salen en inglés (por eso se muestra `e.GetType().Name` y no `e.Message`, salvo en las excepciones propias), `FileNotFoundException` trae una ruta al azar, y la carpeta de mentira empieza vacía en cada ejecución (cada micro-misión escribe y lee en el mismo programa).
- El jefe, **el Liche del Archivo Mudo**: ficha escrita; insignia «Guardiana de la Memoria» y el **Compás Perdido** (otra parte de la melodía del Vidriero). Con retrato, cuerpo y hoja; los tres ítems de jefe (Cuerda de la Quimera, Partitura del Coro y Compás Perdido) ya tienen imagen. Desde el Acto IV las escenas van en un proyecto de Stitch propio, «Conservatorio - Actos IV y V» (`9034180179663220768`), porque en el de los Talleres cada pedido se cortaba por tiempo; ahí están subidas las hojas de los personajes que aparecen.
- Sin personajes nuevos.

### El Acto V (aprobado por el docente el 2026-11-11: emular los cuatro temas; el jefe, el Eco de la Ventanilla)

Material 21 a 24: asincronía, pruebas con xUnit, SQLite y API web. Lo que se probó en el ejecutor antes de proponer:

| Tema | En el navegador hoy | Propuesta |
|---|---|---|
| 21 · `async`/`await` | anda: `Task.Delay`, `Task.WhenAll` (tres esperas de 300 ms tardan 300, no 900), `Task.Run`, cancelación. No hay `Parallel` ni hilos de verdad: todo corre en uno, y la «carrera» de diez aprendices con `c++` siempre da bien | se enseña tal cual. La carrera se muestra con `await Task.Yield()` entre leer y escribir (pierde aplausos siempre igual, sin azar) y se arregla con `SemaphoreSlim`; `Parallel` se nombra en la teoría |
| 22 · xUnit | la reflexión con atributos anda (un `[Fact]` propio se descubre y se corre) | una **xUnit de mentira** que viene puesta: `[Fact]`, `[Theory]`/`[InlineData]`, `Assert.Equal/True/False/Throws/Contains/Null`, y al terminar el programa corre las pruebas y muestra `✓`/`✗` y «Pasaron 3 de 4», como `dotnet test`. El código del alumno es el mismo que en un proyecto real |
| 23 · SQLite | no hay `System.Data` ni `Microsoft.Data.Sqlite` | **la Bóveda**: una `Microsoft.Data.Sqlite` de mentira (`SqliteConnection`, `CreateCommand`, `CommandText`, `Parameters.AddWithValue`, `ExecuteNonQuery`, `ExecuteScalar`, `ExecuteReader` con `Read`/`GetString`/`GetInt32`, transacciones) que por dentro usa el mismo SQLite en WebAssembly de las micro-misiones de SQL (`sql.js`, que es sincrónico), en el mismo worker y con una base vacía en memoria en cada ejecución. Sin red y sin disco |
| 24 · API web | ASP.NET necesita un servidor | **la ventanilla**: `WebApplication.CreateBuilder().Build()`, `app.MapGet/MapPost/MapPut/MapDelete`, `Results.Ok/NotFound/Created/BadRequest` con la forma de las *minimal APIs*, y en vez de `app.Run()`, pedidos de mentira (`await app.PedirAsync("GET", "/instrumentos/2")`) que muestran el código de estado y el JSON, como el Puerto de JS |

**Cómo quedó armado (hecho, 2026-11-11):** la xUnit, la Bóveda y la ventanilla están en `scripts/csharp-runner/Prelude/` (`Xunit.cs`, `Sqlite.cs`, `Ventanilla.cs`). El ejecutor las compila **una sola vez**, al cargar, como la biblioteca `Conservatorio.Prelude` (compilarlas en cada ejecución costaba 2 s), y el programa del alumno la usa como una referencia más. Los `using` globales suman `System.Net.Http`, `System.Net.Http.Json`, `Microsoft.AspNetCore.Builder` y `Microsoft.AspNetCore.Http`, como en un proyecto web; `Xunit` y `Microsoft.Data.Sqlite` se escriben a mano, como en uno de verdad. Un archivo que solo tiene pruebas (sin programa principal, CS5001) se compila como biblioteca, y al terminar cualquier programa se corren sus `[Fact]`/`[Theory]`. La Bóveda le habla en el acto al `sql.js` del worker (`globalThis.csharpSql`, que se baja solo si el código usa `Sqlite`), con una base vacía por ejecución; los errores salen como en la de verdad (`SQLite Error 1: 'no such table: t'.`). La ventanilla contesta 404 si la ruta no existe, 405 si existe con otro verbo, 400 si el JSON no sirve y 500 con el nombre de la excepción si el manejador se rompe; el JSON va en camelCase y con tildes legibles. Para la carrera sin hilos: `await Task.Yield()` entre leer y escribir pierde aplausos siempre igual (100 de 1000), y `SemaphoreSlim` la arregla. `probar-ejecutor.mjs`: 25 de 25; `probar.mjs`: 308 de 308. El código del alumno sigue sin salir del navegador.

**Nodos (unos 7, uno por idea):** R05-N01 esperar sin trabar (`async`/`await`, `Task.Delay`) · N02 todas juntas (`WhenAll`, `WhenAny`, cancelar) · N03 la carrera y el candado (`SemaphoreSlim`) · N04 ensayar con pruebas (`[Fact]`, `Assert`) · N05 la Bóveda (crear tabla, insertar con parámetros, leer) · N06 buscar, actualizar y transacciones · N07 la ventanilla (rutas, verbos, códigos) · y el jefe R05-N08.

**El jefe:** la tabla de la historia dice «la Sirena de la Red», pero PHP ya tiene a **la Sirena de los Tipos Débiles** (R01-N10). Para no repetir criatura, se propone otro: **el Eco de la Ventanilla**, un espíritu hecho de cartas y campanillas que contesta antes de que le pregunten (pedidos sin `await`, rutas que no existen, datos sin validar). Necesita ficha, retrato, cuerpo y hoja.

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
| La tienda de Don Cedro, el luthier | hecho (fase 2, 2026-11-08): ficha, retrato y cuerpo (`36d7ce93…`), hoja (`cddb912e…`) en el proyecto de la Feria; aparece en el Taller de Instrumentos (R02) |
| Expediciones y mapa | hecho: `public/img/mundos/conservatorio/mapa.webp` (proyecto de Stitch «Conservatorio - mapa», sin letras) y 9 lugares del Acto I; los de los actos II a V se suman con sus nodos (en el mapa ya están el taller del luthier, la torre del archivo con la bóveda y la arena) |
| Montura e ítems del Conservatorio | hecho: **Trino** (`public/img/monturas/trino/n1…n5`, del pajarito de notas al fénix de partituras); 16 ítems del taller y el Diapasón Verde (lo deja el Slime) con imagen: `php artisan app:item-images cursos/csharp/items --apply`, **falta en producción**; 4 recetas |
| Jefe del bloque (Slime Desafinado) y el resto de los nodos | Acto I **hecho** (2026-11-07); siguen los actos II a V (§ 2 bis) |
| Temporada en las Crónicas en Inglés | **pendiente**: cuando el curso esté más avanzado |
| Copia de las imágenes en `publicidad/logos cursos/personajes/` | **pendiente** |
