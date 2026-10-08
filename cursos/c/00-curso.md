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

> Qué hace falta: nada para empezar. Las micro-misiones y los ejemplos se ejecutan acá mismo, en tu navegador. Para las misiones, una compu con Linux o Windows y un entorno de C: **ZinjaI** o **Code::Blocks** (traen todo) o **VS Code** con `gcc` (en Windows, el de MSYS2). La Clase 0 explica cómo instalar cada uno. Las misiones se entregan pegando el código o subiendo un archivo.

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
| story.course_intro | Bienvenida a las Forjas | | f | | Kira era aprendiz de espadachina en un pueblo común. Una noche, un **vitral** se encendió como un portal y despertó en la boca de las **Forjas de Hierro**, la región más antigua de {mundo}, con la espada en la mano. Lo primero que hizo fue darle un espadazo al portón. La espada se rajó; el portón se abría tirando.<br><br>Soy {mentor}, el Forjador. Acá nada se abre a golpes: cada pieza se forja a mano y **cada byte se cuenta**. Primero se escribe la receta; después el **Horno**, el compilador, la convierte en una pieza que trabaja.<br><br>Vos vas a ser su mente: cada micro-misión que resuelvas la hace avanzar, cada tema que domines templa una pieza nueva y cada misión aprobada te da lingotes para abrir el siguiente. | curso |
| story.branch_completed | ¡Rama templada! | | f | | {mentor} golpea el yunque dos veces, que es lo más parecido a un aplauso que se le escucha. —Otra parte de las Forjas ya trabaja con el metal de Kira. Tizón lo anota en la libreta, con la fecha, la hora y los minutos. | curso |
| story.course_completed | ¡Dominaste la lengua de las Forjas! | | f | | {mentor} le entrega a Kira el martillo que usó durante cuarenta años y golpea el yunque **tres** veces. —Llegaste rompiendo una espada contra un portón y te vas con una que forjaste vos, midiendo cada grado. Desde la Encrucijada del Yunque salen dos caminos que pocos recorren: la Forja Viva y el Taller de los Autómatas. Elegí el tuyo. | curso |
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

Kira despierta de cara al piso, junto a un vitral apagado, con la espada de aprendiz todavía en la mano. Hace calor. Mucho calor. Delante tiene un portón de hierro del tamaño de una casa, y detrás se oyen martillazos.

Kira hace lo que sabe hacer: toma carrera y le da un espadazo al portón. La espada **se raja** de punta a mango. El portón ni se entera. Un enano de barba trenzada y un ojo de luz naranja lo abre **tirando** de la manija, sin esfuerzo: es **{mentor}**, el Forjador.

—Se abre para afuera —dice, y mira la espada rota—. Acá nada se abre a golpes, muchacha. Se abre **sabiendo cuánto pesa cada cosa**. En las Forjas la magia se escribe en **C**: primero escribís la receta y después el **Horno**, el compilador, la convierte en una pieza que trabaja.

Detrás de él asoma un enano joven con un calibre colgado del cuello, que le mide la espada rota a Kira sin pedir permiso. —Se rajó por acá —dice—. ¿La mediste antes de pegar? Es **Tizón**. Sobre el hombro de Kira aparece un gecko de luz con antiparras: **Gheco**.

### Objetivos

Escribir, compilar y ejecutar tu primer programa en C. Entender qué hace el
compilador, mostrar texto con `printf` y **leer los mensajes de error y las
advertencias**.

### Antes de empezar

Nada: este es el punto de partida. Para los ejemplos y las micro-misiones alcanza
con este navegador (tocá **Ejecutar**: la primera vez baja el compilador y tarda
un poco). Para las misiones vas a necesitar un entorno de C en tu compu: abajo
está cómo instalarlo en Linux y en Windows.

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

#### Dónde escribir y compilar (Linux y Windows)
Tres caminos; elegí uno y usalo todo el curso.

**1. ZinjaI** (el más simple, pensado para aprender; Linux y Windows). Bajalo de
su página (`zinjai.sourceforge.net`): en Windows trae el compilador adentro; en
Linux, instalá antes `gcc` (`sudo apt install build-essential`). Archivo → Nuevo,
escribís y **F9** compila y ejecuta.

**2. Code::Blocks** (Linux y Windows). En Windows, bajá el instalador que dice
**mingw-setup**: es el que trae `gcc`. En Linux: `sudo apt install codeblocks`.
Archivo → Nuevo → Archivo vacío, guardalo como `main.c` y **F9**.

**3. VS Code con `gcc` y la terminal.**
- **Linux:** `sudo apt install build-essential` y listo: `gcc --version`.
- **Windows:** instalá **MSYS2** (`msys2.org`), abrí la terminal **MSYS2 UCRT64**
  y escribí `pacman -S mingw-w64-ucrt-x86_64-gcc`. Agregá `C:\msys64\ucrt64\bin`
  a la variable `Path` de Windows para que `gcc` ande en cualquier terminal.
  Probá `gcc --version`.
- En VS Code, la extensión **C/C++** de Microsoft. Se compila desde la terminal
  integrada (Ctrl+ñ):

| | Linux | Windows |
|---|---|---|
| Compilar | `gcc -Wall -Wextra -std=c11 main.c -o programa` | `gcc -Wall -Wextra -std=c11 main.c -o programa.exe` |
| Ejecutar | `./programa` | `programa.exe` (o `.\programa.exe` en PowerShell) |
| Ver el `return` | `echo $?` | `echo %errorlevel%` (cmd) o `$LASTEXITCODE` (PowerShell) |

**Las tildes en la consola de Windows:** si ves `Â¡Hola` en lugar de `¡Hola`,
escribí `chcp 65001` en la consola antes de ejecutar (o, en ZinjaI y
Code::Blocks, configurá la consola en UTF-8). En Linux se ven bien siempre.

**`make`:** algunos ejemplos traen un `Makefile` con las recetas (`make run`,
`make clean`). En Linux ya está; en Windows con MSYS2,
`pacman -S mingw-w64-ucrt-x86_64-make` y se usa `mingw32-make`. No es
obligatorio: el comando `gcc` de la tabla hace lo mismo.

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
  ve justo después de ejecutar (`echo $?` en Linux, `echo %errorlevel%` en Windows).
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
- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks:** pegá el código en un archivo nuevo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `gcc -Wall -Wextra -std=c11 main.c -o programa` y `./programa`
  - Windows: `gcc -Wall -Wextra -std=c11 main.c -o programa.exe` y `programa.exe`

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

### Micro-misión R00-N01-P1 · La primera receta

```meta
lugar: La boca de la Forja
personajes: Kira, Gheco, Maese Ferrum
carta: Mostrar texto | printf("texto\n"); · \n salta de línea · cada instrucción termina con ;
recompensa: xp 10, oro 10
```

#### Escena
Kira despierta junto a un vitral apagado, frente al portón de las Forjas. Un enano de barba trenzada la mira de arriba abajo: **Maese Ferrum**.
—Acá la magia se escribe en C. Decime quién sos. Por escrito.
Sobre el hombro de Kira aparece un gecko de luz con antiparras: **Gheco**. —Escribilo en la receta. Acá las recetas se **compilan**.

#### Gheco sugiere
`printf("…");` muestra el texto entre comillas. `\n` al final baja a la línea siguiente. Tocá **Ejecutar**: C se compila acá mismo, en tu navegador (la primera vez baja el compilador y tarda un poco).

#### Desafío
Completá la instrucción para que Kira se presente.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    ___("Me llamo Kira y vengo de muy lejos.\n");
    return 0;
}
```

#### Salida esperada
```
Me llamo Kira y vengo de muy lejos.
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    printf("Me llamo Kira y vengo de muy lejos.\n");
    return 0;
}
```

#### Al superarla
Ferrum lee la receta compilada y asiente una sola vez. —De muy lejos. Ya se nota. —Mira la espada que Kira tiene en la mano, y no dice nada más.

#### Imagen
- La boca de las Forjas de Hierro de noche: un portón de hierro enorme, chimeneas y ríos de lava al fondo, un vitral apagado en el piso.
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) se levanta del piso con una espada de aprendiz en la mano.
- Maese Ferrum (enano macizo, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) la mira con los brazos cruzados.
- Gheco, un gecko cian con antiparras, aparece sobre el hombro de Kira.

### Micro-misión R00-N01-P2 · Tres líneas, un solo printf

```meta
lugar: La boca de la Forja
personajes: Kira, Gheco, Maese Ferrum
carta: Secuencias de escape | \n salto de línea · \t tabulación · \" comillas · %% un signo %
recompensa: xp 10, oro 10
```

#### Escena
—La ficha de entrada va en tres renglones —dice Ferrum—: nombre, oficio y "lo que trae". Con comillas, como se debe.

#### Gheco sugiere
Dentro del texto, `\n` baja de línea, `\t` deja una tabulación y `\"` escribe unas comillas sin cerrar el texto.

#### Desafío
Escribí las secuencias que faltan para que la ficha quede en tres líneas y con comillas.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    printf("Nombre:\tKira___Oficio:\tespadachina___Trae:\t___una espada___\n");
    return 0;
}
```

#### Salida esperada
```
Nombre:	Kira
Oficio:	espadachina
Trae:	"una espada"
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    printf("Nombre:\tKira\nOficio:\tespadachina\nTrae:\t\"una espada\"\n");
    return 0;
}
```

#### Al superarla
Ferrum tacha «espada» y escribe arriba «espada (rajada)». Kira no le dice nada. Todavía.

#### Imagen
- Una ficha de hierro con tres renglones grabados en luz cian: Nombre, Oficio, Trae.
- Maese Ferrum (enano macizo, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) corrige la ficha con una tiza.

### Micro-misión R00-N01-P3 · El punto y coma olvidado

```meta
lugar: La boca de la Forja
personajes: Kira, Gheco, Tizón
criatura: slime
carta: Error de compilación | el Horno revisa ANTES de ejecutar · expected ';' : falta un punto y coma · arreglá el primer error y volvé a compilar
recompensa: xp 10, oro 10
```

#### Escena
Un enano joven con un calibre colgado del cuello se acerca a mirar la receta de Kira: **Tizón**. Del renglón dos gotea un **slime**.
—El Horno no la quiere —dice, midiéndole el renglón—. Le falta algo. Chiquito.

#### Gheco sugiere
Un **error de compilación** frena todo antes de ejecutar. `expected ';' before …` quiere decir que falta un punto y coma al final de la línea anterior a la que marca.

#### Desafío
Arreglá la receta para que el Horno la acepte.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    printf("Kira conoce a Tizon.\n")
    printf("Tizon mide todo.\n");
    return 0;
}
```

#### Salida esperada
```
Kira conoce a Tizon.
Tizon mide todo.
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    printf("Kira conoce a Tizon.\n");
    printf("Tizon mide todo.\n");
    return 0;
}
```

#### Al superarla
El slime se evapora con un *plop*. Tizón anota en su libreta: «Punto y coma: 1 mm. Importancia: enorme».

#### Imagen
- Una receta de pergamino con una marca roja en un renglón, de la que gotea un slime verde.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) mide el renglón con el calibre.

### Micro-misión R00-N01-P4 · Lo que el Horno ignora

```meta
lugar: La boca de la Forja
personajes: Kira, Gheco, Tizón
carta: Comentarios | /* … */ ocupa varias líneas · // hasta el final de la línea · el compilador los ignora
recompensa: xp 10, oro 10
```

#### Escena
Tizón deja notas para sí mismo en todas partes, incluso adentro de las recetas. El problema es que el Horno intenta leerlas como si fueran C.

#### Gheco sugiere
Los **comentarios** son para las personas: `/* … */` puede ocupar varias líneas y `//` llega hasta el final de la línea. El compilador los saltea.

#### Desafío
Convertí las notas de Tizón en comentarios para que la receta compile y muestre solo los dos saludos.

#### Código inicial
```c
#include <stdio.h>

int main(void)
{
    Nota de Tizon: medir antes de pegar
    printf("Hola, Forjas.\n");
    recordar: el cajon de clavos llega hasta 255
    printf("Hola, Horno.\n");
    return 0;
}
```

#### Salida esperada
```
Hola, Forjas.
Hola, Horno.
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    /* Nota de Tizon: medir antes de pegar */
    printf("Hola, Forjas.\n");
    // recordar: el cajon de clavos llega hasta 255
    printf("Hola, Horno.\n");
    return 0;
}
```

#### Al superarla
Las notas de Tizón quedan en la receta, pero el Horno ya no se atraganta con ellas. —Así las leo yo y no él —dice Tizón, satisfecho.

#### Imagen
- Una receta llena de notas a mano en los márgenes, algunas encerradas en /* */ que brillan en gris.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) escribe una nota más con un lápiz detrás de la oreja.

### Micro-misión R00-N01-P5 · El portón se abre tirando

```meta
lugar: La boca de la Forja
personajes: Kira, Gheco, Maese Ferrum, Tizón
carta: La anatomía | #include <stdio.h> trae printf · int main(void) { … } es donde empieza · return 0; avisa que todo salió bien
recompensa: xp 15, oro 15
item: Espada Rajada
```

#### Escena
Kira toma carrera y le da un espadazo al portón. La espada **se raja** de punta a mango; el portón ni se entera. Ferrum lo abre **tirando** de la manija.
—Acá nada se abre a golpes. Escribí la receta entera, de punta a punta: lo que se trae, dónde empieza y cómo termina.

#### Gheco sugiere
Todo programa de C trae `#include <stdio.h>` para usar `printf`, empieza en `int main(void)` (entre llaves) y termina con `return 0;`.

#### Desafío
A la receta le falta el comienzo de `main` y el final. Completala.

#### Código inicial
```c
#include <stdio.h>

___
{
    printf("El porton se abre tirando.\n");
    printf("Kira guarda la espada rajada.\n");
    ___
}
```

#### Salida esperada
```
El porton se abre tirando.
Kira guarda la espada rajada.
```

#### Solución
```c
#include <stdio.h>

int main(void)
{
    printf("El porton se abre tirando.\n");
    printf("Kira guarda la espada rajada.\n");
    return 0;
}
```

#### Al superarla
El portón se abre de par en par. Ferrum le devuelve la espada rajada. —Guardala. Algún día vas a querer acordarte de esto. —La **Espada Rajada** va a tu mochila. En la pared de la entrada, alguien escribe con tiza: «Espadazos: 1».

#### Imagen
- Kira (pelo negro corto con un mechón cian, visor cian sobre la oreja izquierda, traje negro ajustado con líneas cian) mira su espada rajada de punta a mango, frente a un portón de hierro intacto.
- Maese Ferrum (enano macizo, barba gris larga trenzada, ojo derecho cibernético naranja, delantal de cuero y brazos de armadura) abre el portón tirando de la manija, sin esfuerzo.
- Tizón (enano joven, pelo rojizo revuelto, hollín en las mejillas, antiparras en la frente, un calibre de bronce colgado del cuello) se ríe por lo bajo detrás de él.

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
    printf("Kira conoce a Tizon.\n")
    Printf("Tizon es aprendiz de herrero.\n");
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
    printf("Kira conoce a Tizon.\n")
    Printf("Tizon es aprendiz de herrero.\n");
    return 0;
}
```

#### Salida esperada

```
Kira conoce a Tizon.
Tizon es aprendiz de herrero.
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
    printf("Kira conoce a Tizon.\n");
    printf("Tizon es aprendiz de herrero.\n");
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

Los alumnos de la UNLaR usan Code::Blocks, ZinjaI y VS Code; los de la UTN, VS Code. En Windows, ZinjaI y Code::Blocks (versión mingw-setup) traen `gcc`; con VS Code, MSYS2 (UCRT64). Los ejemplos y las micro-misiones también corren en el navegador (D98).
