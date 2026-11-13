# C# · El arco de Ceci (borrador 1, a revisar)

Región: **el Conservatorio de Do Sostenido** (C# se lee «do sostenido»), del material de FullCursos (cap. 27). Los programas son **partituras** y el compilador es **el ensayo general**: si la partitura tiene un error, no hay concierto. Personajes y aspecto: [PERSONAJES.md](PERSONAJES.md). Regla del curso: [../CSHARP.md](../CSHARP.md) § 2.

## 1. El arco

**Ceci** tiene 15 años, toca el violín de oído en el teatro de títeres de su hermano **Hilván**, en la **Feria de las Luces**, y nunca leyó una partitura. Una noche, después de que Nima le dio cuerda a la **cajita de música** del teatro ([javascript.md](javascript.md), R03-N05), Hilván le confiesa algo: la cajita suena desafinada desde que él la encontró, con una etiqueta que dice *«para quien llegue»*. Ceci la lleva al único lugar donde saben de música escrita: el Conservatorio de **Clave**.

**Lo que busca:** saber qué melodía guarda la cajita. Clave le contesta que nadie toca nada acá sin ensayarlo antes, y le pone delante la primera nota.

**Cómo cambia:** de **tocar de oído y sonar ya** a **escribir, ensayar y recién después sonar**. No pierde la alegría: aprende que el ensayo es lo que la deja tocar sin miedo.

**El misterio:** la cajita es del **Vidriero**, el mismo de la llave de Zed y del vitral del portal. Le dejó a Clave una partitura sin terminar. **Al final, la melodía de la cajita completa esa partitura: el vitral, que Nima hizo mover, también tiene que cantar.** Cada líder sabe una parte; Clave sabe la música.

## 2. Cómo se une con los demás

| Con quién | Cómo |
|---|---|
| **Hilván y Nima** (JS) | Ceci es la hermana menor de Hilván; la cajita es la del Teatro. En R01-N04, una **flecha de luz de Nima** llega al Conservatorio con un pedido para Ceci. |
| **Nilo y Elefa** (PHP) | Nilo trae las cartas del Puerto al Conservatorio, y con ellas, encargos (R01-N01). |
| **Kaffa y Zed** (Java) | Clave y Kaffa aprendieron juntos: por eso C# y Java se parecen. La etiqueta de la cajita es igual a la de la llave de Zed. |
| **Tizón** (C) y **Baldo** | Piden encargos: el reparto de lingotes de las Forjas (R01-N03) y las cuentas del puesto de Baldo (R01-N02). |
| **El universo de temas** | Cada nodo marca sus `temas:` (`cursos/temas.md`), y el mapa de *Admin → Universo* lo une con los mismos temas de los otros cursos. |

**Los encargos del Gremio vienen de otras regiones:** cada nodo tiene un encargo que manda alguien de otro curso (el Teatro, el Puerto, Baldo, las Forjas, la Feria). Así, el alumno ve que lo que aprende sirve en todo el mundo.

## 3. Los actos (del material)

| Acto | Lugar | Jefe | Estado |
|---|---|---|---|
| I · Fundamentos | **La Sala de Ensayo** | el Slime Desafinado | hecho |
| II · Objetos | el Taller de Instrumentos | la Quimera de las Mil Partituras | hecho |
| III · Colecciones y funciones | el Archivo y la batuta | la Hidra del Coro | hecho |
| IV · Errores y archivos | el Archivo Mudo | el Liche del Archivo Mudo | hecho |
| V · El mundo real | la Bóveda y la ventanilla | el Duende de la Ventanilla | hecho |
| VI · Proyectos | la Arena, el Jardín de los Setos y el Libro Mayor | el Dragón del Conservatorio | texto hecho (2026-11-13) |

## 4. Las criaturas en C#

| Criatura | En C# |
|---|---|
| Slime | sintaxis: `CS1002: Se esperaba ;` |
| Goblin | tipos: `CS0029`, `CS0266`, `FormatException` |
| Esqueleto | nombres que no existen: `CS0103`; variable sin asignar: `CS0165` |
| Orco | `IndexOutOfRangeException`, `KeyNotFoundException` |
| Ogro | lógica: el programa corre y da otra cosa |
| Troll | `NullReferenceException`, referencias compartidas |

El **pergamino de la maldición** es el *stack trace*: los errores de compilación traen archivo, línea y columna.

## 5. El final (Acto VI, 2026-11-13)

Cada jefe deja una parte de la melodía del Vidriero (el Diapasón Verde, la Cuerda de la Quimera, la Partitura del Coro, el Compás Perdido, la Campanilla Afinada). En la Arena, el **Dragón del Conservatorio**, hecho de todas las partituras que alguien escribió sin ensayar, guarda la última: la **Escama de Do Sostenido**. Ceci rellena la partitura sin terminar con las notas de la cajita, la toca entera con el violín y la cajita juntos, y el dragón se deshace en hojas en blanco que salen volando. La cajita ya no suena desafinada: suena **incompleta, como si esperara otra voz** (`story.course_completed`): el vitral del portal, que también canta.
