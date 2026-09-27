# CLAUDE.md

Plataforma de cursos de programación de uso personal (un docente, alumnos por comisiones). Laravel + Livewire + Tailwind + MariaDB, CodeMirror 6 y Pyodide en el navegador.

## Documentos
- [docs/GAMIFICACION.md](docs/GAMIFICACION.md) — decisiones del modelo (cerrado el 2026-09-27; ESPECIFICACION y PLAN ya lo incorporan): árbol con nodos y hojas, monedas, XP, insignias, ranking, CV. La gamificación pasó a ser el eje (antes estaba fuera de alcance). Primer curso: Python.
- [docs/ESPECIFICACION.md](docs/ESPECIFICACION.md) — qué hay que construir (fuente de verdad funcional).
- [docs/PLAN.md](docs/PLAN.md) — cómo: estructura, migraciones, rutas, componentes, decisiones y preguntas abiertas.
- [docs/DISENO.md](docs/DISENO.md) — análisis de las referencias visuales y tokens de diseño.
- [docs/IDENTIDAD-VISUAL.md](docs/IDENTIDAD-VISUAL.md) — marca GhecoSoft-Code (geco), paleta "DevLevel Obsidian", tipografías.
- [docs/ARBOL-HABILIDADES.md](docs/ARBOL-HABILIDADES.md) — forma y dibujo del árbol (radial tipo PoE + estilo del grafo de `force-graph`; § 6–8 mandan).
- [docs/CURSOS-EXISTENTES.md](docs/CURSOS-EXISTENTES.md) — el material de `/home/djmov/Programas/Cursos/FullCursos/` y cómo se traduce a cursos, unidades y clases. Esa carpeta es solo lectura: no se modifica desde este proyecto.

## Reglas de trabajo
- Trabajar por fases (ver PLAN.md § 9) y **frenar al final de cada una** para que el docente pruebe. No arrancar una fase sin su OK.
- Commits chicos y descriptivos por funcionalidad.
- Interfaz en **español rioplatense** ("Continuá", "Entregá tu tarea"); código, nombres de rutas, clases y columnas en **inglés**. URIs visibles en español.
- Si una decisión cambia, actualizar PLAN.md (tabla de decisiones) en el mismo commit.

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
- `php artisan migrate:fresh --seed` — base local con admin/admin123, cliente/cliente123 y el curso demo de Python
- `npm run build` — assets para producción
- `vendor/bin/pint` — formato del código
- `php artisan app:create-admin` — crear el admin en producción

## Convenciones del código
- Monedas y XP: solo `App\Services\Ledger`. Acceso al árbol: `App\Services\TreeAccess`. Abrir nodos: `NodeUnlocker`. Aprobar pagos: `EnrollmentApprover`. Editar el árbol (crear, mover, borrar, duplicar): `TreeEditor`; orden por arrastre: `App\Support\Reorder` + `wire:sort`.
- Textos narrativos con `term('clave', $course, $cantidad)` (diccionario), nunca escritos a mano en las vistas.
- Estados y tipos como PHP enums (`app/Enums`) con `label()` en español.
- Los modelos declaran en `$attributes` los mismos valores por defecto que la base.
- Tests en estilo Pest; helpers `makeCourse()`, `enrolledStudent()`, `approveRequiredPractices()` en `tests/Pest.php`.
