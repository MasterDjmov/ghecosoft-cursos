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

> Qué hace falta: los ejemplos y las micro-misiones corren en este navegador. Para las misiones, una compu con `g++` y un editor: ZinjaI, Code::Blocks o VS Code (en Linux y en Windows), y Qt Creator para la rama de Qt. En Linux: `sudo apt install g++`; en Windows, MSYS2 o el compilador que trae el editor; en macOS, las herramientas de Xcode). Los programas de C++ se compilan y se prueban en tu compu, y se entregan pegando el código o subiendo un archivo.

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
| story.course_intro | Bienvenida a la Ciudadela | | f | | Bron era mecánico en un pueblo común: arreglaba todo a mano, pieza por pieza, con su llave inglesa cian. Una noche, un **vitral** se encendió como un portal y despertó al pie de la cuesta de la **Ciudadela de los Artífices**, en {mundo}: torres, poleas y engranajes que giran solos. Todos, menos los del portón.<br><br>Soy {mentor}. Acá no fabricamos cada pieza a mano: dibujamos **planos**, y de cada plano salen todas las piezas que haga falta. Primero se escribe el plano; el **Taller**, el compilador, lo revisa y lo construye.<br><br>Cada tema que Bron domine le da un plano nuevo; cada misión aprobada, engranajes para abrir el siguiente. | curso |
| story.branch_completed | ¡Rama ensamblada! | | f | | {mentor} da vuelta una manivela y una torre entera se ilumina. —Otra parte de la Ciudadela ya funciona con los planos de Bron. —Lima lo anota en su cuaderno de relojera, y Bron pregunta para qué le sirve. Esta vez nadie le contesta: ya lo sabe. | curso |
| story.course_completed | ¡Dominaste la lengua de la Ciudadela! | | f | | {mentor} le entrega a Bron su compás de bronce, el que usó para trazar la primera torre. —Llegaste arreglando doscientos engranajes a mano, con una llave mellada, y te vas con una llave que sirve para cualquier tuerca, porque dibujaste su plano. Ya sos artífice. —Desde la Encrucijada de los Engranajes sale un camino más, si Bron lo quiere: la Linterna Mágica. | curso |
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

Bron despierta al pie de una cuesta, junto a un vitral apagado, con su llave inglesa cian todavía en la mano. Arriba se ve la **Ciudadela de los Artífices**: torres altísimas, puentes que se pliegan solos y engranajes que giran en todas las paredes. Todos, menos los del portón: una pared entera de engranajes trabados.

Bron se arremanga y los arregla **a mano**, uno por uno. Al engranaje 47, la llave se traba en un diente, Bron hace fuerza, y la llave sale **mellada**. Faltan 153. Desde arriba, un muchacho de traje azul y visor cian lo mira con el mentón apoyado en la mano; baja por una polea, de un salto.

—Soy {mentor}. Ese portón tiene un **plano** —dice, y le muestra una hoja—. Arreglás el plano una vez, y el Taller (el compilador) arregla los doscientos engranajes. Acá no se fabrica cada pieza a mano: se dibuja cómo es, y se construye mil veces.

Bron mira la hoja, mira su llave mellada, y hace la pregunta que va a hacer durante todo el viaje: —¿Y esto para qué me sirve? —Detrás de Tesla, una chica de delantal azul con una lima en la mano se tapa la boca para no reírse.

### Objetivos

Escribir, compilar y ejecutar tu primer programa en C++. Entender qué hace el
compilador, mostrar texto y números con `std::cout` y **leer los mensajes de
error y las advertencias**.

### Antes de empezar

Nada: este es el punto de partida. Para los ejemplos y las micro-misiones alcanza
con este navegador (tocá **Ejecutar**: la primera vez baja el compilador y tarda
un poco). Para las misiones vas a necesitar un entorno de C++ en tu compu: abajo
está cómo instalarlo en Linux y en Windows. El curso usa **C++20**, así que el
compilador tiene que ser `g++` 11 o más nuevo (`g++ --version`).

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

#### Dónde escribir y compilar (Linux y Windows)
Tres caminos; elegí uno y usalo todo el curso (en la rama de Qt se suma Qt Creator).

**1. ZinjaI** (el más simple, pensado para aprender; Linux y Windows). Bajalo de
su página (`zinjai.sourceforge.net`): en Windows trae el compilador adentro; en
Linux, instalá antes `g++` (`sudo apt install build-essential`). Archivo → Nuevo,
escribís y **F9** compila y ejecuta. Para C++20, agregá `-std=c++20` en las
opciones de compilación (si el compilador que trae es viejo y no lo reconoce,
probá `-std=c++2a` o configurale el `g++` de MSYS2).

**2. Code::Blocks** (Linux y Windows). En Windows, bajá el instalador que dice
**mingw-setup**, de la versión **25.03 o más nueva**: trae un `g++` moderno (la
20.03 trae `g++` 8, que no conoce C++20). En Linux: `sudo apt install codeblocks`.
Archivo → Nuevo → Archivo vacío, guardalo como `main.cpp`. En *Settings → Compiler*
tildá la opción de **C++20** (o escribí `-std=c++20` en *Other compiler options*),
y **F9**.

**3. VS Code con `g++` y la terminal.**
- **Linux:** `sudo apt install build-essential` y listo: `g++ --version`.
- **Windows:** instalá **MSYS2** (`msys2.org`), abrí la terminal **MSYS2 UCRT64**
  y escribí `pacman -S mingw-w64-ucrt-x86_64-gcc` (trae `gcc` y `g++`). Agregá
  `C:\msys64\ucrt64\bin` a la variable `Path` de Windows para que `g++` ande en
  cualquier terminal. Probá `g++ --version`.
- En VS Code, la extensión **C/C++** de Microsoft. Se compila desde la terminal
  integrada (Ctrl+ñ):

| | Linux | Windows |
|---|---|---|
| Compilar | `g++ -std=c++20 -Wall -Wextra main.cpp -o programa` | `g++ -std=c++20 -Wall -Wextra main.cpp -o programa.exe` |
| Ejecutar | `./programa` | `programa.exe` (o `.\programa.exe` en PowerShell) |
| Ver el `return` | `echo $?` | `echo %errorlevel%` (cmd) o `$LASTEXITCODE` (PowerShell) |

**Las tildes en la consola de Windows:** si ves `Â¡Hola` en lugar de `¡Hola`,
escribí `chcp 65001` en la consola antes de ejecutar (o, en ZinjaI y
Code::Blocks, configurá la consola en UTF-8). En Linux se ven bien siempre.

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

#### Cómo compilarlo y ejecutarlo

- **Acá mismo:** tocá **Ejecutar** en el ejemplo.
- **ZinjaI o Code::Blocks** (Linux y Windows): abrí el archivo y apretá **F9**.
- **Terminal** (VS Code o la de tu sistema):
  - Linux: `g++ -std=c++20 -Wall -Wextra main.cpp -o programa` y `./programa`
  - Windows: `g++ -std=c++20 -Wall -Wextra main.cpp -o programa.exe` y `programa.exe`

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

### Micro-misión R00-N01-P1 · La primera orden

```meta
lugar: El portón de engranajes
personajes: Bron, Gheco, Tesla
carta: Mostrar texto | std::cout << "texto\n"; · \n salta de línea · cada instrucción termina con ;
recompensa: xp 10, oro 10
```

#### Escena
Bron despierta al pie de la cuesta, junto a un vitral apagado. Arriba, el portón de la Ciudadela es una pared de engranajes trabados. Sobre su hombro aparece un gecko de luz con antiparras: **Gheco**.
—Acá las órdenes se escriben en C++ —le dice—. Antes de arreglar nada, presentate. Por escrito.

#### Gheco sugiere
`std::cout << "…";` muestra el texto entre comillas, y `\n` al final baja a la línea siguiente. Tocá **Ejecutar**: C++ se compila acá mismo, en tu navegador (la primera vez baja el compilador y tarda un poco).

#### Desafío
Completá la instrucción para que Bron se presente.

#### Código inicial
```cpp
#include <iostream>

int main()
{
    ___ << "Soy Bron, mecanico. Arreglo todo a mano.\n";
    return 0;
}
```

#### Salida esperada
```
Soy Bron, mecanico. Arreglo todo a mano.
```

#### Solución
```cpp
#include <iostream>

int main()
{
    std::cout << "Soy Bron, mecanico. Arreglo todo a mano.\n";
    return 0;
}
```

#### Al superarla
El portón no se abre, pero uno de los engranajes gira medio diente, como saludando. Gheco asiente.

#### Imagen
- Al pie de una cuesta, de noche, un vitral apagado y arriba un portón enorme hecho de engranajes de bronce trabados.
- Bron (mecánico grandote de 24 años, pelo castaño corto peinado hacia arriba, remera táctica negra, cinturón de herramientas, rodilleras con luz ámbar, llave inglesa cian al hombro) mira el portón con la llave en la mano.
- Gheco (gecko de luz con antiparras) sobre su hombro.

### Micro-misión R00-N01-P2 · Un slime en el portón

```meta
lugar: El portón de engranajes
personajes: Bron, Gheco
criatura: slime
carta: Error de sintaxis | expected ';' · el compilador no produce nada hasta que se arregla · se lee la PRIMERA línea del error
recompensa: xp 10, oro 10
```

#### Escena
Entre los dientes del portón se asoma un **slime**: una gota de baba verde que se alimenta de los punto y coma olvidados. Bron le escribe una orden al portón, y el Taller ni la mira: devuelve un error.

#### Gheco sugiere
Leé el primer error: dice la línea y que **esperaba** algo (`expected ';'`). Cada instrucción termina con `;`.

#### Desafío
Encontrá lo que falta para que el programa compile.

#### Código inicial
```cpp
#include <iostream>

int main()
{
    std::cout << "Engranaje 1: listo\n"
    std::cout << "Engranaje 2: listo\n";
    return 0;
}
```

#### Salida esperada
```
Engranaje 1: listo
Engranaje 2: listo
```

#### Solución
```cpp
#include <iostream>

int main()
{
    std::cout << "Engranaje 1: listo\n";
    std::cout << "Engranaje 2: listo\n";
    return 0;
}
```

#### Al superarla
El slime se resbala por el portón y desaparece en una grieta. Los dos primeros engranajes giran.

#### Imagen
- Un portón de engranajes de bronce con un slime verde y brillante asomado entre dos dientes.
- Bron (mecánico grandote de 24 años, pelo castaño corto peinado hacia arriba, remera táctica negra, cinturón de herramientas, rodilleras con luz ámbar, llave inglesa cian al hombro) señala la línea del error en una pantalla flotante.
- Gheco (gecko de luz con antiparras) se tapa la nariz.

### Micro-misión R00-N01-P3 · Las cuentas del portón

```meta
lugar: El portón de engranajes
personajes: Bron, Lima
carta: Números | std::cout << 200 - 47; muestra 153 · entre comillas es texto: "200 - 47" se muestra tal cual
recompensa: xp 10, oro 10
```

#### Escena
Bron lleva 47 engranajes arreglados a mano. Una chica de delantal azul, con una lupa de relojero en el ojo y una lima en la mano, se le acerca: **Lima**.
—¿Cuántos te faltan? —Bron escribe la cuenta… y el Taller le muestra la cuenta, no el resultado.

#### Gheco sugiere
Lo que va entre comillas se muestra **tal cual**. Para que C++ haga la cuenta, la cuenta va **afuera** de las comillas, con su propio `<<`.

#### Desafío
Hacé que el programa muestre el resultado de la cuenta.

#### Código inicial
```cpp
#include <iostream>

int main()
{
    std::cout << "Faltan " << "200 - 47" << " engranajes\n";
    return 0;
}
```

#### Salida esperada
```
Faltan 153 engranajes
```

#### Solución
```cpp
#include <iostream>

int main()
{
    std::cout << "Faltan " << 200 - 47 << " engranajes\n";
    return 0;
}
```

#### Al superarla
Ciento cincuenta y tres. Bron suspira. Lima se tapa la boca para no reírse.

#### Imagen
- Frente al portón de engranajes, una pila de engranajes arreglados y una montaña más grande sin arreglar.
- Bron (mecánico grandote de 24 años, pelo castaño corto peinado hacia arriba, remera táctica negra, cinturón de herramientas, rodilleras con luz ámbar, llave inglesa cian al hombro) cuenta con los dedos, agotado.
- Lima (aprendiz de relojera de 16, chiquita, dos rodetes castaños con un lápiz clavado, lupa de relojero en un ojo, delantal azul petróleo, una lima en la mano) lo mira con la lupa puesta, conteniendo la risa.

### Micro-misión R00-N01-P4 · El plano del portón

```meta
lugar: El portón de engranajes
personajes: Bron, Tesla, Lima
carta: Varias líneas | cada \n es un salto · sin \n todo queda en un solo renglón · endl también salta
recompensa: xp 15, oro 15
item: Llave Mellada
```

#### Escena
Al engranaje 47 la llave se traba en un diente, Bron hace fuerza y la llave sale **mellada**. Desde arriba baja por una polea un muchacho de traje azul y visor cian: **Tesla**, el Artífice Mayor.
—El portón tiene un plano —dice, y le muestra una hoja—. Escribilo bien, línea por línea, y el Taller arregla los doscientos de una vez.

#### Gheco sugiere
Cada parte del plano tiene que ir en su renglón: falta el `\n` al final de cada texto.

#### Desafío
Hacé que cada paso del plano salga en su propia línea.

#### Código inicial
```cpp
#include <iostream>

int main()
{
    std::cout << "Plano del porton";
    std::cout << "1. Alinear los 200 engranajes";
    std::cout << "2. Girar la manivela";
    std::cout << "3. Abrir";
    return 0;
}
```

#### Salida esperada
```
Plano del porton
1. Alinear los 200 engranajes
2. Girar la manivela
3. Abrir
```

#### Solución
```cpp
#include <iostream>

int main()
{
    std::cout << "Plano del porton\n";
    std::cout << "1. Alinear los 200 engranajes\n";
    std::cout << "2. Girar la manivela\n";
    std::cout << "3. Abrir\n";
    return 0;
}
```

#### Al superarla
Los doscientos engranajes giran a la vez y el portón se abre con un suspiro de vapor. Bron mira su llave mellada. —¿Y esto para qué me sirve? —pregunta. Tesla sonríe: es la primera vez, y no va a ser la última.

#### Imagen
- El portón de engranajes abriéndose de par en par, con vapor y luz cian saliendo de adentro.
- Tesla (muchacho delgado de pelo negro azulado en punta, visor cian, traje azul ajustado con líneas de luz cian y engranajes de bronce en los hombros) sostiene un plano iluminado.
- Bron (mecánico grandote de 24 años, pelo castaño corto peinado hacia arriba, remera táctica negra, cinturón de herramientas, rodilleras con luz ámbar, llave inglesa cian al hombro) mira su llave inglesa mellada.

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
