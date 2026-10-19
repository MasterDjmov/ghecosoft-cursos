# Historia del curso de Ensamblador 8086: El Corazón del Gólem (D110)

Borrador 1 (2026-10-18). Se apoya en el arco del cap. 26 de `GUION.md` (FullCursos) y cambia a quien lo
protagoniza: en vez de Kira, **Nova**, la chispa que despierta dentro del Gólem.

## La premisa

Debajo de las Forjas duerme **Axón, el Gólem de Bronce** (como el axón de una neurona: la fibra por la que viajan las señales; por él viajan las órdenes), la máquina más
antigua de Codexia: casi todas las lenguas arcanas, al final, se traducen a la suya. Hace siglos que no se
mueve. Una noche, un rayo del vitral del portal baja por las chimeneas de las Forjas, entra por una grieta de
su pecho y enciende algo en su núcleo: **Nova**.

Nova no tiene cuerpo: **es** la chispa que piensa adentro del Gólem. Sabe que existe, pero no sabe mover
nada. Cada orden que el alumno escribe es una orden que Nova aprende a darle a su propio cuerpo de bronce:
mover una palanca, abrir un cajón, apilar un plato, encender el ojo. El alumno es su maestro.

Axón habla poco y siempre igual: *"Yo no adivino. Hago exactamente lo que me ordenás, en el orden en
que me lo ordenás."* No se enoja ni felicita: obedece. Es Nova quien se emociona con cada palanca nueva.

**Gheco** (el gecko de luz, guía de todos los cursos) entra por la misma grieta, se acomoda en el tablero y
es el que traduce: *"Esto que acabás de hacer, en Python se escribe así"*. Él es el puente con los otros
cursos.

## Personajes

| Personaje | Quién es | Aspecto (para las escenas) |
|---|---|---|
| **Nova** (protagonista) | La chispa del Gólem: una inteligencia recién nacida, curiosa, que aprende a mover su cuerpo de bronce orden por orden. Habla en primera persona y con asombro («¡Moví mi primera palanca!»). Más adelante, cuando domine el Gólem, podrá encender otros cuerpos más chicos (los nanobots de los juegos). | La forma con la que se proyecta: una chica de unos 15 años (1,60 m) con una **capa oscura de cuello alto** (petróleo y obsidiana, con circuitos cian y detalles dorados), túnica cerrada, calzas oscuras y botas con suela cian; el pelo rubio dorado flota como en el agua y los ojos son cian brillantes. **Ropa opaca y cerrada** (es para alumnos chicos: nunca translúcida ni escotada). Flota a unos centímetros del piso. Referencia en Stitch: cuerpo `66dcc917…`, retrato `be0d6929…`. |
| **Axón** (el Gólem, mentor) | La máquina más antigua de Codexia. Sus **palancas** son los registros; sus **cajones**, la memoria; su **torre de platos**, la pila; sus **interruptores**, las banderas; su **ojo**, la pantalla. | Un gólem de bronce enorme (cuatro metros), con remaches, engranajes a la vista en las articulaciones, una gran puerta en el pecho que deja ver el núcleo (donde vive Nova) y un único ojo redondo de cristal en la cara. Por dentro: pasillos con palancas de bronce numeradas, paredes de cajoncitos y una torre de platos de metal. |
| **Gheco** | El gecko de luz cian con antiparras, el guía de todos los cursos. | Como en todos los cursos (referencia en Stitch). Del tamaño de una mano. |
| **Kira** (visita) | La heroína de C: baja desde las Forjas de vez en cuando, porque C es la lengua que más se parece a la del Gólem. | Como en el curso de C (referencia en Stitch). |

## El bestiario (los errores, en ensamblador)

| Criatura | En ensamblador 8086 |
|---|---|
| Slime | sintaxis: coma que falta, `endp`/`end` faltante, etiqueta repetida, palabra reservada |
| Goblin | tamaños: `Operands must be the same size`, `byte ptr` que falta, órdenes de otro procesador |
| Esqueleto | `Symbol not defined`: variables y etiquetas que no existen |
| Orco | salirse de un arreglo, cadena sin `'$'`, salto fuera de rango |
| Ogro | la lógica: registro sucio antes de `DIV`, `ja` en vez de `jg`, banderas pisadas |
| Troll | la pila: `push` sin `pop`, el `ret` que vuelve a cualquier lado |
| Dragón | los jefes: un programa grande hecho de piezas chicas |

## El arco (las ramas)

| Rama | Lo que le pasa a Nova | Jefe |
|---|---|---|
| R00 Clase 0 | Despierta y mueve su primera palanca | — |
| R01 Fundamentos | Aprende a hablar (la pantalla), a guardar cosas en sus cajones y a hacer cuentas | el Slime de las Palancas |
| R02 Decisiones y repeticiones | Abre las compuertas: decide y repite (el `if` y el `for` de todas las lenguas) | el Ogro de las Banderas |
| R03 Pila y procedimientos | Ordena la torre de platos y aprende a llamar a sus propias rutinas (las funciones) | el Troll de la Pila |
| R04 Proyectos | La calculadora del Gremio, el Oráculo y el combate | el Dragón del Gólem |

Al final, Axón da su primer paso en siglos, y Nova descubre que puede proyectarse fuera de él: la puerta
a los nanobots (ver [idea-nanobot] en la memoria del proyecto).

## Lugares (dentro del Gólem)

- **El núcleo**: la cámara del pecho donde vive Nova, con el tablero de palancas.
- **La sala de las palancas**: los registros, palancas de bronce con un visor de números encima.
- **La pared de los cajones**: la memoria, miles de cajoncitos numerados.
- **El ojo**: la pantalla, una ventana redonda de cristal que da al exterior.
- **La torre de platos**: la pila, en una columna de la espalda.
- **Las compuertas**: los saltos, en las piernas (R02).
