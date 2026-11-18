# Historia del curso de TypeScript: El Mirador de las Constelaciones — aprobada (2026-11-16)

El docente pidió arrancar TypeScript con **un héroe nuevo con aire steampunk**, y que **todo el Mirador** sea steampunk (2026-11-16). Esto reemplaza lo aprobado el 2026-10-30 en [JAVASCRIPT-TYPESCRIPT.md](../JAVASCRIPT-TYPESCRIPT.md) § 10, donde la heroína de TS era Nima otra vez. Lo demás de § 4 se mantiene, adaptado:
- el Mirador;
- Astrea;
- las estrellas;
- las ramas;
- los jefes.

Lo que decidió el docente está en § 10.

## 1. El lugar: un observatorio de latón y vapor

Al final de JavaScript, la flecha de Nima mueve el vitral del portal por primera vez. El vitral muestra **el lugar adonde fue el Vidriero**: un observatorio en la cima de la montaña, arriba de la Feria. Ese lugar es **el Mirador de las Constelaciones**.

El Mirador es **steampunk**:
- cúpulas de latón con remaches;
- telescopios enormes que se mueven con engranajes y bielas;
- caños de cobre que silban vapor;
- relojes astronómicos;
- mapas del cielo grabados en discos de bronce que giran.

En el centro está **el Gran Planisferio**, un planetario mecánico del tamaño de una sala: cada estrella es una pieza de vidrio montada en un brazo de latón. **El Planisferio está parado desde que se fue el Vidriero.**

**Para no confundirlo con la Ciudadela de los Artífices (C++):**

| | La Ciudadela (C++) | El Mirador (TS) |
|---|---|---|
| Qué es | una fábrica de engranajes | un observatorio |
| Paleta | rayos y cian | latón, cobre, cielo de noche y el azul de TypeScript |
| Su oficio | fabricar piezas con planos | **medir el cielo y ponerle forma a cada estrella** |

**La lengua del Mirador:**
- cada pieza lleva grabada su **medida** antes de montarse;
- si una estrella no encaja en la ranura de su figura, **el mecanismo no la acepta**: se traba antes de girar, no después.

Eso es el chequeo de tipos: el error aparece al armar (al compilar), no cuando la máquina ya está andando (al ejecutar).

## 2. El héroe: Rigel, el aprendiz de relojero

**Propuesta:** un chico. Los últimos cursos tienen protagonista mujer (Nima, Ceci, Nova, Iris).

**Rigel** (por la estrella de Orión) es **aprendiz de Tesla** en la Ciudadela de los Artífices. Arregla relojes y autómatas chicos.
- Tiene manos rápidas y mucha imaginación.
- Arma todo **a ojo**: prueba, y si no anda, lo desarma y vuelve a probar.
- Le explotan muchos inventos, siempre **con la máquina ya andando**.

Cuando el vitral del balcón se mueve, en la Ciudadela todos los engranajes dan **un solo golpe al mismo tiempo**. Tesla lo entiende: **el Planisferio del Mirador quiere volver a andar.** Lo construyeron él y el Vidriero hace años, y ahora necesita a alguien que lo repare. Le da a Rigel un plano y lo manda montaña arriba.

En el Mirador, Rigel aprende lo contrario de lo que sabe: **medir antes de armar**.

## 3. La medida antes que la pieza (la metáfora del curso)

| En el Mirador | En TypeScript |
|---|---|
| la medida grabada en cada pieza | el **tipo** (`string`, `number`, `boolean`) |
| el calibre que mide sin armar nada | el **compilador** (`tsc`): revisa antes de ejecutar |
| una pieza que no entra en su ranura | un **error de tipos** (`TS2322`) |
| la ficha técnica de una pieza: qué tiene y cómo se usa | `interface` y `type` |
| un molde que sirve para cualquier pieza, con su medida adentro | los **genéricos** (`Caja<T>`) |
| una ranura que acepta dos formas, con una palanca que pregunta cuál llegó | las **uniones** y el **narrowing** |
| la pieza que dice «capaz que no estoy» | `null` y `undefined` con `strictNullChecks` |
| la pieza sin medida, que entra en cualquier lado y rompe todo | `any` (el Camaleón Any) |
| volver a poner en marcha el Planisferio | el proyecto final: *Junta las Gemas* tipado |

## 4. Ficha de Rigel (para PERSONAJES.md cuando se apruebe)

- **Curso y rol:** TypeScript, el Mirador de las Constelaciones. Protagonista.
- **Edad y sexo:** 16, varón.
- **Altura y contextura:** mediano (1,68 m), flaco y ágil, siempre un poco encorvado sobre lo que arregla.
- **Rasgos:**
  - piel trigueña con pecas, ojos grises;
  - **pelo castaño claro, revuelto**, con un mechón quemado por una chispa;
  - **antiparras de latón** con lentes intercambiables (una lupa, una azul, una de ver estrellas), casi siempre subidas a la frente.
- **Ropa:**
  - **chaleco de cuero marrón cerrado**, con muchos bolsillos y botones de bronce, sobre una camisa azul de mangas arremangadas hasta el codo;
  - **guantes sin dedos** de cuero;
  - pantalón de lona oscuro con rodilleras, botas de trabajo;
  - **cinturón de herramientas** (destornilladores chiquitos, pinzas, un aceitero);
  - **ropa opaca y cerrada** (la usan alumnos chicos).
- **Objeto que cambia con él:** **el calibre** (un pie de rey de latón, para medir).
  - Clase 0: **el Calibre de Aprendiz**, gastado, regalo de Tesla.
  - R02: **el Calibre de Constelaciones**, con un nonio de estrellas que mide figuras.
  - Final: **el Calibre del Vidriero**, que mide el portal.
  - En la espalda, siempre, una **mochila con un engranaje a la vista** y un catalejo plegable.
- **Color:** **azul TypeScript** (#3178C6) con **latón**.
- **Personalidad:**
  - curioso, inventor, charlatán y entusiasta;
  - **arma primero y piensa después**;
  - se ríe de sus propios desastres;
  - generoso: le arregla el reloj a cualquiera.
- **Le gusta:** los relojes por dentro, el olor a aceite de máquina, mirar las estrellas desde el techo de la Ciudadela, el pan con miel de la Feria (se lo hace conocer Nima).
- **Defecto o miedo:**
  - **no mide**: confía en el ojo y se equivoca en la pieza que importa;
  - le da miedo que un invento suyo lastime a alguien al arrancar.
  - En el Mirador aprende que **lo que se mide antes no explota después**.
- **Frase:** «Mido dos veces, armo una.»
- **Relaciones:**
  - alumno de **Astrea** (§ 5);
  - aprendiz de **Tesla**: lo conoce **Lima**, y **Bron** le prestó la llave inglesa una vez;
  - **Nima** sube al Mirador con la imagen que mostró el vitral, y lo ayuda en las Sendas;
  - **Gheco** lo guía, como en todos los cursos.
- **Cómo llega:** los engranajes de la Ciudadela dan un golpe al mismo tiempo, Tesla le da el plano y Rigel sube la montaña hasta el Mirador por un **ascensor de vapor** abandonado.
- **Primera aparición:** TypeScript, Clase 0. Antes no se lo nombra en ningún curso; se puede sumar una mención en la Ciudadela.

## 5. La líder, la moneda y la montura

- **Líder: Astrea, la Lechuza Cartógrafa** (aprobada el 2026-10-30), ahora steampunk:
  - una lechuza grande, de plumas gris azuladas;
  - **anteojos de varias lentes de latón** que se acomodan con una ruedita;
  - un **compás de bronce** y un **chaleco de cartógrafa** con mapas enrollados.
  - Le pone nombre y figura a cada estrella.
  - Lema: *«Nada brilla sin su forma.»*
- **Moneda: estrellas**, ahora **estrellas de latón**: fichas estampadas con una estrella, las que da el Planisferio cuando una pieza encaja.
- **Montura de Rigel: Fuelle**, un **zorro mecánico de latón** que anda a vapor y suelta silbidos cuando está contento. Rigel lo arma en R01 a partir de un autómata roto del Mirador. Crece por etapas, como Destello: le suma piezas en cada rama.
- **La gente del Mirador** (para ramas y misiones):
  - **un farero de estrellas**, que enciende las lámparas de los telescopios;
  - **una fogonera**, que cuida las calderas;
  - **una aprendiz de Astrea** que copia los mapas;
  - **un viejo relojero** que se acuerda del Vidriero.

## 6. El cruce con el misterio del portal

- **El Planisferio y el portal están conectados:** el Vidriero lo construyó para **medir el portal**. Cada figura del Planisferio es una de las figuras del vitral.
- En **el Atlas del Vidriero** (R05), Rigel encuentra el **plano entero del portal, con todas sus figuras**. Falta una, y esa queda para React Native o Laravel. No se revela cuál es (como estaba en la propuesta).
- **Final:** Rigel pone en marcha el Planisferio. Las constelaciones giran y el vitral del balcón **se queda quieto en la figura correcta** por primera vez.
- **Cruces con otros cursos:**
  - **C++:** Tesla y el Vidriero construyeron juntos el Planisferio. En la Ciudadela no se cuenta.
  - **JavaScript:** Nima trae la imagen del vitral y es la que sube con la noticia.
  - **Java:** Astrea y Kaffa se pelean amistosamente por quién inventó los moldes (aprobado).

## 7. El arco (las ramas, como en la propuesta)

| Rama | Zona | Lo que se aprende (capítulos) | Lo que le pasa a Rigel | Jefe |
|---|---|---|---|---|
| R00 | El ascensor de vapor | qué es TS, `tsc`, inferencia (01) | Sube la montaña; su primer arreglo explota y Astrea le enseña a medir | — |
| R01 | La Sala de las Figuras | tipos básicos, tuplas, `any`/`unknown`/`never`, `interface` y `type`, funciones tipadas, sobrecarga (02–04) | Mide sus primeras piezas; arma a Fuelle | **el Camaleón Any**, un autómata que cambia de forma y esconde los errores |
| R02 | Los Moldes de Estrellas | clases tipadas, `private` contra `#`, `abstract`, `implements`, enums, `as const`, genéricos (05–08) | Hace moldes que sirven para muchas estrellas | **la Mantícora de las Mil Formas** (genéricos) |
| R03 | El Telescopio | uniones, narrowing, uniones discriminadas, `never`, utility types, módulos, `import type` (09–12) | Ajusta el telescopio para ver cada estrella como es | **el Cerbero de las Uniones** (cada cabeza, un tipo) |
| R04 | La Cúpula | errores tipados, `Result<T>`, `Promise<T>`, DOM tipado, `strictNullChecks`, decoradores, `tsconfig` (13–19) | Abre la cúpula; aparecen las piezas que «capaz que no están» | **el Espejismo Null** |
| R05 | El Atlas del Vidriero | JS contra TS, el modelo tipado del juego, *Junta las Gemas* en TS (20–22) | Encuentra el Atlas y pone en marcha el Planisferio | **el Dragón de las Constelaciones Rotas** |

**Jefes:** los cinco están aprobados. Con el Mirador steampunk, se dibujan como **autómatas de latón y vidrio**, con piezas del Planisferio mal armadas. La Hidra y la Quimera de la propuesta cambiaron de bicho porque se repetían con C# y C++ (§ 10).

## 8. El bestiario (los errores, en TypeScript)

| Criatura | En TypeScript |
|---|---|
| Slime | sintaxis: llave sin cerrar, `:` de más, anotación mal escrita |
| Goblin | tipos que no encajan: `TS2322` (un `string` donde va un `number`), `TS2345` en los argumentos |
| Esqueleto | lo que no existe: `TS2339` (la propiedad no está), `TS2304` (el nombre no está) |
| Orco | los límites: tuplas de largo fijo, el índice que «capaz que no está», `TS2532` (`Object is possibly undefined`) |
| Ogro | la lógica: un `switch` que se olvida de un caso (`never`), el `as` que miente |
| Troll | el tiempo: `Promise<T>` sin `await`, el tipo de lo que todavía no llegó |
| Dragón | los jefes: un modelo grande hecho de tipos chicos |

Igual que en los otros cursos: «el Goblin del Mirador», «el Esqueleto de la Cúpula». Con el estilo steampunk, son **criaturas de cuerda**: slimes de aceite, goblins con engranajes en la espalda, esqueletos de alambre.

## 8 bis. Lo que se agregó al material de base

FullCursos (cap. 23) está resumido. El docente pidió, el 2026-11-17, sumar lo que falte para no saltear criterios que después hacen falta. Se agregó:
- **R01-N08 · Más formas:** firmas de índice, intersecciones (`&`), arreglos `readonly` y tipos literales (`let` contra `const`).
- **R02-N04 · static y set:** miembros `static`, fábricas y `set` que valida.
- **En R02-N06 y R02-N07:** `Map` y `Set` tipados, `keyof`, `T[K]`, `typeof` en los tipos y genéricos por defecto.
- **En R03:** el `filter` con guardia, `NonNullable`, `satisfies` (R03-N05) y **R03-N06 · Tipos que fabrican tipos** (mapped types, modificadores, template literal types y `as`). Los guardias propios (`x is T`) y `in` ya estaban en FullCursos.
- **En R04:** `Awaited` (R04-N02), `noUncheckedIndexedAccess` y `exactOptionalPropertyTypes` (R04-N06), `noImplicitReturns`/`noUnusedLocals` en micro-misiones con su `tsconfig`, archivos `.d.ts` y `declare` (R04-N08), la trampa de las funciones con la pregunta por `null` (R04-N04 y N05) y los decoradores con parámetros (R04-N07).
- **En las Sendas:** `toSorted` y los arreglos `readonly` al ordenar (S01-N02); `Promise.race` con `Promise<never>`, reintentos con `return await` y listas por páginas (S02-N03); máquinas de estados con tabla de transiciones (S03); **tipos condicionales e `infer`** (S04-N02, cómo está hecho `ReturnType`), validadores con el tipo calculado desde el esquema (como Zod) y `verbatimModuleSyntax` con `import type` obligatorio (S04-N04).

**Gente nueva:**
- **Don Péndulo**, el relojero viejo de la fundición (R02), que conoció al Vidriero.
- Se nombra a la **fogonera** de las calderas (sin nombre todavía).

## 9. Lo que sigue (las fases de D115)

| Fase | Qué | Para probar |
|---|---|---|
| 5 | El compilador de TypeScript en el navegador: micro-misiones de tipo **Compilador** y errores en español | una micro-misión de prueba que da `TS2322` |
| 6 | El curso de TS completo (22 capítulos de FullCursos), con Clase 0 en Próximamente | todo el curso, con la simulación |
| 7 | Imágenes: proyecto de Stitch nuevo para el Mirador, con la hoja de Rigel, Astrea, Fuelle, el fondo, el logo, la moneda, los jefes, las escenas, los ítems y el mapa | publicarlo |

Mientras no esté aprobada la historia, se puede avanzar la fase 5, que no depende de ella.

## 10. Lo que decidió el docente (2026-11-16)

Aprobó todos los puntos como estaban propuestos:
1. **Rigel**, chico de 16, aprendiz de relojero de Tesla.
2. **Viene de la Ciudadela** (C++). Tesla y el Vidriero construyeron juntos el Planisferio.
3. **Astrea steampunk**, las **estrellas de latón** como moneda y **Fuelle**, el zorro mecánico, como montura.
4. **Nima** aparece solo como cruce.
5. **Los jefes repetidos cambian de bicho.** El Kraken de la propuesta también se repetía (C++ tiene el Kraken de los Contenedores), así que quedaron:
   - R02: **la Mantícora de las Mil Formas**;
   - R03: **el Cerbero de las Uniones**, tres cabezas, cada una un tipo.
6. **Se empieza la fase 5** (el compilador).

También pidió **armar los personajes con sus hojas de perfil (8 ángulos)** antes de las escenas, para que después salgan siempre bien (§ 11).

## 11. Imágenes y hojas

Proyecto de Stitch nuevo para el Mirador. De cada uno: imagen de cuerpo entero (la referencia) y su hoja de 8 ángulos (ver [ESCENAS.md](../ESCENAS.md) § Hojas):
- Rigel;
- Astrea;
- Fuelle;
- Gheco.

Proyecto de Stitch: **`7987528111863289727`** («El Mirador de las Constelaciones (TypeScript)»). Copias en `scripts/escenas/referencias/7987528111863289727/` y las hojas anotadas en `referencias/hojas.json`.

| Quién | Cuerpo entero | Hoja de 8 ángulos | Detalles aceptados |
|---|---|---|---|
| Rigel | `169e526a…` | `9d90852f…` (2026-11-17) | la figura sentada quedó arriba a la derecha, no abajo |
| Astrea | `f12c34b1…` | `ab58ee50…` (2026-11-17) | — |
| Fuelle | `20837fe3…` | `62a7aff4…` (2026-11-17) | la vista de espaldas es poco clara |
| Gheco | falta | falta | el MCP no sube imágenes: el docente tiene que subir la oficial (`gheco-code.webp`) en la web de Stitch, y ahí se le hace la hoja |
| Don Péndulo | `ea76e5e1…` | `9244a9f3…` (2026-11-18) | — |
| la fogonera | `14eb2a00…` | `f0d544d4…` | — |
| el Camaleón Any | `3ef2e868…` | `da3b196f…` | franja blanca abajo |
| la Mantícora | `85ec12ec…` | `45a01c90…` | — |
| el Cerbero | `acc511e2…` | `39ddd228…` | en la figura 7 cambia el orden de los colores; franja abajo |
| el Espejismo Null | `2b8d2ea2…` | `2d66524f…` | el engranaje del cuerpo entero no es hueco (en la hoja sí) |
| el Dragón | `c7a6ee79…` | `7add35e1…` | alas más de murciélago que en el cuerpo entero |
| la Polilla de Bronce | `ca3f7924…` | `3a21259c…` | orejitas de gato |
| el Autómata Falsificador | `dcbb76c9…` | `e0759b12…` | dos ojos en la figura de frente |
| el Gólem de Vapor | `5d3be231…` | `ced88c5f…` | franja abajo |
| la Urraca de Cobre | `2ec1c615…` | `f767fb01…` | franja abajo |
| el Eclipse de Hierro | `59e10421…` | `9cc949c9…` | — |
| goblin de cuerda | `15f7f0e0…` | `96dfd131…` | — |
| esqueleto de alambre | `73b6b91c…` | `e4191c54…` | — |
| ogro de cuerda | `947320f9…` | `225536b8…` | — |
| troll de cuerda | `e427f195…` | `8a5e6f53…` | — |
| orco de cuerda | `40e0c7d6…` | `1e4912fa…` | franja abajo |

Hecho en la fase 7 (2026-11-18): el fondo del Mirador (`cursos/typescript/marca/mundo_astrea.webp`), la moneda (`marca/moneda.webp`), el mapa de las expediciones (`public/img/mundos/mirador/mapa.webp`), los 6 aspectos de Rigel, los 5 niveles de Fuelle, los 16 ítems y la enciclopedia del elenco. Las ids completas, en `scripts/escenas/pendientes.py` (`REFS['typescript']`) y `referencias/hojas.json`.

**Falta:**
- **subir a la web de Stitch, en este proyecto, las imágenes oficiales de Gheco, Nima, Elefa y Tesla** (el MCP no sube imágenes); ahí se les hace la hoja y recién entonces arrancan las escenas (316 de las 317 llevan a Gheco);
- el logo del curso, como los demás: Gheco con «GhecoSoft - TS» (lo hace el docente);
- (hecho) los ítems de los cinco jefes del camino principal, con el nombre de su insignia; los jefes de las Sendas no dejan ítem, como en JS.
