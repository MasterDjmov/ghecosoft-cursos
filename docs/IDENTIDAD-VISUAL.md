# Identidad visual — GhecoSoft-Code

> Fuentes, en la raíz del proyecto:
> - `docs/referencias/logo/logo.jpeg` (1024×1024);
> - `docs/referencias/logo/banner.jpeg` (1376×768);
> - `docs/referencias/colores/colores.md` + `docs/referencias/colores/colores.png`: el sistema **"DevLevel Obsidian"**.
>
> Complementa a [DISENO.md](DISENO.md). Este material **define la dirección de la idea 2** (CodeQuest).

---

## 1. Marca

| Elemento | Qué es |
|---|---|
| **Nombre** | **GhecoSoft-Code** ("GhecoSoft" en blanco + "-Code" en cian). Reemplaza el nombre provisorio "La Rioja Aprende" de PLAN.md (P5) |
| **Mascota** | Un **geco holográfico**: cian/verde con reflejos violeta, anteojos-visor con código y una pantallita flotante con cursor. Pose segura, sonriente |
| **Personalidad** | Ciber-aprendizaje, cercano, tecnológico, con humor. Tono "compañero que ya sabe", no "profesor serio" |
| **Emblema** | Círculo con trazos de circuito y los signos `</>`, `<`, `>` en los cuatro puntos cardinales |

### El geco como tutor

`colores.md` lo nombra "Gheco Hologram" y habla de un **"asistente flotante del geco tutor"**. Encaja con "Las Crónicas del Código" ([CURSOS-EXISTENTES.md](CURSOS-EXISTENTES.md) § 1), donde **cada región tiene un mentor** (Ofidia, Maese Ferrum, Kaffa). Hay dos lecturas posibles:

- **a)** el geco es la mascota **de la plataforma**: bienvenida, estados vacíos, errores 404, avisos. Los mentores quedan **dentro de cada curso**;
- **b)** el geco reemplaza a los mentores.

Recomiendo **a)**, porque no obliga a reescribir el guion. Ver pregunta V3.

### Estado de los archivos de logo (para usarlos en la web)

| Necesidad | Lo que hay | Qué falta |
|---|---|---|
| Logo en la barra superior (horizontal, chico) | Solo el emblema cuadrado con fondo negro | Versión **horizontal** (geco + texto) y versión **solo isotipo** |
| Fondo transparente | JPEG con fondo negro (no tiene transparencia) | **PNG con transparencia o SVG** |
| Favicon / ícono de pestaña | — | 32×32, 180×180 (Apple), 512×512 (PWA). La cara del geco sola se lee mejor que el emblema completo |
| Portada del login / registro / catálogo | `banner.jpeg`: el geco y un alumno programando | Sirve tal cual como imagen de fondo o héroe. Conviene exportarlo en **WebP** (~100 KB) |
| Imagen al compartir un link (Open Graph) | — | 1200×630 a partir del banner |

> Detalle: el texto que aparece en las pantallas del banner es "pseudo-código" generado por IA (no es código real). Sirve como ambientación; no lo usaría como ejemplo de programación.

---

## 2. Paleta "DevLevel Obsidian" (de `docs/referencias/colores/colores.md`)

### Superficies (tema oscuro)

| Token | Hex | Uso |
|---|---|---|
| `surface` | `#0B1326` | Fondo principal |
| `surface-lowest` | `#060E20` | Terminales, sidebars, paneles hundidos |
| `surface-low` | `#131B2E` | Tarjetas, topbar |
| `surface-container` | `#172036` | Superficies intermedias |
| `surface-high` | `#1D263D` | Tarjeta activa / destacada |
| `surface-highest` | `#242E47` | Hover, inputs activos |
| `surface-bright` | `#31394D` | Bordes de sección, elevaciones |
| `neutral` (paleta base) | `#0F172A` | Escala de grises azulados |

### Acentos

| Token | Hex | Uso |
|---|---|---|
| `primary` | `#06B6D4` (base) / `#22D3EE` (brillo) | Acción principal, elemento activo, el geco |
| `secondary` | `#8B5CF6` / `#A855F7` | Acento secundario, rareza, circuitos |
| `tertiary` / `success` | `#10B981` | Completado, aprobado, "build OK" |
| `warning` | `#F59E0B` | Programada, "Rehacer", avisos |
| `danger` | `#EF4444` | Errores, rechazada, tiempo agotado |

### Texto

| Token | Hex | Uso |
|---|---|---|
| `on-surface` | `#E2E8F0` | Texto principal |
| `on-surface-variant` | `#94A3B8` | Metadatos, descripciones |
| `outline` | `#334155` o `rgba(6,182,212,.2)` | Bordes sutiles, "trazos de circuito" |

### Tipografía

| Rol | Fuente | Dónde |
|---|---|---|
| Títulos, navegación, cifras | **Space Grotesk** | h1–h3, títulos de clase/unidad, contadores |
| Lectura | **Inter** | Explicaciones, consignas, crónicas |
| Código y etiquetas | **JetBrains Mono** | Editor, consola, badges ("UNIDAD 01"), atajos |

### Formas y efectos

- Radios **chicos**: 4–8 px (`rounded-md`/`rounded-lg`), estilo "hardware". Es distinto de los 12 px que propuse para la idea 1.
- **Halo** para el elemento activo: `0 0 20px -3px rgba(6,182,212,.35)` (cian) o `rgba(139,92,246,.35)` (violeta).
- **Vidrio**: `backdrop-blur-md` sobre `rgba(11,19,38,.85)`, para modales, el panel lateral de la clase y el menú del avatar.
- Sombra profunda: `0 4px 24px -2px rgba(0,0,0,.7)`.

### Chequeos de accesibilidad (a validar en Fase 1)

| Combinación | Resultado esperado |
|---|---|
| Texto `#E2E8F0` sobre `#0B1326` | ✅ muy alto contraste |
| Texto `#94A3B8` sobre `#131B2E` | ✅ alcanza para texto normal |
| Texto **blanco** sobre botón `#06B6D4` | ❌ contraste bajo → en los botones cian, **texto oscuro** (`#0B1326`), como en la maqueta de CodeQuest |
| Texto `#22D3EE` sobre `#0B1326` | ✅ sirve para links y resaltados |
| `#8B5CF6` como **texto** sobre fondo oscuro | ⚠️ justo; usar `#A855F7` o más claro para texto chico |

---

## 3. Qué choca con la especificación y qué queda de ella

| Especificación original | Identidad nueva | Propuesta |
|---|---|---|
| "Fondo gris claro, tarjetas blancas" (DH) | Tema oscuro Obsidian | **Oscuro por defecto** y tema claro como opción en *Mi cuenta* (ver V1). Todos los colores como variables CSS, así los dos temas comparten componentes |
| Primario violeta | Primario **cian**, violeta secundario | Cian como primario; el violeta de DH pasa a ser el secundario, así que no se pierde |
| Estructura DH: sidebar mínima, "Continuá cursando", acordeón, vista de clase | — | **Se mantiene igual**: cambia la piel, no el recorrido |
| Sin gamificación | `colores.md` describe: nivel "LVL 42", bóveda de bits/monedas, racha de fuego, Arena PvP y ranking | **Fuera de alcance.** Del HUD se toma solo el estilo: la topbar muestra usuario, campanita y avatar, sin nivel ni monedas. Ver V2 |
| Editor en tema claro | "Player & Terminal Shell": paneles divididos, consola, asistente flotante | Vista de la tarea con 3 paneles en escritorio (ver DISENO.md § 2); CodeMirror con tema oscuro propio tomado de esta paleta |

### Traducción a Tailwind v4 (borrador, se hace en la Fase 1)

```css
@theme {
  --color-surface: #0B1326;
  --color-surface-lowest: #060E20;
  --color-surface-low: #131B2E;
  --color-surface-container: #172036;
  --color-surface-high: #1D263D;
  --color-surface-highest: #242E47;
  --color-primary: #06B6D4;
  --color-primary-bright: #22D3EE;
  --color-secondary: #8B5CF6;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-ink: #E2E8F0;
  --color-ink-muted: #94A3B8;
  --color-outline: #334155;
  --font-display: "Space Grotesk", sans-serif;
  --font-sans: "Inter", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}
```

El tema claro, si se hace, redefine los mismos nombres dentro de `[data-theme="light"]`.

---

## 4. Preguntas

| # | Pregunta | Recomendación |
|---|---|---|
| V1 | ¿Solo tema oscuro, o oscuro + claro con selector? | Oscuro por defecto + claro opcional (hay alumnos que leen mucho texto, y en un proyector el claro se ve mejor) |
| V2 | Del HUD de `colores.md` (nivel, monedas, racha, Arena PvP, ranking), ¿algo entra en esta versión? | Nada: queda anotado para una etapa de gamificación futura |
| V3 | El geco: ¿mascota de la plataforma, con los mentores dentro de cada curso, o reemplaza a los mentores del guion? | Mascota de la plataforma |
| V4 | ¿Tenés o podés generar el logo en **PNG transparente o SVG** y una versión **horizontal**? | Si no, en la Fase 1 uso el JPEG recortado en círculo y el nombre en texto con Space Grotesk |
| V5 | ¿"Gheco" con **h** es intencional (marca) o es "Gecko"? | Asumo que es intencional |
| V6 | ¿La marca es **GhecoSoft-Code** para todo (título del sitio, mails, favicon)? | Sí; editable desde *Configuración* |

---

## 5. Monedas por lenguaje

Referencia: `docs/referencias/monedas-por-lenguaje.png`, monedas metálicas con brillo neón, una por lenguaje: Python, JavaScript, TypeScript, Java, C++ y una con engranaje (parece Rust).

- Cada **moneda del curso** usa el logo de su lenguaje (ver tipos de moneda en [GAMIFICACION.md](GAMIFICACION.md)). La **moneda comodín** necesita un diseño propio, quizás con el geco o con `</>`.
- En la interfaz se usan chicas (16–24 px) junto a los saldos y precios. Hacen falta versiones **simplificadas** (PNG transparente o SVG): la imagen de referencia es una ilustración 3D que a ese tamaño no se lee.
- ⚠️ **Marcas registradas** (el mismo cuidado que con "Codexia"):
  - **Java** (la taza) es marca de **Oracle**, que es estricta con su uso. Conviene una moneda propia ("J" o una taza genérica) en lugar del logo oficial.
  - **Python:** la PSF permite usos comunitarios y educativos del logo sin modificarlo; en una moneda estilizada conviene revisar su política de marca.
  - **TypeScript** (Microsoft) y **C++** (Standard C++ Foundation) tienen políticas más abiertas, pero conviene revisarlas igual.
  - **JavaScript:** el logo amarillo "JS" es comunitario, sin dueño.
  - Criterio general: usar el logo para **identificar** el lenguaje suele estar permitido; **modificarlo** (convertirlo en moneda) es lo que conviene revisar o evitar con diseños propios.

---

## 6. Detalles de interfaz tomados del "Mapa de Conectividad Escolar"

Referencia: `/var/www/html/marcos/visualizador-escuelas/` (al docente le gusta su interfaz). Análisis completo del grafo en [ARBOL-HABILIDADES.md](ARBOL-HABILIDADES.md) § 8.

- **Fondo con grilla de puntos:** `background-image: radial-gradient(circle, rgba(148,163,184,.14) 1px, transparent 1px); background-size: 22px 22px;` sobre el azul noche. Da el toque "tablero técnico" sin recargar.
- **Paneles de vidrio:** fondo del panel al 90–95 % + `backdrop-blur` + borde `#1e293b` + sombra. Para el panel de referencias, filtros y tarjetas flotantes.
- **Encabezado de página:** título chico en negrita + **punto verde que late** ("en vivo") + subtítulo apagado + breadcrumb.
- **Etiquetas técnicas:** en mayúsculas chicas con espaciado ("TECNOLOGÍA DE TRANSMISIÓN"), y badges en monoespaciada ("● VIVO", "Flujo activo").
- **Selector segmentado** (Mapa | Red) arriba a la derecha, con la opción activa en cian sólido y **texto oscuro**.
- **Barra lateral de filtros** con selects oscuros y un resumen abajo ("Mostrando 45 de 45…") en monoespaciada.
- Tipografía: ese proyecto usa **Geist**. Para GhecoSoft-Code seguimos con Space Grotesk + Inter + JetBrains Mono (§ 2); el estilo se logra igual.
