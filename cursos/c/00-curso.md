# CURSO

```meta
slug: c
titulo: C: Las Forjas de Hierro
lenguaje: c
nivel: desde_cero
descripcion_corta: C desde cero hasta programas completos: memoria, archivos y el metal de la máquina.
precio_raiz: 10
dias_abono: 30
destacado: si
proximamente: no
publicado: si
```

### Descripción

Aprendé **C desde cero**. No hace falta saber programar: cada tema se explica antes de usarse, y el curso llega hasta programas completos, con memoria dinámica, archivos, módulos, depuración y pruebas.

C es la lengua sobre la que están construidos los sistemas operativos, los microcontroladores y buena parte de los programas que usás todos los días. Entender C es entender qué pasa **por debajo**.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, compilás el ejemplo en tu compu y resolvés las **misiones**: al aprobarlas ganás lingotes para abrir el siguiente. Cada rama termina con un **jefe**, un proyecto que junta todo lo que aprendiste.

Al final del camino principal llegás a la **Encrucijada del Yunque**, de donde salen dos Sendas optativas: videojuegos 2D con **SDL3** y electrónica con **Arduino**.

> Qué hace falta: una compu con `gcc` (en Linux: `sudo apt install build-essential`; en Windows, WSL o MSYS2). Los programas de C se compilan y se prueban en tu compu, y se entregan pegando el código o subiendo un archivo.

### Temario

- Compilar, variables, operadores y bits
- Entrada y salida, decisiones, bucles y funciones
- Arrays, textos, structs y punteros
- Memoria dinámica, listas y punteros a función
- Archivos de texto y binarios, módulos y menús
- Depuración, pruebas y proyectos completos

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | lingote | lingotes | m | La moneda de las Forjas: se gana aprobando misiones obligatorias y abre los nodos del curso. | | curso |
| mentor.name | Maese Ferrum | | m | Herrero enano, el Forjador: guía de las Forjas de Hierro. | Forjó su primera hoja cuando las Forjas todavía no tenían techo. Es viejo amigo de Bron, no tolera una advertencia del compilador sin arreglar y dice que el metal no perdona, pero tampoco miente. | curso |
| world.region | Forjas de Hierro | | f | La región del mundo cuya lengua arcana es C. | | curso |
| story.course_intro | Bienvenida a las Forjas | | f | | Bajás del paso de montaña, {heroe}, y el calor te pega en la cara: llegaste a las **Forjas de Hierro**, la región más antigua de {mundo}.<br><br>Soy {mentor}. Acá nadie hace el trabajo por vos: cada pieza se forja a mano y cada byte se cuenta. Primero escribís la receta; después el **Horno**, el compilador, la convierte en una pieza que trabaja.<br><br>Cada tema que domines templa una pieza nueva; cada misión aprobada te da lingotes para abrir el siguiente. | curso |
| story.branch_completed | ¡Rama templada! | | f | | {mentor} golpea el yunque dos veces, que es lo más parecido a un aplauso que se le escucha. —Otra parte de las Forjas ya trabaja con tu metal, {heroe}. | curso |
| story.course_completed | ¡Dominaste la lengua de las Forjas! | | f | | {mentor} te entrega el martillo que usó durante cuarenta años. —Ya no sos aprendiz, {heroe}. Desde la Encrucijada del Yunque salen caminos que pocos recorren: la Forja Viva y el Taller de los Autómatas. Elegí el tuyo. | curso |
| story.portal_piece | Lo que forjó Maese Ferrum | | f | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | Me encargó el plomo para un vitral enorme, más grande que cualquier ventana que yo hubiera visto. Pagó por adelantado y nunca me dijo para qué era. Tenía la misma mirada que tiene Tesela cuando sueña. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis: el Horno no puede ni empezar. | Los slimes brotan de los punto y coma olvidados, las llaves sin cerrar y las comillas perdidas. Son débiles, pero están en todos lados: hasta que no los eliminás, el compilador no produce nada. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tipos y formatos que no coinciden. | Los goblins roban en silencio: un %d para un double, un & que falta en sscanf, un entero que se desborda. El compilador a veces los ve (con -Wall); otras veces solo los ve quien prueba. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de los nombres que no existen o no se encuentran. | Los esqueletos son nombres sin cuerpo: una variable sin declarar, una función sin prototipo, un .c que nadie enlazó. Gritan "undeclared" o "undefined reference". | curso |
| beast.orc | orco | orcos | m | Nace de los índices fuera de rango y los textos que se desbordan. | Los orcos atacan donde terminan los arrays: el elemento 10 de un array de 10, el texto sin lugar para su tapón, el %s sin ancho. En C no avisan: leen o pisan memoria ajena. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica y del comportamiento indefinido. | El ogro es el más traicionero: el programa compila, corre y termina tranquilo… con el resultado equivocado. O anda en tu compu y en otra no. Solo lo vence quien prueba y depura. | curso |
| beast.troll | troll | trolls | m | Nace de la memoria mal manejada: fugas, punteros colgantes, dobles liberaciones. | El troll vive en las Minas: se come la memoria que nadie devolvió, usa bloques ya liberados y apunta a donde no hay nada. El sanitizador es su única luz. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un problema grande hecho de problemas chicos. | Un dragón no se vence de un golpe. Se lo divide en partes, se vence cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, C

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, prog.salida, herr.compilacion
```

### Crónica

Bajás del paso de montaña y llegás a las **Forjas de Hierro**, la región más antigua de {mundo}. Entre el humo y los martillazos, un enano de barba trenzada te mira de arriba abajo: es **{mentor}**, el Forjador.

—Acá la magia se escribe en **C**, {heroe}: casi todas las demás lenguas se forjaron con ella. Primero escribís la receta. Después el **Horno** (el compilador) la convierte en una pieza terminada. Y recién ahí la pieza trabaja.

### Objetivos

Escribir, compilar y ejecutar tu primer programa en C. Entender qué hace el
compilador, mostrar texto con `printf` y **leer los mensajes de error y las
advertencias**.

### Antes de empezar

Nada: este es el punto de partida. Necesitás una terminal y el compilador `gcc`
(ver "Instalación / dependencias" en el [README del capítulo](../README.md)).
Probá `gcc --version`.

### Explicación

#### Del texto al programa
Un programa en C es un archivo de texto terminado en `.c`. La computadora **no**
lo entiende así: hay que **compilarlo**, traducirlo a código de máquina. Eso lo
hace `gcc`:
```bash
gcc -Wall -Wextra -std=c11 -o programa main.c    # compilar
./programa                                         # ejecutar
```
- `-o programa`: cómo se va a llamar el ejecutable.
- `-Wall -Wextra`: que avise **todas** las advertencias (*warnings*). Usalas
  siempre: son el mejor aliado en C.
- `-std=c11`: la versión del lenguaje (C11, del año 2011).
- `./programa`: ejecuta el archivo `programa` de la carpeta actual (`./`).

Por dentro, `gcc` hace tres pasos:
1. **Preprocesador**: procesa las líneas que empiezan con `#`. Por ejemplo,
   `#include <stdio.h>` pega el contenido de ese archivo.
2. **Compilador**: traduce el C a código de máquina (un archivo objeto, `.o`).
3. **Enlazador** (*linker*): une tu código con el de las bibliotecas (el de
   `printf` ya viene hecho) y arma el ejecutable.

Casi siempre se hacen los tres de una vez, pero conviene saber que existen: los
errores de cada paso se ven distintos.

#### `make`: no escribir el comando cada vez
Cada ejemplo trae un `Makefile`, un archivo con las "recetas" para compilar:
```bash
make          # compila (solo si algo cambió)
make run      # compila y ejecuta
make clean    # borra el ejecutable
```
Por dentro, `make` ejecuta el mismo comando `gcc` de arriba.

#### Anatomía del programa
```c
#include <stdio.h>

int main(void)
{
    printf("¡Hola, Forjas de Hierro!\n");
    return 0;
}
```
- **`#include <stdio.h>`**: trae las funciones de entrada y salida estándar
  (*standard input/output*), entre ellas `printf`.
- **`int main(void)`**: el **punto de entrada**. El programa empieza en la
  primera línea de `main` y termina cuando `main` termina. `int` significa que
  al terminar devuelve un número entero; `void`, que no recibe nada.
- **Llaves `{ }`**: marcan dónde empieza y dónde termina el bloque de `main`.
- **Punto y coma `;`**: termina cada instrucción.
- **`return 0;`**: termina `main` y le avisa al sistema operativo que todo
  salió bien. Cualquier otro número significa "algo falló". En la terminal se
  ve con `echo $?` justo después de ejecutar.
- **Mayúsculas y minúsculas importan**: `printf` no es lo mismo que `Printf`.

#### `printf`: mostrar texto
`printf("texto")` muestra el texto **tal cual**: no agrega un salto de línea al
final. Para bajar de línea hay que escribir `\n`. Dentro del texto se pueden usar
**secuencias de escape**:

| Se escribe | Se ve |
|---|---|
| `\n` | salto de línea |
| `\t` | tabulación |
| `\"` | comillas dobles |
| `\\` | una barra invertida |
| `%%` | un signo `%` (porque `%` sola tiene otro significado en `printf`, 02) |

Los textos van entre **comillas dobles**. Pueden llevar tildes y eñes: el
archivo se guarda en UTF-8 y la terminal las muestra bien.

#### Comentarios
El compilador los ignora; son para las personas.
- `/* ... */` puede ocupar varias líneas.
- `// ...` hasta el final de la línea (desde C99).

#### Errores y advertencias
| | Error (`error:`) | Advertencia (`warning:`) |
|---|---|---|
| Qué significa | el código **no es C válido** | es C válido, pero **huele mal** |
| ¿Se genera el programa? | no | sí |
| Qué hacer | arreglarlo | **arreglarla igual**: casi siempre es un bug |

Cómo leer un mensaje de `gcc`:
```
e1.c:4:19: error: expected ‘;’ before ‘return’
    4 |     printf("Hola")
      |                   ^
      |                   ;
```
**archivo:línea:columna**, qué pasó, la línea copiada y un `^` que señala dónde.
Muchas veces `gcc` hasta sugiere el arreglo (acá, el `;` que falta). Ojo: el
error real puede estar en la línea **anterior** a la que indica. Arreglá **el
primer** error y volvé a compilar: los siguientes suelen desaparecer solos.

#### Cómo compilarlo y ejecutarlo

```bash
make run
# o a mano:
gcc -Wall -Wextra -std=c11 -o programa main.c
./programa
```

### Código de ejemplo

```c
/*
 * 01 - Hola, C: el primer programa.
 *
 * Compilar:  gcc -Wall -Wextra -std=c11 -o programa main.c
 * Ejecutar:  ./programa
 * (o simplemente: make run)
 */

#include <stdio.h>   /* trae printf: la "caja de herramientas" de entrada/salida */

/* main es el PUNTO DE ENTRADA: el sistema operativo empieza a ejecutar por aca. */
int main(void)
{
    printf("¡Hola, Forjas de Hierro!\n");     /* \n = salto de linea */
    printf("Esto queda ");                     /* sin \n: la linea sigue abierta */
    printf("en la misma línea.\n");

    /* Secuencias de escape: caracteres especiales dentro de un texto */
    printf("Ferrum dijo: \"el metal no perdona\".\n");   /* \" = comillas */
    printf("Herramienta:\tmartillo\n");                  /* \t = tabulacion */
    printf("Línea 1\nLínea 2\n");
    printf("Una barra invertida: \\\n");                 /* \\ = una barra */
    printf("Cien por ciento: 100%%\n");                  /* %% = un signo % */

    /* Comentario de una linea (estilo C99): */
    // tambien existe este estilo; el compilador lo ignora igual

    return 0;   /* 0 = "termine bien". Otro numero = "algo fallo" */
}
```

### Salida esperada

```
¡Hola, Forjas de Hierro!
Esto queda en la misma línea.
Ferrum dijo: "el metal no perdona".
Herramienta:	martillo
Línea 1
Línea 2
Una barra invertida: \
Cien por ciento: 100%
```

### ¿Para qué sirve?

C está debajo de casi todo lo que usás: el sistema operativo de tu compu y de tu celular, el firmware del router, los controladores de un auto, los motores de muchos videojuegos y hasta el intérprete de Python están escritos en C. Aprender a compilar y a leer los mensajes del compilador es la primera herramienta de cualquiera que trabaje "cerca de la máquina": sistemas embebidos, robótica, drivers o programación de videojuegos.

### Errores habituales

Mensajes reales de `gcc` 13.

**Slime: falta el punto y coma.**
```
e1.c:4:19: error: expected ‘;’ before ‘return’
    4 |     printf("Hola")
      |                   ^
      |                   ;
```

**Esqueleto: falta el `#include`.** C no sabe qué es `printf`. Es "solo" una
advertencia, pero el programa queda mal:
```
e2.c:3:5: warning: implicit declaration of function ‘printf’ [-Wimplicit-function-declaration]
    3 |     printf("Hola\n");
      |     ^~~~~~
e2.c:1:1: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
```

**Esqueleto: un nombre mal escrito.** `gcc` hasta sugiere el correcto:
```
e3.c:5:20: error: ‘Vida’ undeclared (first use in this function); did you mean ‘vida’?
```

**Ogro: olvidar el `\n`.** El texto siguiente sale pegado, y el *prompt* de la
terminal puede aparecer en la misma línea que la última salida.

**Ogro: ejecutar un programa viejo.** Cambiaste el código, no recompilaste y
ejecutaste `./programa`: corre la versión anterior. `make run` evita el
problema porque recompila si algo cambió.

### Misión R00-N01-M1 · La ficha de Kira

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá una ficha con nombre, clase, región y mentor,
alineada con `\t`.

#### Criterio de aprobación

- Muestra nombre, clase, región y mentor, uno por línea.
- Alinea los valores con `\t`.
- Compila sin advertencias con `-Wall -Wextra`.

#### Salida esperada

```
=== FICHA ===
Nombre:	Kira
Clase:	Espadachina
Región:	Las Forjas de Hierro
Mentor:	Maese Ferrum
```

#### Solución de referencia

```c
/*
 * Mision 1 - La ficha de Kira, alineada con tabulaciones.
 */
#include <stdio.h>

int main(void)
{
    printf("=== FICHA ===\n");
    printf("Nombre:\tKira\n");
    printf("Clase:\tEspadachina\n");
    printf("Región:\tLas Forjas de Hierro\n");
    printf("Mentor:\tMaese Ferrum\n");
    return 0;
}
```

### Misión R00-N01-M2 · El pergamino roto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este código tiene **tres** errores. Compilalo, leé
cada mensaje y arreglalo **de a uno**:
```c
int main(void)
{
    printf("Kira conoce a Bron.\n")
    Printf("Bron es mecánico y guerrero.\n");
    return 0;
}
```

#### Criterio de aprobación

- Corrige los tres errores: el `#include <stdio.h>` que falta, el `;` que falta y `Printf` con mayúscula.
- Compila sin errores ni advertencias.
- Muestra las dos líneas del pergamino.

#### Código inicial

```c
int main(void)
{
    printf("Kira conoce a Bron.\n")
    Printf("Bron es mecánico y guerrero.\n");
    return 0;
}
```

#### Salida esperada

```
Kira conoce a Bron.
Bron es mecánico y guerrero.
```

#### Solución de referencia

```c
/*
 * Mision 2 - El pergamino roto, ya reparado.
 *
 * El original tenia tres errores:
 *   1. faltaba #include <stdio.h>  -> "implicit declaration of function 'printf'"
 *   2. faltaba el ; despues del primer printf -> "expected ';' before ..."
 *   3. Printf con mayuscula -> C distingue mayusculas: no existe "Printf"
 */
#include <stdio.h>

int main(void)
{
    printf("Kira conoce a Bron.\n");
    printf("Bron es mecánico y guerrero.\n");
    return 0;
}
```

### Misión R00-N01-M3 · La espada de Ferrum

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dibujá una espada con caracteres (`/\`, `||`, `##`) y
una frase entre comillas debajo. Vas a necesitar `\\` y `\"`.

#### Criterio de aprobación

- Dibuja la espada usando `\\` para la barra invertida.
- Muestra la frase entre comillas con `\"`.
- Compila sin advertencias.

#### Salida esperada

```
      /\
      ||
      ||
      ||
    \=||=/
      ##
"Forjada en C", dice la hoja.
```

#### Solución de referencia

```c
/*
 * Mision 3 - Dibujar la espada de Ferrum con caracteres.
 * La barra invertida se escribe \\ y las comillas \".
 */
#include <stdio.h>

int main(void)
{
    printf("      /\\\n");
    printf("      ||\n");
    printf("      ||\n");
    printf("      ||\n");
    printf("    \\=||=/\n");
    printf("      ##\n");
    printf("\"Forjada en C\", dice la hoja.\n");
    return 0;
}
```

### Encargo R00-N01-E1 · El cartel de la panadería

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

La panadería del Gremio quiere un **cartel de horarios** para la vidriera:
título, una tabla "Día / Horario" alineada con tabulaciones y la frase
"¡Pan fresco al 100%!" al pie.

#### Criterio de aprobación

- Muestra el título y una tabla Día / Horario alineada con `\t`.
- Escribe el `%` como `%%` en "¡Pan fresco al 100%!".

#### Salida esperada

```
PANADERÍA DEL GREMIO
Día		Horario
Lunes a viernes	7 a 20 h
Sábados		8 a 13 h
Domingos	cerrado
¡Pan fresco al 100%!
```

#### Solución de referencia

```c
/*
 * Encargo del Gremio - El cartel de horarios de la panaderia.
 */
#include <stdio.h>

int main(void)
{
    printf("PANADERÍA DEL GREMIO\n");
    printf("Día\t\tHorario\n");
    printf("Lunes a viernes\t7 a 20 h\n");
    printf("Sábados\t\t8 a 13 h\n");
    printf("Domingos\tcerrado\n");
    printf("¡Pan fresco al 100%%!\n");
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace `gcc`? ¿Cuáles son sus tres pasos?

Traduce el código fuente a un programa ejecutable. Sus pasos: **preprocesar** (resuelve los `#include`), **compilar** (traduce a código de máquina) y **enlazar** (junta tu código con la biblioteca, por ejemplo `printf`).

#### ¿Para qué sirven `-Wall -Wextra`?

Encienden las advertencias: avisos de cosas que compilan pero probablemente están mal. Con ellas, el compilador te marca muchos errores antes de ejecutar.

#### ¿Qué diferencia hay entre un error y una advertencia? ¿Hay que arreglar las advertencias?

Un **error** impide generar el programa; una **advertencia** no, pero casi siempre señala un problema real. Sí: en el curso se arreglan todas, como si fueran errores.

#### ¿Qué muestra `printf("a\tb\nc");`?

`a`, un tabulador y `b`; en la línea siguiente, `c` (sin salto de línea al final).

#### ¿Qué significa `return 0;`? ¿Cómo ves ese número en la terminal?

Que el programa terminó bien (0 = sin errores). Se ve con `echo $?` justo después de ejecutarlo.

#### ¿Cómo se escribe un `%` dentro de un `printf`?

Con `%%`: `printf("100%%")` muestra `100%`.

### Soluciones (docente)

Material original: `01-C/01-HolaMundo` (soluciones completas en `soluciones/`, con sus archivos de entrada y salida).

Si alguien trabaja en Windows, recomendar WSL o MSYS2 con `gcc`; el curso asume `gcc` y `make`.
