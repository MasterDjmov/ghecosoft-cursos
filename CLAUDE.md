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
- [cursos/python/](cursos/python/) — el curso de Python en el formato del importador (lo carga el seeder local; se reimporta sin tocar el progreso). Se edita ahí y se reimporta.
- [docs/CURSOS-EXISTENTES.md](docs/CURSOS-EXISTENTES.md) — el material de `/home/djmov/Programas/Cursos/FullCursos/` y cómo se traduce a cursos, unidades y clases. Esa carpeta es solo lectura: no se modifica desde este proyecto.

## Reglas de trabajo
- Trabajar por fases (ver PLAN.md § 9) y **frenar al final de cada una** para que el docente pruebe. No arrancar una fase sin su OK.
- Commits chicos y descriptivos por funcionalidad.
- Interfaz en **español rioplatense** ("Continuá", "Entregá tu tarea"); código, nombres de rutas, clases y columnas en **inglés**. URIs visibles en español.
- Si una decisión cambia, actualizar PLAN.md (tabla de decisiones) en el mismo commit.
- **Todo se diseña para cualquier lenguaje** (D39): Python es el primer curso, pero secciones, prácticas, Sendas, monedas, jefes, importador e historia no pueden depender de Python (salvo el ejecutor del navegador).

## Reglas que no se rompen
- El código del alumno **nunca** se ejecuta en el servidor. Python corre con Pyodide en un Web Worker (timeout 5 s).
- Qué puede ver y hacer un alumno (nodo abierto, abono vigente) se calcula **en cada request**; **no** usar cron para abrir ni vencer nada.
- Comprobantes, entregas, apuntes y autorizaciones de menores van al disco privado y se sirven solo por controladores con `authorize()`.
- Un alumno nunca ve nodos que no abrió, cursos cuyo raíz no abrió ni entregas ajenas; con el abono vencido no abre ni entrega. Toda regla nueva de acceso va con Policy + test Pest.
- Toda moneda y todo XP pasa por un **único servicio con libro de movimientos**; nunca se suma un saldo "a mano".
- Hosting compartido (cPanel/CloudLinux, servidor `mate`): PHP **8.3**, MariaDB, Node 20 (build por SSH; hay "Setup Node.js App" pero esta plataforma no lo usa), sin workers, sin PostgreSQL. `QUEUE_CONNECTION=sync`. `composer.json` fija `platform.php = 8.3.33`.
- Fuera de alcance (por ahora): pagos online, certificados, foros, quizzes, corrección automática, ejecución de C/C++/Java. La **gamificación y el abono de 30 días SÍ están dentro** (ver GAMIFICACION.md).

## Comandos
- `composer run dev` — servidor + Vite en desarrollo (o `php artisan serve` + `npm run dev`)
- `php artisan test` — suite Pest (usa la base `ghecosoft_code_testing`, MariaDB)
- `php artisan migrate:fresh --seed` — base local con admin/admin123, cliente/cliente123 y el curso de Python importado de `cursos/python/`
- `npm run build` — assets para producción
- `vendor/bin/pint` — formato del código
- `php artisan app:import-course carpeta/ [--apply]` — revisar (o importar con `--apply`) un curso en el formato de FORMATO-CURSO.md; también desde *Admin → Cursos → Importar*
- `php artisan app:create-admin` — crear el admin en producción
- `php artisan db:seed --class=ProductionSeeder` — datos mínimos en producción (nunca `db:seed` a secas). Deploy: [docs/DEPLOY.md](docs/DEPLOY.md)

## Convenciones del código
- Monedas y XP: solo `App\Services\Ledger`. Acceso al árbol: `App\Services\TreeAccess`. Abrir nodos: `NodeUnlocker`. Aprobar pagos: `EnrollmentApprover`. Cuentas creadas por el docente y reseteo de clave: `StudentAccounts`. Editar el árbol (crear, mover, borrar, duplicar): `TreeEditor`; entregar: `PracticeSubmitter` (en Livewire, el trait `WorksOnPractice`, que comparten la tarjeta del nodo y el modo misión); corregir y pagar: `SubmissionReviewer`; rankings (y top/tendencia de la landing): `Ranking`; cursos Próximamente y "Avisame": `CourseCatalog`; importar cursos: `CourseImporter` (+ `Support\CourseImport`); toda subida de archivos lleva la regla `App\Rules\SafeUpload` (contenido = extensión, nada ejecutable); límites de intentos de los formularios de cuenta: `ThrottleAuthForms`; avisos: `PlatformNotification`; orden por arrastre: `App\Support\Reorder` + `wire:sort`.
- Textos narrativos con `term('clave', $course, $cantidad)` (diccionario), nunca escritos a mano en las vistas. La compañía que presenta cada sección del nodo sale de `companion.theory|uses|errors|guild` (`<x-companion>`).
- Textos narrativos del curso para el alumno: `Narrative::render()` (reemplaza `{heroe}`, `{mentor}`, `{mundo}`, `{region}` y pasa a markdown); historia del diccionario con `Story::get()`.
- Soluciones del docente (`nodes.teacher_solutions`, `practices.reference_solution`) van en `$hidden` y nunca se renderizan en vistas del alumno; hay test que lo verifica.
- Estados y tipos como PHP enums (`app/Enums`) con `label()` en español.
- Los modelos declaran en `$attributes` los mismos valores por defecto que la base.
- Tests en estilo Pest; helpers `makeCourse()`, `enrolledStudent()`, `approveRequiredPractices()` en `tests/Pest.php`.
