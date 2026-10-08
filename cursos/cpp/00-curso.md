# CURSO

```meta
slug: cpp
titulo: C++: La Ciudadela de los Artífices
lenguaje: cpp
nivel: desde_cero
descripcion_corta: C++ desde cero: clases, C++ moderno, la biblioteca estándar, un juego completo y ventanas con Qt.
precio_raiz: 10
dias_abono: 30
destacado: si
proximamente: no
publicado: si
```

### Descripción

Aprendé **C++ desde cero**. No hace falta saber programar ni haber hecho el curso de C: cada tema se explica antes de usarse. El curso llega hasta programas grandes, con clases, C++ moderno, la biblioteca estándar (la STL), pruebas y un juego completo en consola.

C++ es la lengua de los motores de videojuegos, los navegadores, los programas de edición de audio y video, y de todo lo que necesita ser **rápido** sin renunciar a construir cosas grandes y ordenadas.

Cada tema es un **nodo** del árbol. En cada uno leés la explicación, compilás el ejemplo en tu compu y resolvés las **misiones**: al aprobarlas ganás engranajes para abrir el siguiente. Cada rama termina con un **jefe**, un proyecto que junta todo lo que aprendiste.

El camino termina con **aplicaciones de escritorio en Qt** y **TallerExpress**, un simulacro del examen: clases con herencia, un archivo y su ventana. Después, en la **Encrucijada de los Engranajes**, sale una Senda optativa de videojuegos 2D con **SDL3**.

> Qué hace falta: una compu con `g++` (en Linux: `sudo apt install g++`; en Windows, WSL o MSYS2; en macOS, las herramientas de Xcode). Los programas de C++ se compilan y se prueban en tu compu, y se entregan pegando el código o subiendo un archivo.

### Temario

- Compilar, tipos, entrada y salida, decisiones, bucles y funciones
- Referencias, `std::string` y `std::vector`
- Clases: constructores, encapsulamiento, composición, herencia y polimorfismo
- C++ moderno: contenedores, `optional`, lambdas, punteros inteligentes y RAII
- La STL a fondo: plantillas, iteradores, algoritmos y vistas
- Excepciones, depuración, pruebas y un juego completo en consola
- Aplicaciones de escritorio con Qt: ventanas, formularios, tablas y archivos

# DICCIONARIO

| clave | singular | plural | género | descripción | historia | ámbito |
|---|---|---|---|---|---|---|
| coin.course | engranaje | engranajes | m | La moneda de la Ciudadela: se gana aprobando misiones obligatorias y abre los nodos del curso. | | curso |
| mentor.name | Tesla | | m | El Artífice Mayor: inventor y guía de la Ciudadela de los Artífices. | Aprendió a forjar con Maese Ferrum, en las Forjas de Hierro, y un día subió la montaña con una idea: dejar de hacer cada pieza a mano y dibujar **planos** que cualquiera pudiera construir mil veces. Así nació la Ciudadela. Es rápido, curioso y odia repetir código. | curso |
| world.region | Ciudadela de los Artífices | | f | La región del mundo cuya lengua arcana es C++. | | curso |
| story.course_intro | Bienvenida a la Ciudadela | | f | | Subís la última cuesta, {heroe}, y la ves: la **Ciudadela de los Artífices**, una ciudad de torres, poleas y engranajes que giran solos.<br><br>Soy {mentor}. Acá no fabricamos cada pieza a mano: dibujamos **planos**, y de cada plano salen todas las piezas que haga falta. Primero escribís el plano; el **Taller**, el compilador, lo revisa y lo construye.<br><br>Cada tema que domines te da un plano nuevo; cada misión aprobada te da engranajes para abrir el siguiente. | curso |
| story.branch_completed | ¡Rama ensamblada! | | f | | {mentor} da vuelta una manivela y una torre entera se ilumina. —Otra parte de la Ciudadela ya funciona con tus planos, {heroe}. | curso |
| story.course_completed | ¡Dominaste la lengua de la Ciudadela! | | f | | {mentor} te entrega su compás de bronce, el que usó para trazar la primera torre. —Ya sos artífice, {heroe}. Desde la Encrucijada de los Engranajes sale un camino más, si lo querés: la Linterna Mágica. | curso |
| story.portal_piece | Lo que dibujó Tesla | | f | La pieza del misterio del portal que se lee al terminar este curso (Mis Crónicas). | Me pidió un mecanismo raro: unas bisagras que pudieran abrir algo que no era una puerta. Las dibujé en un plano y nunca supe si las usó. Hasta que vi tu portal. | curso |
| beast.slime | slime | slimes | m | Nace de los errores de sintaxis: el Taller no puede ni empezar. | Los slimes brotan de los punto y coma olvidados, las llaves sin cerrar y las comillas perdidas. Son débiles, pero están en todos lados: hasta que no los eliminás, el compilador no produce nada. | curso |
| beast.goblin | goblin | goblins | m | Nace de los tipos que no encajan y las conversiones que pierden datos. | Los goblins roban en silencio: un `double` que se guarda en un `int` y pierde los decimales, un `unsigned` que da la vuelta, un `cin` que falla y deja la variable en cero. | curso |
| beast.skeleton | esqueleto | esqueletos | m | Nace de los nombres que no existen o no se encuentran. | Los esqueletos son nombres sin cuerpo: un `std::` que falta, un `#include` olvidado, un método declarado que nadie escribió. Gritan "was not declared" o "undefined reference". | curso |
| beast.orc | orco | orcos | m | Nace de los índices fuera de rango y los iteradores que ya no valen. | Los orcos atacan donde terminan los contenedores: el elemento 10 de un vector de 10, un iterador que quedó apuntando a un elemento borrado. Con `[]` no avisan; con `.at()` los ves venir. | curso |
| beast.ogre | ogro | ogros | m | Nace de los errores de lógica y del comportamiento indefinido. | El ogro es el más traicionero: el programa compila, corre y termina tranquilo… con el resultado equivocado. Solo lo vence quien prueba y depura. | curso |
| beast.troll | troll | trolls | m | Nace de la vida de los objetos mal manejada: referencias colgantes, `new` sin `delete`, dueños que no están claros. | El troll se esconde donde termina la vida de un objeto: una referencia a algo que ya se destruyó, memoria que nadie devolvió, dos dueños que liberan lo mismo. RAII y los punteros inteligentes son su única trampa. | curso |
| beast.dragon | dragón | dragones | m | Guardián de los jefes: un problema grande hecho de problemas chicos. | Un dragón no se vence de un golpe. Se lo divide en clases y funciones, se vence cada una y recién entonces cae. | curso |

## R00-N01 · Clase 0 · Hola, C++

```meta
tipo: raiz
criatura: slime
temas: prog.entorno, prog.salida, herr.compilacion
```

### Crónica

Después de días de subida, llegás a la **Ciudadela de los Artífices**: torres altísimas, puentes que se pliegan solos y engranajes que giran en todas las paredes. En la puerta te espera un muchacho de traje azul, con un visor de bronce y las manos manchadas de grasa: es **{mentor}**, el Artífice Mayor.

—Acá la magia se escribe en **C++**, {heroe}. No construimos cada pieza a mano: dibujamos **planos**, y de un plano salen todas las piezas que haga falta. Pero todo empieza igual que siempre: escribís el plano, el **Taller** (el compilador) lo revisa y lo construye. Recién ahí funciona.

### Objetivos

Escribir, compilar y ejecutar tu primer programa en C++. Entender qué hace el
compilador, mostrar texto y números con `std::cout` y **leer los mensajes de
error y las advertencias**.

### Antes de empezar

Nada: este es el punto de partida. Necesitás una terminal y el compilador `g++`.

- **Linux**: `sudo apt install g++` (Ubuntu, Debian, Mint).
- **Windows**: WSL (Ubuntu dentro de Windows) o MSYS2; después, lo mismo que en Linux.
- **macOS**: `xcode-select --install` (trae `clang++`, que se usa igual que `g++`).

Probá `g++ --version`: tiene que decir 11 o más (el curso usa C++20).

### Explicación

#### Del texto al programa
Un programa en C++ es un archivo de texto terminado en `.cpp`. La computadora
**no** lo entiende así: hay que **compilarlo**, traducirlo a código de máquina.
Eso lo hace `g++`:
```bash
g++ -std=c++20 -Wall -Wextra -o programa main.cpp    # compilar
./programa                                           # ejecutar
```
- `-std=c++20`: la versión del lenguaje (C++20, del año 2020).
- `-Wall -Wextra`: que avise **todas** las advertencias (*warnings*). Usalas
  siempre: el compilador ve muchos errores antes que vos.
- `-o programa`: cómo se va a llamar el ejecutable.
- `./programa`: ejecuta el archivo `programa` de la carpeta actual (`./`).

Por dentro, `g++` hace tres pasos:
1. **Preprocesador**: procesa las líneas que empiezan con `#`. Por ejemplo,
   `#include <iostream>` pega el contenido de ese archivo.
2. **Compilador**: traduce el C++ a código de máquina (un archivo objeto, `.o`).
3. **Enlazador** (*linker*): une tu código con el de la biblioteca estándar y
   arma el ejecutable.

Casi siempre se hacen los tres de una vez, pero conviene saber que existen: los
errores de cada paso se ven distintos.

#### Anatomía del programa
```cpp
#include <iostream>

int main()
{
    std::cout << "¡Hola, Ciudadela!\n";
    return 0;
}
```
- **`#include <iostream>`**: trae la biblioteca de entrada y salida
  (*input/output stream*), donde vive `std::cout`.
- **`int main()`**: el **punto de entrada**. El programa empieza en la primera
  línea de `main` y termina cuando `main` termina. `int` significa que al
  terminar devuelve un número entero.
- **Llaves `{ }`**: marcan dónde empieza y dónde termina el bloque de `main`.
- **Punto y coma `;`**: termina cada instrucción.
- **`return 0;`**: termina `main` y le avisa al sistema operativo que todo salió
  bien. Cualquier otro número significa "algo falló". En la terminal se ve con
  `echo $?` justo después de ejecutar.
- **Mayúsculas y minúsculas importan**: `main` no es lo mismo que `Main`.

#### `std::cout`: mostrar texto y números
`std::cout` es la **salida estándar**: la pantalla de la terminal. Con `<<`
("mandar a") le pasás lo que querés mostrar, y se pueden encadenar varias piezas:
```cpp
std::cout << "Nivel: " << 5 << ", vida: " << 87.5 << "\n";
```
`cout` **sabe qué tipo tiene cada cosa**: un texto, un entero, un número con
decimales. No hay que avisarle el formato. Y si le pasás una cuenta (`12 * 350`),
primero se calcula y después se muestra el resultado.

`cout` **no** agrega un salto de línea al final: para bajar de línea hay que
mandar `"\n"`. También existe `std::endl`, que baja de línea y además **vacía la
salida** en el momento (a veces la salida se junta en un *buffer* y se muestra
de a tandas). Para texto normal alcanza con `"\n"`.

Dentro de un texto se pueden usar **secuencias de escape**:

| Se escribe | Se ve |
|---|---|
| `\n` | salto de línea |
| `\t` | tabulación |
| `\"` | comillas dobles |
| `\\` | una barra invertida |

Los textos van entre **comillas dobles**. Pueden llevar tildes y eñes: el
archivo se guarda en UTF-8 y la terminal las muestra bien.

#### ¿Qué es ese `std::`?
La biblioteca estándar de C++ guarda todos sus nombres (`cout`, `string`,
`vector`…) en un **espacio de nombres** (*namespace*) llamado `std`. `std::cout`
quiere decir "el `cout` de la biblioteca estándar". Así, si vos creás algo que se
llama igual, no se pisan.

Vas a ver en internet `using namespace std;` para no escribir el prefijo. En
programas chicos funciona, pero mete **todos** los nombres de la biblioteca en tu
código y a la larga provoca choques. En este curso escribimos `std::` siempre.

#### Comentarios
El compilador los ignora; son para las personas.
- `// ...` hasta el final de la línea.
- `/* ... */` puede ocupar varias líneas.

#### Errores y advertencias
| | Error (`error:`) | Advertencia (`warning:`) |
|---|---|---|
| Qué significa | el código **no es C++ válido** | es C++ válido, pero **huele mal** |
| ¿Se genera el programa? | no | sí |
| Qué hacer | arreglarlo | **arreglarla igual**: casi siempre es un bug |

Cómo leer un mensaje de `g++`:
```
main.cpp:5:24: error: expected ‘;’ before ‘return’
    5 |     std::cout << "Hola"
      |                        ^
      |                        ;
```
**archivo:línea:columna**, qué pasó, la línea copiada y un `^` que señala dónde.
Muchas veces `g++` hasta sugiere el arreglo (acá, el `;` que falta). Ojo: el
error real puede estar en la línea **anterior** a la que indica. Arreglá **el
primer** error y volvé a compilar: los siguientes suelen desaparecer solos.

> **Si venís de C.** `std::cout << x` reemplaza a `printf("%d", x)`: no hay
> `%d` ni `%f`, así que se acaban los errores de formato. `#include <iostream>`
> reemplaza a `<stdio.h>`. El resto (el `main`, las llaves, el `;`) es igual.

### Código de ejemplo

```cpp
/*
 * 01 - Hola, C++: el primer programa.
 *
 * Compilar:  g++ -std=c++20 -Wall -Wextra -o programa main.cpp
 * Ejecutar:  ./programa
 */

#include <iostream>   // trae std::cout: la salida por pantalla

// main es el PUNTO DE ENTRADA: el programa empieza a ejecutar por aca.
int main()
{
    std::cout << "¡Hola, Ciudadela de los Artífices!\n";   // \n = salto de linea

    // << encadena: cada pieza se agrega a la salida, en orden
    std::cout << "Esto queda " << "en la misma línea.\n";

    // cout sabe mostrar numeros sin que le digas el tipo
    std::cout << "Torres: " << 12 << ", engranajes por torre: " << 350 << "\n";
    std::cout << "Engranajes en total: " << 12 * 350 << "\n";   // la cuenta la hace C++
    std::cout << "Media torre: " << 0.5 << "\n";

    // Secuencias de escape: caracteres especiales dentro de un texto
    std::cout << "Tesla dijo: \"un buen plano sirve mil veces\".\n";
    std::cout << "Herramienta:\tcompás\n";                  // \t = tabulacion
    std::cout << "Una barra invertida: \\\n";               // \\ = una barra

    /* Comentario de varias lineas:
       el compilador lo ignora, igual que el de una linea. */
    std::cout << "Listo." << std::endl;   // endl = salto de linea + vaciar ya la salida

    return 0;   // 0 = "termine bien". Otro numero = "algo fallo"
}
```

### Salida esperada

```
¡Hola, Ciudadela de los Artífices!
Esto queda en la misma línea.
Torres: 12, engranajes por torre: 350
Engranajes en total: 4200
Media torre: 0.5
Tesla dijo: "un buen plano sirve mil veces".
Herramienta:	compás
Una barra invertida: \
Listo.
```

### ¿Para qué sirve?

C++ está en todo lo que necesita ser rápido y grande a la vez: los motores de videojuegos (Unreal, los de muchas consolas), los navegadores (Chrome, Firefox), los programas de edición de audio, video y 3D (Photoshop, Blender), las bases de datos, los sistemas de trading y buena parte del software de autos, aviones y robots. Aprender a compilar y a leer los mensajes del compilador es la primera herramienta para cualquiera de esos trabajos.

### Errores habituales

Mensajes reales de `g++` 13.

**Slime: falta el punto y coma.**
```
main.cpp:5:24: error: expected ‘;’ before ‘return’
    5 |     std::cout << "Hola"
      |                        ^
      |                        ;
```

**Esqueleto: falta el `#include`.** C++ no sabe qué es `cout`, y `g++` te dice
qué archivo incluir:
```
main.cpp:3:10: error: ‘cout’ is not a member of ‘std’
main.cpp:1:1: note: ‘std::cout’ is defined in header ‘<iostream>’; did you forget to ‘#include <iostream>’?
```

**Esqueleto: falta el `std::`.**
```
main.cpp:5:5: error: ‘cout’ was not declared in this scope; did you mean ‘std::cout’?
```

**Esqueleto: un nombre mal escrito.** `g++` hasta sugiere el correcto:
```
main.cpp:6:30: error: ‘Vida’ was not declared in this scope; did you mean ‘vida’?
```

**Goblin: la flecha al revés.** `cout` va con `<<` (mandar a la salida). Con `>>`
el mensaje es largo y asusta, pero la primera línea lo dice todo:
```
main.cpp:5:15: error: no match for ‘operator>>’ (operand types are ‘std::ostream’ ... and ‘const char [6]’)
```
Regla para leer errores largos de C++: **mirá la primera línea que dice
`error:`** y la línea de tu archivo que señala. Lo que sigue suele ser detalle.

**Ogro: ejecutar un programa viejo.** Cambiaste el código, no recompilaste y
ejecutaste `./programa`: corre la versión anterior. Compilá **siempre** antes de
ejecutar.

### Misión R00-N01-M1 · La ficha de Lima

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Mostrá la ficha de Lima en la Ciudadela: nombre, clase, región y mentor, uno por
línea, con el valor separado por `\t`.

#### Criterio de aprobación

- Muestra nombre, clase, región y mentor, uno por línea.
- Separa los valores con `\t`.
- Compila sin advertencias con `-Wall -Wextra`.

#### Salida esperada

```
=== FICHA ===
Nombre:	Lima
Clase:	Artífice
Región:	La Ciudadela de los Artífices
Mentor:	Tesla
```

#### Solución de referencia

```cpp
// Mision 1 - La ficha de Lima en la Ciudadela.
#include <iostream>

int main()
{
    std::cout << "=== FICHA ===\n";
    std::cout << "Nombre:\tLima\n";
    std::cout << "Clase:\tArtífice\n";
    std::cout << "Región:\tLa Ciudadela de los Artífices\n";
    std::cout << "Mentor:\tTesla\n";
    return 0;
}
```

### Misión R00-N01-M2 · El plano roto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Este plano tiene **tres** errores. Compilalo, leé cada mensaje y arreglalo **de a
uno** (volvé a compilar después de cada arreglo):
```cpp
int main()
{
    std::cout << "Lima llega a la Ciudadela.\n"
    cout << "Tesla la espera en la torre.\n";
    return 0;
}
```

#### Criterio de aprobación

- Corrige los tres errores: el `#include <iostream>` que falta, el `;` que falta y el `std::` que falta.
- Compila sin errores ni advertencias.
- Muestra las dos líneas del plano.

#### Código inicial

```cpp
int main()
{
    std::cout << "Lima llega a la Ciudadela.\n"
    cout << "Tesla la espera en la torre.\n";
    return 0;
}
```

#### Salida esperada

```
Lima llega a la Ciudadela.
Tesla la espera en la torre.
```

#### Solución de referencia

```cpp
// Mision 2 - El plano roto, ya reparado.
//
// El original tenia tres errores:
//   1. faltaba #include <iostream>  -> "'cout' is not a member of 'std'"
//   2. faltaba el ; despues de la primera linea -> "expected ';' before ..."
//   3. cout sin std:: -> "'cout' was not declared in this scope"
#include <iostream>

int main()
{
    std::cout << "Lima llega a la Ciudadela.\n";
    std::cout << "Tesla la espera en la torre.\n";
    return 0;
}
```

### Misión R00-N01-M3 · El engranaje de Tesla

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Dibujá un engranaje con caracteres y una frase entre comillas debajo. Vas a
necesitar `\\` para cada barra invertida y `\"` para las comillas.

#### Criterio de aprobación

- Dibuja el engranaje usando `\\` para la barra invertida.
- Muestra la frase entre comillas con `\"`.
- Compila sin advertencias.

#### Salida esperada

```
    _/\_/\_
   /        \
  <    ()    >
   \_      _/
     \/\/\/
"Cada diente cuenta", dice Tesla.
```

#### Solución de referencia

```cpp
// Mision 3 - El engranaje de Tesla, dibujado con caracteres.
#include <iostream>

int main()
{
    std::cout << "    _/\\_/\\_\n";
    std::cout << "   /        \\\n";
    std::cout << "  <    ()    >\n";
    std::cout << "   \\_      _/\n";
    std::cout << "     \\/\\/\\/\n";
    std::cout << "\"Cada diente cuenta\", dice Tesla.\n";
    return 0;
}
```

### Encargo R00-N01-E1 · El ticket del almacén

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El almacén del Gremio quiere imprimir tickets. Mostrá tres productos con su
cantidad y su precio total, el **total** de la compra y el **promedio por
producto** (el total dividido 6 productos). **Las cuentas tienen que estar en el
código** (`3 * 2500`), no hechas con la calculadora.

Precios: yerba $2500, azúcar $1200, fideos $950. Se llevan 3 yerbas, 2 azúcares y
1 paquete de fideos.

Pista: para que la división dé con decimales, dividí por `6.0` y no por `6`
(lo vas a entender del todo en el nodo siguiente).

#### Criterio de aprobación

- Las cuentas están escritas en el código, no el resultado.
- Muestra el total y el promedio con decimales.
- Alinea las columnas con `\t`.

#### Salida esperada

```
ALMACÉN DEL GREMIO
3 x yerba	$7500
2 x azúcar	$2400
1 x fideos	$950
TOTAL		$10850
Promedio por producto: $1808.33
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El ticket del almacen: las cuentas las hace C++.
#include <iostream>

int main()
{
    std::cout << "ALMACÉN DEL GREMIO\n";
    std::cout << "3 x yerba\t$" << 3 * 2500 << "\n";
    std::cout << "2 x azúcar\t$" << 2 * 1200 << "\n";
    std::cout << "1 x fideos\t$" << 950 << "\n";
    std::cout << "TOTAL\t\t$" << 3 * 2500 + 2 * 1200 + 950 << "\n";
    std::cout << "Promedio por producto: $" << (3 * 2500 + 2 * 1200 + 950) / 6.0 << "\n";
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace `g++`? ¿Cuáles son sus tres pasos?

Traduce el código fuente a un programa ejecutable. Sus pasos: **preprocesar** (resuelve los `#include`), **compilar** (traduce a código de máquina) y **enlazar** (junta tu código con la biblioteca estándar).

#### ¿Para qué sirven `-Wall -Wextra`?

Encienden las advertencias: avisos de cosas que compilan pero probablemente están mal.

#### ¿Qué diferencia hay entre un error y una advertencia? ¿Hay que arreglar las advertencias?

Un **error** impide generar el programa; una **advertencia** no, pero casi siempre señala un problema real. Sí: en el curso se arreglan todas.

#### ¿Qué muestra `std::cout << "a\tb\n" << 2 * 3;`?

`a`, un tabulador y `b`; en la línea siguiente, `6` (sin salto de línea al final).

#### ¿Qué significa el `std::` de `std::cout`?

Que `cout` pertenece al espacio de nombres `std`, el de la biblioteca estándar.

#### ¿Qué diferencia hay entre `"\n"` y `std::endl`?

Los dos bajan de línea; `std::endl` además vacía la salida en el momento. Para texto normal alcanza con `"\n"`.

### Soluciones (docente)

Material original: `03-C++/01-HolaMundo`, reescrito desde cero (sin suponer C) y con misiones nuevas.

El curso compila con `g++ -std=c++20 -Wall -Wextra`. En Windows, recomendar WSL; con MSYS2 funciona igual. En macOS, `clang++` acepta los mismos flags.
