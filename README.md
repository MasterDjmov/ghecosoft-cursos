# GhecoSoft-Code

Plataforma de cursos de programación **gamificada** de un docente. El alumno avanza por un **árbol de habilidades** (estilo Path of Exile):

- abre cada tema con **monedas**;
- gana esas monedas con **prácticas aprobadas** por el docente;
- suma **XP**, niveles e insignias;
- puede compartir un **CV público**.

Primer curso: **Python**, que se ejecuta en el navegador con Pyodide.

## Stack

- **Laravel 13 + Livewire 4 + Flux**, **Tailwind 4** (tema oscuro "DevLevel Obsidian") y **MariaDB**.
- **CodeMirror 6** (editor), **Pyodide** en un Web Worker (Python en el navegador, corte a los 5 s) y **force-graph** (el árbol dibujado).
- **Pest 4** para los tests.
- Pensado para hosting compartido (cPanel, PHP 8.3): sin workers ni colas. El código de los alumnos **nunca** se ejecuta en el servidor.

## Empezar en local

Requisitos: PHP 8.3, Composer, Node 20 y MariaDB.

```bash
composer install
npm install
cp .env.example .env && php artisan key:generate
# crear las bases ghecosoft_code y ghecosoft_code_testing, y completar DB_* en .env
php artisan migrate:fresh --seed
php artisan storage:link
composer run dev              # o: php artisan serve + npm run dev
```

Usuarios de prueba (solo en desarrollo):

| Usuario | Clave | Rol |
|---|---|---|
| `admin` | `admin123` | docente |
| `cliente` | `cliente123` | alumno, con la inscripción aprobada al curso demo |

## Comandos

| Comando | Para qué |
|---|---|
| `php artisan test` | Suite Pest (usa la base `ghecosoft_code_testing`) |
| `vendor/bin/pint` | Formato del código |
| `npm run build` | Assets de producción |
| `php artisan app:create-admin` | Crear el docente en producción |
| `php artisan db:seed --class=ProductionSeeder` | Datos mínimos en producción (sin usuarios de prueba) |

## Recorrido

**Alumno:**

1. Se registra y pide la inscripción (comprobante o WhatsApp).
2. Cuando el docente aprueba, recibe las monedas y 30 días de abono.
3. Abre la clase 0 y el árbol, lee y ejecuta los ejemplos, y entrega las prácticas.
4. Cada aprobación le paga monedas y XP, que abren el nodo siguiente.
5. Ve su lugar en el ranking y su CV.

**Docente:**

- arma cursos y árboles (ramas, nodos, hojas, recursos);
- aprueba solicitudes y corrige entregas (Aprobada / Rehacer);
- ajusta monedas y XP con motivo;
- administra el diccionario narrativo, los niveles, las insignias y las autorizaciones de menores.

## Documentación

| Documento | Contenido |
|---|---|
| [docs/ESPECIFICACION.md](docs/ESPECIFICACION.md) | Qué hace la plataforma (fuente de verdad funcional) |
| [docs/PLAN.md](docs/PLAN.md) | Decisiones técnicas, modelo de datos, rutas y fases |
| [docs/GAMIFICACION.md](docs/GAMIFICACION.md) | Reglas del juego: monedas, XP, abono, ranking, CV, menores |
| [docs/ARBOL-HABILIDADES.md](docs/ARBOL-HABILIDADES.md) | Forma y dibujo del árbol |
| [docs/IDENTIDAD-VISUAL.md](docs/IDENTIDAD-VISUAL.md) · [docs/DISENO.md](docs/DISENO.md) | Marca, paleta y tipografías |
| [docs/DEPLOY.md](docs/DEPLOY.md) | Cómo subirlo al servidor (cPanel) |
| [CLAUDE.md](CLAUDE.md) | Reglas de trabajo y convenciones del código |
