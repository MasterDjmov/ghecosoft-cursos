# Gamificación — el corazón de la plataforma

> **Estado: EN CONVERSACIÓN.** Este documento junta lo que el docente definió (2026-09-26) y lo que falta cerrar.
> Cuando esté cerrado, se reescriben [ESPECIFICACION.md](ESPECIFICACION.md) y [PLAN.md](PLAN.md): la gamificación **deja de estar fuera de alcance** y pasa a ser el eje.

---

## 1. La idea en una frase

No es "te activo el curso y ves todo". El alumno **avanza por un árbol de habilidades que sigue la historia del curso**, y para abrir cada parte **gasta monedas que gana aprobando prácticas**. Así el docente se asegura de que lea, intente y entregue.

---

## 2. Lo que ya está decidido

### Foco
- **Primer curso: Python.** Es donde va a haber más alumnos de prueba. Todo se diseña y se prueba con Python primero.
- Cada lenguaje tiene su **historia (guion)**. La de Python se escribe aparte.
- La historia es la misma de `GUION.md` (Kira), pero **el mundo cambia de nombre**: "Codexia" ya existe en internet y se evita el choque legal. **Nombre nuevo: pendiente.**

### El árbol: nodo raíz, nodos y hojas
- **Cada curso es un árbol.** El **nodo raíz** lleva el **logo del curso** (Python, C…) y da acceso al curso. Se abre de tres maneras:
  1. con las **monedas base que entrega el docente** cuando confirma el pago (G13 y G17);
  2. (a confirmar, G23) con **monedas comodín** ahorradas.

  **El alumno siempre abre el raíz él mismo**: el pago le da las monedas, no le abre el curso. Después avanza nodo a nodo según su progreso, **mientras tenga el abono vigente** (ver "Abono de 30 días").
- **Forma del árbol: radial, como el de Path of Exile** (el docente lo eligió). El **logo del curso va en el centro** y las **ramas base salen alrededor**, igual que en PoE salen las clases (bruja, guerrero…). Las **ramas o el árbol de extras** (optativas) van **pegados al árbol principal**, en un anillo exterior o en un árbol "Extras" al lado. Detalle visual en [ARBOL-HABILIDADES.md](ARBOL-HABILIDADES.md).
- El **precio del nodo raíz es configurable por curso**, 10 por defecto (G14).
- El nodo raíz es una **"clase 0"**: instalar Python, presentarse, primer programa, y 1–2 obligatorias simples para ganar las primeras monedas enseguida (G15). El docente pidió **guía y orientación** para armar su contenido: es trabajo conjunto, junto con el guion de Python.
- Debajo del raíz, los **nodos** (temas) siguen un orden fijo que responde al aprendizaje: Comentarios → Variables → Estructuras de control…
- **Para abrir el nodo siguiente hacen falta las DOS cosas** (G1, decidido):
  - las **prácticas obligatorias del nodo anterior aprobadas**;
  - las **monedas** del costo del nodo.

  Tener ahorro no permite saltearse prácticas.
- El alumno **se organiza solo** con su ritmo y sus monedas.
- Al desbloquear un nodo se abren sus **hojas (prácticas)**. Ejemplo: 7 prácticas, de las cuales:
  - **5 obligatorias**: aprobadas, pagan **monedas del curso** para desbloquear el **siguiente nodo**;
  - **2 optativas**: pagan **monedas comodín** (extra) que el alumno puede ahorrar.
- La cantidad de hojas, obligatorias y optativas **varía por nodo** (7 = 5 + 2 es un ejemplo).

### Monedas
- **Una cuenta nueva arranca con 0 monedas** (G13). Si arrancara con 10, cualquiera que se registre tendría un curso gratis.
- **Flujo de ingreso:** se registra → pide inscripción (comprobante o WhatsApp) → clase virtual inicial → el docente confirma el pago y **le entrega las monedas base** (el precio del raíz) → el alumno abre el raíz.
- En ese momento **empieza el abono de 30 días** y el **conteo de días de cursada** (ver abajo).
- Se ganan con **prácticas aprobadas** por el docente, con un **monto fijo** por práctica.
- **No hay notas**: solo *Aprobada* o *Rehacer*. El alumno no tiene que sentirse forzado a una nota.
- **Intentos ilimitados.** Si le marcan *Rehacer*, reentrega hasta aprobar. **Paga lo mismo** que aprobar al primer intento.
- **La entrega fuera de término paga igual.**
- **Ajustes manuales** del docente (dar o quitar monedas) con motivo obligatorio. Hoy no se piensan usar como premio, pero sirven para **corregir una injusticia o un error**.

### Tipos de moneda (G19, decidido)

Las monedas **tienen tipo**, y cada tipo tiene su **ícono**. Referencia: `docs/referencias/monedas-por-lenguaje.png`, una moneda por lenguaje con su logo (Python, JS, TS, Java, C++…).

| Tipo | Ícono | Cómo se gana | En qué se gasta |
|---|---|---|---|
| **Moneda del curso** (por ejemplo, "moneda Python") | Moneda con el logo del curso | Monedas base del pago + prácticas **obligatorias** aprobadas de ese curso | **Solo en ese curso**: el raíz y los nodos del árbol principal |
| **Moneda comodín** | Ícono propio (a diseñar) | Prácticas **optativas** aprobadas | Nodos y clases **optativas / extras** de **cualquier curso con abono vigente**. **Nunca abre un nodo raíz**: el raíz se abre solo pagando (G23) |

- Así, **las monedas de un pago no se escapan** a otro curso: pagar Python da monedas Python.
- Esto reemplaza la idea anterior de "monedas globales que sirven en cualquier curso" (G3 queda resuelta con los tipos).

### Abono de 30 días y acceso permanente (G18, decidido)

**Son dos plazos distintos y no hay que confundirlos:**

| | **Plazo del abono** | **Acceso a lo visto** |
|---|---|---|
| Dura | **30 días** desde que el docente confirma el pago (**configurable por curso**, G24) — **cada curso tiene su propio abono** (G20) | **Para siempre** |
| Mientras está vigente | Puede **desbloquear nodos y avanzar** (incluidas ramas de extras) | Puede **ver y repasar** todo lo que ya desbloqueó, cuantas veces quiera |
| Cuando vence | **No puede desbloquear nada más ni entregar prácticas** (tampoco de nodos que ya abrió) hasta renovar, aunque tenga monedas y aunque haya dejado una rama por la mitad (G21). La **renovación solo extiende el plazo**: no da monedas (G22) | Sigue viendo todo hasta donde llegó |

- Ejemplo: paga Python, hace la mitad del árbol en 30 días y se le vence el abono. Sigue viendo esa mitad para siempre; para continuar, **renueva** 30 días.
- Si termina todo antes de los 30 días, el curso sigue disponible para repasar: "ya vio todo".
- El **conteo de días de cursada** (desde el primer pago hasta completar el árbol) se guarda **para todo**: CV, estadísticas del docente, ranking.
- ⚠️ **Cambia la regla 1 de la especificación** ("el acceso es permanente, sin vencimientos"). Ahora es: **acceso de lectura permanente + abono de 30 días para avanzar**.
- La renovación usa el **mismo circuito** que la inscripción (comprobante o WhatsApp → el docente aprueba). Sigue sin haber pago online.
- El vencimiento se calcula **en cada request** (`abono_vence_en >= hoy`), sin depender de cron. Un aviso "te quedan 3 días" se muestra al entrar; si hay cron, también se manda por mail.

### Corrección
- El docente corrige **todos los días**: una entrega no espera más de **24 h**. No hace falta pagar "a cuenta" al entregar.
- No se busca frustrar al alumno: si no le sale, sigue intentando y el docente lo acompaña con el hilo de comentarios.

### Ritmo: avance libre (G2, decidido)
- **No hay tope por fecha ni por comisión.** Si el alumno termina las prácticas al día siguiente de la clase y se las aprobás, sigue avanzando.
- La clase (presencial o virtual) es de acompañamiento: arranque, dudas, repaso. Un alumno que avanza solo no la necesita.
- **Consecuencia en el plan:** desaparecen la **liberación de clases por comisión** (`lesson_releases`: bloqueada/programada/disponible), la **grilla de liberación** del admin y los vencimientos (`due_at`). Lo que decide qué ve el alumno es **el árbol**, no el calendario.
- Nuevos estados de un nodo para el alumno:

  | Estado | Significa |
  |---|---|
  | **Bloqueado** | Le faltan obligatorias del nodo anterior |
  | **Listo para abrir** | Requisitos cumplidos; falta pagar las monedas |
  | **Abierto** | Pagado; está haciendo sus prácticas |
  | **Completado** | Todas sus obligatorias aprobadas |

- La regla de seguridad "un alumno nunca ve clases no liberadas" pasa a ser **"nunca ve nodos que no abrió"**, con Policy y tests igual que antes. Excepción (2026-09-30, D71): la **Clase 0 de prueba** — cualquier cuenta sin abono de un curso lee y practica su raíz gratis, sin entregar ni dejar registros; para que el profe corrija y seguir, pide el abono (y el mes corre desde que se aprueba).

### Prácticas sin entrega (instalar, leer, extras)
- **Todas** las prácticas, obligatorias y optativas, tienen **"Marcar como completada"**.
- Para las que no tienen entrega real, como instalar el entorno o leer un extra, el docente **elige por práctica** si paga monedas o no. Por defecto **no pagan**: son comunes a todos.

### Además de las monedas
- Se suman **XP, niveles, insignias y ranking (top ten)**.
- La plataforma **genera un CV** del alumno que pueden mirar **entidades externas**, por ejemplo el Ministerio de Educación o el de Trabajo.
- Idea de origen: el proyecto **La Rioja Aprende** (ver § 4).

---

## 3. Modelo propuesto (borrador para discutir)

### Dos contadores distintos: monedas ≠ XP

| | **Monedas** | **XP** |
|---|---|---|
| Para qué | **Gastar**: desbloquear nodos, cursos, extras | **Medir**: nivel, ranking, CV |
| ¿Baja? | Sí, al gastar | **Nunca** |
| Se gana con | prácticas aprobadas, ajustes manuales | prácticas aprobadas, nodos completados, insignias |

**Por qué separarlas:** si el ranking fuera por monedas, **gastar te hundiría en la tabla**. Entonces el alumno ahorraría en vez de avanzar, que es justo lo contrario de lo que se busca.

### Libro de movimientos (no solo un saldo)

- Cada moneda y cada punto de XP que entra o sale es **un registro**: quién, cuánto, por qué (práctica aprobada, nodo desbloqueado, ajuste del docente), en qué curso y cuándo.
- El saldo es la suma de los movimientos.
- Con esto:
  - se ve en *Mi cuenta* de dónde salió cada moneda;
  - un error se corrige con un **movimiento inverso**, sin borrar nada;
  - cada movimiento lleva su **tipo de moneda** (moneda Python, comodín…): el saldo de cada tipo sale del mismo libro, sin billeteras separadas.

> Lección de La Rioja Aprende: ahí el XP se suma con `increment('xp_total')` en **8 lugares distintos** del código y no hay historial. Acá toda la plata pasa por **un solo servicio** (`Wallet`/`Ledger`).

### Economía de ejemplo (números a ajustar)

| Concepto | Monedas | XP |
|---|---|---|
| Saldo al registrarse | 0 | 0 |
| Pago confirmado por el docente | +10 **moneda Python** (precio del raíz) | — |
| Abrir el nodo raíz | −10 moneda Python | — |
| Desbloquear un nodo | −10 | — |
| Práctica obligatoria aprobada (×5) | +2 moneda Python c/u → **10** | +10 c/u |
| Práctica optativa aprobada (×2) | +3 **comodín** c/u → **6 de ahorro** | +15 c/u |
| Nodo completo (todas las obligatorias) | — | +20 bonus |

Con estos números:
- cada nodo se "paga" solo con sus obligatorias;
- las optativas generan **ahorro**;
- un alumno que hace todas las optativas junta ~6 monedas por nodo.

Todos los montos se configuran **por nodo y por práctica** desde el admin.

### Cómo se traduce el material de `FullCursos` (Python)

| Árbol | Material |
|---|---|
| Rama / región | Bloque ("Fundamentos — Kira despierta en el Valle") |
| **Nodo** | Ejemplo `NN-Tema` (01-Hola-Python, 02-Tipos…): explicación + ejemplo resuelto |
| **Hojas obligatorias** | Las **Misiones** del README (hoy son 3) |
| **Hojas optativas** | **Encargo del Gremio** + desafíos extra (hoy hay 1) |
| Nodo final del bloque | Proyecto / jefe del bloque |

> ⚠️ Hoy cada ejemplo tiene **3 misiones + 1 encargo = 4 prácticas**, no 7. O se escriben más prácticas por tema, o el número por nodo queda variable (3–5 obligatorias, 1–2 optativas). Ver G6.

### Cambios en el modelo de datos (respecto de PLAN.md)

- `assignments` pasa de "1 por clase" a **N prácticas por nodo**, cada una con: `is_required`, `coin_reward`, `xp_reward`, `requires_submission` y el modo de entrega.
- `submissions.grade` **se elimina**: solo `entregada` | `aprobada` | `rehacer`.
- Tablas nuevas:
  - `currencies`: tipos de moneda (código, nombre, ícono, `course_id` nulo = comodín);
  - `coin_transactions` (con `currency_id`) y `xp_transactions`;
  - `course_subscriptions`: abonos (alumno, curso, desde, **vence_en**, solicitud de pago que lo originó). Las renovaciones son filas nuevas;
  - `node_unlocks` (quién desbloqueó qué nodo, cuándo, cuánto pagó);
  - `badges` + `user_badges`;
  - `levels`.
- El nodo del árbol = la clase (`lessons`) + su orden + su costo en monedas.

---

## 4. La Rioja Aprende: qué se puede aprovechar y qué no

Proyectos analizados: `/var/www/html/larioja-aprende-api-fase3` (backend) y `/var/www/html/larioja-aprende-web-fase3` (frontend). Todavía no están en producción.

### Qué es

| | La Rioja Aprende | Esta plataforma (GhecoSoft-Code) |
|---|---|---|
| Público | Inicial, primaria, secundaria (**menores**) | Secundaria, terciario, universidad, particulares |
| Estructura | Instituciones → aulas → docentes, secretarios, directores, técnicos, ministerio | Un docente → cursos → comisiones |
| Identificación | **DNI** (el alumno entra con DNI + clave) | Email (el alumno se registra solo) |
| Backend | Laravel 13 API + Sanctum + Spatie Permission | Laravel + Livewire (monolito) |
| Frontend | **Next.js 16 + React 19** (necesita Node corriendo) | Blade/Livewire, sin Node en el servidor |
| Base | **PostgreSQL 16** | **MariaDB** |
| Hosting | (a definir) | Duplika, cPanel compartido |

### Gamificación que ya tiene (ideas reutilizables)

| Pieza | Cómo está hecha allá | Qué tomar |
|---|---|---|
| **XP y niveles** | `alumnos.xp_total` + tabla `niveles_xp` con nombre de rango y descripción narrativa ("Explorador Nova", "Cadete Nova") | ✅ La idea de **rangos con nombre narrativo** del guion |
| **Insignias** | `insignias` + `insignias_alumno`; se otorgan **automáticamente por condición** (primera misión, 5 nodos…) o a mano | ✅ Igual: catálogo + reglas automáticas + otorgamiento manual |
| **Árbol** | `arboles_curriculares` + `arbol_nodos` (padre, orden, `es_opcional`, `ph_requeridos`, `costo_recursos`, posición x/y, assets por estado) + `arbol_progreso_alumno` | ✅ Casi el mismo concepto: nodos con costo y opcionales. Hay que agregarle las hojas/prácticas |
| **Recursos / objetos** | cristales, núcleos; `desbloqueos_catalogo` (qué se compra con qué) | ✅ Modelo de "tienda": catálogo de desbloqueos con precio |
| **Avatar** | Personaje que se viste: `items_avatar` (gorro, torso, pantalón, accesorio, en SVG) comprados con recursos | 🟡 Lindo para después; no es prioridad para Python |
| **Ranking** | Provincial / institución / aula, ordenado por XP, con caché de 5 min | ✅ Top ten por curso y global, ordenado por XP |
| **CV** | `ServicioCvNova`: datos, rango, historial institucional, misiones, nodos completados, insignias, progreso por isla | ✅ La estructura del CV |
| **Panel Ministerio** | Dashboard provincial, destacados, **score** configurable (XP × 0,7 + misiones × 10 + nodos × 15), olimpiadas, becas | ✅ La idea del **score configurable** y la vista de "entidad observadora" |
| Duelos, laberinto, pozo cooperativo, runner | Juegos para chicos | ❌ No aplican a este público |

### ¿Fusionar los proyectos?

**Recomendación: no fusionar el código ahora, pero dejarlo preparado para conectarse.**

1. **Choque técnico con el hosting** (verificado el 2026-09-26 en el servidor `mate`):
   - **Node 20 está, y cPanel ofrece "Setup Node.js App"** (CloudLinux + Passenger). **Next.js puede correr en el servidor**, así que ya no es un impedimento técnico. Lo que queda por medir:
     - consumo de memoria de `next start` frente a los límites del plan compartido (Next suele pedir 200–500 MB);
     - que Passenger reinicia la app cuando está inactiva (el primer pedido después es lento).

     La alternativa sigue siendo exportarlo como sitio **estático** (`output: 'export'`) si no usa funciones de servidor de Next.
   - **No hay PostgreSQL.** Pasar La Rioja Aprende a MariaDB es posible (Laravel abstrae casi todo), pero hay que revisar columnas JSON, búsquedas con `ILIKE`, *data migrations* con SQL propio y los tipos específicos de Postgres.
2. **Público y datos distintos:** allá hay menores e instituciones; acá, adultos y particulares.
   - Mezclarlos en una base complica permisos y **protección de datos** (Ley 25.326).
   - Más todavía si un ministerio va a mirar perfiles.
3. **Tamaño:** La Rioja Aprende tiene 16 dominios y ~80 migraciones. Meter los cursos ahí retrasa el curso de Python.

**Cómo dejarlo preparado:**
- Guardar el **DNI** como dato **opcional** del perfil. Es la llave natural para cruzar las dos plataformas.
- Usar los **mismos conceptos y nombres** (XP, nivel, insignia, nodo, CV) para que una integración futura sea directa.
- Más adelante, una **API de solo lectura** ("logros del alumno X por DNI") para que La Rioja Aprende o un ministerio consulten el CV, **con consentimiento del alumno**.

---

## 5. CV, ranking y entidades externas: cuidados

- **Consentimiento:** el CV y la aparición en el ranking público tienen que ser **opt-in**. El alumno tilda "Compartir mi CV públicamente" (decidido en G10, § 7).
  - Sin eso, figura con alias o no figura.
- **Menores (G12, decidido):** hay alumnos menores de 18. Se les da una **nota de autorización** que firman el **docente**, el **alumno** y su **adulto responsable** (madre, padre o tutor: legalmente la firma que cuenta es la del adulto). El alumno **la sube a la plataforma** (disco privado, como los comprobantes). El docente la revisa y la marca como válida. **Hasta entonces, el menor no aparece en el ranking global ni tiene CV público.** Hace falta guardar la **fecha de nacimiento** (o un tilde "soy menor de 18") para saber a quién pedírsela.
- **Rol `observador`** (opción B, **para más adelante**; hoy se usa la opción A, ver § 7):
  - una cuenta para cada entidad (por ejemplo, Ministerio de Trabajo);
  - **solo lectura** de rankings y CVs públicos;
  - sin acceso a entregas, código ni comentarios.
- **Qué muestra el CV:**
  - cursos y nodos completados, prácticas aprobadas, insignias, nivel, fechas;
  - **nunca** el código entregado ni los comentarios del docente, salvo que el alumno lo elija.
- **Justicia del ranking:** como las aprobaciones dependen del docente, el ranking mide **constancia y avance**, no "nota". Conviene aclararlo en la vista pública.

---

## 6. Preguntas para seguir la charla

**Cerradas:**
- **G1:** obligatorias aprobadas **+** monedas.
- **G2:** avance libre, sin tope.
- **G5:** el nodo raíz de cada curso se abre con monedas (iniciales o ahorradas) o con pago real.

**Cerradas también (tanda 4):**
- **G20:** abono **por curso**.
- **G21:** vencido = no desbloquea **ni entrega**; leer y repasar sigue libre.
- **G22:** renovar solo extiende el plazo, sin monedas.
- **G23:** el comodín sirve para extras de cualquier curso con abono vigente, **nunca para raíces**.
- **G24:** duración del abono configurable por curso, 30 días por defecto.

**Cerradas también (tanda 3):**
- **G18:** abono de 30 días para avanzar + acceso de lectura permanente; los días de cursada se registran para todo.
- **G19** (y con ella G3): monedas con tipo. Las del curso solo sirven en ese curso; las comodín salen de las optativas.

**Cerradas también (tanda 2):**
- **G13:** 0 monedas al registrarse; el docente entrega las monedas base al confirmar el pago, después de la clase virtual.
- **G14:** precio del raíz configurable por curso, 10 por defecto.
- **G15:** el raíz es una clase 0; se arma con guía.
- **G16:** comisiones como grupo opcional por ahora. Las clases suelen ser **individuales**; un **proyecto grupal** puede sumarse más adelante.
- **G17:** el pago solo entrega las monedas base; el alumno abre el raíz y avanza según su progreso.

**Cerradas también (tanda 5):**
- **G4:** los comodines se gastan en **extras de otros cursos**, siempre que el alumno tenga abierto el **nodo raíz** de ese curso (y abono vigente, G23). Más adelante, **pistas, cosméticos y eventos**: se irán viendo.
- **G6:** cantidad de prácticas **variable por nodo**. Para Python se arranca con 3 obligatorias + 1–2 optativas. En el admin, cada nodo tiene un botón **"+ Nueva hoja"** para sumar prácticas cuando haga falta.
- **G7:** al final de **cada bloque** hay un **nodo jefe (boss)**: un proyecto integrador que da XP extra y una **insignia**. El nodo completo también suma XP bonus.
- **G9:** top ten **por curso**, visible entre compañeros. Ranking global y CV público **solo con opt-in**.
- **G11:** **DNI opcional**. No se pide al registrarse, pero el alumno lo puede cargar en *Mi cuenta*, por si más adelante se dan **certificados**.
- **G12:** **sí hay menores**. Para ellos, una **nota de autorización firmada** (por el docente, el alumno y su adulto responsable, ver § 5) que se **sube a la plataforma** y queda como constancia.

**G8 y G10 (explicadas y resueltas):**

| # | Tema | Estado |
|---|---|---|
| G8 | Nombres narrativos de monedas y niveles | **Resuelto el mecanismo**: diccionario narrativo editable en el admin (§ 8). Los nombres concretos se cargan con el guion de Python |
| G10 | Entidades externas (ministerios, etc.) | **Cerrada: opción A** (link público del CV), con **tilde del alumno** para compartirlo o no (§ 7) |

---

## 7. Entidades externas (G10): opciones

Qué se busca: que el Ministerio de Educación, el de Trabajo u otras instituciones puedan ver a los alumnos destacados y su CV.

| Opción | Cómo funciona | Esfuerzo | Control |
|---|---|---|---|
| **A. Link público del CV** | Cada alumno que acepta tiene una página `ghecosoft…/cv/kira-perez`, que él comparte (con un ministerio, en LinkedIn, en una búsqueda laboral). También se descarga en PDF | Bajo | El alumno decide a quién se la manda |
| **B. Cuentas de "observador"** | El docente crea una cuenta para cada entidad. Entra y ve **rankings y CVs** de los que aceptaron, con filtros (curso, provincia, edad) | Medio | El docente decide qué entidad entra |
| **C. Conexión con La Rioja Aprende** | Una API de solo lectura: La Rioja Aprende consulta "logros del alumno con DNI X" y los muestra en su panel del Ministerio | Alto | Depende de acuerdos entre plataformas |

**Recomendación:** **A** en la primera versión (sale casi gratis con el CV), **B** cuando una entidad lo pida concretamente y **C** solo si La Rioja Aprende llega a producción y hay un acuerdo.

---

## 8. Diccionario narrativo (decidido: se gestiona desde el admin)

El docente pidió un **diccionario online en el admin** para manejar los nombres de los elementos del juego y partes de la historia **sin tocar código**. Resuelve G8: los nombres se cargan cuando esté el guion y se cambian cuando haga falta.

### Cómo funciona

- En el código, cada elemento tiene una **clave fija en inglés** (`coin.course`, `coin.wildcard`, `xp`, `level.3`, `node.boss`…). En la pantalla se muestra **el nombre que el docente cargó** en el diccionario.
- **Dos niveles:**
  - **General (plataforma):** valores por defecto ("Moneda", "Comodín", "Experiencia").
  - **Por curso / región:** reemplaza al general dentro de ese curso ("Escama" en Python, otro nombre en C).
  - Si un curso no define un término, usa el general.
- Si falta un término en los dos niveles, se muestra el nombre técnico en español, así nunca queda un hueco en pantalla.

### Qué tiene cada entrada

| Campo | Para qué | Ejemplo |
|---|---|---|
| Clave | Fija, la usa el código (no se edita) | `coin.course` |
| Ámbito | General o un curso | Python |
| Singular / plural | "1 escama", "3 escamas" | Escama / Escamas |
| Género | Para que las frases salgan bien en español ("**la** escama", "**el** rubí"; "ganaste **una**…") | femenino |
| Ícono / imagen | La moneda, la insignia, el retrato del mentor | `escama.png` |
| Descripción corta | Tooltip o leyenda | "Se ganan aprobando misiones del Valle" |
| Texto de historia (lore) | Párrafo narrativo, en markdown | La crónica del rango o del jefe |

### Qué entra en el diccionario (primera lista)

| Grupo | Claves |
|---|---|
| Mundo | nombre del mundo (reemplaza a "Codexia"), nombre de la región del curso, mentor (nombre, retrato, presentación) |
| Economía | moneda del curso, moneda comodín, XP |
| Progreso | cada **nivel/rango** (nombre, XP necesaria, texto narrativo), nodo, hoja/práctica, nodo jefe |
| Estados | "Bloqueado", "Listo para abrir", "Abierto", "Completado" (si se quieren con sabor narrativo) |
| Historia | crónica de entrada al curso, texto de cada jefe, mensaje al completar un bloque, mensaje al completar el curso |
| Bestiario | slime, goblin, esqueleto, orco, ogro, troll, dragón: nombre e imagen (se usan en "Errores habituales") |

### Pantalla del admin

- **Configuración → Diccionario**, con filtro por ámbito (General / cada curso) y por grupo.
- Edición en línea con **vista previa**: "Así lo ve el alumno: *Ganaste 3 escamas*".
- Botón **"Copiar del general"** para arrancar un curso nuevo con los valores por defecto.
- Solo el admin lo edita. Los cambios se ven al instante; los textos se guardan en caché y la caché se limpia al guardar.

### Qué NO va en el diccionario

- El **contenido de las clases** (explicaciones, prácticas): eso va en el editor de nodos.
- Los **montos** (precio del raíz, monedas por práctica, días de abono): eso es configuración del curso y de cada nodo, no texto.

### Decisión (G10): opción A con tilde del alumno

- En *Mi cuenta → Privacidad*, el alumno tiene un tilde **"Compartir mi CV públicamente"**, **apagado por defecto**.
  - **Apagado:** la página `/cv/{alias}` responde "Este perfil es privado" (no revela ni el nombre). Tampoco aparece en el ranking global.
  - **Encendido:** la página muestra el CV y se puede descargar en PDF. El alumno copia el link y lo comparte donde quiera.
- El alumno lo puede **prender y apagar cuando quiera**. Al apagarlo, el link deja de mostrar datos al instante.
- **Menores:** el tilde está **deshabilitado** hasta que el docente apruebe la nota de autorización firmada (G12).
- El **alias** del link lo elige el alumno (por ejemplo, `kira-perez`) y no puede ser el DNI ni el email.
- El **ranking dentro del curso** (top ten entre compañeros) no depende de este tilde. El alumno puede aparecer con su **nombre o con un apodo**, a elección (ver § 5).
- Las opciones **B** (cuentas de observador) y **C** (conexión con La Rioja Aprende) quedan para más adelante.
