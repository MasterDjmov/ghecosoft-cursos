# Plan técnico

> Reescrito el 2026-09-27 con el modelo gamificado. Basado en [ESPECIFICACION.md](ESPECIFICACION.md) y [GAMIFICACION.md](GAMIFICACION.md).
> **Estado:** aprobado por el docente. Fases 1 a 4 terminadas (2026-09-27). **Fase 5 terminada (2026-09-27)**: plataforma completa según el plan. **En producción desde el 2026-09-28** (ver § 10); la etapa actual es pulir y sumar lo que pide el docente, de a un cambio por vez.

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
| D36 | Email del alumno | **Opcional** (en el registro y en el alta por el docente). Se entra con usuario o email. El docente puede cambiarle el email y resetearle la clave desde el admin para reactivar la cuenta | Hay alumnos sin email o que pierden el acceso; no se los bloquea por eso (2026-09-27) |
| D37 | Contenido del nodo | **Secciones como campos separados**: crónica, objetivos, antes de empezar, explicación (Mia; es el `content` actual), ¿para qué sirve? (Bron), errores habituales (Zed, con la criatura del bestiario), prueba del sello (autoevaluación sin nota, respuestas desplegables) y **soluciones solo del docente** (nunca se mandan al alumno). Práctica: suma criterio de aprobación, solución de referencia (solo docente), salida esperada y entorno Navegador/Local | Permite dibujar cada sección con su personaje, ocultar las soluciones de forma segura e importar el curso del super prompt (2026-09-27) |
| D38 | Nombre del héroe | **Público y único en toda la plataforma** (sin distinguir mayúsculas ni tildes). Lo elige el alumno; 3 a 20 caracteres, letras, números y espacios; el docente lo puede cambiar (moderación). Hasta que lo elija, los textos usan `hero.name` del diccionario ("Kira") y en los tops aparece sin héroe. Se muestra en ranking, CV y en el **top de la landing** | La idea es que los alumnos compitan en los tops con su héroe (2026-09-27) |
| D39 | **Estructura para todos los lenguajes** | Todo lo que se arma para Python (secciones del nodo, prácticas, Sendas bloqueadas que se abren con monedas del curso o comodines, jefes, insignias, extras, importador, historia) es **genérico**: nada depende de Python salvo el ejecutor del navegador. Cada curso define su lenguaje, su diccionario (región, mentor, moneda) y su árbol; el formato del importador y el super prompt tienen una parte común y un anexo por lenguaje | Python es el primero, pero si funciona se suben C, C++, Java y el resto con la misma estructura (2026-09-27) |
| D40 | Importador de cursos | Markdown con títulos fijos + bloques ```meta (formato en FORMATO-CURSO.md, sin dependencias nuevas). IDs estables en `branches/nodes/practices.code`; reimportar actualiza por ID, no borra y no toca el progreso. Todo en una transacción; "Revisar" deshace al final. `publicado` del curso vale solo al crearlo; el de un nodo, solo si está escrito. Claves generales del diccionario por defecto: `world.name`, `hero.name`, `coin.wildcard`, `xp*`, `level*`, `companion.*`, `state.*` | Cargar 150–200 nodos a mano es inviable; el super prompt entrega directamente este formato (2026-09-28) |
| D41 | Sendas y requisitos | Las ramas tienen tipo (`branches.kind`: tronco, extra, senda; `is_extra` queda como "no es tronco"). Requisitos extra en `node_requirements` (además del padre), validados contra ciclos por padre y por requisito. Nodo tipo **Ventana**. **Cualquier nodo salvo el raíz** puede cobrarse en comodines (antes, solo los extras): así la entrada a una Senda cuesta comodines y lo de adentro, moneda del curso. "Curso completado" y el progreso del CV cuentan solo el **tronco** (las Ventanas sí; extras y Sendas no). En el árbol, cada Senda sale dibujada desde su nodo de origen | Pedido del super prompt (§ 7): Sendas que brotan del tronco y exigen temas más avanzados (2026-09-28) |
| D42 | Historia en pantalla y héroe | Marcadores `{heroe}`, `{mentor}`, `{mundo}`, `{region}` en todos los textos del curso (`Narrative`). Bienvenida (`story.course_intro`) en la ficha y en el árbol (se puede cerrar); aviso con `story.branch_completed` al completar una rama y con `story.course_completed` al terminar el curso (campanita + panel en el árbol); presentación del jefe con su insignia; historia de la criatura en Errores habituales. Héroe elegido en *Mi cuenta*, moderable en la ficha del alumno, visible en ranking y CV | Fase 9 (2026-09-28) |
| D43 | Todo nodo tiene hojas | **Todo nodo publicado tiene al menos una práctica obligatoria** (raíz, temas, jefes, ventanas, extras y la Encrucijada, que lleva una misión de reflexión, puede ser sin entrega). El editor no publica un nodo sin obligatorias, un nodo nuevo desde el árbol nace como borrador, la última obligatoria de un nodo publicado no se borra ni pasa a optativa, y el importador lo marca como error (o aviso con `publicado: no`) | Pedido del docente: un nodo sin hojas no se gana ni se completa (2026-09-28) |
| D44 | Catálogo y landing | **Mundos** separa "Seguí donde dejaste" (con el último nodo abierto sin completar) de "Descubrí más mundos". El curso suma nivel, temario corto (un tema por línea), portada, **destacado** (sale en la landing; si no hay ninguno, salen todos los publicados) y **Próximamente** (`is_upcoming`, vale solo sin publicar: se ve pero no se abre). "Avisame cuando salga" (`course_interests`) avisa una sola vez al publicarlo. **Landing** en `/` para quien no entró: portada con login al lado, cursos, Próximamente, monedas y top 10 con podio (héroe, nombre de ranking, rango, insignias, XP; nunca el usuario de login). Tendencia ▲▼ contra una foto diaria (`ranking_snapshots`) que se toma en la primera carga del día. Precio en pesos: no se muestra ("Consultá" por WhatsApp) | Pedidos del docente del 2026-09-27/28 (§ 11) |
| D45 | Modo misión | Distribución **A · centro de comando** (elegida por el docente sobre una maqueta): barra con misión, recompensa, estado, **Ejecutar** y **Entregar**; a la izquierda Historia / Consigna / Teoría y las misiones del nodo como checklist (se pliega, y lo recuerda por navegador); al centro editor y consola a todo el alto; a la derecha la devolución del profe **solo si hay**. Ruta `cursos/{curso}/nodos/{nodo}/mision/{práctica}`, mismas reglas que el nodo (Policy del nodo). Solo para prácticas con código y pantallas grandes (en celular, la vista del nodo). Entregar, marcar y comentar comparten el trait `WorksOnPractice` con la tarjeta del nodo | Otra presentación de la misma práctica: no cambia lógica, monedas ni reglas (2026-09-28) |
| D46 | Curso de Python real | El curso se arma con las 28 unidades de `FullCursos/17-Python` en el formato del importador, versionado en **`cursos/python/`** (reemplaza al demo: el seeder local lo importa y en producción se carga con `app:import-course cursos/python/ --apply` o desde el admin). Tronco en 3 ramas con un **jefe** por rama (proyectos integradores nuevos) y la **Encrucijada** (ventana) al final; pygame y Python aplicado son **Sendas**. 01–11 se convirtieron del formato nuevo; 12–42 se reescribieron desde cero (estaban escritas como diferencia con C/C++). Las salidas esperadas salen de ejecutar las soluciones y se verificaron en Pyodide (109/109). El importador suma `nivel`, `destacado`, `proximamente`, `### Temario` y `ejecutable: no` | Pedido del docente: ver el material completo gamificado (2026-09-28) |
| D47 | Árbol en espiral | Si una rama del tronco sigue a otra (el padre de su primer nodo es de otra rama), el tronco se dibuja como **espiral de Arquímedes** con paso fijo entre nodos, en vez de un sector por rama con la distancia al raíz (que en Python dejaba saltos de ~2000 px entre un jefe y la rama siguiente). Con varias ramas desde el raíz, cada una es un brazo de la espiral; si todas salen del raíz, queda el abanico. Sendas y ramas que salen de un nodo del medio brotan hacia afuera | Pedido del docente: el árbol de Python "se abría muchísimo" (2026-09-28) |
| D48 | Seguridad antes de subir | **Login**: Fortify cuenta solo los intentos fallidos (5 por minuto para el mismo usuario desde la misma IP) y `ThrottleAuthForms` suma topes por IP (20 logins por minuto, para que no se prueben muchos usuarios), a *Olvidé mi clave* (5 cada 10 min), a la nueva clave y a confirmar la clave; cambiar la clave desde el perfil también tiene tope. Los límites se muestran como error del formulario, en español. *Olvidé mi clave* responde igual exista o no la cuenta. **Subidas**: la regla `SafeUpload` va en toda subida (entregas, comprobantes, autorizaciones, recursos, importador): el contenido tiene que coincidir con la extensión (un .exe renombrado a .pdf no pasa; el código y el texto no pueden ser binarios) y nunca se aceptan archivos del servidor ni ejecutables (`tarea.php.txt`, `.htaccess`, `.exe`…), tampoco si el docente los habilita en una práctica o en un curso importado. **Cabeceras** en todas las páginas (`SecurityHeaders`: sin iframes ajenos, `nosniff`, `Referrer-Policy`, HSTS con HTTPS). **Cloudflare**: `TRUSTED_PROXIES=cloudflare` con sus rangos | Pedido del docente: revisar la seguridad antes de subir (2026-09-28) |
| D49 | Movimientos por curso | *Mi cuenta → Movimientos* (y la ficha del alumno en el admin) muestran un resumen por curso (saldo de su moneda y XP ganada ahí), los comodines y la XP total, y **una sola lista** donde las monedas y la XP de un mismo hecho van juntas, con el detalle: qué práctica («Misión de «Nodo»», intento), qué nodo se abrió, completó o qué jefe se venció, y la nota del ajuste. Se filtra por curso (`?curso=slug`). Solo lee el libro: los saldos siguen saliendo del Ledger | Pedido del docente: pronto habrá cursos en paralelo y faltaba decir qué se entregó (2026-09-28) |
| D50 | Súper test por curso | `php artisan app:simulate-course <slug>` (solo local, [SIMULACION.md](SIMULACION.md)): 5 alumnos con estilos distintos se inscriben, el docente los aprueba y juegan día por día (reloj simulado, 90 días) hasta abrir todo; el docente corrige ejecutando el código con `python3` (en Python) o comparando con la solución de referencia, y pide rehacer con el motivo. Todo por los servicios de siempre; al final controla saldos, pagos dobles, XP, aperturas, insignias y fin de curso. Se corre con **cada curso nuevo** antes de abrirlo. Primer hallazgo: un nodo sin prácticas obligatorias nunca se completaba (ni cerraba el curso) → ahora se completa al abrirlo (`NodeUnlocker` → `SubmissionReviewer::completeWithoutPractices`) | Pedido del docente: probar el sistema de punta a punta y ver cómo queda un alumno al final (2026-09-28) |
| D51 | Link y código del CV | El CV deja de usar el usuario de login (publicarlo regalaba la mitad del acceso): cada alumno tiene `users.cv_slug` = nombre-apellido + 6 caracteres al azar, y en *Privacidad* puede **generar un link nuevo** (el anterior da «perfil privado»). **Código de acceso opcional** (opción B del docente, apagado por defecto): 6 cifras guardadas cifradas (`cv_code`, se le muestran al alumno y puede generar otro, que invalida los accesos dados); el visitante lo escribe y ese navegador lo ve 2 h. Contra fuerza bruta: 5 intentos fallidos cada 10 min por IP y 30 por hora por CV. El dueño y el docente lo ven sin código. El PDF sigue siendo la impresión del navegador (no queda archivo en el servidor) | Pregunta del docente sobre la seguridad del CV (2026-09-28) |
| D52 | Curso de C | `01-C` + `02-C-Intermedio` como *C: Las Forjas de Hierro* en **`cursos/c/`** (historia de `GUION.md`: Maese Ferrum, moneda **lingote**). 41 nodos y 149 prácticas: raíz + 5 ramas de tronco con jefe cada una (Gólem de Escoria, Araña de las Direcciones = proyecto 16, Sanguijuela de las Minas, Guardián del Archivo = proyecto 28, Dragón bajo la Montaña = mazmorra 30), la **Encrucijada del Yunque** y dos Sendas: **Forja Viva** (SDL3) y **Autómatas** (Arduino, con el lado de la compu en C). 01–16 convertidas; 17, 18, 19, 21, 22, 25 y 28 reescritas (formato viejo); 20, 23, 24, 26, 27, 29 y 30 escritas desde cero. Todas las prácticas son `entorno: local`; las de varios archivos, SDL y Arduino se entregan como `.zip`. Todo el código compila sin advertencias (gcc; SDL3 contra la biblioteca real; sketches con arduino-cli) y las salidas esperadas salen de ejecutarlo. La plataforma suma resaltado de C/C++ en el editor y el súper test compila y ejecuta C | Pedido del docente: el curso de C completo, con el mismo proceso que Python (2026-09-28) |
| D53 | Curso de C++ | `03-C++` + `04-C++-Moderno` + `11-STL` (+ `05-C++-Videojuegos` en la última rama) como *C++: La Ciudadela de los Artífices* en **`cursos/cpp/`** (la región de `GUION.md` que estaba «a definir»: mentora **Tesla, la Artífice Mayor**, alumna de Maese Ferrum; moneda **engranaje**). Reemplaza al «C++ intermedio» de Próximamente (mismo slug `cpp`) y es **desde cero**, como pide la auditoría: la comparación con C va en un recuadro opcional. 52 nodos y 192 prácticas: raíz + 5 ramas de tronco con jefe (Autómata de Latón, Quimera de la Arena = proyecto Arena, Mímico del Bestiario = proyecto Bestiario, Kraken de los Contenedores = ToDo-List + sistema de entidades, Minotauro del Laberinto = mazmorra de `05`), la **Encrucijada de los Engranajes** y dos Sendas: **Linterna Mágica** (SDL3 en C++, `07-SDL3-Cpp`) y **Vitrales** (Qt 6, `12-Qt-GUI`; su jefe es un editor de niveles para el Laberinto). Todo el formato viejo se reescribió; se agregaron nodos que faltaban (operadores, archivos, excepciones, depuración, pruebas). Todo compila sin advertencias con `g++ -std=c++20 -Wall -Wextra`, las salidas salen de ejecutarlo; SDL3 y Qt se compilan y enlazan contra las bibliotecas reales y arrancan sin pantalla (driver *dummy* / `offscreen`). El súper test compila C++ con `-std=c++20`. Los cursos Próximamente de ejemplo pasan a ser Java y JavaScript | Pedido del docente: el curso de C++ completo desde FullCursos, con Tesla, las dos Sendas (SDL y Qt) y la Ciudadela (2026-09-28) |
| D54 | Comisiones en el admin | Se crean, editan, cierran y borran en *Admin → Cursos → Datos del curso* (`Admin\Courses\Cohorts`). Son **opcionales** y solo una etiqueta del abono: sin comisiones el alumno se inscribe igual. En la ficha del alumno se asigna o cambia la comisión de cada curso (`StudentAccounts::changeCohort`, que la pone en todos sus abonos de ese curso) sin tocar aperturas, monedas, XP ni vencimientos. Una renovación sin comisión elegida conserva la del último abono. Borrar una comisión deja a sus alumnos sin comisión. |
| D55 | Temario completo en la landing | Cada tarjeta del catálogo (landing y Mundos) tiene **Ver temario**: un modal con el temario entero del curso y, aparte, las **Sendas como opcionales** (título de la rama `tipo: senda` partido en «nombre: tema»). No muestra títulos de nodos: la regla de no ver nodos sin abrir sigue igual y descubrirlos es parte del juego. Los temas admiten `código` en línea (markdown escapado). Las Sendas salen del temario de `cursos/*/00-curso.md` porque se muestran solas. |
| D56 | 100 niveles | `LevelSeeder` genera 100 niveles con XP = 35 · (n − 1)^1.58, redondeada (de a 5, 10, 50 o 100). Pensada para que sigan subiendo con cada curso nuevo: el primer nodo ya da el nivel 2; Python completo, el 15; C, el 19; C++, el 21; los tres, el 37; el 100 (50 000 XP) pide unos 12 cursos. El nivel se calcula de la XP en cada request, así que cambiar la curva reubica a todos sin tocar el libro. El seeder solo toca la XP: los nombres de rango (`level.N`) quedan. En producción: `php artisan db:seed --class=LevelSeeder --force`. |
| D57 | Rol equivocado y página 403 | Quien abre con GET una página que no es para su rol (un alumno con un marcador a `/admin`) vuelve a su inicio (`EnsureRole` → `home`); los pedidos que no son GET o esperan JSON siguen con 403. Los 403 que quedan (archivos ajenos, Policies) muestran `errors/403.blade.php`: la imagen del geco guardián (`public/images/error-403.webp`) entera sobre su reflejo desenfocado, el mensaje «Esta puerta está sellada» y **Volver a mi inicio** (o a la landing sin sesión). La barra de saldos muestra la imagen de cada moneda (`<x-coin-icon>`, de `coin.course` / `coin.wildcard` del diccionario). |
| D58 | Curso de Java | `18-Java` + `19-Java-Avanzado` + `20-SpringBoot-Lombok` como *Java: El Imperio de las Clases* en **`cursos/java/`** (historia de `GUION.md`: mentora **Kaffa, la Arquitecta Imperial**; moneda **denario**). Reemplaza al Java de Próximamente (mismo slug `java`). 60 nodos y 224 prácticas: raíz + 5 ramas de tronco con jefe (Centinela de la Aduana, Quimera de las Mil Herencias, Espectro Nulo, Liche de las Tablas Huérfanas, Dragón del Imperio), la **Encrucijada de los Denarios** y tres Sendas: **Arcade Imperial** (juego 2D con Swing), **Corrientes** (Java moderno: streams, records, `sealed`, concurrencia; de `19-Java-Avanzado`) y **Puerto de Spring** (servicios web con Spring Boot 3, JPA y Lombok; de `20-SpringBoot-Lombok`). Java 17; las bases de datos, en PostgreSQL. Todo compila sin advertencias (`javac -Xlint:all`) y las salidas esperadas salen de ejecutarlo: JDBC contra PostgreSQL real, Swing se crea sin pantalla y se captura, y los proyectos de Spring corren `mvn test` (H2 en los tests). El editor colorea Java y el súper test ejecuta con `java Main.java` lo que es un solo archivo sin base ni ventana (lo demás lo compara con la solución de referencia). Los cursos Próximamente de ejemplo pasan a ser JavaScript y PHP | Pedido del docente: el curso de Java completo desde FullCursos, con moneda denario, las tres Sendas y tronco de 5 ramas (2026-09-29) |
| D59 | Curso de PHP | `21-PHP` (y lo que faltaba) como *PHP: El Puerto de los Mensajeros* en **`cursos/php/`**: mentora **Elefa, la Capitana del Puerto** (una elefanta que nunca olvida un pedido), moneda **sello** (de lacre). Reemplaza al PHP de Próximamente (mismo slug `php`). **Orientado a MySQL/MariaDB** y a PHP 8.2 (lo que trae XAMPP; nada exclusivo de 8.3). 63 nodos y 231 prácticas: raíz + 5 ramas de tronco con jefe (Muelle de las Primeras Cartas: fundamentos; Astillero de los Moldes: objetos y Composer; Oficina de Correos: la web, formularios, sesiones, seguridad y login; Bodega del Puerto: MariaDB, PDO, consultas preparadas, ABM, transacciones; el Faro: MVC sin framework, API REST, PHPUnit, errores y hosting), la **Encrucijada de los Sellos** y cuatro Sendas: **Arena** (RPG por turnos, de `21`–`23` + ranking en MariaDB), **Ciudadela** (lo esencial de Laravel 12 en 3 nodos: rutas y Blade, Eloquent y formularios, jefe), **Mensajes Veloces** (JavaScript con `fetch` contra la API propia en 3 nodos: DOM, formularios y sesión, jefe con *polling*) y **Escaparate** (HTML y CSS, 5 nodos, optativa que brota del jefe de la rama 1 con 3 comodines). Laravel y JavaScript van mínimos a propósito: el docente quiere cursos propios de cada uno. Todo se verificó de verdad: los programas con `php8.3` y todos los avisos (las salidas esperadas salen de ejecutarlos), el SQL y PDO contra MariaDB, las páginas con `php -S` y pedidos reales (CSRF, sesiones, subidas, redirecciones), Composer y PHPUnit, Laravel con `php artisan test` y `migrate:fresh --seed` en MariaDB, y el JavaScript, el HTML y el CSS en Chromium (Playwright: clics, formularios, dos navegadores a la vez, estilos computados y cajas en 375 y 1000 px). El editor colorea PHP (`@codemirror/lang-php`) y el súper test corre con `php8.3` lo que es un solo archivo de consola (lo web, con base, `include` o varios archivos lo compara con la solución). El único curso Próximamente de ejemplo queda JavaScript | Pedido del docente: el curso de PHP completo, con la misma métrica que el resto, orientado a MySQL/MariaDB, Sendas de RPG, Laravel y API + JavaScript, y HTML/CSS como optativas (2026-09-29) |
| D60 | Intentos y horario de corrección | Cada práctica muestra cuántas veces se entregó (`<x-attempts>`: 1 verde, 2–3 amarillo, 4 o más rojo) en la tarjeta del nodo y en la lista del modo misión, para que el alumno piense antes de entregar. El docente corrige de **8 a 22 h** (`App\Support\ReviewHours`): lo que se entrega fuera de ese horario avisa al entregar y mientras espera corrección cuándo se revisa («mañana (02/10) entre las 8 y las 22 h»). Los logos del catálogo («Elegí tu mundo») miden 200 px y los de los mundos en curso, 100 px | Pedidos del docente (2026-09-30) |
| D61 | Contador de abono y emojis | Cada curso muestra sus días de abono (`<x-subscription-countdown>`, hasta `TreeAccess::paidUntil()`: cuenta la renovación ya aprobada) en neón: cian con más de 7, ámbar de 7 a 4, rojo y latiendo con 3 o menos; va en el encabezado del árbol, en la tarjeta de cada mundo en curso y en la ficha del curso. Los cuadros para escribirle al profe (y las respuestas y notas del docente) tienen un botón de emojis (`<x-emoji-field>`, 40 emojis fijos, Alpine) | Pedidos del docente (2026-09-29 y 2026-09-30) |
| D62 | Avisos en vivo | Sin workers ni WebSockets (hosting compartido): la campanita (`NotificationsBell`) consulta cada 20 s con la pestaña a la vista y cada 60 s en segundo plano, y enseguida al volver a la pestaña (`liveBell` en `live-alerts.js`, para no cargar el hosting compartido; 2026-09-30) y manda al navegador cuántos avisos hay sin leer y el último. `resources/js/live-alerts.js` pone la cantidad en el título de la pestaña (`(3) …`), un punto rojo en el ícono y, si el aviso es nuevo (se recuerda el último por navegador), toca un tono corto (Web Audio, sin archivos) y muestra la notificación del sistema si no se está mirando la plataforma. Cada usuario (docente o alumno) elige el sonido y la notificación del sistema en **Mi cuenta → Avisos** (`users.alert_sound`, `users.alert_desktop`). Con el navegador cerrado no llega nada (eso sería Web Push, más adelante) | Pedido del docente (2026-09-29 y 2026-09-30) |
| D63 | Consultas por práctica | Un hilo por alumno y práctica (`practice_messages`), sin necesidad de entregar. El alumno lo usa en la solapa **Mensajes** del modo misión y en «Consultas al profe» de la tarjeta de la práctica; el docente, en **Admin → Mensajes** (sin leer primero; también desde la ficha del alumno y desde la campanita, que lleva al hilo). `PracticeMessenger` guarda y avisa al otro lado (`PlatformNotification`, que llega en vivo por D62); `PracticeChat` es el hilo (se actualiza cada 20 s, carga diferida, emojis). Acceso (`PracticeMessagePolicy`): el alumno ve solo su hilo y solo de nodos que abrió; escribir pide el abono vigente (leer, no). Máximo 10 mensajes por minuto y 2000 letras | Pedido del docente (2026-09-29 y 2026-09-30) |
| D64 | CV en acordeón con su árbol | En el CV cada curso es un acordeón (`<details>`) cerrado de entrada, con la barra de avance a la vista; al abrirlo, los temas completados y **Ver árbol**: `/cv/{link}/arbol/{curso}` muestra el árbol coloreado del alumno solo para mirar (`TreeGraph::forVisitor`: sin links, precios ni motivos; las hojas de nodos que no abrió siguen como «?»), con las mismas reglas que el CV (público o dueño/docente, código de acceso) y solo de cursos que empezó. Al imprimir se abren todos los cursos y se ocultan los botones | Pedido del docente (2026-09-30) |
| D65 | Sesión única para alumnos | Una cuenta de alumno solo está abierta en un lugar a la vez (`EnsureSingleSession` + `SingleSession`): al iniciar sesión (clave, passkey o «recordarme») esa sesión se queda con la cuenta (`users.session_token`); la anterior, en su próximo pedido, se cierra (también su «recordarme») y ve en el login «Tu cuenta se abrió en otro dispositivo…». Cada cierre se anota (`session_evictions`: IP y navegador); al **3.º en 24 h** le llega al docente el aviso «¿Cuenta compartida?». El docente, en la ficha del alumno: **Pausar cuenta** (`users.blocked_at`: corta todas las sesiones y no deja entrar) / **Reactivar**, más **Resetear clave**. El bloqueo es solo manual. No aplica al docente. La red (IP) no se usa: los datos móviles darían falsos positivos | Decisión del docente (2026-09-30): sesión única; el resto, según la recomendación |
| D66 | Ejecutar C y C++ al corregir | En *Admin → Entregas*, el docente ejecuta una entrega de C o C++ de un solo archivo **en su navegador** (el código del alumno sigue sin tocar el servidor): Clang 22 de YoWASP en WebAssembly (del CDN jsDelivr, versión fija) compila en un Web Worker y el programa corre en otro worker (WASI, `@bjorn3/browser_wasi_shim`) con 5 s de límite, con la *Entrada de ejemplo* y comparando con la *Salida esperada*; la consola muestra primero las advertencias o errores del compilador. C++20 con excepciones gracias a la biblioteca de wasi-sdk 34 con excepciones y a un encabezado precompilado con los `#include` de siempre (`public/toolchains/cpp/`, ~20 MB, fuera de git: se arma con `scripts/build-cpp-toolchain.sh` y `deploy.sh` lo sube solo si cambió). La primera vez baja ~105 MB del compilador (después queda en la caché); cada ejecución tarda ~8–15 s. Solo el docente (`x-code-runner`); para alumnos, más adelante. Ojo: los mensajes de las excepciones de la biblioteca estándar cambian entre g++ y Clang (`stoi` vs `stoi: no conversion`) | Decisión del docente (2026-09-30): prioridad C++, Java y PHP; por ahora solo el docente |
| D67 | Probar Java en la compu del docente | En una entrega de Java, debajo del código, *Copiar comando* arma un comando de terminal que crea `/tmp/ghecosoft/intento_N/<Clase>.java` (heredoc con delimitador entre comillas: el código llega tal cual), compila con `javac -encoding UTF-8` y corre con la entrada de ejemplo; *Descargar <Clase>.java* baja el archivo. Todo se arma en el navegador (`<x-local-run>`), sin ruta nueva. No hay ejecución en el navegador: CheerpJ requiere licencia para este uso y TeaVM-javac no compila código común de los cursos. |
| D68 | Ejecutar PHP al corregir | En *Admin → Entregas*, el docente ejecuta una entrega de PHP de consola **en su navegador**: PHP 8.3.33 en WebAssembly (`@php-wasm/universal` + `@php-wasm/web-8-3`, versión fija) en un Web Worker (`php.worker.js`), con 5 s de límite. Un envoltorio define `STDIN` (la entrada de ejemplo), `STDOUT`, `STDERR`, `readline()` y `$argv`; avisos y errores salen en la salida como en la terminal. El `.wasm` (18 MB, 7 MB comprimido) no va al build: `scripts/build-php-toolchain.sh` lo copia a `public/toolchains/php` (lo corre `deploy.sh`) y Vite lo reemplaza por un módulo vacío. Lo que usa MariaDB (PDO), web o varios archivos se sigue probando en la compu. |
| D69 | Ejecutor local de Java | *Ejecutar* también en las entregas de Java, para el docente: la página le manda el código a `scripts/JavaRunner.java`, un programa Java de un solo archivo que el docente deja abierto en su compu (`java scripts/JavaRunner.java`, sin instalar nada). Compila con `javac`, corre con `java` (256 MB, 5 s, salida hasta 256 KB) con la entrada de ejemplo y devuelve salida, errores y diagnósticos a la misma consola. Escucha solo en `127.0.0.1:17017` y atiende únicamente al `Origin` de la plataforma (producción y `localhost:8000`; se agregan con `--origin`) y a `Host` 127.0.0.1/localhost (contra DNS rebinding); Chrome pide una vez permiso de «red local». El comando para la terminal (D67) queda plegado como alternativa. El código corre con los permisos del docente, como cuando prueba un zip. |
| D70 | Universo de cursos | *Admin → Universo*: todos los cursos en un mapa 3D (3d-force-graph, todo el ancho y pantalla completa) unidos por los temas del catálogo `cursos/temas.md` (familias **de lenguaje** —cada lenguaje los enseña a su manera— y **compartidas** —HTML, CSS, JS, SQL, web, algoritmos, juegos…—, cada una de lo básico a lo avanzado; es una lista ideal, con temas que todavía nadie enseña). Cada nodo marca en su `meta` qué temas enseña (`temas:`) y cuáles da por sabidos (`usa:`); se guardan en `nodes.topics`/`nodes.uses` y el alumno no los ve. El mapa muestra lo repetido entre cursos, lo que falta y lo que falta pero algún nodo usa; abajo, un tablero por familia y la cobertura de cada lenguaje. Los cursos que ya están no se tocan: sirve para analizar y, más adelante, para armar cursos nuevos con copias de lo que existe (paso 4, pendiente). |
| D71 | Clase 0 de prueba | Cualquier cuenta registrada **sin abono de un curso** (nuevas o de otro curso) entra gratis a la **Clase 0** (el raíz) publicada de un curso publicado: la lee, ve el ejemplo, descarga sus recursos y practica en el editor (en Python, también ejecuta), y ve el árbol con el resto cerrado. **No** la abre (sin `node_unlocks`, sin monedas), no entrega, no marca ni consulta al profe: no queda ningún registro. Para que el profe corrija y seguir, pide el abono; al aprobarse, el flujo es el de siempre (recibe las monedas, abre la Clase 0 y el mes corre desde la aprobación). Los que ya abrieron la Clase 0 no ven cambios. Regla en `TreeAccess::isTrial` (Policy de nodo y de árbol); se ofrece en la landing (registrarse y probar), en *Elegí tu mundo* y en la ficha del curso. |
| D72 | Rol docente y temario | Tercer rol, **Docente** (`teacher`; el admin pasa a llamarse *Administrador*). El administrador hace docente a una cuenta desde la ficha del alumno (*Hacer docente*) y la vuelve a alumno desde *Alumnos → Docentes*. Los cursos son de la plataforma (los habilita el administrador); el docente **crea sus comisiones** en *Comisiones* (`cohorts.teacher_id`; el administrador puede asignar el docente de cualquiera) y **alcanza a los alumnos de sus comisiones, en el curso de cada una** (`TeacherScope`): bandeja de entregas (corrige y ejecuta), mensajes, ficha del alumno (sin cuenta, monedas, héroe ni seguridad) y resetear la clave si el alumno lo pide; los avisos de entregas y consultas le llegan a él y al administrador. **No** aprueba pagos ni solicitudes, no edita cursos, monedas, diccionario ni configuración. En *Alumnos*, tocar un alumno despliega sus cursos con la comisión de cada uno para cambiarla ahí (el docente suma alumnos a sus comisiones desde *Sumar alumnos*, que muestra solo nombre y usuario, y no mueve alumnos de la comisión de otro docente). La bandeja del administrador filtra por docente. **Temario** (`admin/cursos/{curso}/temario`, administrador y docentes): el árbol entero como índice para dar la clase, con objetivos, explicación, enunciados y resoluciones; se imprime todo desplegado. La sesión única sigue siendo solo para alumnos. **Árbol del alumno** (2026-10-01): *Ver árbol* en cada curso, en *Alumnos* y en la ficha, abre `admin/alumnos/{usuario}/arbol/{curso}` con su avance coloreado, solo para mirar como el del CV (D64); el docente, solo con alumnos de su comisión en ese curso (`UserPolicy::viewProgress`). |
| D73 | Corrección asistida (etapas 1 a 4 hechas) | La corrección sigue siendo del docente (sin aprobación automática): se agiliza con **varias pruebas por práctica** (`practice_tests`, solo del docente) que corren en su navegador al abrir una entrega y desde la bandeja (*Probar pendientes*), comentarios guardados y un tablero de «dónde se traban». El indicio (*Entrada de ejemplo* + *Salida esperada*) se muestra **igual en todos los cursos** (hecho: `<x-expected-io>`, «Cómo debería verse», cerrado de entrada, en la tarjeta, el modo misión, el ejemplo del nodo y la entrega; la consola de Python pierde la solapa *Esperada*). Comentarios guardados: de cada docente. Etapa 2 (2026-10-01): tabla `practice_tests`, parte `#### Pruebas` del formato, importador (las reemplaza enteras si cambian), `app:course-tests` (verifica con la solución de referencia y completa salidas con `--fill`), `Support\LocalCodeRunner` (compartido con el súper test, que ahora también corre las pruebas al corregir). Etapa 3 (2026-10-01): pruebas escritas en los cinco cursos (225 prácticas, 1166 casos, todos verificados); detalle en CORRECCION-ASISTIDA.md. Etapa 4 (2026-10-01): panel *Pruebas* al abrir una entrega (corre en el navegador de quien corrige, `runners/cases.js`), resultado en `submissions.check_result` (`SubmissionCases::store`) y en la bandeja la marca, el filtro *Pruebas* y *Probar pendientes*. Etapa 5, en parte (2026-10-01): «Estadísticas · Prácticas» en el *Inicio* del administrador (`Support\PracticeStats`: por curso y período, las más elegidas y dónde se traban); faltan los comentarios guardados y la versión del docente. Diseño en [CORRECCION-ASISTIDA.md](CORRECCION-ASISTIDA.md) | Conversado con el docente (2026-09-30) |
| D74 | Fondos de los mundos | Cada curso tiene un **fondo 16:9 de su región** y el universo uno del **Mundo del Código**, cargados en el Diccionario como imagen de `world.region` (del curso) y de `world.name` (General): sin columnas nuevas. Se ven en la **Clase 0** (franja arriba del nodo raíz, con el nombre de la región) y de fondo en la **bienvenida del curso** (`story.course_intro`, con degradé para leer el texto); un curso sin región con imagen usa la del Mundo del Código (`Glossary::scene`). En el Diccionario general, «Personajes y regiones propios de los cursos» las lista con el botón *Fondo*; `app:glossary-portraits` reconoce `mundo_codigo` y `mundo_<líder>` (va a la región del curso de esa líder). Los fondos de la compañía (Kira, Mia, Bron, Zed, el Gremio, el profe) quedan para más adelante | Pedido del docente (2026-10-01) |

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

**Público:** `/cv/{cv_slug}` (D51: link propio, no el usuario; código de acceso opcional).

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

### Fases del curso completo (acordadas el 2026-09-27, a partir de `super-prompt-v2-curso-python.md`)
Todo genérico para cualquier lenguaje (D39).

| Fase | Entregable para probar |
|---|---|
| **6** ✅ | **Modelo de contenido** (D37, terminada el 2026-09-28): secciones del nodo y campos nuevos de la práctica, soluciones solo del docente, editor del admin y vista del alumno con cada sección y su personaje |
| **7** ✅ | **Importador** (terminada el 2026-09-28): formato fijo (común + anexo por lenguaje) documentado, `app:import-course` con modo de prueba e IDs estables que actualiza sin borrar el progreso; se ajusta el super prompt para que entregue ese formato |
| **8** ✅ | **Sendas** (terminada el 2026-09-28): requisitos múltiples por nodo, tipo Ventana, Sendas que brotan de un nodo (se abren con comodines o monedas del curso) y su dibujo en el árbol |
| **9** ✅ | **Historia en pantalla** (terminada el 2026-09-28) (bienvenida, crónica, rama completada, jefe, criatura, Encrucijada) y **héroe** (D38) |

Después, las tareas del § 11: ~~alta de alumnos + email opcional + WhatsApp~~ y ~~"Mis cursos" + landing (con el top de héroes)~~ (hechas el 2026-09-28, D44), y ~~modo misión~~ (D45).

---

## 10. Producción (en vivo desde el 2026-09-28)

La plataforma está en `https://gamificado.lariojaclick.ar` desde el **2026-09-28** (subdominio en cPanel detrás de **Cloudflare**; base `lariojac_code_cursos`). La guía de instalación es [DEPLOY.md](DEPLOY.md).

**Repositorio:** `git@github.com:MasterDjmov/ghecosoft-cursos.git` (primer push el 2026-09-28).

**Actualizar:** desde la compu del docente, después de `git push`: `scripts/deploy.sh` (código, estilos, migraciones y caché) o `scripts/deploy.sh --cursos` (además reimporta los cursos de `cursos/`). En el servidor `npm run build` no anda: los assets se compilan en la compu y se sube `public/build/`.

**Pendiente:**
- Hecho (2026-10-01): **copias de seguridad** con `scripts/backup.sh` (todos los días por *Cron Jobs* de cPanel y antes de cada deploy, 14 días) y `scripts/pull-backups.sh` para traerlas a la compu (DEPLOY.md § 8). El docente agenda la tarea en cPanel.
- La clave SSH del servidor como *deploy key* de solo lectura (DEPLOY.md § 2), si hace falta.

Lo que sigue quedó como registro de la instalación.

**Antes de subir (código)** — registro de la instalación:
- Hecho: las ideas de [IDEAS-GAMIFICACION.md](IDEAS-GAMIFICACION.md) se revisaron; la corrección sigue siendo humana y se agiliza con D73. Las monedas, por ahora, abren nodos; un evento de canje queda para más adelante.
- Hecho (D48): confiar en el proxy de Cloudflare con `TRUSTED_PROXIES=cloudflare` (`config/security.php`, con test).
- `APP_URL=https://gamificado.lariojaclick.ar`, `TRUSTED_PROXIES=cloudflare` y `SESSION_SECURE_COOKIE=true` en el `.env` del servidor.
- El docente activa la verificación en dos pasos (2FA) en su cuenta: es la que puede todo.

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

### Modo misión ✅ (anotado el 2026-09-27; hecho el 2026-09-28, ver D45)
Pantalla de trabajo a pantalla completa para **una práctica**, inspirada en una maqueta tipo "centro de comando" (historia a la izquierda, editor al centro, terminal abajo). Es **otra presentación**: no cambia lógica, monedas ni reglas.
- Se entra con un botón **"Entrar a la misión"** en cada práctica. La página del nodo queda como está (leer, repasar, celular). En celular no hay modo misión: sigue la vista actual.
- **Izquierda**, con pestañas: *Historia* (la crónica del nodo; resuelve dónde mostrar la historia), *Consigna* y *Teoría*. Debajo, las prácticas del nodo como checklist con los colores de estado; tocar una cambia de archivo.
- **Centro**: el editor ventana y la consola con pestañas que ya existen (`x-code-runner`).
- **Arriba**: misión, recompensa (+XP, +monedas) y **Entregar** siempre visible. Derecha opcional: devolución del profe y estado de la entrega.
- **Afuera**: inspector de memoria o Valgrind (propio de C++), "Ejecutar tests" (no hay corrección automática; lo más cercano es "coincide con la salida esperada") e indicadores decorativos falsos. "Pista (−XP)" sería una regla nueva de economía: se decide primero en GAMIFICACION.md.
- Estética: la paleta y tipografías actuales, más sobria que la maqueta.
- Próximo paso: propuesta de distribución (qué va en cada zona) para que el docente la ajuste antes de programar.

### Catálogo y "mis cursos" ✅ (anotado el 2026-09-27; hecho el 2026-09-28, ver D44)
Hoy *Mundos* muestra todos los cursos publicados (los propios y los cerrados, que llevan a la ficha con la inscripción), pero mezclados: el alumno no distingue cuáles son suyos ni si hay más. Y la raíz del sitio manda directo al login, así que un visitante no ve la oferta.

1. **Separar en el panel del alumno** (prioridad):
   - arriba, **"Mis cursos" / "Seguí donde dejaste"**: los que tiene abiertos o con abono, con el último nodo en el que va y un botón para continuar;
   - abajo, **"Descubrí más mundos"**: los publicados en los que no está, más los "Próximamente";
   - si no tiene ninguno, que se vea primero la oferta con un mensaje de bienvenida.
2. **Landing pública** (sin iniciar sesión) con una sección, más abajo, de **los cursos que más se dictan**: tarjetas con el logo, una línea de descripción, y los botones *Crear cuenta* y *Consultar por WhatsApp*. Estética del geco (DISENO.md), no corporativa. Probablemente haga falta una marca de **"destacado"** en el curso para elegir cuáles salen ahí.
3. **Datos para decidir** en cada tarjeta y ficha: nivel (desde cero / intermedio), duración aproximada (cantidad de nodos o semanas), modalidad y horario (ya existe en comisiones). **A decidir:** si se muestra el precio en pesos (hoy no es un dato del sistema; se maneja por WhatsApp o comprobante) o queda "Consultá".
4. **Cursos "Próximamente"**: un estado del curso para mostrarlo como adelanto sin abrirlo, con "Avisame cuando salga" (sirve para medir interés). Candidatos, según el material de FullCursos: C (01–02), C++ (03–11), Java (18–20), PHP (21), JS (22), TypeScript (23), Arduino (15), Phaser (16).
- **Top de héroes en la landing**: héroe (D38), cómo aparece en el ranking (apodo, o nombre e inicial) y XP de los mejores, para que los alumnos compitan. **Nunca el usuario de login** (es la mitad del acceso a la cuenta; decidido el 2026-09-27). Mismas reglas de privacidad que el ranking global: solo quienes tienen perfil público (los menores, con la autorización aprobada).
- **Ideas de diseño del docente (2026-09-28)**: referencias del Hall of Fame de La Rioja Aprende y una maqueta de Stitch. Se mantiene la paleta actual (azules y neones, DevLevel Obsidian).
  - **Portada**: título "Aprendé a programar avanzando por tu árbol de habilidades", botones *Ver cursos* y *Top 10*, y el **login a la derecha**, en la misma pantalla.
  - **Tarjetas de cursos**: logo, lenguaje, descripción corta, cantidad de nodos, nivel y botón.
  - **Cursos "Próximamente"** (decidido 2026-09-28): tarjeta con **imagen de referencia** (la portada del curso, `courses.cover`) y **qué se va a dar** (un temario corto: bloques o temas principales), sin botón de entrar. Nunca se presentan como si ya estuvieran disponibles ni como si se ejecutaran en el navegador (hoy solo Python).
  - **Monedas por curso** como coleccionables (cada curso tiene la suya, con su ícono del diccionario): encaja con el modelo real.
  - **Top 10**: **podio** para los 3 primeros (el 1.º más grande, con corona) y lista del 4 al 10 con héroe, apodo, rango (nombre del nivel), insignias y XP.
  - **Tendencia ▲▼** (viable, decidido 2026-09-28): no hace falta tiempo real. Se guarda una **foto diaria de las posiciones** la primera vez que alguien carga el ranking ese día (sin cron, como pide la regla de "todo en cada request"), y la flecha compara la posición de hoy con la foto anterior.
  - Nunca DNI ni datos personales en rankings.

**Posibles mejoras para más adelante** (Stitch las propuso; se evalúan cuando toque, no se hacen ahora):
- **Rachas de días** (🔥 "14 días"): días seguidos con actividad. Hay que definir qué cuenta (entregar, aprobar, abrir un nodo) y si da premio; se decide en GAMIFICACION.md.
- **Temporadas y ligas** con cierre y cuenta regresiva: choca con la XP permanente; posible como un ranking aparte que se reinicia (por ejemplo, XP del mes).
- **Especialidad en el ranking** ("C++ · Memory Guru"): posible con las Sendas (Fase 8) y sus insignias.
- **Entrar con passkey**.
- **Indicadores de estado del sistema** (compilador en línea, uptime): solo si algún día son reales.
- **Progreso de nodos por curso en las tarjetas** ("18/24"): solo para el alumno que inició sesión, en su panel.
- Sin filtros ni categorías por ahora: con 1–5 cursos no aportan.
- Toda regla de acceso nueva (landing pública, curso "Próximamente" que no se puede abrir) va con Policy y test Pest.

### Alta de alumnos por el docente ✅ (anotado el 2026-09-27; hecho el 2026-09-28)
Hay gente a la que el docente le crea la cuenta.

**Cómo quedó:** *Alumnos → Nuevo alumno* (`admin.students.create`) con clave provisoria generada (`StudentAccounts`, sin l/o/i para dictarla) y marca `users.must_change_password`: el middleware `password.changed` lo manda a *Elegí tu clave* (`password.change`) hasta que la cambie. La inscripción directa crea una solicitud de tipo `admin` y la aprueba con `EnrollmentApprover`. En la ficha: *Cuenta y contacto* (usuario, email, teléfono, botón de WhatsApp) y *Resetear clave*. Login y "Olvidé mi clave" muestran WhatsApp y Llamar al número de *Configuración*. Sin email, los avisos van solo a la campanita. Tests: `tests/Feature/Admin/StudentAccountsTest.php`.

Lo pedido:
- En *Alumnos* → **"Nuevo alumno"**: nombre, apellido, usuario, email, fecha de nacimiento (para saber si es menor) y **clave provisoria**. La cuenta se crea verificada.
- **Cambio de clave obligatorio** en el primer ingreso: hace falta una marca nueva en `users`.
- Botón para **copiar los datos de acceso** (usuario, clave provisoria y link), para mandarlos por WhatsApp.
- Opcional en el mismo formulario: **inscribirlo directo a un curso y a una comisión**. Pasa por `EnrollmentApprover`, así recibe las monedas del raíz y el abono como cualquier inscripción aprobada, y queda en el libro de movimientos.
- Si es menor, queda pendiente la autorización como en el registro normal.
- **Email opcional (decidido, D36)**: la cuenta puede ser solo con usuario. `users.email` pasa a nullable (sigue único cuando está). El formulario de registro también lo deja opcional.
- En la ficha del alumno: **editar email y usuario** y **"Resetear clave"** (otra clave provisoria + cambio obligatorio al entrar). Así el docente reactiva a quien perdió el acceso.
- Sin email: no hay "Olvidé mi clave" ni avisos por mail (los avisos siguen en la campanita).
- **Contacto por teléfono** (pedido del docente, para poder dar una mano):
  - el alumno ya puede cargar su **teléfono** (opcional) en *Mi cuenta → Perfil*; sumarlo también al **registro** y al **alta por el docente**, y que el docente lo vea y lo edite en la ficha del alumno, con botón para escribirle por WhatsApp;
  - en **"Olvidé mi clave"** y en el **login**: "¿No tenés email o no te llega? Escribile al profe" con botón de **WhatsApp** (chat o llamada) al número de *Configuración*. Si el número no está cargado, no se muestra;
  - el número del docente pasa a verse en páginas públicas: es una decisión consciente del docente.
- Solo el admin puede hacerlo: Policy y tests Pest.

### Cuentas compartidas: sesión única (y la IP como refuerzo) ✅ (anotado y decidido el 2026-09-30: sesión única, ver D65; la IP queda como refuerzo si hiciera falta)
Pedido: que una cuenta de alumno no la use otra persona. Dos caminos que el docente aceptó; se propone empezar por el primero.

**A · Sesión única (propuesta).** Una cuenta de alumno solo puede estar abierta en un lugar a la vez.
- Al iniciar sesión se borran las demás sesiones del usuario (las sesiones ya viven en la base: `SESSION_DRIVER=database`, tabla `sessions` con `user_id`). Quien estaba adentro, en su próximo pedido, vuelve al login con el aviso «Entraste desde otro lugar: por seguridad cerramos esta sesión».
- Cada desalojo se anota (`session_evictions`: usuario, cuándo, IP y navegador de las dos puntas, con `TRUSTED_PROXIES=cloudflare` para tener la IP real). Si pasa **3 o más veces en 24 h** (a definir), le llega un aviso en vivo al docente (D62) con el detalle.
- El docente, desde la ficha del alumno: **Bloquear** (no puede entrar; se cierran sus sesiones), **Desbloquear** y **Resetear clave** (ya existe en `StudentAccounts`). Bloqueado ve «Tu cuenta está pausada: escribile al profe» con el WhatsApp del docente.
- No afecta al docente (puede tener varias sesiones). No depende de la IP: los datos móviles no dan falsos positivos.
- Costo para el alumno honesto: PC y celular no pueden estar abiertos a la vez (uno cierra al otro).

**B · Distinta red (refuerzo, solo si A no alcanza).** Guardar la red de cada ingreso y comparar por rango (/24 en IPv4, /48 en IPv6). PC y celular en la misma casa comparten IP pública: valen. **Problema:** los datos móviles (4G, CGNAT) cambian de IP seguido → falsos positivos. Si se hace: redes conocidas por alumno que el docente aprueba, y al principio **solo alertar** (no bloquear) para medir.

**Para decidir:** ¿arrancamos con A? ¿cuántos desalojos por día disparan el aviso? ¿el bloqueo es solo manual (el docente decide) o automático al pasar el límite? Toda regla nueva de acceso va con Policy y tests Pest.

### Ejecutar las entregas al corregir (lado docente) 🔲 (anotado el 2026-09-30; decidido: primero **C++, Java y PHP** —de esos llegan correcciones— y después el resto; por ahora solo el docente, anotado para alumnos más adelante)
Pedido: poder correr en la plataforma el código de una entrega simple sin copiarlo a un editor local. Hoy ya pasa con **Python** (Pyodide en `x-code-runner` de *Admin → Entregas*).

- **Siempre en el navegador del docente** (WebAssembly en un Web Worker, con tiempo límite): el código del alumno sigue sin ejecutarse nunca en el servidor. El worker no ve la sesión ni las cookies.
- Solo **código simple**: un archivo, de consola, con la *Entrada de ejemplo* y comparando con la *Salida esperada* (la misma consola de Python: Salida / Entrada; la esperada, en «Cómo debería verse», D73). Los zip, lo que usa una base real (PDO/MariaDB, JDBC/PostgreSQL), ventanas (Swing, Qt, SDL), Laravel/Spring y Arduino se siguen probando en la compu del docente.
- Cada ejecutor es un módulo más en `resources/js/runners/` (como `python.js`), cargado solo cuando se usa y cacheado por el navegador.

| Orden | Lenguaje | Cómo | Descarga (una vez) | Nota |
|---|---|---|---|---|
| 1 | PHP (consola) | php-wasm (PHP 8.x) | ~15–20 MB | sin MariaDB; `readline`/`STDIN` con la entrada de ejemplo |
| 2 | JavaScript / HTML / CSS | iframe con `sandbox` (sin mismo origen) | nada | muestra la página y la consola |
| 3 | C | TinyCC compilado a WebAssembly | ~1–2 MB | C99 de consola (`scanf`/`printf`) |
| 4 | C++ | clang compilado a WebAssembly | ~30–60 MB | pesado pero solo del lado docente |
| 4 | Java | CheerpJ (`javac` + JVM en el navegador) | ~20 MB+ | lento al arrancar; **revisar la licencia** antes |
| — | SQL | sql.js (SQLite) | ~1 MB | aproximado: lo específico de MariaDB no anda |

**Avance (2026-09-30):**
- **C y C++: hecho** (D66). Clang 22 en WebAssembly desde el CDN, C++20 con excepciones, ~8–15 s por ejecución. Primera vez: ~105 MB de compilador (queda en caché).
- **PHP: hecho** (D68). PHP 8.3 en WebAssembly, ~60 ms por ejecución; primera vez: ~7 MB. Probado con 12 soluciones de referencia del curso (todas coinciden con la salida esperada), errores fatales, de sintaxis y bucles infinitos.
- **Java: decidido (D67), se prueba en la compu del docente.** CheerpJ es gratis solo para uso personal, libre o de evaluación (no permite alojarlo) y TeaVM-javac —la alternativa libre— hoy no sirve: su `javac` no resuelve `getMessage()`, `getClass()` ni `Integer.sum` y no trae `Scanner` (probado el 2026-09-30, también en su playground). Después se sumó el ejecutor local (D69): `scripts/JavaRunner.java` deja usar *Ejecutar* también en Java.

**Para decidir:** ¿el orden está bien? ¿se habilita también para los alumnos más adelante? (hoy la regla dice que C/C++/Java corren en la compu del alumno: cambiarla es una decisión aparte, en GAMIFICACION/ESPECIFICACION).

### Universo de cursos: mapa 3D y cursos nuevos armados con lo que ya existe 🔄 (anotado el 2026-09-30; pasos 1–3 hechos, ver D70; el 4 cuando se arme el curso de HTML)
Pedido: una vista grande del docente para ver cómo se vinculan todos los cursos (PHP da HTML y CSS; Python tiene Sendas web; JS va a necesitar HTML), encontrar lo repetido y lo que falta, y que los cursos que vengan (HTML, CSS, JS…) se armen con lo que ya está escrito en el universo en vez de cargarlo de nuevo.

**Decidido con el docente:**
- **Los cursos que ya están no se tocan**: su contenido se queda donde está, sin cambios de monedas, aperturas, abonos ni progreso. Los vínculos sirven para analizar y para armar cursos **nuevos**.
- **Vínculos por tema** (no nodo a nodo): un catálogo de temas y cada nodo marca qué temas enseña y cuáles usa. Solo así aparecen los faltantes.
- **En el mapa, solo nodos**: las prácticas se ven al elegir un nodo.

**1. Catálogo de temas.** `cursos/temas.md`: claves estables por familia y en orden de dificultad dentro de la familia (`html.estructura`, `html.formularios`, `css.selectores`, `css.flexbox`, `sql.joins`, `poo.herencia`, `web.http`…), con título y una línea de qué abarca. El orden es el que después usa el armado de un curso (de lo básico a lo avanzado).

**2. Marcar los nodos.** Dos claves nuevas en el `meta` del nodo (FORMATO-CURSO § 5), en el Markdown del curso para que sobrevivan al reimportar:
```meta
temas: html.formularios, css.selectores   # lo que el nodo ENSEÑA
usa: html.estructura                      # lo que da por sabido (de este u otro curso)
```
Marcar a mano los ~250 nodos actuales es mucho: Claude propone los temas de cada nodo leyendo su contenido y el docente los revisa en el mapa (aceptar / cambiar). Son metadatos: el alumno no ve nada distinto.

**3. El mapa (Admin → Universo).** 3D con **3d-force-graph** (mismo autor y API que `force-graph`, el del árbol), con rotación, zoom y botón para pasar a 2D.
- Cada curso es una galaxia con su color y su logo en el centro; sus nodos, como en el árbol.
- Arcos entre cursos: **mismo tema** (dos nodos enseñan lo mismo: repetido), **usa** (un nodo usa un tema que enseña otro curso).
- **Nodos fantasma** (grises, translúcidos): temas del catálogo que algún nodo *usa* pero ningún curso *enseña*, y los cursos «Próximamente».
- Clic en un nodo: curso, rama, temas, prácticas y los nodos de otros cursos con los mismos temas. Filtros por curso, por familia de temas y por tipo de vínculo; buscador.
- Tablero al costado: por familia de temas, qué está enseñado, dónde, cuántas veces y qué falta.

**4. Armar un curso nuevo desde el universo.** Se elige una familia (p. ej. `html.*` y `css.*`) y la plataforma junta **copias** de los nodos que enseñan esos temas, ordenadas según el catálogo, y escribe un **borrador** en el formato del importador (`cursos/<nuevo>/`), que se completa y revisa como cualquier curso (luego `app:simulate-course` antes de abrirlo).
- Se copia, no se comparte: cada curso queda independiente (corregir el de HTML no cambia el de PHP). Cada nodo copiado anota de dónde salió (`origen: php/R04-N02`), y el mapa lo muestra.
- Los temas del catálogo sin ningún nodo quedan como nodos vacíos marcados **FALTA**.
- Los textos con nombres del otro mundo (mentor, héroe, lugares, moneda) se marcan para reescribirlos con la historia del curso nuevo.

**Orden propuesto:** 1–2 (catálogo y marcado, sin interfaz nueva), 3 (el mapa), 4 (el armado; se usa cuando se arme el curso de HTML).

**Decidido después (2026-09-30):** el catálogo es una lista **ideal** (muestra también lo que ningún curso da; se le agregan ramas y caminos, como SDL, OpenGL o SFML, a medida que aparezcan) y el armado de un curso nuevo escribe el borrador como **archivos en `cursos/`** (el circuito de siempre: editar, revisar, simular, importar).
