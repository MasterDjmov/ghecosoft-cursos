# CLAUDE.md

Plataforma de cursos de programación de uso personal (un docente, alumnos por comisiones). Laravel + Livewire + Tailwind + MariaDB, CodeMirror 6 y Pyodide en el navegador.

## Documentos
- [docs/GAMIFICACION.md](docs/GAMIFICACION.md) — decisiones del modelo (cerrado el 2026-09-27; ESPECIFICACION y PLAN ya lo incorporan): árbol con nodos y hojas, monedas, XP, insignias, ranking, CV. La gamificación pasó a ser el eje (antes estaba fuera de alcance). Primer curso: Python.
- [docs/ESPECIFICACION.md](docs/ESPECIFICACION.md) — qué hay que construir (fuente de verdad funcional).
- [docs/PLAN.md](docs/PLAN.md) — cómo: estructura, migraciones, rutas, componentes, decisiones y preguntas abiertas.
- [docs/DISENO.md](docs/DISENO.md) — análisis de las referencias visuales y tokens de diseño.
- [docs/IDENTIDAD-VISUAL.md](docs/IDENTIDAD-VISUAL.md) — marca GhecoSoft-Code (geco), paleta "DevLevel Obsidian", tipografías.
- [docs/ARBOL-HABILIDADES.md](docs/ARBOL-HABILIDADES.md) — forma y dibujo del árbol (radial tipo PoE + estilo del grafo de `force-graph`; § 6–8 mandan).
- [docs/super-prompt-v2-curso-python.md](docs/super-prompt-v2-curso-python.md) — el prompt con el que Claude online diseña el curso de Python (reglas pedagógicas, plantilla de nodo, Sendas). Lo que pide define las fases 6–9 de PLAN § 9.
- [docs/FORMATO-CURSO.md](docs/FORMATO-CURSO.md) — formato Markdown para importar un curso entero (IDs estables, secciones, prácticas, diccionario). Ejemplo probado en `tests/Fixtures/curso-ejemplo.md`.
- [docs/HISTORIA-BRIEF.md](docs/HISTORIA-BRIEF.md) — resumen del sistema que se le pasa a Claude online para definir la historia del curso de Python (el primero en salir). Actualizarlo si cambian el diccionario, la economía o dónde se muestra la historia.
- [cursos/python/](cursos/python/), [cursos/c/](cursos/c/), [cursos/cpp/](cursos/cpp/), [cursos/java/](cursos/java/) y [cursos/php/](cursos/php/) — los cursos de Python, C, C++, Java y PHP en el formato del importador (los carga el seeder local; se reimportan sin tocar el progreso). Se editan ahí y se reimportan.
- [docs/IDEAS-GAMIFICACION.md](docs/IDEAS-GAMIFICACION.md) — análisis de lo bueno, lo malo y un abanico de mejoras (respuesta inmediata, pistas, retos cortos, ligas, logros). **Revisar y decidir antes de subir a producción.**
- [docs/SIMULACION.md](docs/SIMULACION.md) — el "súper test": `app:simulate-course` hace cursar un curso entero a 5 alumnos con el docente corrigiendo, y revisa economía, aperturas, insignias y fin del curso. Se corre con cada curso nuevo antes de abrirlo.
- [docs/CURSOS-EXISTENTES.md](docs/CURSOS-EXISTENTES.md) — el material de `/home/djmov/Programas/Cursos/FullCursos/` y cómo se traduce a cursos, unidades y clases. Esa carpeta es solo lectura: no se modifica desde este proyecto.

## Reglas de trabajo
- Trabajar por fases (ver PLAN.md § 9) y **frenar al final de cada una** para que el docente pruebe. No arrancar una fase sin su OK.
- Commits chicos y descriptivos por funcionalidad.
- Interfaz en **español rioplatense** ("Continuá", "Entregá tu tarea"); código, nombres de rutas, clases y columnas en **inglés**. URIs visibles en español.
- Si una decisión cambia, actualizar PLAN.md (tabla de decisiones) en el mismo commit.
- **Todo se diseña para cualquier lenguaje** (D39): Python es el primer curso, pero secciones, prácticas, Sendas, monedas, jefes, importador e historia no pueden depender de Python (salvo el ejecutor del navegador).

## Reglas que no se rompen
- El código del alumno **nunca** se ejecuta en el servidor. Python corre con Pyodide en un Web Worker (timeout 5 s); C y C++, solo para el docente al corregir, con Clang en WebAssembly en su navegador (D66); PHP, igual, con PHP 8.3 en WebAssembly (D68); Java, en la compu del docente con `scripts/JavaRunner.java` abierto (D69) o con el comando que arma la entrega (D67).
- Qué puede ver y hacer un alumno (nodo abierto, abono vigente) se calcula **en cada request**; **no** usar cron para abrir ni vencer nada.
- Comprobantes, entregas, apuntes y autorizaciones de menores van al disco privado y se sirven solo por controladores con `authorize()`.
- Un alumno nunca ve nodos que no abrió, cursos cuyo raíz no abrió ni entregas ajenas; con el abono vencido no abre ni entrega. Toda regla nueva de acceso va con Policy + test Pest.
- Toda moneda y todo XP pasa por un **único servicio con libro de movimientos**; nunca se suma un saldo "a mano".
- Hosting compartido (cPanel/CloudLinux, servidor `mate`): PHP **8.3**, MariaDB, Node 20 (build por SSH; hay "Setup Node.js App" pero esta plataforma no lo usa), sin workers, sin PostgreSQL. `QUEUE_CONNECTION=sync`. `composer.json` fija `platform.php = 8.3.33`.
- Fuera de alcance (por ahora): pagos online, certificados, foros, quizzes, corrección automática, ejecución de C/C++/Java/PHP. La **gamificación y el abono de 30 días SÍ están dentro** (ver GAMIFICACION.md).

## Comandos
- `composer run dev` — servidor + Vite en desarrollo (o `php artisan serve` + `npm run dev`)
- `php artisan test` — suite Pest (usa la base `ghecosoft_code_testing`, MariaDB)
- `php artisan migrate:fresh --seed` — base local con admin/admin123, cliente/cliente123 y los cursos de Python, C, C++, Java y PHP importados de `cursos/`
- `npm run build` — assets para producción
- `vendor/bin/pint` — formato del código
- `php artisan app:import-course carpeta/ [--apply]` — revisar (o importar con `--apply`) un curso en el formato de FORMATO-CURSO.md; también desde *Admin → Cursos → Importar*
- `php artisan app:simulate-course python [--reset]` — súper test local: 5 alumnos cursan todo y el docente corrige (docs/SIMULACION.md)
- `php artisan app:create-admin` — crear el admin en producción
- `php artisan db:seed --class=ProductionSeeder` — datos mínimos en producción (nunca `db:seed` a secas). Deploy: [docs/DEPLOY.md](docs/DEPLOY.md)
- `scripts/build-cpp-toolchain.sh` — arma `public/toolchains/cpp/` (biblioteca de C++ con excepciones + PCH) para que el docente ejecute C/C++ al corregir (D66); una vez, o al cambiar las versiones de `resources/js/runners/cpp-config.js`
- `scripts/build-php-toolchain.sh` — copia PHP 8.3 en WebAssembly (de `node_modules/@php-wasm/web-8-3`) a `public/toolchains/php/` para ejecutar PHP al corregir (D68); lo corre solo `deploy.sh`
- `java scripts/JavaRunner.java` — ejecutor local de Java: dejarlo abierto mientras se corrige para que *Ejecutar* ande en las entregas de Java (D69; escucha solo en 127.0.0.1:17017)
- `scripts/deploy.sh [--cursos]` — actualizar producción desde la compu (el servidor no puede compilar los assets: se compilan acá y se sube `public/build/`)

## Convenciones del código
- Monedas y XP: solo `App\Services\Ledger` (para mostrarlos por curso y con su detalle: `Support\MovementFeed` + `<livewire:movement-feed>`). Acceso al árbol: `App\Services\TreeAccess`. Abrir nodos: `NodeUnlocker`. Aprobar pagos: `EnrollmentApprover`. Cuentas creadas por el docente y reseteo de clave: `StudentAccounts`. Editar el árbol (crear, mover, borrar, duplicar): `TreeEditor`; entregar: `PracticeSubmitter` (en Livewire, el trait `WorksOnPractice`, que comparten la tarjeta del nodo y el modo misión); corregir y pagar: `SubmissionReviewer`; consultas por práctica: `PracticeMessenger` (+ `<livewire:practice-chat>`, Policy `PracticeMessagePolicy`); avisos en vivo: la campanita + `resources/js/live-alerts.js`; rankings (y top/tendencia de la landing): `Ranking`; cursos Próximamente y "Avisame": `CourseCatalog`; importar cursos: `CourseImporter` (+ `Support\CourseImport`); toda subida de archivos lleva la regla `App\Rules\SafeUpload` (contenido = extensión, nada ejecutable); límites de intentos de los formularios de cuenta: `ThrottleAuthForms`; avisos: `PlatformNotification`; orden por arrastre: `App\Support\Reorder` + `wire:sort`.
- Textos narrativos con `term('clave', $course, $cantidad)` (diccionario), nunca escritos a mano en las vistas. La compañía que presenta cada sección del nodo sale de `companion.theory|uses|errors|guild` (`<x-companion>`).
- Textos narrativos del curso para el alumno: `Narrative::render()` (reemplaza `{heroe}`, `{mentor}`, `{mundo}`, `{region}` y pasa a markdown); historia del diccionario con `Story::get()`.
- Soluciones del docente (`nodes.teacher_solutions`, `practices.reference_solution`) van en `$hidden` y nunca se renderizan en vistas del alumno; hay test que lo verifica.
- Estados y tipos como PHP enums (`app/Enums`) con `label()` en español.
- Los modelos declaran en `$attributes` los mismos valores por defecto que la base.
- Tests en estilo Pest; helpers `makeCourse()`, `enrolledStudent()`, `approveRequiredPractices()` en `tests/Pest.php`.
