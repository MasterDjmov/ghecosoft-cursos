# Árbol de habilidades — análisis y propuesta

> Referencias en `docs/referencias/arbol de habilidades/` (4 imágenes) y `docs/referencias/mapa-mundos-codecombat.png`.
>
> ⚠️ **Actualización 2026-09-26:** el árbol pasó a ser el **centro de la plataforma** (ver [GAMIFICACION.md](GAMIFICACION.md)): ya no es "solo mostrar", **es lo que da acceso**. Y el docente eligió la **forma radial de Path of Exile** (§ 6), no la grilla simple que recomendaba la § 1. Las secciones 1 a 5 quedan como análisis histórico; **§ 6 manda**.

---

## 1. Qué muestran las referencias

| Archivo | Juego / origen | Forma | Qué aporta |
|---|---|---|---|
| `450_1000.webp` | Assassin's Creed Origins | Nodo central + **3 ramas** con nombre (Guerrero, Cazador, Vidente); nodos dorados = obtenidos, grises = pendientes | Ramas **temáticas** claras; se entiende de un vistazo |
| `images.jpeg` | Juego móvil (vertical) | Red **radial** que baja en scroll; bordes de color por tipo de nodo | Pensado para **celular**: se recorre scrolleando, no con zoom |
| `how-complex-should-a-skill-tree-be…webp` | Debate "¿qué tan complejo tiene que ser un árbol?" | Izquierda: **grilla** simple de pocas conexiones. Derecha: **red** densa, con zoom | La comparación misma: la grilla se lee sin esfuerzo, la red intimida |
| `poe2_…atlas_passive_tree…webp` | Path of Exile 2 (atlas pasivo) | Red gigantesca con cientos de nodos | Ejemplo de **lo que no conviene** para aprender: impresiona, pero no guía |

**Conclusión:** para alumnos que están empezando a programar, el árbol tiene que parecerse a **Assassin's Creed o a la grilla izquierda**:
- pocas ramas;
- nodos grandes con nombre;
- conexiones que muestran el orden.

El estilo Path of Exile sirve de fondo decorativo, no como mapa de estudio.

---

## 2. Qué representaría en la plataforma

El árbol **no suma puntos** (la gamificación está fuera de alcance). Es **otra forma de ver el progreso y el orden de los contenidos**, en la misma línea de "Las Crónicas del Código" y de la estética de la idea 2.

| En el árbol | En la plataforma | Dato que ya existe |
|---|---|---|
| Rama | **Unidad** (el bloque del capítulo: "Fundamentos", "Objetos"…) | `units` |
| Nodo | **Clase** (un ejemplo `NN-Tema`) | `lessons` |
| Conexión | **Correlatividad**: "para esta clase conviene haber hecho aquella" | La sección **"Antes de empezar"** de cada README del material ya las nombra por número (por ejemplo, "13 Punteros → 14 Punteros y structs") |
| Nodo final de la rama | **Proyecto del bloque / jefe** ("el Rey Slime", "el Dragón de las Forjas") | Los proyectos integradores de cada `AUDITORIA.md` |
| Estado del nodo | Los **mismos 4 estados** de la vista de contenidos | `LessonAvailability` + `lesson_progress` |

### Estados del nodo (con la paleta de [IDENTIDAD-VISUAL.md](IDENTIDAD-VISUAL.md))

| Estado | Aspecto |
|---|---|
| Completada | Relleno `success` (#10B981), conexión saliente encendida |
| Disponible | Borde `primary` (#22D3EE) con **halo**: "podés entrar" |
| Programada | Borde `warning` con la fecha en el tooltip ("Se abre el 12/10 08:00") |
| Bloqueada | Gris atenuado + candado, sin link |
| Proyecto / jefe | Nodo más grande, con borde `secondary` (violeta) |

> Regla que **no cambia**: el árbol **solo muestra**. Lo que se puede abrir lo sigue decidiendo la liberación por comisión. Un alumno nunca entra por el árbol a una clase no liberada.

---

## 3. Dos niveles de árbol

1. **Árbol del curso**: una pestaña más en el curso inscripto (*Visión general · Contenidos · **Mapa***), con las unidades como ramas y las clases como nodos. Es el que tiene sentido primero.
2. **Mapa de Codexia (global)**: los **cursos** como regiones conectadas según la progresión del `README.md` de FullCursos (C → C++ → videojuegos…; Python; Java; web). Mostraría en qué región está el alumno y cuáles le faltan. Tiene sentido cuando haya varios cursos publicados. Es el "Árbol de Habilidades" del sidebar de CodeQuest.

---

## 4. Cómo se construiría (a nivel técnico)

- **Datos:**
  - Tabla opcional `lesson_prerequisites (lesson_id, requires_lesson_id)`.
  - Si una clase no tiene correlativas cargadas, se asume la **anterior de su unidad**, así el árbol funciona sin cargar nada extra.
  - El importador (`app:import-course`, ver [CURSOS-EXISTENTES.md](CURSOS-EXISTENTES.md) § 6.7) puede leer "Antes de empezar" y proponerlas.
- **Dibujo:**
  - **SVG generado en el servidor** (Blade), sin librerías pesadas.
  - Ubicación automática: columna = unidad, fila = profundidad (la cadena de correlativas más larga).
  - Líneas rectas o curvas suaves entre nodos.
  - Alpine para el tooltip (título, estado, fecha) y el click.
- **Celular:** el árbol se dibuja **vertical** (las unidades una debajo de otra, como `images.jpeg`) y se recorre con scroll, sin zoom.
- **Rendimiento:** con 30–50 nodos por curso, un SVG simple alcanza de sobra.
- **Admin:** en el editor de clase, un selector "Correlativas" (multiselect de clases del mismo curso) y una vista previa del árbol.

---

## 5. Preguntas

| # | Pregunta | Recomendación |
|---|---|---|
| A1 | ¿El árbol entra en esta versión (como Fase 5 o una Fase 6), o queda para más adelante? | **Fase 6**, después de tener el circuito completo (clases → entregas → corrección) funcionando |
| A2 | ¿Nodos = **clases**, o nodos = **habilidades** abstractas ("Punteros", "Recursión") que se completan con varias clases? | Nodos = clases: usa datos que ya existen. Las habilidades abstractas necesitan otra tabla y cargar a mano qué clase aporta a cada una |
| A3 | ¿Las correlativas **bloquean** (no podés abrir la 14 sin completar la 13) o solo **orientan**? | Solo orientan: el acceso lo maneja la liberación por comisión, y un bloqueo extra complica el aula invertida |
| A4 | ¿Querés también el **mapa global** de Codexia con los cursos como regiones? | Sí, pero después del árbol por curso |
| A5 | ¿El árbol usa íconos por tema (como los juegos) o solo el número y el título? | Número + título + ícono del estado; los íconos por tema serían un extra de diseño |

---

## 6. Decisión del docente: árbol radial estilo Path of Exile

### Árbol de un curso

```
              [extra]   [extra]
                 \        /
      rama 3 ── ● ── ● ── ●          ← anillo exterior: extras / optativas (monedas comodín)
               /            \
   rama 2 ── ●     (LOGO)     ● ── rama 4
               \   Python   /
      rama 1 ── ● ── ● ── ●
                 ↑
          nodo raíz = "clase 0"
```

- **Centro:** el **logo del curso** (nodo raíz). En PoE el centro no es un personaje, pero las clases (bruja, guerrero…) arrancan desde posiciones distintas alrededor. Acá el centro es el logo y **las ramas base salen alrededor**.
- **Ramas base:** los bloques del curso (Fundamentos, Objetos, Errores y archivos…). Cada rama es una **secuencia** de nodos (temas), en el orden obligatorio de aprendizaje.
- **Hojas:** al abrir un nodo aparecen sus prácticas alrededor (obligatorias y optativas), como los "racimos" de nodos chicos de PoE.
- **Extras:** en un **anillo exterior** o en un árbol "Extras" pegado al principal. Se pagan con **monedas comodín**.
- **Estados** (de [GAMIFICACION.md](GAMIFICACION.md)): bloqueado, listo para abrir (muestra el precio con el ícono de la moneda), abierto, completado. Las **conexiones** se encienden a medida que avanza, como en PoE.
- **Abono vencido:** el árbol se sigue viendo y se puede entrar a lo abierto, pero los nodos "listo para abrir" muestran "Renová tu abono".

### Qué tomar de PoE y qué no

| De PoE, sí | De PoE, no |
|---|---|
| Forma radial, centro fuerte, ramas que salen hacia afuera | Cientos de nodos: un curso de Python tiene ~50 temas + prácticas, no 1.300 |
| Conexiones que se encienden, racimos de nodos chicos alrededor de uno grande | Caminos libres en cualquier dirección: acá cada rama es **secuencial** |
| Zoom y arrastre para explorar | Depender del zoom en celular |
| Fondo oscuro con ilustración tenue detrás | Texto diminuto en los nodos |

### Celular

Un árbol radial no entra en 360 px de ancho. Opciones:
- **a)** mismo árbol con zoom/arrastre táctil, arrancando centrado en el nodo actual;
- **b)** en celular, cada **rama se muestra como lista vertical** (como `images.jpeg`), con el logo arriba.

Recomiendo **b** como vista por defecto en celular y **a** como opción "Ver árbol completo".

### Cómo se dibuja

- **SVG** generado desde los datos: posiciones calculadas en círculo (ángulo por rama, radio por profundidad), guardables a mano desde el admin si hace falta retocar (como `pos_x`/`pos_y` en La Rioja Aprende).
- Zoom y arrastre con una librería chica (por ejemplo, `panzoom`, ~10 KB) o a mano con Alpine.
- Sin motores de juego (Phaser/Pixi): con decenas de nodos, SVG alcanza y es accesible (se puede recorrer con teclado y lector de pantalla).

## 7. Mapa de mundos: los cursos como islas

Referencia: `docs/referencias/mapa-mundos-codecombat.png` (CodeCombat).

- Cada **curso es una isla o mundo** con su ilustración, su nombre narrativo, el progreso (`0/44`), el estado (*Bloqueado* / botón *Jugar*) y una frase de gancho ("¡Escapá de la mazmorra y mejorá tus habilidades!").
- Es el **reemplazo gamificado de "Mis cursos" + "Cursos disponibles"**: las islas abiertas muestran el progreso y las otras muestran el precio o "Solicitar inscripción".
- ⚠️ Es **inspiración**: nombres, ilustraciones y estilo de CodeCombat no se pueden usar. Hacen falta ilustraciones propias, del mismo estilo que el banner del geco.

**Recorrido del alumno:** Mapa de mundos (islas) → isla de Python → **árbol radial** del curso → nodo → clase y prácticas.

---

## 8. Referencia fuerte: el "Mapa de Conectividad Escolar" (grafo de red)

Proyecto: `/var/www/html/marcos/visualizador-escuelas/` (Next.js 16, MVP). Al docente le gusta **su interfaz y su árbol**, y lo propone como alternativa válida a la forma PoE.

### Qué hace

- Un **grafo jerárquico** dibujado en `<canvas>` con **`force-graph`** (vasturiano; en ese proyecto vía `react-force-graph-2d`):
  - provincia al centro;
  - departamentos;
  - localidades;
  - escuelas como hojas, con íconos.
- **Detalles que lo hacen lucir:**
  - **Nodo central** cian con un **anillo que late** (pulso animado).
  - **Colores por nivel:** centro `#22d3ee`, nivel 1 azul `#3b82f6`, nivel 2 violeta `#a855f7`. Las **hojas** llevan un **ícono** según su tipo y un color según su estado (verde / ámbar / rojo).
  - **Conexiones:**
    - las troncales, grises y finas;
    - las de hoja, **punteadas** con un patrón según el estado;
    - las activas llevan **partículas que viajan** por la línea ("flujo activo").
  - **Etiquetas** en cajita oscura con borde tenue. Las de las hojas **se ocultan si el zoom es chico** y aparecen al acercarse, así cientos de nodos no se vuelven ilegibles.
  - **Click en un nodo → zoom a esa rama** (`zoomToFit` filtrado), sin sacar al resto del grafo. Botón "↺ Ver todo el árbol".
  - **Panel de referencias** flotante (arriba a la derecha, vidrio + borde) con íconos, estados y un badge "● VIVO".
  - **Barra lateral de filtros** (departamento, localidad, estado, tecnología) + **breadcrumb** + selector **Mapa / Red**.
  - Fondo casi negro `#05070d` con una **grilla de puntos** (`radial-gradient` 1 px cada 22 px).
- La paleta "NOC" es casi la misma que "DevLevel Obsidian" ([IDENTIDAD-VISUAL.md](IDENTIDAD-VISUAL.md)): cian, violeta, verde, ámbar y rojo sobre azul noche. **Combinan sin esfuerzo.**

### Cómo se traduce al árbol de un curso

| En el mapa escolar | En el árbol del curso |
|---|---|
| Provincia (centro, con pulso) | **Logo del curso** (nodo raíz) |
| Departamento (azul, grande) | **Rama base** (bloque: Fundamentos, Objetos…) |
| Localidad (violeta) | **Nodo / tema** (Variables, Control…) |
| Escuela (hoja con ícono) | **Práctica** (obligatoria u optativa) |
| Tipo de conexión (ícono de la hoja) | **Tipo de práctica**: código, archivo, lectura, instalación, optativa (comodín) |
| Estado (operativo / degradado / sin conexión) | **Estado de la práctica**: aprobada (verde), entregada esperando corrección (ámbar), rehacer (rojo), sin hacer (gris) |
| Partículas en enlaces activos | **Camino desbloqueado**: el "flujo" llega hasta donde avanzó el alumno |
| Enlace punteado | Tramo **listo para abrir** (falta pagar) |
| Nodo apagado | Tramo **bloqueado** |
| Filtros laterales | Filtrar por rama, estado, solo obligatorias / solo extras |
| Toggle Mapa / Red | Toggle **Mundos** (islas, § 7) / **Árbol** |
| "Referencias de Red" | "Referencias": tipos de práctica, estados, monedas |

### Grafo de fuerzas y PoE: se pueden combinar

- Un grafo de **fuerzas puro** acomoda los nodos solos y de forma "orgánica": cada vez que carga pueden quedar en otro lugar, y **no se lee el orden** de aprendizaje.
- `force-graph` tiene **`dagMode: 'radialout'`**: ubica cada nodo en un **anillo según su profundidad** desde el centro. Eso da **la forma radial de PoE** (logo al centro, ramas hacia afuera, la profundidad marca el orden) con la estética y las animaciones del mapa escolar.
- Para que el árbol no "baile" y cada alumno lo vea igual, se **fijan las posiciones** (`fx`/`fy`) calculadas una vez y guardadas, retocables desde el admin (como `pos_x`/`pos_y` en La Rioja Aprende).

**Propuesta:** `force-graph` con `dagMode: 'radialout'` + posiciones fijas + el estilo del mapa escolar (pulso, partículas, etiquetas por zoom, click para enfocar rama, panel de referencias).

**Cómo se ubican los nodos** (`resources/js/tree/layout.js`, D47):

- Si **todas las ramas salen del raíz**: abanico, cada rama en su sector y sus nodos hacia afuera.
- Si **una rama sigue a otra** (Objetos después del jefe de Fundamentos, como en Python): el tronco va en **espiral**. Cada rama sale pegada al último nodo de la anterior, los nodos quedan siempre a la misma distancia (130 px) y entre una vuelta y la siguiente hay 240 px. Así no aparecen tramos larguísimos entre un jefe y la rama que sigue.
- Una rama que sale de un nodo del medio, y las **Sendas**, brotan de su nodo de origen hacia afuera.
- Los nodos que el docente mueve a mano se respetan.

### Cómo se lleva a esta plataforma (Livewire, no Next)

- `force-graph` es **JavaScript puro** (no necesita React): se instala con npm, se empaqueta con **Vite** y se monta en un `<div wire:ignore>` con Alpine.
- Livewire entrega los datos del árbol del alumno en JSON (nodos, estados, precios). Al abrir un nodo o aprobarse una práctica, se refresca el JSON y el grafo se actualiza sin recargar la página.
- **Peso:** `force-graph` incluye d3-force y ronda los 150–200 KB. Se carga **solo en la página del árbol** (import dinámico), no en toda la plataforma.
- **Accesibilidad y celular:** el canvas no lo lee un lector de pantalla ni es cómodo a 360 px. Por eso sigue existiendo la **vista en lista por rama** (§ 6) como alternativa y como vista por defecto en celular. Los datos son los mismos.
- **Rendimiento:** el MVP escolar se probó con escala (`EscalaTester`). Un curso tiene ~50 nodos + ~250 prácticas, un volumen que `force-graph` maneja sin problema.
- Los íconos de las hojas se dibujan en canvas con `Path2D` a partir de paths SVG (como hace `iconosConexion.ts` con Heroicons). Se puede hacer lo mismo con los íconos de tipo de práctica.
