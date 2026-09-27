# Diseño visual — análisis de referencias

> Capturas en las carpetas `docs/referencias/imagenes digital house idea 1/` (17 capturas) y `docs/referencias/stich idea 2 me gusta/` (2 imágenes).
> **Estado:** la idea 2 quedaba en pausa hasta que el docente explicara cómo encararla.
> **Actualización:** la marca **GhecoSoft-Code** y la paleta oscura **"DevLevel Obsidian"** ([IDENTIDAD-VISUAL.md](IDENTIDAD-VISUAL.md)) confirman la dirección de la idea 2. La **estructura** de la idea 1 (DH) se mantiene; lo que cambia es la **piel**. Los tokens claros de § 1 quedan como base del tema claro opcional.

---

## 1. Idea 1 — Digital House Playground (base definida en la especificación)

### Qué muestran las capturas

| Captura | Pantalla | Qué tomamos |
|---|---|---|
| `…200222` | Catálogo público | Hero violeta con degradé, tarjetas de categoría, grilla de tarjetas de curso |
| `…200224`, `…200226` | Mis contenidos | Topbar blanca (hamburguesa + logo / avatar), sidebar mínima "APRENDER", pestañas *En curso / Finalizados* con subrayado violeta, tarjeta con patrón de puntos, pill "8 clases" y barra de progreso en el borde inferior |
| `…200227` | Registro | Formulario centrado de 1 columna, nombre+apellido en 2 columnas, texto de reglas de contraseña, **medidor de 3 barras** + "Seguridad", botón violeta a lo ancho |
| `…200229` | Menú del avatar | Avatar cuadrado-redondeado violeta con iniciales; menú con nombre+email, "Mi cuenta" y "Salir de la cuenta" en rojo |
| `…200231`–`…200241` | Mi cuenta | Sub-navegación en tarjeta a la izquierda; tarjetas de formulario con **encabezado / cuerpo / pie gris con botón Guardar** |
| `…200243`, `…200245` | Curso → Contenidos | Acordeón de unidades con **número en círculo verde**, "n clases"; clases en verde; tarjeta lateral **"Continuá cursando"** con progreso y botón Continuar |
| `…200246`, `…200249` | Vista de clase | Barra superior con nombre del curso, título centrado con flechas ← →, contenido en tarjeta blanca grande, **panel "Contenido" a la derecha** colapsable con el mismo acordeón |
| `…200251` | Evaluación | Tarjeta con ilustración, lista de condiciones con íconos, badge "Aprobado" |

### Qué **no** tomamos (fuera de alcance o pedido explícito)
- Pagos, Educación y empleo, Preferencias de idioma, datos de residencia, bio.
- Filtros por Tecnología/Nivel/Duración del catálogo (con pocos cursos no hacen falta).
- Reproducción automática entre clases.

### Tokens propuestos (Tailwind v4 `@theme`)

| Token | Valor aprox. | Uso |
|---|---|---|
| `--color-bg` | `#F4F4F6` | Fondo general |
| `--color-surface` | `#FFFFFF` | Tarjetas, topbar |
| `--color-border` | `#D9D6E3` | Bordes suaves (tinte violeta) |
| `--color-primary` | `#9A5CF5` | Botones, pestaña activa, avatar |
| `--color-primary-soft` | `#E9E3F7` | Ítem activo de sidebar, botón secundario |
| `--color-success` | `#22C55E` | Unidad/clase completada, "Aprobada" |
| `--color-warning` | `#F59E0B` | Programada, "Rehacer" |
| `--color-danger` | `#EF4444` | Salir, errores, rechazada |
| `--color-muted` | `#6B6880` | Textos secundarios |
| Tipografía | **Plus Jakarta Sans** (títulos) + **Inter** (texto) + **JetBrains Mono** (código) | Google Fonts, o autoalojadas en `public/fonts` |
| Radios | 8 px (inputs/botones), 12 px (tarjetas) | |

> En DH el botón "Continuar" es azul (`#3B5BFD`). Propongo **unificar en violeta** para tener un solo color primario.

### Íconos de estado de clase
| Estado | Ícono | Color |
|---|---|---|
| Completada | check en círculo | verde |
| Disponible | play / documento | violeta |
| Programada | reloj + "Se abre el 12/10 08:00" | ámbar |
| Bloqueada | candado, título en gris, sin link | gris |

### Responsive
- < 1024 px: la sidebar pasa a *drawer* con la hamburguesa; la tarjeta "Continuá cursando" pasa arriba del acordeón.
- Vista de clase en celular: el panel "Contenido" se abre como hoja desde la derecha; flechas ← → fijas abajo.

---

## 2. Idea 2 — "CodeQuest" (Stitch) — análisis sin decidir

### Qué muestran las imágenes

**`image.png` — tablero / roadmap**
- Tema **oscuro** (azul noche `#0B1220`), acento **cian** (`#22D3EE`), secundarios violeta/ámbar/verde.
- Tipografía monoespaciada para etiquetas (`SYSTEM / CAMPAIGN_MAP / …`, "TRACK 01", "LVL 5/5").
- Hero de "misión actual" con progreso y un gran botón **"Continuar Misión: Lab 07"** — equivale a nuestra tarjeta *Continuá cursando*.
- **Rutas** (tracks) con tarjetas de módulo por estado: completado (verde), en curso (borde cian brillante), bloqueado (atenuado con candado) — equivale a unidades → clases con íconos de estado.
- Columna derecha con *bounty diario*, *battle pass*, *leaderboard*, XP, gemas, rachas → **gamificación: fuera de alcance** según la especificación.

**`WhatsApp Image … .jpeg` — vista de una misión (clase/tarea)**
- Layout tipo **IDE de 3 columnas**:
  1. Izquierda: *Briefing* (explicación) con pestañas Briefing / Objetivos / Docs y un **checklist de objetivos**.
  2. Centro: **editor con pestañas de archivos**, números de línea, barra de estado y **consola de salida** abajo.
  3. Derecha: inspector de memoria / resultado de Valgrind y botones "Pista", "Ejecutar tests", "Desplegar".
- Encaja muy bien con nuestro bloque **Tarea** (editor CodeMirror + stdin + salida + Entregar).

### Qué se podría reutilizar sin salir del alcance
- Layout de 3 columnas para la **tarea** (consigna | editor + salida | entrega + historial/hilo).
- Tema oscuro para el **editor y la consola** (CodeMirror con tema oscuro) aunque el resto sea claro.
- Tarjetas de estado por clase con borde de color (completada / en curso / bloqueada).
- Etiquetas monoespaciadas como detalle tipográfico.

### Qué choca con la especificación
- XP, gemas, niveles, rankings, recompensas, "raids" → gamificación (fuera de alcance).
- "Ejecutar tests" automáticos, compilador C++ en vivo, Valgrind → corrección automática y ejecución de C/C++ (fuera de alcance).
- Modo oscuro total vs. "fondo gris claro" pedido para el alumno.

### Preguntas para cuando expliques cómo encararla
1. ¿La idea 2 **reemplaza** a la de Digital House o se **combina** (por ejemplo, DH claro para navegación y estilo IDE oscuro solo en la vista de clase/tarea)?
2. ¿Querés **modo claro/oscuro con selector** en *Mi cuenta*, o un solo tema?
3. ¿Algún elemento "de juego" querés mantener como puramente visual (por ejemplo, etiquetas tipo "UNIDAD 01" en mono, barras de progreso con brillo), sin puntos ni rankings?
4. ¿El layout de 3 columnas va solo en escritorio, con pestañas (Consigna / Código / Entrega) en celular?
5. ¿Qué nombre y logo usa la plataforma?

Hasta tener estas respuestas, la **Fase 1** arma el layout con los tokens de la idea 1, todos definidos como variables CSS, para poder cambiar a la idea 2 (o sumar tema oscuro) sin reescribir componentes.
