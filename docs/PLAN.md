# Plan técnico

> Reescrito el 2026-09-27 con el modelo gamificado. Basado en [ESPECIFICACION.md](ESPECIFICACION.md) y [GAMIFICACION.md](GAMIFICACION.md).
> **Estado:** aprobado por el docente. Fases 1 a 4 terminadas (2026-09-27). **Fase 5 terminada (2026-09-27)**: plataforma completa según el plan. **Etapa actual: pulido de detalles** con el docente; el deploy queda para después (ver § 10).

---

## 0. Entorno verificado

| | Local | Servidor `mate` (cPanel, CloudLinux) |
|---|---|---|
| PHP | 8.4.26 | **8.3.33** + OPcache. Extensiones ✅: pdo_mysql (`nd_pdo_mysql`), mbstring, fileinfo, openssl, tokenizer, xml, ctype, curl, zip, gd, intl, bcmath |
| Composer | 2.9.5 | 2.8.12 |
| Node / npm | 20.20 / 10.8 | 20.20.2 / 10.8.2 (por línea de comandos; también hay "Setup Node.js App", que no se usa) |
| MariaDB | 10.11 (bases `ghecosoft_code` y `ghecosoft_code_testing`) | ✅ |
| PostgreSQL | — | ❌ |

- **Compatibilidad de versiones:** `composer.json` fija `"config": {"platform": {"php": "8.3.33"}}` para que el lock sirva en los dos lados.
- **Deploy:** `git pull` → `composer install --no-dev` → `npm ci && npm run build` → `php artisan migrate --force` → `optimize` (detalle en `DEPLOY.md`, Fase 5).

---

## 1. Decisiones técnicas

| # | Tema | Decisión | Por qué |
|---|---|---|---|
| D1 | Archivos privados | Comprobantes, entregas, apuntes y autorizaciones en `private`; se sirven con controladores que llaman a `authorize()` | Nada sensible por URL directa |
| D2 | Archivos públicos | Portadas, logos de curso, íconos del diccionario, avatares y logo de la plataforma en `public` (`storage:link`) | No son sensibles |
| D3 | Zona horaria | `America/Argentina/Buenos_Aires` | Abonos y fechas en hora local |
| D4 | Markdown | `league/commonmark` + GFM. **Contenido de nodos**: HTML con lista blanca (`details`, `summary`, `kbd`, `br`). **Comentarios**: todo el HTML escapado. Resaltado con highlight.js | XSS + respeta el material existente |
| D5 | Pyodide | Desde CDN jsDelivr (URL configurable). Timeout de 5 s → `worker.terminate()` y worker nuevo | Pesa ~10 MB |
| D6 | `CodeRunner` | En JS, un registro de runners por lenguaje; en PHP, la interfaz `CodeRunner` + `NullCodeRunner` | Servicio externo futuro |
| D7 | Enums | Columnas `string` + **PHP enums** casteados | Más fácil de extender que `ENUM` de MariaDB |
| D8 | Monedas y XP | **Libro de movimientos** (`coin_transactions`, `xp_transactions`) escrito **solo** por `App\Services\Ledger`, dentro de transacciones con bloqueo de fila del usuario (`lockForUpdate`). `users.xp_total` es una caché que mantiene el mismo servicio | Nada de saldos sumados "a mano" (lección de La Rioja Aprende) |
| D9 | Acceso | `App\Services\TreeAccess` decide en cada request: raíz abierto, nodo abierto, abono vigente, requisitos cumplidos. Lo usan las Policies | Un solo lugar, sin cron |
| D10 | Textos narrativos | `App\Support\Glossary` + helper `term('coin.course', $course, count: 3)` con caché por curso | Diccionario editable en el admin |
| D11 | Login | Usuario **o** email (se ajusta Fortify con `authenticateUsing`) | Pedido del docente |
| D12 | Componentes | Livewire basados en clase (`app/Livewire/...`); las pantallas del starter kit se re-estilizan | Testeables |
| D13 | Árbol gráfico | `force-graph` con `dagMode: 'radialout'`, posiciones fijas (`pos_x`/`pos_y`), import dinámico solo en esa página | Forma PoE + estilo del mapa escolar |
| D14 | Tests | Pest contra **MariaDB** (`ghecosoft_code_testing`) | Mismo motor que producción |
| D16 | Pest | **Pest 4** (Pest 5 exige PHP 8.4 y el servidor tiene 8.3). Con la plataforma fijada en 8.3.33, Symfony quedó en 7.4 | Mismo `composer.lock` en local y servidor |
| D17 | Verificación de email | **Desactivada** (sin `MustVerifyEmail`); la cuenta se usa apenas se registra | Hosting con SMTP opcional; el docente valida en la clase inicial |
| D18 | Fuentes | Inter, Space Grotesk y JetBrains Mono **autoalojadas** por el plugin de Vite (sin CDN en tiempo de ejecución) | Privacidad y velocidad |
| D15 | Mail | Canal `mail` solo si hay SMTP configurado; `QUEUE_CONNECTION=sync` | Hosting sin workers |
| D19 | Insignia del jefe | `nodes.badge_id` (nulo): el jefe elige qué insignia entrega | G7: cada jefe da una insignia |
| D20 | Borrados en el editor | No se borra el raíz, un nodo con dependientes, un nodo/hoja con actividad de alumnos, una rama con nodos ni un curso con alumnos: se **despublica** | No perder el historial de nadie |
| D21 | Nombres de niveles | Van al diccionario como `level.{n}` (se editan desde *Niveles*); sin valor, "Nivel n" | Una sola fuente para los textos |
| D23 | Árbol dibujado | `force-graph` en canvas (import dinámico, solo en la página del árbol) con **posiciones fijas**: cada rama en su sector y la distancia al centro según la profundidad (pasos desde el raíz). El docente arrastra nodos para retocar (`pos_x`/`pos_y`) o usa "Reacomodar". Vista **Lista / Árbol** en el editor; el alumno usa el mismo módulo en la Fase 3 | Estética del mapa escolar + forma PoE (ARBOL-HABILIDADES § 8) |
| D24 | Pyodide | **v0.29.5** (Python 3.13) desde jsDelivr (`PYODIDE_URL`); el reloj de 5 s arranca cuando Python ya cargó (la primera descarga no cuenta) | La primera carga tarda según la conexión |
| D25 | Qué ve el alumno de un nodo cerrado | Nombre, tipo, precio y por qué está bloqueado; **nunca** el contenido ni las consignas (sus hojas aparecen como "?"). Un nodo sin publicar y sin abrir no aparece | Gamificación visible sin filtrar contenido |
| D26 | Renovación | Se puede pedir con el abono vencido o a 7 días de vencer; los días nuevos se suman al final | Evita pedidos duplicados |
| D27 | XP extra | `config/game.php`: nodo completo +20, jefe vencido +50 (una sola vez cada uno, además de la XP de las hojas) | Premia cerrar nodos y ramas |
| D28 | "Marcar como completada" | En una hoja **sin entrega** cuenta como aprobada (paga lo que tenga). En las demás es una marca personal que no aprueba nada | Así "Instalá Python" puede ser obligatoria |
| D29 | Entregas | Nueva entrega solo con el nodo abierto, abono vigente, sin otra esperando corrección y sin haberla aprobado; el primer aprobado de cada hoja paga, los siguientes no | Intentos ilimitados sin duplicar pagos |
| D30 | Notificaciones | Una sola clase `PlatformNotification` (título, texto, link, ícono) en base de datos + mail si hay SMTP; campanita con consulta cada 60 s | Hosting sin workers ni websockets |
| D31 | Alumnos (admin) | Buscador y ficha con abonos, saldos, movimientos, entregas y **ajuste manual con motivo** (se adelantó a la Fase 4) | Lo pide la especificación y usa los mismos movimientos |
| D32 | Ranking | Por curso: XP ganada **en ese curso**, entre quienes tuvieron abono; global: solo perfiles públicos. Nombre + inicial del apellido, o apodo. Caché de 5 min que se limpia al sumar XP | Privacidad y justicia (G9) |
| D33 | Perfil público | Requiere fecha de nacimiento cargada; si es menor, la autorización aprobada. Sin eso el tilde está deshabilitado | G10 + G12 |
| D34 | CV en PDF | Impresión del navegador ("Descargar PDF") con hoja de estilos de impresión, sin librerías de PDF en el servidor | Liviano para hosting compartido |
| D35 | Producción | `ProductionSeeder` (sin usuarios de prueba), `URL::forceHttps` en producción y el usuario no puede ser solo números (no es un DNI) | Seguridad del deploy |
| D22 | Archivos de recursos | Disco privado, se validan por **extensión** (lista en `config/uploads.php`) y se descargan con `nosniff` | `mimes` no reconoce `.py` (lo ve como texto) |

---

## 2. Modelo de datos

Todas las columnas en inglés. `→` = clave foránea.

### Usuarios y configuración

| Tabla | Columnas principales |
|---|---|
| `users` | name, last_name, **username** (unique), email (unique), password, role (`admin`\|`student`), phone?, dni? (unique), birth_date?, avatar?, xp_total (caché), nickname?, ranking_display (`name`\|`nickname`), cv_public (bool, false) |
| `guardian_authorizations` | → user, file_path, original_name, status (`pending`\|`approved`\|`rejected`), admin_note?, reviewed_at?, → reviewed_by? |
| `settings` | key (unique), value |
| `glossary_terms` | key, → course? (null = general), singular, plural?, gender (`f`\|`m`), icon_path?, short_description?, lore? — unique(key, course_id) |

### Cursos y árbol

| Tabla | Columnas principales |
|---|---|
| `courses` | title, slug, short_description, description, language, logo?, cover?, is_published, position, root_price (10), subscription_days (30) |
| `cohorts` | → course, name, modality, schedule_text?, starts_on?, is_open_for_enrollment |
| `branches` | → course, title, position, is_extra (bool) |
| `nodes` | → course, → branch? (null en el raíz), → parent? (nodo requisito), type (`root`\|`topic`\|`boss`\|`extra`), title, position, price, → price_currency? (null = moneda del curso), → badge? (jefes), video_url?, content?, example_code?, example_language?, expected_output?, sample_input?, pos_x?, pos_y?, is_published |
| `node_resources` | → node, type (`link`\|`file`), title, url?, file_path?, original_name?, position |
| `practices` (hojas) | → node, title, instructions, is_required, submission_mode (`code`\|`file`\|`both`\|`none`), allowed_extensions?, starter_code?, sample_input?, coin_reward, xp_reward, position |

- **Requisito de un nodo:** su `parent`. Para abrirlo, todas las obligatorias del `parent` tienen que estar aprobadas.
  - El primer nodo de cada rama tiene como `parent` al raíz, o al jefe de la rama anterior si las ramas son secuenciales.
  - El raíz no tiene `parent`.

### Economía

| Tabla | Columnas principales |
|---|---|
| `currencies` | code (unique), → course? (null = comodín), is_wildcard |
| `coin_transactions` | → user, → currency, amount (± entero), reason (`enrollment_grant`\|`practice_approved`\|`node_unlock`\|`manual_adjustment`\|`reversal`), → course?, source (morph)?, note?, → created_by?, created_at |
| `xp_transactions` | → user, amount, reason (`practice_approved`\|`node_completed`\|`boss_defeated`\|`manual_adjustment`\|`reversal`), → course?, source (morph)?, note?, → created_by?, created_at |
| `levels` | number (unique), xp_required |
| `badges` / `user_badges` | code, → course?, name, description, icon? / → user, → badge, awarded_at |

### Inscripción, abono y progreso

| Tabla | Columnas principales |
|---|---|
| `enrollment_requests` | → user, → course, → cohort?, kind (`new`\|`renewal`), type (`receipt`\|`contact`), receipt_path?, receipt_original_name?, message?, status (`pending`\|`approved`\|`rejected`), admin_note?, reviewed_at?, → reviewed_by? |
| `course_subscriptions` | → user, → course, → cohort?, starts_at, ends_at, → enrollment_request?, → granted_by? (una fila por abono o renovación) |
| `node_unlocks` | → user, → node, → currency?, price_paid, unlocked_at — unique(user, node) |
| `submissions` | → practice, → user, attempt, code?, file_path?, file_original_name?, status (`submitted`\|`approved`\|`redo`), submitted_at, reviewed_at?, → reviewed_by? — unique(practice, user, attempt) |
| `submission_comments` | → submission, → user, body |
| `practice_marks` | → user, → practice, completed_at — "Marcar como completada" del alumno |
| `course_completions` | → user, → course, completed_at, days_taken |
| `notifications` | estándar de Laravel |

---

## 3. Servicios clave

| Servicio | Responsabilidad |
|---|---|
| `Ledger` | `credit()`, `debit()` (falla si no hay saldo), `balance(user, currency)`, `addXp()`, `reverse()`. Todo en transacción con `lockForUpdate` sobre el usuario |
| `TreeAccess` | `hasActiveSubscription(user, course)`, `isRootOpen`, `isUnlocked(user, node)`, `canUnlock(user, node)` (requisitos + abono + saldo), `canView`, `canSubmit` |
| `NodeUnlocker` | Abre un nodo: valida con `TreeAccess`, debita con `Ledger`, crea `node_unlocks`. Todo junto o nada |
| `EnrollmentApprover` | Aprueba la solicitud: acredita monedas del curso (solo si `kind=new`) y crea el abono. Si es renovación, el abono nuevo arranca al vencer el actual o hoy, lo que sea posterior |
| `SubmissionReviewer` | Aprobar o marcar Rehacer. Al **primer** aprobado de una práctica paga moneda y XP (idempotente) y revisa si completó el nodo o venció al jefe |
| `Glossary` | Resuelve términos: curso → general → valor por defecto |

---

## 4. Rutas (URIs en español, nombres de ruta en inglés)

**Alumno** (`auth`):
- `/mundos` — mapa de cursos (inicio)
- `/cursos/{slug}` — detalle de un curso sin abrir
- `/cursos/{slug}/arbol` — árbol del curso
- `/cursos/{slug}/nodos/{node}` — un nodo
- `/ranking/{slug}`
- `/mi-cuenta`, `/mi-cuenta/movimientos`, `/mi-cuenta/privacidad`
- `/archivos/...` — descargas autorizadas

**Público:** `/cv/{username}`.

**Admin** (`auth`, `role:admin`, prefijo `/admin`):
- inicio;
- `solicitudes`, `alumnos`, `cursos` (+ editor del árbol), `entregas`, `diccionario`, `insignias`, `niveles`, `configuracion`, `autorizaciones`.

---

## 5. Estructura de carpetas (agregados sobre Laravel)

```
app/
├── Console/Commands/CreateAdmin.php
├── Contracts/CodeRunner.php
├── Enums/            Role, Language, NodeType, SubmissionMode, SubmissionStatus,
│                     RequestStatus, RequestKind, RequestType, CoinReason, XpReason, …
├── Http/Controllers/Files/   (descargas autorizadas)
├── Http/Middleware/EnsureRole.php
├── Livewire/Student/ … Livewire/Admin/ …
├── Models/
├── Policies/
├── Services/         Ledger, TreeAccess, NodeUnlocker, EnrollmentApprover, SubmissionReviewer
└── Support/Glossary.php (+ helper term())
resources/js/  editor/, runners/, workers/, tree/ (force-graph)
docs/          especificación, plan, gamificación, diseño, referencias/
```

---

## 6. Seeders (Fase 1)

| Usuario | Clave | Rol |
|---|---|---|
| `admin` (admin@ghecosoft.test) | `admin123` | admin |
| `cliente` (cliente@ghecosoft.test) | `cliente123` | alumno |

⚠️ Son **solo para desarrollo** (no cumplen la regla de contraseñas). En producción, el admin se crea con `app:create-admin`.

**Curso demo "Python":**
- raíz (clase 0) → rama "Fundamentos" (Comentarios → Variables → Jefe) y rama "Control" (Condicionales → Bucles → Jefe);
- 3 obligatorias + 1 optativa por tema;
- monedas del curso + comodín, niveles 1–5 y términos generales del diccionario.

A `cliente` se le aprueba una inscripción: tiene 10 monedas Python y el abono vigente, pero **todavía no abrió el raíz**, para probar el circuito desde el principio.

---

## 7. Seguridad

- Policies: `CoursePolicy`, `NodePolicy`, `SubmissionPolicy`, `EnrollmentRequestPolicy`, `GuardianAuthorizationPolicy`. `Gate::before` → el admin puede todo.
- Uploads validados por mime **y** extensión, tamaño en `config/uploads.php`, nombre `Str::uuid()`.
- Rate limiting en login, registro, entregas, comentarios y abrir nodos.

---

## 8. Ejecución de Python (sin cambios)

Worker de Pyodide cargado cuando se usa por primera vez, stdin desde un textarea (una línea por `input()`), timeout de 5 s, tope de salida. Se usa en el ejemplo del nodo, en las hojas y en la bandeja del admin.

---

## 9. Fases

| Fase | Entregable para probar |
|---|---|
| **1** | Proyecto base (Laravel + Livewire + Pest + MariaDB), login con usuario o email, registro con apellido/usuario y medidor, roles y middleware, **tema oscuro** y layouts alumno/admin, **todas las migraciones y modelos**, servicios `Ledger`/`TreeAccess`/`Glossary` con tests, seeders (admin, cliente, curso demo), `app:create-admin` |
| **2** | Admin: CRUD de cursos, **editor del árbol** (ramas, nodos, hojas con "+", orden, precios), recursos, diccionario, niveles e insignias |
| **3** | Alumno: mapa de mundos, detalle, **solicitudes** (comprobante y WhatsApp) y renovación; admin aprueba (monedas + abono); **abrir raíz y nodos**; **árbol** (lista + gráfico); vista del nodo con ejemplo ejecutable (Pyodide) |
| **4** | Hojas: CodeMirror, Pyodide con stdin, **entregas**, bandeja de corrección, pago de recompensas, XP y jefes, hilo de comentarios, notificaciones, movimientos en *Mi cuenta* |
| **5** | Ranking, **CV público** + privacidad, **autorización de menores**, pulido responsive, `DEPLOY.md`, `README.md`, suite Pest completa |

Al final de cada fase: `php artisan test` + `npm run build` + qué probar → **freno**.

---

## 10. Producción (pendiente: todavía no se sube)

El docente decidió **pulir detalles antes de subirla**. Cuando llegue el momento se sigue [DEPLOY.md](DEPLOY.md). Lo que hay que tener presente:

**Dónde va:** `https://gamificado.lariojaclick.ar` (anotado el 2026-09-27). El subdominio ya está creado en cPanel y pasa por **Cloudflare**; hoy sirve un `index.html` de prueba que se borra al subir el proyecto. Detalles en [DEPLOY.md § 9](DEPLOY.md).

**Repositorio:** `git@github.com:MasterDjmov/ghecosoft-cursos.git` (creado vacío el 2026-09-27, sin primer push todavía). Pendiente: la clave SSH del servidor como *deploy key* de solo lectura (DEPLOY.md § 2); se hace más adelante.

**Antes de subir (código):**
- Confiar en el proxy de Cloudflare (`trustProxies` en `bootstrap/app.php` con los rangos de Cloudflare o `at: '*'` si el servidor solo recibe tráfico de Cloudflare), con su test. Sin esto la app ve la IP de Cloudflare: los límites de intentos se comparten entre todos los alumnos.
- `APP_URL=https://gamificado.lariojaclick.ar` y `SESSION_SECURE_COOKIE=true` en el `.env` del servidor.

**Cuidados al instalar:**
- Datos iniciales con `php artisan db:seed --class=ProductionSeeder`, **nunca** `db:seed` a secas: crea `admin/admin123` y `cliente/cliente123`.
- El docente se crea con `php artisan app:create-admin`, con clave fuerte.
- En producción: `APP_ENV=production`, `APP_DEBUG=false`. Todo va por HTTPS (`URL::forceHttps`) y `migrate:fresh` queda bloqueado.
- El dominio apunta a `public/`; el proyecto nunca va dentro de `public_html`. Después de instalar, correr `php artisan storage:link`.
- Límites de PHP: `upload_max_filesize` 25M y `post_max_size` 30M.
- Borrar el `index.html` de prueba del subdominio (Apache lo prefiere a `index.php`).
- Cloudflare: SSL en *Full (strict)* (con *Flexible* hay bucle de redirecciones) y *Rocket Loader* apagado (rompe Livewire).
- Copias de seguridad de la base y de `storage/app/private`.

**Lo que falta cargar o decidir (del lado del docente):**
- Nombre del mundo que reemplaza a "Codexia", nombres narrativos e historia (en *Diccionario*). **En curso (2026-09-27):** el docente la está definiendo con Claude online a partir de [HISTORIA-BRIEF.md](HISTORIA-BRIEF.md); Python es el primer curso que sale. Falta decidir en qué pantallas ve el alumno la historia, el bestiario y el mentor (hoy se cargan pero no se muestran).
- Contenido real de Python a partir de FullCursos: clase 0 y temas.
- Modelo de la nota de autorización para menores.
- Logo en PNG con fondo transparente y versión horizontal.
- Confirmar la XP extra: +20 por nodo y +50 por jefe (`config/game.php`).
- WhatsApp y mensaje prearmado (en *Configuración*, ya en el servidor).
- Casilla de correo para los avisos por mail (SMTP), por ejemplo en `lariojaclick.ar`.


## 11. Ideas aprobadas para más adelante (pulido)

### Modo misión (anotado el 2026-09-27; al docente le gusta la idea, todavía no se diseña)
Pantalla de trabajo a pantalla completa para **una práctica**, inspirada en una maqueta tipo "centro de comando" (historia a la izquierda, editor al centro, terminal abajo). Es **otra presentación**: no cambia lógica, monedas ni reglas.
- Se entra con un botón **"Entrar a la misión"** en cada práctica. La página del nodo queda como está (leer, repasar, celular). En celular no hay modo misión: sigue la vista actual.
- **Izquierda**, con pestañas: *Historia* (la crónica del nodo; resuelve dónde mostrar la historia), *Consigna* y *Teoría*. Debajo, las prácticas del nodo como checklist con los colores de estado; tocar una cambia de archivo.
- **Centro**: el editor ventana y la consola con pestañas que ya existen (`x-code-runner`).
- **Arriba**: misión, recompensa (+XP, +monedas) y **Entregar** siempre visible. Derecha opcional: devolución del profe y estado de la entrega.
- **Afuera**: inspector de memoria o Valgrind (propio de C++), "Ejecutar tests" (no hay corrección automática; lo más cercano es "coincide con la salida esperada") e indicadores decorativos falsos. "Pista (−XP)" sería una regla nueva de economía: se decide primero en GAMIFICACION.md.
- Estética: la paleta y tipografías actuales, más sobria que la maqueta.
- Próximo paso: propuesta de distribución (qué va en cada zona) para que el docente la ajuste antes de programar.

### Catálogo y "mis cursos" (anotado el 2026-09-27; aprobado por el docente)
Hoy *Mundos* muestra todos los cursos publicados (los propios y los cerrados, que llevan a la ficha con la inscripción), pero mezclados: el alumno no distingue cuáles son suyos ni si hay más. Y la raíz del sitio manda directo al login, así que un visitante no ve la oferta.

1. **Separar en el panel del alumno** (prioridad):
   - arriba, **"Mis cursos" / "Seguí donde dejaste"**: los que tiene abiertos o con abono, con el último nodo en el que va y un botón para continuar;
   - abajo, **"Descubrí más mundos"**: los publicados en los que no está, más los "Próximamente";
   - si no tiene ninguno, que se vea primero la oferta con un mensaje de bienvenida.
2. **Landing pública** (sin iniciar sesión) con una sección, más abajo, de **los cursos que más se dictan**: tarjetas con el logo, una línea de descripción, y los botones *Crear cuenta* y *Consultar por WhatsApp*. Estética del geco (DISENO.md), no corporativa. Probablemente haga falta una marca de **"destacado"** en el curso para elegir cuáles salen ahí.
3. **Datos para decidir** en cada tarjeta y ficha: nivel (desde cero / intermedio), duración aproximada (cantidad de nodos o semanas), modalidad y horario (ya existe en comisiones). **A decidir:** si se muestra el precio en pesos (hoy no es un dato del sistema; se maneja por WhatsApp o comprobante) o queda "Consultá".
4. **Cursos "Próximamente"**: un estado del curso para mostrarlo como adelanto sin abrirlo, con "Avisame cuando salga" (sirve para medir interés). Candidatos, según el material de FullCursos: C (01–02), C++ (03–11), Java (18–20), PHP (21), JS (22), TypeScript (23), Arduino (15), Phaser (16).
- Sin filtros ni categorías por ahora: con 1–5 cursos no aportan.
- Toda regla de acceso nueva (landing pública, curso "Próximamente" que no se puede abrir) va con Policy y test Pest.

### Alta de alumnos por el docente (anotado el 2026-09-27; pedido del docente)
Hay gente a la que el docente le crea la cuenta. Hoy solo existe el registro del alumno y `app:create-admin`.
- En *Alumnos* → **"Nuevo alumno"**: nombre, apellido, usuario, email, fecha de nacimiento (para saber si es menor) y **clave provisoria**. La cuenta se crea verificada.
- **Cambio de clave obligatorio** en el primer ingreso: hace falta una marca nueva en `users`.
- Botón para **copiar los datos de acceso** (usuario, clave provisoria y link), para mandarlos por WhatsApp.
- Opcional en el mismo formulario: **inscribirlo directo a un curso y a una comisión**. Pasa por `EnrollmentApprover`, así recibe las monedas del raíz y el abono como cualquier inscripción aprobada, y queda en el libro de movimientos.
- Si es menor, queda pendiente la autorización como en el registro normal.
- **A decidir:** alumnos **sin email**. Hoy el email es obligatorio y único; sin email tampoco puede recuperar la clave solo, y el docente se la resetea. Opciones: email opcional (columna nullable) o pedirlo siempre.
- También: botón **"Resetear clave"** en la ficha del alumno, con otra clave provisoria.
- Solo el admin puede hacerlo: Policy y tests Pest.
