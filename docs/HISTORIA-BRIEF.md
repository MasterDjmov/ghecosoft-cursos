# GhecoSoft-Code: resumen para armar la historia (curso de Python)

> **Para qué es este archivo:** es el contexto que se le pasa a Claude online (claude.ai) para definir la historia del curso de Python, que es el primero en salir. Se armó el 2026-09-27 a partir del código y de `FullCursos`. Si cambia el sistema (claves del diccionario, economía, dónde se muestra la historia), actualizarlo antes de volver a pasarlo. Lo que se decida en esa charla se carga en el **Diccionario** del admin y en los nodos, y se anota en [PLAN.md § 10](PLAN.md).

Te paso el contexto de una plataforma de cursos de programación gamificada que estoy construyendo (soy el docente). Necesito tu ayuda para cuadrar la historia/narrativa. Abajo está cómo funciona el sistema hoy, qué textos se pueden cargar, el contenido de Python que existe y las limitaciones. Al final te digo qué necesito.

## 1. Qué es
- Plataforma web de un solo docente, alumnos por comisiones (muchos adolescentes; hay autorización para menores). Español rioplatense ("Entregá", "Probá").
- El alumno avanza por un **árbol de habilidades estilo Path of Exile** (grafo radial). Cada curso = un lenguaje. El primero es **Python**.
- El código Python se ejecuta **en el navegador del alumno** (Pyodide). No hay corrección automática: **el docente corrige a mano** (Aprobada / Rehacer + comentario).

## 2. Estructura del árbol
- **Curso** (= región del mundo). Tiene un **nodo raíz** ("Clase 0"), que se paga para entrar al curso.
- **Ramas**: bloques del árbol (ej. "Fundamentos"). Puede haber una rama de **Extras** (optativa).
- **Nodos** (un tema cada uno), de 4 tipos:
  - **Raíz**: la entrada al curso (preparar el entorno).
  - **Tema**: una clase normal.
  - **Jefe**: cierra cada rama; es un proyecto integrador; al vencerlo da XP extra y una **insignia**.
  - **Extra**: optativo, se abre con otra moneda (comodines).
- Cada nodo tiene: título, explicación (markdown), video opcional, **ejemplo de código ejecutable** con salida esperada y entrada (stdin) de ejemplo, recursos descargables y **hojas (prácticas)**.
- **Hojas / prácticas** de cada nodo:
  - **Obligatorias**: pagan monedas del curso; aprobarlas todas completa el nodo.
  - **Optativas** ("Desafíos extra"): pagan comodines.
  - Tipos de entrega: código escrito en el editor, archivo, ambos, o "sin entrega" (se marca como completada, ej. "Instalá Python").
- **Estados de un nodo** para el alumno: Bloqueado → Listo para abrir → Abierto → Completado.
- **Para abrir un nodo**: tener el nodo anterior completado (sus obligatorias aprobadas) y pagar su precio en monedas. Además hay un **abono de 30 días**: con el abono vencido puede repasar lo abierto pero no abrir ni entregar.

## 3. Economía y progreso
- **Moneda del curso** (en Python se llama "**escama**"): se gana con prácticas obligatorias y se gasta en abrir nodos. En el demo cada nodo cuesta 10 y sus obligatorias pagan justo 10.
- **Moneda comodín** (general, de todos los cursos): se gana con optativas y abre los nodos Extra.
- **XP**: nunca se gasta; sube de **nivel**. Por práctica (10 a 50 XP), +20 XP al completar un nodo, +50 XP al vencer un jefe.
- **Niveles** (XP necesaria): 1 = 0 · 2 = 100 · 3 = 250 · 4 = 500 · 5 = 1000 · 6 = 1750 · 7 = 2750. Cada nivel puede tener nombre propio (rango).
- **Insignias**: una por jefe (ej. "Cazador de slimes").
- **Ranking**: top 10 por curso y global (por XP). **CV público** del alumno con cursos, nivel e insignias.

## 4. Dónde entra la narrativa (qué textos puedo cargar sin programar)
Hay un **diccionario narrativo** editable desde el panel: cada elemento tiene una clave fija y el nombre que yo le ponga. Se puede definir general o **por curso** (el del curso pisa al general). Cada entrada tiene: singular, plural, género (para "la escama"/"el rubí"), ícono, descripción corta y un **texto de historia largo** (markdown).

Claves actuales y su valor por defecto hoy:
- Mundo: `world.name` = "el Mundo del Código" (reemplaza a "Codexia", nombre por decidir) · `world.region` = "región" · `mentor.name` = "el profe"
- Economía: `coin.course` = moneda (en Python: escama) · `coin.wildcard` = comodín · `xp` = experiencia · `xp.short` = XP
- Progreso: `level` = nivel · `level.1` … `level.7` (nombre de cada rango) · `branch` = rama · `node` = nodo · `node.root` = nodo raíz · `node.boss` = jefe · `node.extra` = extra · `practice` = práctica · `badge` = insignia
- Estados: `state.locked` Bloqueado · `state.available` Listo para abrir · `state.unlocked` Abierto · `state.completed` Completado
- Historia: `story.course_intro` (crónica de entrada al curso) · `story.branch_completed` (al completar una rama) · `story.course_completed` (al completar el curso). Se pueden crear claves nuevas (ej. `story.dragon_intro`).
- Bestiario (errores = monstruos): `beast.slime`, `beast.goblin`, `beast.skeleton`, `beast.orc`, `beast.ogre`, `beast.troll`, `beast.dragon`

Importante: hoy el alumno **ve** los nombres de mundo, monedas, XP, niveles, estados, jefe/raíz, títulos de ramas/nodos/prácticas, explicaciones e insignias. Los textos largos de **historia**, el **bestiario**, el **mentor** y la **región** ya se pueden cargar pero **todavía no se muestran** en ninguna pantalla del alumno (hay que decidir dónde: bienvenida del curso, al completar una rama, al vencer un jefe, recuadro de "Errores habituales", etc.).

Además, fuera del diccionario, se escribe historia en: título y explicación de cada nodo (la "Crónica" puede ir como recuadro al principio), títulos y consignas de las prácticas, nombre y descripción de cada rama e insignia.

## 5. Lo que hay HOY cargado de Python (curso demo, contenido de prueba)
"Python desde cero", moneda "escama":
- **Raíz · Clase 0 · Preparar el entorno**: Instalá Python (sin entrega) · Tu primer programa · Pedile datos al usuario · (optativa) Saludo decorado.
- **Rama Fundamentos**: Comentarios → Variables → **Jefe: el Rey Slime** (proyecto "Ficha de personaje"; insignia "Cazador de slimes").
- **Rama Control**: Condicionales → Bucles → **Jefe: el Golem del Bucle** (proyecto "Menú de la posada"; insignia "Rompe-bucles").
- **Rama Extras**: "f-strings a fondo" (se abre con comodines).
- Cada tema: 3 obligatorias ("Misión 1/2/3", genéricas) + 1 optativa ("Encargo del Gremio").

Es un esqueleto para probar el sistema; se va a reemplazar por el contenido real.

## 6. El material real (mis cursos existentes) y la historia que ya tenía
Historia común "Las Crónicas del Código": **Kira**, aprendiz de espadachina, cruza un portal a **Codexia**, donde la magia no se recita: **se escribe**. Cada región tiene su lengua arcana (un lenguaje) y su mentor. Criaturas nacidas de hechizos mal escritos invaden el mundo; para volver a casa Kira aprende cada lengua y vence al jefe de cada región.
- Compañía fija: **Bron** (guerrero enano, "¿para qué sirve?": usos reales), **Mia** (maga curiosa: la teoría), **Zed** (pícaro de los atajos: trampas y errores habituales), **el Gremio** (encargos fuera de los juegos: calculadoras, archivos, datos, APIs).
- Bestiario: slime = sintaxis/indentación · goblin = tipos (TypeError/ValueError) · esqueleto = nombres (NameError) · orco = índices/claves · ogro = lógica · troll = estado compartido/mutabilidad · dragón = jefe/proyecto integrador. Una "maldición" es un error en ejecución y su "pergamino" es el traceback.
- Python = **El Valle de la Serpiente**, mentora **Ofidia** (serpiente sabia). Otras regiones: C = Las Forjas de Hierro (Maese Ferrum), Java = El Imperio de las Clases (Kaffa), C++/PHP/JS/TS a definir.
- Cada tema del material tiene: Crónica (2–4 líneas) · Objetivo · Antes de empezar · Explicación · Código · Salida esperada · Errores habituales (bestiario) · 3 Misiones · Encargo del Gremio · Prueba del sello (autoevaluación) · Soluciones.

Arco de Python (8 bloques = 8 ramas, 47 temas en el índice; ✅ = formato nuevo completo):
1. Fundamentos (01–11 ✅: hola/REPL/traceback, tipos, operadores, strings, control, listas/tuplas, dicts/sets, referencias y copias, funciones, alcance/recursión, módulos) — "Kira despierta en el Valle" — jefe **el Rey Slime**
2. Objetos (12–15: clases, dataclass/enum, herencia, composición) — "forma su compañía" — **la Hidra de las Mil Formas**
3. Errores y archivos (16–19: excepciones, archivos, JSON/CSV, SQLite) — "la Gran Biblioteca" — **el Liche de los Archivos Perdidos**
4. Iteración (20–23: iteradores, generadores, itertools, decoradores) — "el Paso del Río" — **el Enjambre**
5. Calidad (24–28: type hints, entornos, testing, logging, código limpio) — "el Gremio de Artífices" — **el Ogro de los Bugs Silenciosos**
6. Concurrencia (29–31: hilos, asyncio, rendimiento) — "la Torre del Reloj" — **el Golem de Engranajes**
7. pygame (32–35: "Junta las Gemas") — "la Arena" — **el Rey Orco**
8. Aplicado (36–42: automatización, regex, APIs, Tkinter, datos, IA, robótica) — "la magia al servicio del reino" — **el Dragón del Valle** (proyecto final)

Más proyectos integradores 43–47.

## 7. Límites técnicos que afectan a la historia
- En el navegador solo corren **programas de consola**: print/input (la entrada se escribe antes de ejecutar, una línea por cada input()), corte a los 5 segundos. pygame, Tkinter, puerto serie, archivos del disco real o red no corren ahí: esas prácticas se entregan **como archivo** hecho en la compu del alumno.
- La corrección es humana: las prácticas pueden pedir cosas creativas (no hace falta salida exacta).
- Un tema puede tener cantidad variable de prácticas (hoy el material trae 3 misiones + 1 encargo).

## 8. Qué necesito de vos
1. Un **nombre para el mundo** que reemplace a "Codexia" (con 3–4 alternativas y por qué), manteniendo o ajustando la premisa de Kira.
2. Revisar la historia para que **encaje con el árbol**: cada rama = un acto, cada jefe = proyecto integrador, y que la economía (escamas, comodines, XP) tenga sentido dentro del mundo.
3. Nombres para: moneda del curso de Python (hoy "escama"), moneda comodín, XP, los **7 niveles/rangos**, estados del nodo si les queda bien un sabor narrativo, y el mentor/la región.
4. Textos cortos para `story.course_intro`, `story.branch_completed`, `story.course_completed` y una presentación de cada jefe (2–4 líneas, tono aventura, para adolescentes, español rioplatense con voseo).
5. Proponer **dónde conviene mostrar** la historia en la plataforma (sin llenar de texto: el foco es aprender a programar).

Formato de respuesta, para cargarlo directo:
- Términos: `clave | singular | plural | género (f/m) | descripción corta | historia (si aplica)`
- Jefes / ramas: `rama | título del jefe | crónica (2–4 líneas) | nombre de la insignia | descripción de la insignia`
