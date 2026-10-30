# D115 · Los cursos de JavaScript y TypeScript — propuesta 1 (2026-10-30), aprobada con ajustes el mismo día (§ 10)

Dos cursos nuevos armados desde FullCursos (cap. 22 **JS-Vanilla** y cap. 23 **TypeScript**), con lo mismo que ya tienen los demás: micro-misiones que se comprueban solas, monedas, jefes, escenas en Stitch, logo, moneda, ítems, expediciones, enciclopedia, Mis Crónicas y, más adelante, su temporada de inglés.

La historia de JavaScript ya está aprobada ([historias/javascript.md](historias/javascript.md), 2026-10-21): **Nima**, la arquera, en **la Feria de las Luces**, con **Lumina** y la moneda **fichas de la Feria**. Las imágenes de Nima (cuerpo, retrato y 6 aspectos), de Lumina, de Destello (5 etapas) y el fondo de la Feria ya están hechas. Lo que falta es todo lo demás. Esta propuesta lo ordena y deja las preguntas al final (§ 9).

---

## 1. Lo más importante: el ejecutor de JavaScript

Hoy **nada ejecuta JavaScript del alumno**. El HTML se dibuja en un `<iframe sandbox="">` sin ningún permiso (y la regla dice que nunca se le agrega `allow-*`). Para JS hace falta un ejecutor nuevo, en el navegador, que sea igual de seguro.

**Cómo lo propongo (`resources/js/runners/javascript.js`):**
- **Una caja aparte del HTML:** un `<iframe sandbox="allow-scripts">`, **sin** `allow-same-origin`. Es decir: el código corre, pero con un **origen opaco**. No ve las cookies ni la sesión de quien ejecuta (si el docente corre la entrega de un alumno, ese código no puede actuar como el docente), no lee la página de afuera y no abre ventanas ni formularios.
- **Sin red:** una CSP `default-src 'none'` adentro de la caja. `fetch` no sale a internet.
- **El Puerto simulado:** en la caja, `fetch('/puerto/...')` lo contesta un **Puerto de Elefa de mentira**, con datos fijos y una demora. Así se enseñan promesas, `async`/`await` y errores de red sin red de verdad, y queda el cruce con PHP de la historia.
- **`localStorage` de mentira**, que vive solo durante la ejecución (en un origen opaco el de verdad no anda).
- **Tope de tiempo y de vueltas:** 5 s, como Python. Además, cada bucle lleva un contador inyectado (como el tope de órdenes del 8086), así un `while (true)` no congela la pestaña. Si se pasa del tope, la caja se tira y se avisa.
- **Reloj fijo para las animaciones:** `requestAnimationFrame` y `setTimeout` avanzan con un reloj simulado. Una animación de 60 cuadros da siempre el mismo resultado y se puede comprobar.

La regla de CLAUDE.md queda igual para el HTML (`sandbox=""` sin nada). Se suma esta excepción, **solo para el ejecutor de JS y TS**, con su test.

### 1 bis. Todo lo que se pueda, simulado (pedido del docente, 2026-10-30) — hecho en la fase 1

Como el tablero del 8086, que simula los registros: el programa del alumno cree que toca cosas de verdad, pero son de mentira, viven solo mientras corre y se borran al terminar. **No toca nada de la compu ni del navegador de la persona.** Está en `resources/js/runners/js-sandbox/world.js`.

| Qué | Cómo se simula |
|---|---|
| **El reloj** | `Date`, `performance.now()` y los temporizadores avanzan con el reloj de la caja, que arranca el 2 de marzo de 2026 a las 21 h. Diez segundos de animación se comprueban en un instante y dan siempre lo mismo. |
| **Temporizadores** | `setTimeout`, `setInterval`, `requestAnimationFrame` (60 cuadros por segundo), `requestIdleCallback` y `AbortSignal.timeout`, con el ajuste de 4 ms de los navegadores. Si al terminar queda alguno andando, se avisa. |
| **El azar** | `Math.random()` con semilla: la misma ejecución da los mismos números. |
| **Cookies** | `document.cookie`, con `max-age` y `expires` en el reloj de la caja. Las HttpOnly que pone el Puerto no se ven desde JS, pero viajan en los pedidos, como en un navegador de verdad. |
| **Almacenamiento** | `localStorage` y `sessionStorage`, con el tope de 5 MB. La consigna los puede traer cargados («la segunda visita»). |
| **La red** | `fetch` contra el **Puerto de Elefa**, con estas direcciones: `hola`, `puestos` y `puestos/:id`, `heroes`, `clima`, `mensajes` (GET y POST), `lento`, `error`, `roto`, `texto`, `eco` y `fichas?pagina=`. También hay sesión: `login`, `perfil` y `salir`. Con `?demora=` se cambia cuánto tarda y con `?falla=1` falla. `AbortController` funciona. A internet no sale; `XMLHttpRequest`, `WebSocket` y `EventSource` explican que no hay red. |
| **Ventanitas** | `alert`, `confirm` y `prompt` leen sus respuestas de la Entrada, una por línea. |
| **El navegador** | portapapeles, ubicación (La Rioja), vibración, notificaciones, sonido (`play()`), `window.open` y `print`: todos quedan anotados en «Avisos». |
| **Enlaces y formularios** | un enlace no saca de la página, y un formulario sin `preventDefault()` se avisa. |
| **El lienzo** | se graba lo que se dibuja en cada cuadro: `lienzo: fillRect(58, 10, 20, 20) #ffd400`. |
| **Los topes** | 5 s en total, un contador en cada bucle y en cada función, y hasta 200 000 temporizadores. Atajar el corte con `try` no lo esquiva. |

**El tablero** (pestaña *Tablero*, debajo del editor) muestra en vivo el reloj, las cookies, los dos almacenamientos, los pedidos al Puerto con su respuesta y los avisos. Es lo que en un navegador real está escondido en las herramientas de desarrollador.

**Cómo se comprueba una micro-misión de página.** La consigna trae tres cosas:
- su HTML (`page`);
- los **eventos** de prueba, uno por renglón:
  - con el mouse: `click #boton`, `click canvas 120 80`, `doble`, `pasar`, `salir`, `mover`;
  - en los formularios: `escribir #nombre Ana`, `elegir`, `marcar`, `foco`, `enviar form`;
  - con el teclado: `tecla ArrowUp`, `apretar` y `soltar`;
  - con el reloj: `esperar 1000`, `cuadros 30`;
- qué revisar (el **Estado**):
  - de la página: `#cartel`, `li #`, `.farol @class`, `#nombre @value`, `estilo #f { background-color }`, `título`;
  - de lo guardado: `cookie nombre`, `cookies`, `local clave`, `session`;
  - del resto: `lienzo`, `pedidos`, `temporizadores` y `reloj`.

Primero corre la comprobación con el reloj de la caja y, enseguida, la página sigue **en vivo** para que el alumno la toque. La salida que se compara es la consola, más el bloque `── Estado ──`.

**Las pruebas:** `node scripts/js-micro/probar-caja.mjs` corre 54 casos en Chrome sin ventana. Cubren la consola, los errores, los topes, el reloj, el Puerto, las cookies, el almacenamiento, las ventanitas, la página, el lienzo, la seguridad y el modo en vivo.

**Para probarlo:** *Herramientas → La caja de la Feria* (`/herramientas/caja-de-la-feria`). El staff la ve siempre; el alumno, con el abono de un curso de JS. Tiene cinco ejemplos: la consola, el reloj, el Puerto, la página y el lienzo.

**TypeScript:** el compilador oficial (`typescript`, unos 3 MB comprimido, se baja solo la primera vez que hace falta) corre en un Web Worker. Revisa los tipos, muestra los errores con su línea y su explicación en español, y pasa el código a JS para la misma caja. El alumno no instala nada.

## 2. Las micro-misiones (cómo se comprueban)

Igual que Python, PHP o Java: el alumno escribe, ejecuta y la micro-misión compara.

| Tipo | Qué se compara | Para qué |
|---|---|---|
| **Consola** | la salida de `console.log` contra la `Salida esperada` | fundamentos, objetos, clases, closures, promesas |
| **Página** (DOM) | el **estado de la página** después de correr el código y unos eventos simulados (`#### Eventos`: `click #boton`, `escribir #nombre Ana`, `tecla ArrowUp`), contra un `Estado esperado` (el texto de `#cartel`, las clases de `.farol`, cuántos `li` hay) | DOM, eventos, formularios, `localStorage` |
| **Lienzo** (canvas) | lo que dibujó, después de N cuadros con el reloj fijo (posición del personaje, puntaje, cuántas gemas quedan) | game loop, entrada, colisiones |
| **Compilador** (solo TS) | que compile, o el error que tiene que dar (`TS2322 en la línea 3`) | «Arreglá el tipo para que compile», `any` contra `unknown`, exhaustividad con `never` |

Como Java y PHP (`micromisiones_completan: si`): las micro-misiones que vienen de una misión pagan **monedas del curso** y abren el siguiente nodo. Los **proyectos** (una página entera, el juego *Junta las Gemas*) los corrige el docente, ejecutándolos con la misma caja.

Antes de reimportar, un script (`scripts/js-micro/probar.mjs`, como `java-micro/probar.py`) corre con Node la solución de cada micro-misión y la compara con su salida o su estado.

## 3. El curso de JavaScript: la Feria de las Luces

Desde los 22 capítulos de FullCursos (22-JS-Vanilla). La moneda son las **fichas de la Feria**, y cada rama es una zona de la Feria.

| Rama | Zona de la Feria | Lo que aprende Nima (capítulos) | Jefe |
|---|---|---|---|
| R00 Clase 0 | El carrusel | llega, `console.log`, su primer tiro errado (01) | — |
| R01 Fundamentos | Los Puestos de Juegos | `let`/`const`, template literals, tipos, coerción, `NaN`, `undefined` contra `null`, `if`/`switch`, `??`, `?.`, bucles, `for…of`, arreglos con `map`/`filter`/`reduce`, objetos, desestructuración, spread, funciones flecha, `this`, parámetros rest (02–07) | el **Goblin de la Coerción** (`"2" + 2` da `"22"`) |
| R02 La página | La Avenida de los Faroles | `querySelector`, crear y cambiar elementos, `addEventListener`, teclado, formularios, delegación, JSON y `localStorage` (08, 09, 16) | el **Fantasma Undefined** |
| R03 Los títeres | El Teatro del Titiritero | clases, `#privado`, getters, `static`, herencia, polimorfismo, módulos, closures, `let` contra `var` (10–13) | **el Títere sin Hilos** (un objeto que perdió su `this`) |
| R04 Las flechas de luz | La Torre de las Flechas | promesas, `then`/`catch`, `Promise.all`, `async`/`await`, `fetch` al Puerto, errores propios, generadores (14, 15, 17, 18) | el **Troll de las Respuestas Cruzadas** |
| R05 El taller del Vidriero | El fondo de la Feria | `<canvas>`, `requestAnimationFrame`, delta time, entrada por estado, colisiones, oleadas, *Junta las Gemas*, y al final animar el vitral (19–22) | el **Dragón de los Fuegos Artificiales** |

Unos **28 nodos y 200 micro-misiones**, como PHP. Los jefes R01–R04 ya estaban en la historia aprobada. El del Teatro es nuevo y se puede cambiar.

**Sendas optativas (propuesta):**
- **la Senda del Palomar:** JS que habla con una API de PHP de verdad, en la compu del alumno. Es el puente con el curso de PHP;
- **la Senda de TypeScript:** no hace falta, porque TypeScript va como curso aparte (§ 4).

## 4. El curso de TypeScript: el Mirador de las Constelaciones

Desde los 22 capítulos de FullCursos (23-TypeScript). El curso **pide JS** (o se recomienda cursarlo después) y cierra con el mismo *Junta las Gemas*, ahora tipado.

**La historia (propuesta, a decidir):**
- **Dónde sigue:** al final de JS, el vitral se mueve por primera vez y muestra **el lugar adonde fue el Vidriero**. TypeScript es ese lugar: **el Mirador de las Constelaciones**, un observatorio arriba de la Feria.
- **La lengua del Mirador:** cada estrella se dibuja en su figura **antes** de prenderse. Si una estrella no encaja en su figura, no se enciende. Es el chequeo de tipos.
- **La heroína: Nima otra vez** (recomendado). Su arco sigue:
  - en JS aprendió a **esperar sin quedarse quieta**;
  - en TS aprende a **medir antes de tirar**. La frase nueva: «Mido dos veces, tiro una.»
  - Le hacen falta 6 aspectos nuevos (los del Mirador), para no repetir los de la Feria.
  - La otra opción es un héroe nuevo, con su ficha y todas sus imágenes.
- **La líder: Astrea, la Lechuza Cartógrafa.** Una lechuza grande, con anteojos de vidrio y un compás. Le pone nombre y figura a cada estrella. Lema: *«Nada brilla sin su forma.»*
- **La moneda:** **estrellas** (no la usa ningún curso).
- **El Mirador por dentro y lo que se aprende en cada zona:**

| Rama | Zona | Lo que se aprende (capítulos) | Jefe (propuesta) |
|---|---|---|---|
| R00 | La escalera del Mirador | qué es TS, `tsc`, inferencia (01) | — |
| R01 | La Sala de las Figuras | tipos básicos, tuplas, `any`/`unknown`/`never`, `interface` y `type`, funciones tipadas, sobrecarga (02–04) | **el Camaleón Any** (toma cualquier forma y esconde los errores) |
| R02 | Los Moldes de Estrellas | clases tipadas, `private` contra `#`, `abstract`, `implements`, enums, `as const`, genéricos (05–08) | **la Hidra de las Mil Formas** (genéricos) |
| R03 | El Telescopio | uniones, narrowing, uniones discriminadas, exhaustividad con `never`, utility types, módulos, `import type` (09–12) | **la Quimera de las Uniones** |
| R04 | La Cúpula | errores tipados y `Result<T>`, `Promise<T>`, DOM tipado, `strictNullChecks`, decoradores, `tsconfig` (13–19) | **el Espejismo Null** |
| R05 | El Atlas del Vidriero | JS contra TS (el mismo bug), el modelo tipado del juego, *Junta las Gemas* en TS (20–22) | **el Dragón de las Constelaciones Rotas** |

- **La pieza del misterio:** en el Atlas, Nima encuentra el plano entero del portal, con todas sus figuras. Falta una, y esa queda para React Native o Laravel. No se revela qué es.
- **El cruce:** Astrea conoce a Kaffa (Java). Los dos ponen «moldes» a todo, y en el curso se pelean amistosamente por quién lo inventó.

Unos **24 nodos y 170 micro-misiones**. Muchas son del tipo **Compilador**: arreglar el tipo, o predecir el error.

## 5. Las imágenes (Stitch)

**Un proyecto de Stitch nuevo para la Feria** (y otro para el Mirador), recreando ahí las hojas de Nima, Lumina y Gheco, como se hizo con las Forjas.

| Qué | JS | TS |
|---|---|---|
| Logo del curso | Nima con el arco y una luciérnaga, sobre amarillo y negro | Nima con un astrolabio, sobre azul (el color de TS) |
| Logo de la moneda | ficha de la Feria | estrella |
| La gente | el Titiritero, la cocinera de pan con miel, los chicos del puesto de tiro, el Pirotécnico | Astrea, algún aprendiz del Mirador |
| Los jefes | 5 (§ 3) | 5 (§ 4) |
| Escenas | una por micro-misión y una por nodo, como los demás (unas 230) | unas 195 |
| Ítems | los del catálogo del curso (`GameItems`), en hojas 3×3 | los del Mirador |
| Expediciones | el mapa de la Feria y sus lugares | el mapa del Mirador |
| Aspectos de Nima | ya hechos (6) | 6 nuevos |

Todos con ropa opaca y cerrada (alumnos chicos) y sin texto en la imagen.

## 6. Lo demás (ALTA-DE-CURSOS-Y-PERSONAJES.md, punto por punto)

- **Lenguaje:** `JavaScript` y `TypeScript` ya están en el enum. Hay que sumarlos a `runsForStudents()` y a las listas de ejecutores y casos (`SubmissionCases::LANGUAGES`, `components/code-runner`).
- **Juego:** Nima en `config/game.php` → `protagonists` (tienda, expediciones, mapa) y Destello en `mounts.species`.
- **Enciclopedia:** la Feria y el Mirador en `WORLDS`.
- **Monedas:** el logo de cada una en `EncyclopediaItems`.
- **Landing y universo:** logos en `LandingController::IMAGES` y el color en `UniverseGraph`.
- **Personajes:** las fichas nuevas en PERSONAJES.md, y la región en NOVELA-GRAFICA.md.
- **Mis Crónicas:** las crónicas por nodo y la pieza del portal de cada curso.
- **Temas:** los de JS y TS en `cursos/temas.md`.
- **Seeder, deploy y simulación:** que el seeder los importe, `deploy.sh --cursos` los reimporte y `app:simulate-course` los recorra antes de abrirlos.
- **Cruces con otros cursos:**
  - Ensamblador: que la flecha de Nima despertó a Nova, sin revelarlo en ese curso;
  - Python: que Sila recibe la carta de Nima.
- **Inglés:** la temporada 8, la Feria, en Primaria y en Secundaria (con las portadas en el proyecto de la Feria). Va después de los dos cursos.

## 7. Por fases (y frenando en cada una)

| Fase | Qué | Para probar |
|---|---|---|
| 1 | El ejecutor de JS (consola, página, lienzo, Puerto simulado, topes) con sus tests de seguridad | ejecutar código en un nodo de prueba |
| 2 | El curso de JS, R00 y R01 (texto, micro-misiones, `probar.mjs`), con la Clase 0 en producción como Próximamente | la Clase 0 y los Puestos |
| 3 | JS, R02 a R05 | todo el curso, con la simulación |
| 4 | Imágenes de JS: proyecto de Stitch, logo, moneda, gente, jefes, escenas, ítems y mapa; juego, enciclopedia y landing | publicarlo |
| 5 | El compilador de TypeScript en el navegador (micro-misiones de tipo Compilador) | errores de tipos en español |
| 6 | El curso de TS completo | todo el curso |
| 7 | Imágenes de TS | publicarlo |
| 8 | La temporada de inglés de la Feria | — |

## 8. Lo que no entra (por ahora)

- **Node del lado del servidor** (Express, archivos): el código del alumno nunca corre en el servidor, y el curso es de navegador. `fs` y `process` no existen en la caja; los capítulos que usan `node` en FullCursos (01–07, 10–18) solo imprimen por consola, así que andan igual.
- **npm y paquetes de terceros:** FullCursos tampoco los usa en JS. En TS solo hace falta el compilador.
- **Frameworks:** React Native es su propio curso.

## 9. Para decidir

1. **El ejecutor (§ 1):** ¿aceptás la caja `sandbox="allow-scripts"` sin mismo origen, solo para JS y TS, sin red y con el Puerto simulado? Es un cambio a una «regla que no se rompe», así que va escrito en CLAUDE.md con su test.
2. **Dos cursos:** JS y TS aparte, cada uno con su moneda. ¿TS **pide** haber terminado JS, o solo se recomienda?
3. **TypeScript:**
   - ¿El Mirador de las Constelaciones con **Nima otra vez** (6 aspectos nuevos), o un héroe nuevo?
   - ¿Astrea, la Lechuza Cartógrafa, como líder?
   - ¿La moneda son **estrellas**?
4. **Los jefes nuevos:**
   - en JS, el Títere sin Hilos;
   - en TS, los cinco de § 4.
5. **Las Sendas de JS:** ¿la del Palomar (con PHP), alguna más (por ejemplo un juego de tiro con Destello), o ninguna por ahora?
6. **Proyectos que corrige el docente:** ¿como en PHP (una página o un juego por rama y las Sendas) o, como en Ensamblador, solo micro-misiones?

## 10. Lo que decidió el docente (2026-10-30)

1. **El ejecutor:** aprobado, con todo lo que se pueda simulado (§ 1 bis). Fase 1 hecha.
2. **TypeScript solo se recomienda** después de JS. No pide terminarlo: quien ya sabe JavaScript entra directo a TS.
3. **TypeScript:** el Mirador de las Constelaciones, con Nima, Astrea, la Lechuza Cartógrafa, y la moneda **estrellas**, como en § 4.
4. **Los jefes nuevos:** aprobados (el Títere sin Hilos en JS y los cinco de TS).
5. **Las Sendas:** siempre gamificadas, y algunas atadas a los otros cursos (HTML, PHP…). La propuesta para JS, a confirmar:

| Senda | Con qué curso se cruza | Qué se hace |
|---|---|---|
| **El Escaparate Vivo** | HTML y CSS (los Talleres, con Tesela y Teo) | darles vida a las páginas de los Talleres: un menú que se abre, una galería, el modo oscuro, un formulario que avisa |
| **El Palomar** | PHP (el Puerto, con Nilo y Elefa) | JS que habla con el Puerto: listar, crear y borrar mensajes, iniciar sesión, manejar los errores |
| **El Archivo de Sila** | Python (el Valle) | ordenar y filtrar las fichas del Archivo en JSON (`map`, `filter`, `reduce`, `sort`). Al final, Nima le escribe a Sila |
| **El Tablero del Gólem** | Ensamblador (Nova) | un emulador chiquito en JS: registros, cuatro órdenes y el paso a paso |
| **El Puesto de Tiro** | (juego) | un juego de tiro en canvas con Destello: puntaje, niveles y récord en `localStorage` |

6. **Proyectos:** **solo micro-misiones**, como Ensamblador. Las que vienen de una misión pagan fichas (`micromisiones_completan: si`) y no hay entregas que corrija el docente.
