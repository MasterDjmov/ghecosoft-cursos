# RAMA R01 · Los Cimientos: los fundamentos

```meta
tipo: tronco
posicion: 1
```

## R01-N01 · Variables, tipos y operadores

```meta
tipo: tema
padre: R00-N01
precio: 10
criatura: goblin
```

### Crónica

El depósito de la Ciudadela es un laberinto de estantes. Cada cajón tiene una etiqueta: "engranajes", "resortes", "planos". Y cada uno es de un tamaño distinto.

—En C++ cada dato vive en un cajón con **nombre y tipo** —te explica {mentor}—. El tipo dice qué cabe adentro. Si metés un número con coma en un cajón de enteros, los goblins se roban los decimales y nadie te avisa.

### Objetivos

Declarar variables del tipo adecuado (`int`, `double`, `bool`, `char`), hacer
cuentas con los operadores, entender la división entera y el resto, declarar
constantes y convertir entre tipos a propósito con `static_cast`.

### Antes de empezar

- Compilar, ejecutar y mostrar con `std::cout` (Clase 0).

### Explicación

#### Variables
Una variable es un **cajón con nombre** en la memoria. En C++ se declara con su
**tipo**, que dice qué se puede guardar:
```cpp
int nivel = 5;        // tipo, nombre, valor inicial
nivel = 6;            // cambiar el valor (sin repetir el tipo)
```
Reglas para los nombres: letras, números y `_`, sin empezar con número, sin
espacios ni tildes. Mayúsculas y minúsculas son distintas (`vida` ≠ `Vida`).
Elegí nombres que digan qué guardan: `vida_maxima` es mejor que `vm`.

#### Los tipos básicos
| Tipo | Guarda | Ejemplo |
|---|---|---|
| `int` | enteros (hasta unos ±2100 millones) | `int torres = 12;` |
| `double` | números con decimales | `double altura = 37.5;` |
| `bool` | `true` o `false` | `bool abierta = true;` |
| `char` | **un** carácter, entre comillas simples | `char sector = 'B';` |

También existen `long long` (enteros enormes), `float` (decimales con menos
precisión) y `unsigned` (sin negativos), que vas a ver cuando hagan falta. Los
textos (`std::string`) llegan en el nodo siguiente.

Los decimales se escriben con **punto**: `37.5`, nunca `37,5`.

**Siempre inicializá** las variables. Una variable declarada sin valor
(`int total;`) tiene **basura**: lo que haya quedado en esa memoria.

#### Inicializar con llaves
También se puede escribir `int torres{12};`. La diferencia: con llaves, el
compilador **no deja** perder datos sin avisar:
```cpp
double d = 3.7;
int a = d;     // compila en silencio: a vale 3 (el goblin se llevó el .7)
int b{d};      // advertencia: "narrowing conversion"
```

#### Constantes
`const` marca un valor que **no puede cambiar**. Si alguien lo intenta, no
compila. Se usan para los números fijos del programa, así no aparecen "números
mágicos" sueltos:
```cpp
const int DIENTES = 24;
```

#### Operadores aritméticos
| Operador | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `+ - *` | suma, resta, multiplicación | `3 * 4` | `12` |
| `/` | división | `7 / 2` | `3` (¡entera!) |
| `%` | resto de la división entera | `7 % 2` | `1` |

**La división entera** es la trampa más común: si los **dos** números son
enteros, el resultado es entero y **se pierde lo que va después de la coma**
(no se redondea: se corta). Si al menos uno tiene decimales, el resultado
también: `7.0 / 2` da `3.5`.

El **resto** (`%`) sirve para mucho: saber si un número es par (`n % 2 == 0`),
dar vueltas (`hora % 24`), separar cifras (`n % 10` es la última).

La precedencia es la de la matemática: primero `* / %`, después `+ -`. Ante la
duda, paréntesis.

#### Modificar una variable
```cpp
torres = torres + 1;   // la forma larga
torres += 5;           // suma 5 (también -=, *=, /=, %=)
torres++;              // suma 1
torres--;              // resta 1
```

#### Convertir de tipo: `static_cast`
Para convertir a propósito se usa `static_cast<tipo>(valor)`:
```cpp
int engranajes = 350, cajas = 8;
double por_caja = static_cast<double>(engranajes) / cajas;   // 43.75
int truncado = static_cast<int>(37.9);                       // 37
```
Convertir a `int` **corta** los decimales (no redondea).

#### Cuánto ocupa y hasta dónde llega
`sizeof(tipo)` dice cuántos bytes ocupa. Un `int` suele ocupar 4 bytes y llegar
hasta 2147483647 (`INT_MAX`, de `<climits>`). Si te pasás, **se desborda**: el
resultado es un número sin sentido, y en C++ ese desborde es *comportamiento
indefinido* (el programa puede hacer cualquier cosa).

> **Si venís de C.** Los tipos y operadores son los mismos. Lo nuevo: `bool`
> es un tipo del lenguaje (sin `#include`), `static_cast` reemplaza al
> `(double) x` de C, y la inicialización con llaves te cuida de perder datos.

### Código de ejemplo

```cpp
/*
 * Variables, tipos y operadores: el deposito de la Ciudadela.
 */
#include <iostream>
#include <climits>   // INT_MAX: el entero mas grande

int main()
{
    // tipo nombre = valor inicial;
    int torres = 12;                 // entero
    double altura = 37.5;            // numero con decimales (metros)
    bool abierta = true;             // verdadero o falso
    char sector = 'B';               // UN caracter, entre comillas simples
    const int DIENTES = 24;          // constante: no se puede cambiar

    std::cout << "Torres: " << torres << ", altura: " << altura << " m\n";
    std::cout << "Sector " << sector << ", abierta: " << abierta << "\n";   // true se ve como 1
    std::cout << std::boolalpha << "Abierta (con boolalpha): " << abierta << "\n";

    // Aritmetica
    std::cout << "\n7 + 2 = " << 7 + 2 << "\n";
    std::cout << "7 / 2 = " << 7 / 2 << "   (entero / entero: se pierde el decimal)\n";
    std::cout << "7 % 2 = " << 7 % 2 << "   (resto de la division)\n";
    std::cout << "7.0 / 2 = " << 7.0 / 2 << "\n";
    std::cout << "2 + 3 * 4 = " << 2 + 3 * 4 << ", (2 + 3) * 4 = " << (2 + 3) * 4 << "\n";

    // Modificar variables
    torres = torres + 1;
    torres += 5;          // lo mismo que torres = torres + 5
    torres++;             // suma 1
    std::cout << "\nTorres despues de construir: " << torres << "\n";

    // Convertir de tipo a proposito: static_cast
    int engranajes = 350;
    int cajas = 8;
    double por_caja = static_cast<double>(engranajes) / cajas;
    std::cout << "Engranajes por caja: " << por_caja << "\n";
    std::cout << "Altura redondeada hacia abajo: " << static_cast<int>(altura) << "\n";

    // Cada tipo ocupa un tamanio y tiene un limite
    std::cout << "\nUn int ocupa " << sizeof(int) << " bytes y llega hasta " << INT_MAX << "\n";
    std::cout << "Un double ocupa " << sizeof(double) << " bytes\n";
    std::cout << "Dientes por engranaje: " << DIENTES << "\n";
    return 0;
}
```

### Salida esperada

```
Torres: 12, altura: 37.5 m
Sector B, abierta: 1
Abierta (con boolalpha): true

7 + 2 = 9
7 / 2 = 3   (entero / entero: se pierde el decimal)
7 % 2 = 1   (resto de la division)
7.0 / 2 = 3.5
2 + 3 * 4 = 14, (2 + 3) * 4 = 20

Torres despues de construir: 19
Engranajes por caja: 43.75
Altura redondeada hacia abajo: 37

Un int ocupa 4 bytes y llega hasta 2147483647
Un double ocupa 8 bytes
Dientes por engranaje: 24
```

### ¿Para qué sirve?

Todo programa guarda datos y hace cuentas: el puntaje de un juego, el saldo de una cuenta, la temperatura de un sensor, el precio con descuento de un producto. Elegir el tipo correcto (entero o con decimales) y conocer la división entera evita errores clásicos, como un promedio que da 3 en vez de 3.5 o un porcentaje que siempre da 0.

### Errores habituales

**Goblin: la división entera.** `int promedio = 7 / 2;` da 3. Y `nota * (9 / 5)`
multiplica por **1**, porque `9 / 5` es 1. Usá `9.0 / 5` o `static_cast<double>`.

**Goblin: perder decimales sin aviso.** `int x = 3.7;` compila y guarda 3. Con
llaves, `g++` avisa:
```
main.cpp:5:10: warning: narrowing conversion of ‘d’ from ‘double’ to ‘int’ [-Wnarrowing]
```

**Ogro: variable sin inicializar.** `int total; total += 5;` suma sobre basura.
Con optimizaciones (`-O1`), `g++` a veces lo ve:
```
main.cpp:4:9: warning: ‘total’ is used uninitialized [-Wuninitialized]
```

**Ogro: desborde.** Un `int` no crece para siempre:
```
main.cpp:1:33: warning: integer overflow in expression of type ‘int’ results in ‘-2147483648’ [-Woverflow]
```
Si necesitás números enormes, usá `long long`.

**Slime: coma en vez de punto.** `double altura = 37,5;` no hace lo que parece.
En C++ los decimales llevan punto.

**Esqueleto: cambiar una constante.**
```
main.cpp:6:13: error: assignment of read-only variable ‘DIENTES’
```

### Misión R01-N01-M1 · El plano de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La base de una torre mide 12.5 por 8 metros. Guardá esas medidas en **constantes**
y mostrá el área, el perímetro y cuántas baldosas de 0.5 × 0.5 m hacen falta para
cubrirla.

#### Criterio de aprobación

- Usa `const double` para las medidas.
- Calcula área, perímetro y baldosas con operadores (no escribe los resultados a mano).

#### Salida esperada

```
Base de la torre: 12.5 x 8 m
Área: 100 m²
Perímetro: 41 m
Baldosas de 0.5 x 0.5: 400
```

#### Solución de referencia

```cpp
// Mision 1 - El plano de la torre: area y perimetro de la base.
#include <iostream>

int main()
{
    const double ANCHO = 12.5;
    const double LARGO = 8.0;
    double area = ANCHO * LARGO;
    double perimetro = 2 * (ANCHO + LARGO);
    std::cout << "Base de la torre: " << ANCHO << " x " << LARGO << " m\n";
    std::cout << "Área: " << area << " m²\n";
    std::cout << "Perímetro: " << perimetro << " m\n";
    std::cout << "Baldosas de 0.5 x 0.5: " << area / (0.5 * 0.5) << "\n";
    return 0;
}
```

### Misión R01-N01-M2 · Repartir engranajes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Hay 1000 engranajes para repartir en partes iguales entre 7 artífices. Mostrá
cuántos le tocan a cada uno (entero), cuántos sobran, el promedio exacto (con
decimales) y una comprobación: `a_cada_uno * artifices + sobran` tiene que dar
1000.

#### Criterio de aprobación

- Usa `/` y `%` con enteros para el reparto.
- Usa `static_cast<double>` para el promedio exacto.
- La comprobación da 1000.

#### Salida esperada

```
A cada artífice: 142
Sobran: 6
Promedio exacto: 142.857
Comprobación: 1000
```

#### Solución de referencia

```cpp
// Mision 2 - Repartir engranajes: division entera y resto.
#include <iostream>

int main()
{
    int engranajes = 1000;
    int artifices = 7;
    int a_cada_uno = engranajes / artifices;
    int sobran = engranajes % artifices;
    std::cout << "A cada artífice: " << a_cada_uno << "\n";
    std::cout << "Sobran: " << sobran << "\n";
    std::cout << "Promedio exacto: " << static_cast<double>(engranajes) / artifices << "\n";
    std::cout << "Comprobación: " << a_cada_uno * artifices + sobran << "\n";
    return 0;
}
```

### Misión R01-N01-M3 · El reloj de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El reloj de la torre cuenta segundos desde la medianoche. Convertí 45296 segundos
a horas, minutos y segundos usando solo `/` y `%`.

#### Criterio de aprobación

- Usa división entera y resto.
- Muestra `45296 segundos son 12 h 34 min 56 s`.

#### Salida esperada

```
45296 segundos son 12 h 34 min 56 s
```

#### Solución de referencia

```cpp
// Mision 3 - El reloj de la torre: segundos a horas, minutos y segundos.
#include <iostream>

int main()
{
    int total = 45296;
    int horas = total / 3600;
    int minutos = total % 3600 / 60;
    int segundos = total % 60;
    std::cout << total << " segundos son " << horas << " h " << minutos << " min " << segundos << " s\n";
    return 0;
}
```

### Encargo R01-N01-E1 · El termómetro del Gremio

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Convertí 23.5 °C a Fahrenheit (`C * 9 / 5 + 32`) y a Kelvin (`C + 273.15`).

Después, para ver al goblin en acción, hacé la cuenta con un **entero** (23) de
dos maneras: `entero * (9 / 5) + 32` (mal: `9 / 5` da 1) y `entero * (9.0 / 5) + 32`
(bien). Mostrá los dos resultados.

#### Criterio de aprobación

- Convierte bien a Fahrenheit y Kelvin.
- Muestra la versión con división entera y la corregida.

#### Salida esperada

```
23.5 °C = 74.3 °F = 296.65 K
Con int y 9 / 5 primero: 55 °F (¡mal!)
Con 9.0 / 5: 73.4 °F (bien)
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Grados Celsius a Fahrenheit y Kelvin.
#include <iostream>

int main()
{
    double celsius = 23.5;
    double fahrenheit = celsius * 9 / 5 + 32;
    double kelvin = celsius + 273.15;
    std::cout << celsius << " °C = " << fahrenheit << " °F = " << kelvin << " K\n";

    int entero = 23;
    std::cout << "Con int y 9 / 5 primero: " << entero * (9 / 5) + 32 << " °F (¡mal!)\n";
    std::cout << "Con 9.0 / 5: " << entero * (9.0 / 5) + 32 << " °F (bien)\n";
    return 0;
}
```

### Prueba del sello

#### ¿Cuánto da `7 / 2`? ¿Y `7 / 2.0`? ¿Por qué?

`3` y `3.5`. Si los dos operandos son enteros, la división es entera y se corta la parte decimal.

#### ¿Para qué sirve `%`? Dá un uso.

Da el resto de la división entera. Por ejemplo, `n % 2 == 0` dice si `n` es par.

#### ¿Qué valor tiene una variable `int` declarada sin inicializar?

Basura: lo que haya quedado en esa memoria. Hay que inicializarla siempre.

#### ¿Qué diferencia hay entre `int a = 3.7;` e `int a{3.7};`?

La primera compila y guarda 3 en silencio; la segunda (con llaves) es una conversión que pierde datos y el compilador avisa.

#### ¿Cómo convertís a propósito un `int` a `double`?

Con `static_cast<double>(valor)`.

### Soluciones (docente)

Nodo nuevo: el capítulo 03 de FullCursos arrancaba suponiendo C; acá se enseña desde cero. Las advertencias de `-Wnarrowing`, `-Wuninitialized` y `-Woverflow` son reales de `g++` 13.

## R01-N02 · Entrada y salida: cin y string

```meta
tipo: tema
padre: R01-N01
precio: 10
criatura: goblin
```

### Crónica

En la puerta de la Ciudadela hay un guardia mecánico con un libro enorme: anota a todos los que entran. Pregunta, escucha y escribe.

—Un programa que no escucha es una caja de música —dice {mentor}—. Linda, pero siempre toca lo mismo. Enseñale a tus planos a **preguntar**, {heroe}.

### Objetivos

Leer datos del teclado con `std::cin`, guardar textos en `std::string`, leer
líneas completas con `std::getline`, detectar una lectura que falló y dar
formato a la salida (columnas y decimales).

### Antes de empezar

- Variables y tipos (Variables, tipos y operadores).

### Explicación

#### `std::cin`: leer del teclado
`std::cin` es la **entrada estándar**: lo que se escribe en la terminal. Con `>>`
("sacar de") guarda lo leído en una variable, y convierte solo al tipo de la
variable:
```cpp
int edad = 0;
std::cin >> edad;                 // espera un número
double precio = 0;
std::string nombre;
std::cin >> nombre >> precio;     // se pueden encadenar: "yerba 2500"
```
`>>` **saltea espacios y Enter** al principio y lee **hasta el próximo espacio**.
Por eso con `std::cin >> nombre` solo se lee **una palabra**.

#### `std::string`: textos que crecen solos
`std::string` (de `<string>`) guarda un texto de cualquier largo:
```cpp
std::string nombre = "Kira";
std::string completo = nombre + " de la Ciudadela";   // + une textos
nombre.size();        // cantidad de caracteres (4)
nombre.empty();       // ¿está vacío?
nombre[0];            // el primer carácter: 'K'
nombre == "Kira";     // comparar textos con ==
```
Ojo con `size()`: cuenta **bytes**, y una letra con tilde o una eñe ocupa 2 en
UTF-8. `"Ñandú".size()` da 7, no 5.

#### `std::getline`: leer la línea entera
Para leer un nombre con espacios o una frase, se usa `std::getline`, que lee
hasta el Enter:
```cpp
std::string frase;
std::getline(std::cin, frase);
```

#### La trampa de mezclar `>>` y `getline`
Después de `std::cin >> edad`, el Enter que escribiste **queda pendiente**. Un
`getline` que venga después lo encuentra y devuelve una línea vacía. La solución
es descartarlo:
```cpp
std::cin >> edad;
std::cin.ignore(10000, '\n');     // tirar todo hasta el Enter (inclusive)
std::getline(std::cin, frase);
```

#### Cuando la lectura falla
Si el programa espera un número y escribís `hola`, la lectura **falla**: la
variable queda en 0 y `cin` queda en estado de error (las lecturas siguientes
tampoco funcionan). Se detecta así:
```cpp
if (!(std::cin >> edad)) {
    std::cout << "Eso no es un número.\n";
    return 1;
}
```
`std::cin >> edad` "vale" verdadero si leyó bien y falso si falló.

#### Formato de la salida (`<iomanip>`)
| Manipulador | Qué hace |
|---|---|
| `std::setw(10)` | el **próximo** valor ocupa 10 lugares (para columnas) |
| `std::left` / `std::right` | alinear a la izquierda o a la derecha |
| `std::fixed << std::setprecision(2)` | siempre 2 decimales: `1234.50` |
| `std::boolalpha` | mostrar `true`/`false` en vez de `1`/`0` |

`setw` vale solo para el valor que sigue; `fixed`, `setprecision` y `left`
quedan puestos hasta que los cambies.

Ojo: `setw` cuenta **bytes**, igual que `size()`. Un texto con tildes o eñes
ocupa un byte más por cada una, y la columna se corre un lugar.

#### Probar un programa con entrada sin escribirla cada vez
En la terminal podés mandarle la entrada desde un archivo:
```bash
./programa < entrada.txt
printf 'Kira\n27\nsin miedo\n' | ./programa
```
Así funcionan las **entradas de ejemplo** de las misiones.

> **Si venís de C.** `std::string` reemplaza a los `char[]`: no hay tamaño fijo
> ni riesgo de desbordar. `std::cin >> x` reemplaza a `scanf` (sin `&` ni `%d`) y
> `std::getline` a `fgets` (sin el `\n` final).

### Código de ejemplo

```cpp
/*
 * Entrada y salida: std::cin, std::string y getline.
 */
#include <iostream>
#include <iomanip>   // std::setw, std::fixed, std::setprecision
#include <string>

int main()
{
    std::string nombre;
    std::cout << "¿Cómo te llamás? ";
    std::cin >> nombre;                       // lee UNA palabra

    int edad = 0;
    std::cout << "¿Edad? ";
    if (!(std::cin >> edad)) {                // si no escribio un numero, la lectura falla
        std::cout << "\nEso no es un número.\n";
        return 1;
    }
    std::cin.ignore(10000, '\n');             // descartar el Enter que quedo pendiente

    std::string frase;
    std::cout << "Escribí tu lema: ";
    std::getline(std::cin, frase);            // lee la linea ENTERA, con espacios
    std::cout << "\n";

    std::cout << "--- ficha ---\n";
    std::cout << "Hola, " << nombre << ". Tenés " << edad << " años.\n";
    std::cout << "Tu nombre tiene " << nombre.size() << " letras.\n";
    std::cout << "Lema: \"" << frase << "\"\n";

    std::string saludo = "Bienvenida, " + nombre + "!";   // + une textos
    std::cout << saludo << "\n";

    // Formato: columnas con setw y decimales fijos con fixed + setprecision
    double precio = 1234.5;
    std::cout << "\n" << std::setw(10) << "Producto" << std::setw(10) << "Precio" << "\n";
    std::cout << std::setw(10) << "Tuerca" << std::setw(10) << std::fixed << std::setprecision(2) << precio << "\n";
    return 0;
}
```

### Entrada de ejemplo

```
Kira
27
un buen plano sirve mil veces
```

### Salida esperada

```
¿Cómo te llamás? ¿Edad? Escribí tu lema: 
--- ficha ---
Hola, Kira. Tenés 27 años.
Tu nombre tiene 4 letras.
Lema: "un buen plano sirve mil veces"
Bienvenida, Kira!

  Producto    Precio
    Tuerca   1234.50
```

### ¿Para qué sirve?

Casi todo programa de consola pregunta algo: un menú, un formulario de alta, una calculadora, un juego por turnos. Y casi todo programa que muestra datos necesita alinearlos en columnas y con decimales fijos: tickets, reportes, tablas de puntajes. Validar la entrada evita que un usuario distraído rompa el programa escribiendo letras donde iba un número.

### Errores habituales

**Ogro: el `getline` que no espera.** Después de `std::cin >> numero`, un
`getline` lee la línea vacía que quedó. Falta `std::cin.ignore(10000, '\n');`.

**Goblin: letras donde iba un número.** `std::cin >> edad` con `hola` falla: la
variable queda en 0 y todas las lecturas siguientes también fallan. Revisá
siempre la lectura con `if (!(std::cin >> edad))`.

**Ogro: `>>` corta en el espacio.** `std::cin >> nombre` con `Kira Vélez` guarda
solo `Kira`; `Vélez` queda esperando para la próxima lectura.

**Esqueleto: falta `#include <string>` o `<iomanip>`.**
```
main.cpp:6:10: error: ‘setw’ is not a member of ‘std’
main.cpp:1:1: note: ‘std::setw’ is defined in header ‘<iomanip>’; did you forget to ‘#include <iomanip>’?
```

**Goblin: comillas simples para un texto.** `'Kira'` no es un texto: las comillas
simples son para **un** carácter. Los textos van entre comillas dobles.

### Misión R01-N02-M1 · El registro de la puerta

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí el **nombre completo** (con espacios) y el **oficio** de quien entra a la
Ciudadela. Mostrá el registro, la cantidad de caracteres del nombre y la inicial.

#### Criterio de aprobación

- Lee líneas completas con `std::getline`.
- Muestra el registro, el largo y la inicial con `nombre[0]`.

#### Entrada de ejemplo

```
Kira Valdez
artífice aprendiz
```

#### Salida esperada

```
Nombre completo: Oficio: 
Registrado: Kira Valdez (artífice aprendiz)
Letras del nombre (con espacios): 11
Inicial: K
```

#### Solución de referencia

```cpp
// Mision 1 - El registro de la puerta: nombre completo y oficio.
#include <iostream>
#include <string>

int main()
{
    std::string nombre;
    std::string oficio;
    std::cout << "Nombre completo: ";
    std::getline(std::cin, nombre);
    std::cout << "Oficio: ";
    std::getline(std::cin, oficio);
    std::cout << "\n";
    std::cout << "Registrado: " << nombre << " (" << oficio << ")\n";
    std::cout << "Letras del nombre (con espacios): " << nombre.size() << "\n";
    std::cout << "Inicial: " << nombre[0] << "\n";
    return 0;
}
```

### Misión R01-N02-M2 · La balanza del mercado

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí un producto (puede tener espacios), su precio y la cantidad. Mostrá la
cuenta con **2 decimales fijos**. Si el precio o la cantidad no son números,
avisá y terminá con `return 1`.

#### Criterio de aprobación

- Lee el producto con `getline` y los números con `>>`.
- Revisa que las lecturas numéricas no fallen.
- Muestra el total con `std::fixed` y `std::setprecision(2)`.

#### Entrada de ejemplo

```
tornillos de bronce
12.5
8
```

#### Salida esperada

```
Producto: Precio: Cantidad: 
8 x tornillos de bronce a $12.50 = $100.00
```

#### Solución de referencia

```cpp
// Mision 2 - La balanza: leer precio y cantidad y mostrar el total con 2 decimales.
#include <iostream>
#include <iomanip>
#include <string>

int main()
{
    std::string producto;
    double precio = 0;
    int cantidad = 0;
    std::cout << "Producto: ";
    std::getline(std::cin, producto);
    std::cout << "Precio: ";
    if (!(std::cin >> precio)) {
        std::cout << "\nPrecio inválido.\n";
        return 1;
    }
    std::cout << "Cantidad: ";
    if (!(std::cin >> cantidad)) {
        std::cout << "\nCantidad inválida.\n";
        return 1;
    }
    std::cout << "\n" << std::fixed << std::setprecision(2);
    std::cout << cantidad << " x " << producto << " a $" << precio << " = $" << precio * cantidad << "\n";
    return 0;
}
```

### Misión R01-N02-M3 · La tabla de materiales

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé tres materiales con su cantidad, todos en una línea (`hierro 40 cobre 15
zinc 7`). Mostrá una tabla: el nombre alineado a la izquierda en 12 lugares y la
cantidad a la derecha en 8. Al final, el total. (Usá nombres sin tildes: `setw` cuenta bytes.)

#### Criterio de aprobación

- Encadena las lecturas con `>>`.
- Alinea con `std::setw`, `std::left` y `std::right`.
- Muestra el total.

#### Entrada de ejemplo

```
hierro 40 cobre 15 zinc 7
```

#### Salida esperada

```
Tres materiales con su cantidad (nombre cantidad): 
Material       Cant.
hierro            40
cobre             15
zinc               7
TOTAL             62
```

#### Solución de referencia

```cpp
// Mision 3 - La tabla de materiales, alineada con setw.
#include <iostream>
#include <iomanip>
#include <string>

int main()
{
    std::string m1, m2, m3;
    int c1 = 0, c2 = 0, c3 = 0;
    std::cout << "Tres materiales con su cantidad (nombre cantidad): ";
    std::cin >> m1 >> c1 >> m2 >> c2 >> m3 >> c3;
    std::cout << "\n";
    std::cout << std::left << std::setw(12) << "Material" << std::right << std::setw(8) << "Cant." << "\n";
    std::cout << std::left << std::setw(12) << m1 << std::right << std::setw(8) << c1 << "\n";
    std::cout << std::left << std::setw(12) << m2 << std::right << std::setw(8) << c2 << "\n";
    std::cout << std::left << std::setw(12) << m3 << std::right << std::setw(8) << c3 << "\n";
    std::cout << std::left << std::setw(12) << "TOTAL" << std::right << std::setw(8) << c1 + c2 + c3 << "\n";
    return 0;
}
```

### Encargo R01-N02-E1 · La deuda del club

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El club del barrio quiere un programa para calcular deudas. Pedí el nombre del
socio (con espacios), la cuota mensual y los meses adeudados. Mostrá la deuda, un
recargo del 10%, el total y cuánto sería cada una de 3 cuotas, todo con 2
decimales.

#### Criterio de aprobación

- Lee el nombre con `getline` y los números con `>>`.
- Calcula deuda, recargo, total y cuotas.
- Muestra 2 decimales fijos.

#### Entrada de ejemplo

```
Ana Gómez
4500
3
```

#### Salida esperada

```
Socio: Cuota mensual: Meses adeudados: 
Socio: Ana Gómez
Deuda: $13500.00
Recargo (10%): $1350.00
Total: $14850.00
En 3 cuotas de: $4950.00
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La cuota del club: total, en cuotas y con recargo.
#include <iostream>
#include <iomanip>
#include <string>

int main()
{
    std::string socio;
    double cuota = 0;
    int meses = 0;
    std::cout << "Socio: ";
    std::getline(std::cin, socio);
    std::cout << "Cuota mensual: ";
    std::cin >> cuota;
    std::cout << "Meses adeudados: ";
    std::cin >> meses;
    std::cout << "\n" << std::fixed << std::setprecision(2);
    double deuda = cuota * meses;
    double recargo = deuda * 0.1;
    std::cout << "Socio: " << socio << "\n";
    std::cout << "Deuda: $" << deuda << "\n";
    std::cout << "Recargo (10%): $" << recargo << "\n";
    std::cout << "Total: $" << deuda + recargo << "\n";
    std::cout << "En 3 cuotas de: $" << (deuda + recargo) / 3 << "\n";
    return 0;
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `std::cin >> s` y `std::getline(std::cin, s)`?

`>>` lee una palabra (corta en el espacio); `getline` lee la línea entera, con espacios.

#### ¿Por qué a veces un `getline` "no espera" y devuelve vacío?

Porque quedó pendiente el Enter de un `>>` anterior. Se descarta con `std::cin.ignore(10000, '\n')`.

#### ¿Cómo sabés si el usuario escribió algo que no era un número?

La lectura falla: `if (!(std::cin >> x))` lo detecta.

#### ¿Cuánto da `std::string("Ñandú").size()`? ¿Por qué no 5?

7: `size()` cuenta bytes, y la Ñ y la ú ocupan 2 bytes cada una en UTF-8.

#### ¿Cómo mostrás siempre 2 decimales?

Con `std::cout << std::fixed << std::setprecision(2)`, de `<iomanip>`.

### Soluciones (docente)

Material original: `03-C++/02-EntradaSalida`, ampliado con validación de la lectura y `<iomanip>`. Las entradas de ejemplo se prueban con `./programa < entrada.txt`.

## R01-N03 · Decisiones

```meta
tipo: tema
padre: R01-N02
precio: 10
criatura: ogro
```

### Crónica

En el patio de la Ciudadela, un autómata de latón espera órdenes frente a tres puertas. No sabe elegir: se queda quieto, zumbando.

—Una máquina que no decide no sirve para nada —dice {mentor}, y le entrega una tarjeta perforada—. Acá está escrito **qué hacer si** pasa una cosa, y **qué hacer si no**. Eso es lo que vas a aprender a escribir, {heroe}.

### Objetivos

Tomar decisiones con `if`, `else if` y `else`; combinar condiciones con `&&`, `||`
y `!`; elegir entre valores fijos con `switch`; y usar el operador ternario para
decisiones cortas.

### Antes de empezar

- Variables, operadores y `std::string` (nodos anteriores).

### Explicación

#### `if`, `else if`, `else`
```cpp
if (energia == 0) {
    std::cout << "Apagado.\n";
} else if (energia < 30) {
    std::cout << "Batería baja.\n";
} else {
    std::cout << "Listo.\n";
}
```
Se evalúan las condiciones **en orden** y se ejecuta **solo el primer bloque**
cuya condición sea verdadera. El `else` final atrapa todo lo demás. Por eso el
orden importa: si pusieras `energia < 30` antes que `energia == 0`, el 0 entraría
en "batería baja".

Usá **siempre llaves**, aunque el bloque tenga una sola línea: evita errores
cuando después agregás otra.

#### Comparar
| Operador | Significa |
|---|---|
| `==` | igual (¡dos signos!) |
| `!=` | distinto |
| `<` `<=` `>` `>=` | menor, menor o igual, mayor, mayor o igual |

Cada comparación da un `bool`: `true` o `false`. Los `std::string` también se
comparan con `==` y `!=`.

#### Combinar condiciones
| Operador | Significa | Verdadero si… |
|---|---|---|
| `&&` | y | **las dos** son verdaderas |
| `\|\|` | o | **al menos una** es verdadera |
| `!` | no | la condición es falsa |

`&&` y `||` son **perezosos**: si con la primera parte ya se sabe el resultado, la
segunda no se evalúa. `b != 0 && a / b > 2` nunca divide por cero.

Un rango se escribe con dos comparaciones: `0 <= x && x <= 100`. **No** existe
`0 <= x <= 100` (compila, pero hace otra cosa).

#### `switch`: elegir entre valores fijos
Cuando comparás **una** variable entera o `char` contra varios valores:
```cpp
switch (orden) {
case 'a':
    std::cout << "avanzar\n";
    break;          // termina el switch
case 'g':
case 'G':           // dos valores, el mismo código
    std::cout << "girar\n";
    break;
default:            // si no coincidió ninguno
    std::cout << "orden desconocida\n";
}
```
Sin `break`, la ejecución **sigue** con el `case` de abajo. `g++` avisa con
`-Wimplicit-fallthrough`. `switch` **no** funciona con `std::string`: para textos
se usa `if`.

#### El operador ternario
Para decisiones cortas que producen un valor:
```cpp
std::cout << (energia >= 30 ? "operativo" : "en reposo");
int precio = es_socio ? 400 : 800;
```
Se lee: "¿condición? entonces esto : si no, esto otro".

> **Si venís de C.** Todo es igual, salvo que en C++ las condiciones son `bool`
> de verdad y los `std::string` se comparan con `==` (en C había que usar
> `strcmp`).

### Código de ejemplo

```cpp
/*
 * Decisiones: if / else, operadores logicos y switch.
 */
#include <iostream>

int main()
{
    int energia = 0;
    std::cout << "Energía del autómata (0 a 100): ";
    std::cin >> energia;
    std::cout << "\n";

    // if / else if / else: se ejecuta SOLO el primer bloque cuya condicion es verdadera
    if (energia < 0 || energia > 100) {
        std::cout << "Valor imposible.\n";
        return 1;
    } else if (energia == 0) {
        std::cout << "Apagado.\n";
    } else if (energia < 30) {
        std::cout << "Batería baja: volvé al taller.\n";
    } else {
        std::cout << "Listo para trabajar.\n";
    }

    // && (y), || (o), ! (no)
    bool de_noche = true;
    if (energia >= 50 && !de_noche) {
        std::cout << "Puede salir a patrullar.\n";
    } else {
        std::cout << "Se queda en la torre.\n";
    }

    // switch: elegir entre valores fijos de un entero o un caracter
    char orden = 'g';
    std::cout << "Orden '" << orden << "': ";
    switch (orden) {
    case 'a':
        std::cout << "avanzar\n";
        break;                 // sin break, sigue con el case de abajo
    case 'g':
    case 'G':                  // varios case pueden compartir el mismo codigo
        std::cout << "girar\n";
        break;
    default:
        std::cout << "orden desconocida\n";
    }

    // Operador ternario: condicion ? si_verdadero : si_falso
    std::cout << "Estado: " << (energia >= 30 ? "operativo" : "en reposo") << "\n";
    return 0;
}
```

### Entrada de ejemplo

```
45
```

### Salida esperada

```
Energía del autómata (0 a 100): 
Listo para trabajar.
Se queda en la torre.
Orden 'g': girar
Estado: operativo
```

### ¿Para qué sirve?

Toda regla de negocio es una decisión: si el cliente es socio, descuento; si el stock baja de 10, avisar; si la contraseña es incorrecta tres veces, bloquear. En un juego, cada colisión, cada tecla y cada condición de victoria es un `if`. Escribir condiciones claras y en el orden correcto es lo que separa un programa que "casi anda" de uno que anda siempre.

### Errores habituales

**Ogro: `=` en vez de `==`.** `if (vida = 0)` **asigna** 0 y la condición es falsa
siempre. `g++` avisa:
```
main.cpp:5:37: warning: suggest parentheses around assignment used as truth value [-Wparentheses]
```

**Ogro: el `break` olvidado.**
```
main.cpp:7:26: warning: this statement may fall through [-Wimplicit-fallthrough=]
```

**Ogro: el `;` después del `if`.** `if (vida > 0);` termina el `if` ahí: el bloque
de abajo se ejecuta **siempre**.
```
main.cpp:5:17: warning: suggest braces around empty body in an ‘if’ statement [-Wempty-body]
```

**Ogro: el orden de los `else if`.** Si la condición más general va primero, las
de abajo nunca se alcanzan. Ordená de la más específica a la más general.

**Ogro: `0 <= x <= 100`.** Compila, pero compara `(0 <= x)` (que da 0 o 1) con
100: siempre es verdadero. Escribí `0 <= x && x <= 100`.

### Misión R01-N03-M1 · La puerta de la torre

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La puerta de la torre se abre solo si tenés **nivel 5 o más** y **llave**. Pedí el
nivel y si tenés llave (`si`/`no`) y mostrá uno de cuatro mensajes: se abre, te
falta la llave, la puerta no reconoce tu nivel (tenés llave pero no nivel), o te
falta todo.

#### Criterio de aprobación

- Combina condiciones con `&&`.
- Cubre los cuatro casos con `if`/`else if`/`else`.

#### Entrada de ejemplo

```
3
si
```

#### Salida esperada

```
Nivel: ¿Tenés llave? (si/no): 
La llave gira, pero la puerta no reconoce a alguien de nivel 3.
```

#### Solución de referencia

```cpp
// Mision 1 - La puerta de la torre: pide nivel y llave.
#include <iostream>
#include <string>

int main()
{
    int nivel = 0;
    std::string llave;
    std::cout << "Nivel: ";
    std::cin >> nivel;
    std::cout << "¿Tenés llave? (si/no): ";
    std::cin >> llave;
    std::cout << "\n";
    bool tiene_llave = (llave == "si");
    if (nivel >= 5 && tiene_llave) {
        std::cout << "La puerta se abre.\n";
    } else if (nivel >= 5) {
        std::cout << "Te falta la llave.\n";
    } else if (tiene_llave) {
        std::cout << "La llave gira, pero la puerta no reconoce a alguien de nivel " << nivel << ".\n";
    } else {
        std::cout << "Volvé cuando seas más fuerte y tengas la llave.\n";
    }
    return 0;
}
```

### Misión R01-N03-M2 · La calculadora del taller

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé una cuenta como `8 * 3` (número, operación, número) y resolvela con un
`switch` sobre la operación: `+`, `-`, `*` (o `x`) y `/`. Si se divide por cero,
avisá. Si la operación no existe, también.

#### Criterio de aprobación

- Usa `switch` con `break` en cada caso.
- Acepta `*` y `x` para multiplicar (dos `case` juntos).
- Evita dividir por cero.

#### Entrada de ejemplo

```
8 / 0
```

#### Salida esperada

```
Cuenta (ej: 8 * 3): 
No se puede dividir por cero.
```

#### Solución de referencia

```cpp
// Mision 2 - La calculadora del taller con switch.
#include <iostream>

int main()
{
    double a = 0, b = 0;
    char op = ' ';
    std::cout << "Cuenta (ej: 8 * 3): ";
    std::cin >> a >> op >> b;
    std::cout << "\n";
    switch (op) {
    case '+':
        std::cout << a << " + " << b << " = " << a + b << "\n";
        break;
    case '-':
        std::cout << a << " - " << b << " = " << a - b << "\n";
        break;
    case '*':
    case 'x':
        std::cout << a << " * " << b << " = " << a * b << "\n";
        break;
    case '/':
        if (b == 0) {
            std::cout << "No se puede dividir por cero.\n";
        } else {
            std::cout << a << " / " << b << " = " << a / b << "\n";
        }
        break;
    default:
        std::cout << "Operación desconocida: " << op << "\n";
    }
    return 0;
}
```

### Misión R01-N03-M3 · El calendario de la Ciudadela

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Un año es **bisiesto** si es divisible por 4 y no por 100, **o** si es divisible
por 400. Pedí un año y decí si es bisiesto y cuántos días tiene febrero, usando el
operador ternario para los dos mensajes.

#### Criterio de aprobación

- Escribe la condición con `%`, `&&` y `||`.
- Usa el operador ternario.
- 1900 no es bisiesto; 2000 y 2024 sí.

#### Entrada de ejemplo

```
1900
```

#### Salida esperada

```
Año: 
1900 no es bisiesto
Febrero tiene 28 días.
```

#### Solución de referencia

```cpp
// Mision 3 - El año bisiesto del calendario de la Ciudadela.
#include <iostream>

int main()
{
    int anio = 0;
    std::cout << "Año: ";
    std::cin >> anio;
    std::cout << "\n";
    bool bisiesto = (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
    std::cout << anio << (bisiesto ? " es bisiesto" : " no es bisiesto") << "\n";
    std::cout << "Febrero tiene " << (bisiesto ? 29 : 28) << " días.\n";
    return 0;
}
```

### Encargo R01-N03-E1 · El boleto del colectivo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El boleto cuesta $800. Menores de 6 viajan gratis; menores de 18 y mayores de 65
pagan $400. Los fines de semana (`sabado` o `domingo`, sin tilde) se descuentan
$100 más, salvo a quien viaja gratis. Pedí edad y día y mostrá el precio.

#### Criterio de aprobación

- Aplica las reglas de edad en el orden correcto.
- Aplica el descuento de fin de semana solo si el boleto no es gratis.

#### Entrada de ejemplo

```
70
domingo
```

#### Salida esperada

```
Edad: Día (lunes..domingo): 
Boleto: $300
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El precio del colectivo segun la edad y el dia.
#include <iostream>
#include <string>

int main()
{
    int edad = 0;
    std::string dia;
    std::cout << "Edad: ";
    std::cin >> edad;
    std::cout << "Día (lunes..domingo): ";
    std::cin >> dia;
    std::cout << "\n";
    int precio = 800;
    if (edad < 6) {
        precio = 0;
    } else if (edad < 18 || edad >= 65) {
        precio = 400;
    }
    if (precio > 0 && (dia == "sabado" || dia == "domingo")) {
        precio -= 100;
    }
    std::cout << "Boleto: $" << precio << "\n";
    return 0;
}
```

### Prueba del sello

#### Con `if / else if / else`, ¿cuántos bloques se pueden ejecutar?

Uno solo: el primero cuya condición sea verdadera (o el `else`).

#### ¿Qué pasa en `if (vida = 0)`?

Asigna 0 a `vida` y la condición es falsa. Se quería `==`.

#### ¿Por qué `b != 0 && a / b > 2` no divide nunca por cero?

Porque `&&` es perezoso: si `b != 0` es falso, no evalúa lo de la derecha.

#### ¿Qué hace un `case` sin `break`?

La ejecución sigue con el código del `case` siguiente.

#### ¿Cómo escribís "x entre 1 y 10"?

`1 <= x && x <= 10`.

### Soluciones (docente)

Nodo nuevo (el capítulo 03 suponía C). Los mensajes de `-Wparentheses`, `-Wimplicit-fallthrough` y `-Wempty-body` son reales de `g++` 13.

## R01-N04 · Bucles

```meta
tipo: tema
padre: R01-N03
precio: 10
criatura: ogro
```

### Crónica

En la sala de máquinas, una rueda enorme gira sin parar. Cada vuelta levanta un balde de agua, lo vuelca y baja a buscar otro.

—La rueda no sabe cuántos baldes faltan —dice {mentor}—. Solo sabe **repetir mientras** el tanque no esté lleno. Si un programa tuviera que escribir cada vuelta a mano, nunca terminaríamos de escribirlo.

### Objetivos

Repetir código con `while`, `do-while` y `for`; salir antes con `break` o saltar
una vuelta con `continue`; acumular y contar dentro de un bucle; anidar bucles; y
recorrer los caracteres de un texto con el `for` de rango.

### Antes de empezar

- Decisiones y condiciones (Decisiones).
- Leer del teclado con `std::cin` (Entrada y salida).

### Explicación

#### `while`: repetir mientras se cumpla
```cpp
while (presion < 100) {
    presion *= 3;
}
```
Antes de cada vuelta se revisa la condición; si es falsa, el bucle termina. Si
es falsa desde el principio, el cuerpo no se ejecuta **nunca**. Adentro tiene que
cambiar algo que haga falsa la condición alguna vez: si no, el bucle es
**infinito** (se corta con Ctrl+C).

#### `for`: contar
Cuando sabés cuántas vueltas hay, `for` junta en una línea las tres partes:
```cpp
for (int i = 1; i <= 5; i++) {    // inicio; condición; paso
    std::cout << i << " ";
}
```
1. **inicio**: se ejecuta una vez (`int i = 1`). Esa `i` existe solo dentro del `for`.
2. **condición**: se revisa antes de cada vuelta.
3. **paso**: se ejecuta después de cada vuelta (`i++`, `i--`, `i += 2`).

La forma más común para recorrer `n` elementos es `for (int i = 0; i < n; i++)`:
empieza en 0 y termina en `n - 1`.

#### `do-while`: al menos una vez
```cpp
do {
    std::cout << "Nivel (1 a 10): ";
    std::cin >> nivel;
} while (nivel < 1 || nivel > 10);
```
La condición se revisa **al final**, así que el cuerpo corre al menos una vez.
Es ideal para pedir un dato hasta que sea válido. (En el ejemplo se agrega
`std::cin &&` para no quedar en un bucle infinito si la lectura falla.)

#### `break` y `continue`
- `break` **sale** del bucle en el acto.
- `continue` **salta** el resto de esta vuelta y pasa a la siguiente.

#### Patrones que vas a usar siempre
- **Contador**: `int cantidad = 0;` antes del bucle, `cantidad++` adentro.
- **Acumulador**: `int suma = 0;` antes, `suma += valor` adentro.
- **Máximo/mínimo**: tomar el primer valor como candidato y reemplazarlo si
  aparece uno mejor.
- **Leer hasta que no haya más**: `while (std::cin >> x)` lee mientras haya
  números; con `&& x != 0` para también frenar en un 0.

#### Bucles anidados
Un bucle dentro de otro: por cada vuelta del de afuera, el de adentro da **todas**
sus vueltas. Sirve para tablas, grillas y dibujos:
```cpp
for (int fila = 1; fila <= 3; fila++) {
    for (int col = 1; col <= 4; col++) {
        std::cout << fila * col << "\t";
    }
    std::cout << "\n";
}
```

#### El `for` de rango
Para recorrer **cada elemento** de algo (por ahora, cada carácter de un texto) sin
manejar índices:
```cpp
for (char c : palabra) {
    // c es cada carácter, uno por vuelta
}
```
Se lee "para cada `c` en `palabra`". Lo vas a usar muchísimo con los vectores.

> **Si venís de C.** `while`, `do-while`, `for`, `break` y `continue` son
> idénticos. El `for` de rango es nuevo.

### Código de ejemplo

```cpp
/*
 * Bucles: while, do-while, for, break y continue.
 */
#include <iostream>
#include <string>

int main()
{
    // while: repetir MIENTRAS la condicion sea verdadera
    int presion = 1;
    int ciclos = 0;
    while (presion < 100) {
        presion *= 3;
        ciclos++;
    }
    std::cout << "La caldera llegó a " << presion << " en " << ciclos << " ciclos.\n";

    // for: contar de un numero a otro (inicio; condicion; paso)
    std::cout << "Cuenta regresiva: ";
    for (int i = 5; i >= 1; i--) {
        std::cout << i << " ";
    }
    std::cout << "¡arranca!\n";

    // Acumular: sumar dentro del bucle
    int total = 0;
    for (int torre = 1; torre <= 4; torre++) {
        total += torre * 10;
    }
    std::cout << "Engranajes en 4 torres (10, 20, 30, 40): " << total << "\n";

    // continue salta a la siguiente vuelta; break sale del bucle
    std::cout << "Impares hasta encontrar un multiplo de 7: ";
    for (int n = 1; n <= 20; n++) {
        if (n % 2 == 0) {
            continue;          // los pares no se muestran
        }
        if (n % 7 == 0) {
            std::cout << "(" << n << ", fin)";
            break;
        }
        std::cout << n << " ";
    }
    std::cout << "\n";

    // Bucles anidados: una tabla
    for (int fila = 1; fila <= 3; fila++) {
        for (int col = 1; col <= 4; col++) {
            std::cout << fila * col << "\t";
        }
        std::cout << "\n";
    }

    // for de rango: recorrer cada caracter de un texto
    std::string palabra = "engranaje";
    int vocales = 0;
    for (char c : palabra) {
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            vocales++;
        }
    }
    std::cout << "\"" << palabra << "\" tiene " << vocales << " vocales.\n";

    // do-while: se ejecuta AL MENOS una vez (ideal para pedir datos)
    int nivel = 0;
    do {
        std::cout << "Nivel (1 a 10): ";
        std::cin >> nivel;
        std::cout << "\n";
    } while (std::cin && (nivel < 1 || nivel > 10));
    std::cout << "Nivel elegido: " << nivel << "\n";
    return 0;
}
```

### Entrada de ejemplo

```
15
4
```

### Salida esperada

```
La caldera llegó a 243 en 5 ciclos.
Cuenta regresiva: 5 4 3 2 1 ¡arranca!
Engranajes en 4 torres (10, 20, 30, 40): 100
Impares hasta encontrar un multiplo de 7: 1 3 5 (7, fin)
1	2	3	4	
2	4	6	8	
3	6	9	12	
"engranaje" tiene 4 vocales.
Nivel (1 a 10): 
Nivel (1 a 10): 
Nivel elegido: 4
```

### ¿Para qué sirve?

Todo lo que se repite es un bucle: recorrer los productos de una factura, procesar las líneas de un archivo, dibujar cada cuadro de un juego, reintentar una conexión, pedir una contraseña hasta que sea correcta. Los patrones de contador, acumulador y máximo están detrás de casi cualquier estadística: promedios de notas, el producto más vendido, la temperatura más alta del mes.

### Errores habituales

**Ogro: el bucle infinito.** Nada dentro del `while` cambia la condición. El
programa se cuelga y hay que cortarlo con Ctrl+C.

**Ogro: el `;` después del `for`.** `for (int i = 0; i < 3; i++);` repite… nada,
tres veces. El bloque de abajo se ejecuta una sola vez.

**Orco: uno de más o uno de menos.** `for (int i = 0; i <= n; i++)` da `n + 1`
vueltas. Para `n` elementos desde 0: `i < n`.

**Ogro: el acumulador sin inicializar.** `int suma;` empieza con basura:
```
main.cpp:4:9: warning: ‘suma’ is used uninitialized [-Wuninitialized]
```

**Ogro: el máximo que empieza en 0.** Si todos los valores son negativos, el
"máximo" queda en 0, que ni siquiera estaba. Empezá con el primer valor leído.

**Goblin: la lectura que falla dentro del bucle.** Si el usuario escribe una
letra, `std::cin >> x` falla y **todas** las lecturas siguientes también: un
`do-while` que pide "hasta que sea válido" queda girando para siempre. Poné la
lectura en la condición (`while (std::cin >> x)`) o revisá `std::cin`.

### Misión R01-N04-M1 · El sensor de la caldera

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé lecturas enteras del sensor hasta que llegue un **0**. Mostrá cuántas hubo, la
suma, el promedio (con decimales), el máximo y el mínimo. Si la primera lectura ya
es 0, mostrá "No hubo lecturas."

#### Criterio de aprobación

- Lee dentro de la condición del `while` y frena en el 0.
- Usa contador, acumulador, máximo y mínimo.
- El máximo y el mínimo arrancan con la primera lectura.

#### Entrada de ejemplo

```
12 -4 30 7 -9 0
```

#### Salida esperada

```
Lecturas (0 para terminar):
Lecturas: 5
Suma: 36
Promedio: 7.2
Máximo: 30, mínimo: -9
```

#### Solución de referencia

```cpp
// Mision 1 - Leer lecturas del sensor hasta el 0: cantidad, suma, promedio, maximo y minimo.
#include <iostream>

int main()
{
    int cantidad = 0;
    int suma = 0;
    int maximo = 0;
    int minimo = 0;
    int valor = 0;
    std::cout << "Lecturas (0 para terminar):\n";
    while (std::cin >> valor && valor != 0) {
        if (cantidad == 0 || valor > maximo) {
            maximo = valor;
        }
        if (cantidad == 0 || valor < minimo) {
            minimo = valor;
        }
        suma += valor;
        cantidad++;
    }
    if (cantidad == 0) {
        std::cout << "No hubo lecturas.\n";
        return 0;
    }
    std::cout << "Lecturas: " << cantidad << "\n";
    std::cout << "Suma: " << suma << "\n";
    std::cout << "Promedio: " << static_cast<double>(suma) / cantidad << "\n";
    std::cout << "Máximo: " << maximo << ", mínimo: " << minimo << "\n";
    return 0;
}
```

### Misión R01-N04-M2 · La pirámide de engranajes

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Pedí la cantidad de pisos y dibujá una pirámide centrada con `o`: el piso 1 tiene
1 engranaje, el 2 tiene 3, el 3 tiene 5… Al final, mostrá cuántos engranajes se
usaron (es `pisos * pisos`).

#### Criterio de aprobación

- Usa bucles anidados: uno para los pisos, otros para espacios y engranajes.
- La pirámide queda centrada.

#### Entrada de ejemplo

```
4
```

#### Salida esperada

```
Pisos: 
   o
  ooo
 ooooo
ooooooo
Engranajes usados: 16
```

#### Solución de referencia

```cpp
// Mision 2 - La piramide de engranajes: bucles anidados.
#include <iostream>

int main()
{
    int pisos = 0;
    std::cout << "Pisos: ";
    std::cin >> pisos;
    std::cout << "\n";
    for (int piso = 1; piso <= pisos; piso++) {
        for (int espacio = 0; espacio < pisos - piso; espacio++) {
            std::cout << " ";
        }
        for (int e = 0; e < 2 * piso - 1; e++) {
            std::cout << "o";
        }
        std::cout << "\n";
    }
    std::cout << "Engranajes usados: " << pisos * pisos << "\n";
    return 0;
}
```

### Misión R01-N04-M3 · El adivino mecánico

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

El adivino piensa el número **37**. Tenés 5 intentos: después de cada uno te dice
"Más alto." o "Más bajo.". Si acertás, el bucle termina antes. Al final, decí si
acertaste o se acabaron los intentos (y cuál era).

#### Criterio de aprobación

- El número secreto y los intentos son constantes.
- El bucle termina al acertar o al agotar los intentos.
- Da una pista después de cada intento fallido.

#### Entrada de ejemplo

```
50
25
37
```

#### Salida esperada

```
Intento 1: 
Más bajo.
Intento 2: 
Más alto.
Intento 3: 
¡Acertaste! Era 37.
```

#### Solución de referencia

```cpp
// Mision 3 - El adivino mecanico: adivinar un numero con pistas, como maximo 5 intentos.
#include <iostream>

int main()
{
    const int SECRETO = 37;
    const int INTENTOS = 5;
    int intento = 0;
    bool acerto = false;
    for (int i = 1; i <= INTENTOS && !acerto; i++) {
        std::cout << "Intento " << i << ": ";
        if (!(std::cin >> intento)) {
            break;
        }
        std::cout << "\n";
        if (intento == SECRETO) {
            acerto = true;
        } else if (intento < SECRETO) {
            std::cout << "Más alto.\n";
        } else {
            std::cout << "Más bajo.\n";
        }
    }
    if (acerto) {
        std::cout << "¡Acertaste! Era " << SECRETO << ".\n";
    } else {
        std::cout << "Se acabaron los intentos. Era " << SECRETO << ".\n";
    }
    return 0;
}
```

### Encargo R01-N04-E1 · La alcancía

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Pedí una meta de ahorro, un depósito mensual y un interés mensual en porcentaje.
Cada mes, el saldo gana el interés y después se suma el depósito. Mostrá el saldo
mes a mes (2 decimales) hasta llegar a la meta, y cuántos meses hicieron falta. Si
el depósito es 0 o negativo, avisá que no se llega nunca.

#### Criterio de aprobación

- Usa un `while` que termina al llegar a la meta.
- Aplica el interés antes de sumar el depósito.
- Evita el bucle infinito cuando el depósito no es positivo.

#### Entrada de ejemplo

```
100000
15000
2
```

#### Salida esperada

```
Meta: Depósito mensual: Interés mensual (%): 
Mes 1: $15000.00
Mes 2: $30300.00
Mes 3: $45906.00
Mes 4: $61824.12
Mes 5: $78060.60
Mes 6: $94621.81
Mes 7: $111514.25
Llegás a la meta en 7 meses.
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El ahorro: cuantos meses hasta llegar a la meta.
#include <iostream>
#include <iomanip>

int main()
{
    double meta = 0, deposito = 0, interes = 0;
    std::cout << "Meta: ";
    std::cin >> meta;
    std::cout << "Depósito mensual: ";
    std::cin >> deposito;
    std::cout << "Interés mensual (%): ";
    std::cin >> interes;
    std::cout << "\n";
    if (deposito <= 0) {
        std::cout << "Con ese depósito no se llega nunca.\n";
        return 1;
    }
    std::cout << std::fixed << std::setprecision(2);
    double saldo = 0;
    int mes = 0;
    while (saldo < meta) {
        mes++;
        saldo = saldo * (1 + interes / 100) + deposito;
        std::cout << "Mes " << mes << ": $" << saldo << "\n";
    }
    std::cout << "Llegás a la meta en " << mes << " meses.\n";
    return 0;
}
```

### Prueba del sello

#### ¿Cuántas veces se ejecuta el cuerpo de un `while` cuya condición es falsa desde el principio? ¿Y el de un `do-while`?

El `while`, ninguna. El `do-while`, una: revisa la condición al final.

#### ¿Qué hace `continue`? ¿Y `break`?

`continue` salta a la siguiente vuelta; `break` sale del bucle.

#### ¿Cuántas vueltas da `for (int i = 0; i < 10; i += 3)`? ¿Qué valores toma `i`?

Cuatro: 0, 3, 6 y 9.

#### ¿Por qué el máximo no debería empezar en 0?

Porque si todos los valores son negativos, el resultado sería 0, que no estaba entre los datos.

#### ¿Qué significa `for (char c : palabra)`?

Para cada carácter `c` de `palabra`, en orden, ejecutar el cuerpo.

### Soluciones (docente)

Nodo nuevo (el capítulo 03 suponía C). El `for` de rango se presenta acá con textos; con vectores vuelve en "Vectores".

## R01-N05 · Funciones

```meta
tipo: tema
padre: R01-N04
precio: 10
criatura: esqueleto
```

### Crónica

En el taller de Tesla hay un cajón con herramientas etiquetadas: "cortar", "doblar", "remachar". Cada una hace **una** cosa, y la hace bien.

—Cuando un plano repite los mismos pasos en diez lugares, está mal dibujado —dice {mentor}—. Esos pasos se guardan en una herramienta con nombre, y después se la llama. Eso es una **función**.

### Objetivos

Escribir funciones que reciben parámetros y devuelven un resultado; declararlas
con un prototipo; entender el alcance de las variables; y usar dos
herramientas de C++: la **sobrecarga** (varias funciones con el mismo nombre) y
los **parámetros por defecto**.

### Antes de empezar

- Decisiones y bucles (nodos anteriores).

### Explicación

#### Anatomía de una función
```cpp
int cuadrado(int x)     // tipo que devuelve, nombre, parámetros
{
    return x * x;       // return: el resultado, y termina la función
}

int area = cuadrado(7);   // llamarla: el 7 se copia en x
```
- Los **parámetros** son variables que se llenan con los valores de la llamada
  (los **argumentos**).
- `return` devuelve el resultado **y termina** la función en ese momento.
- Una función `void` no devuelve nada: solo hace algo (mostrar, modificar).
- Una función que dice devolver `int` **tiene** que llegar a un `return` en todos
  los caminos.

#### Alcance (*scope*)
Las variables declaradas dentro de una función (o de un bloque `{ }`) **existen
solo ahí**: nacen al entrar y desaparecen al salir. Dos funciones pueden tener una
variable `i` cada una sin molestarse. Una función **no ve** las variables de
`main`: lo que necesite, se lo pasás por parámetro.

#### Declarar antes de usar: los prototipos
C++ lee el archivo de arriba hacia abajo. Si `main` llama a una función que está
definida **más abajo**, el compilador todavía no la conoce. La solución es un
**prototipo** arriba: la primera línea de la función, con `;`.
```cpp
bool es_primo(int n);     // prototipo: "existe, se define más adelante"

int main() { ... es_primo(7) ... }

bool es_primo(int n) { ... }    // la definición
```
Así `main` puede quedar arriba, que es lo primero que uno quiere leer.

#### Sobrecarga: el mismo nombre, distintos parámetros
En C++ puede haber varias funciones con **el mismo nombre** si sus parámetros son
distintos (en cantidad o en tipo). El compilador elige según los argumentos:
```cpp
int dano(int base);
int dano(int base, int bonus);
int dano(int base, double multiplicador);

dano(10);        // la primera
dano(10, 5);     // la segunda: 5 es int
dano(10, 1.5);   // la tercera: 1.5 es double
```
Lo que **no** cuenta para distinguirlas es el tipo que devuelven. Si dos versiones
encajan igual de bien con una llamada, es un error de "llamada ambigua".

#### Parámetros por defecto
Un parámetro puede tener un valor que se usa si la llamada no lo pasa:
```cpp
void saludar(const std::string& nombre, const std::string& titulo = "aprendiz");
saludar("Kira");                    // titulo = "aprendiz"
saludar("Tesla", "Artífice Mayor");
```
Los parámetros con valor por defecto van **al final**. Si hay prototipo, el valor
por defecto se escribe **solo en el prototipo**.

(El `const std::string&` del ejemplo es para no copiar el texto: lo explica el
nodo siguiente. Por ahora, leelo como "recibe un texto".)

#### Funciones de la biblioteca: `<cmath>`
Muchas funciones ya vienen hechas. En `<cmath>`: `std::sqrt(x)` (raíz),
`std::pow(b, e)` (potencia), `std::abs(x)`, `std::round(x)`, `std::floor(x)`,
`std::ceil(x)`.

> **Si venís de C.** Las funciones son iguales; lo nuevo es la sobrecarga (en C
> hacían falta `abs`, `fabs`, `labs`…) y los parámetros por defecto.

### Código de ejemplo

```cpp
/*
 * Funciones: definir, llamar, devolver, prototipos, sobrecarga y valores por defecto.
 */
#include <iostream>
#include <string>

// Prototipo: le avisa al compilador que la funcion existe (se define mas abajo).
bool es_primo(int n);

// Una funcion que recibe un valor y devuelve otro.
int cuadrado(int x)
{
    return x * x;
}

// void: no devuelve nada, solo hace algo.
void linea(int largo)
{
    for (int i = 0; i < largo; i++) {
        std::cout << "-";
    }
    std::cout << "\n";
}

// SOBRECARGA: mismo nombre, distintos parametros. El compilador elige cual.
int dano(int base)
{
    return base;
}

int dano(int base, int bonus)
{
    return base + bonus;
}

int dano(int base, double multiplicador)
{
    return static_cast<int>(base * multiplicador);
}

// Parametro POR DEFECTO: si no lo pasan, vale "aprendiz".
void saludar(const std::string& nombre, const std::string& titulo = "aprendiz")
{
    std::cout << "Salud, " << titulo << " " << nombre << ".\n";
}

int main()
{
    std::cout << "cuadrado(7) = " << cuadrado(7) << "\n";
    linea(20);

    std::cout << "dano(10)      = " << dano(10) << "\n";
    std::cout << "dano(10, 5)   = " << dano(10, 5) << "\n";
    std::cout << "dano(10, 1.5) = " << dano(10, 1.5) << "\n";
    linea(20);

    saludar("Kira");                 // usa el valor por defecto
    saludar("Tesla", "Artífice Mayor");
    linea(20);

    std::cout << "Primos hasta 30: ";
    for (int n = 1; n <= 30; n++) {
        if (es_primo(n)) {
            std::cout << n << " ";
        }
    }
    std::cout << "\n";
    return 0;
}

// Definicion de la funcion declarada arriba.
bool es_primo(int n)
{
    if (n < 2) {
        return false;
    }
    for (int d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            return false;          // return termina la funcion en el acto
        }
    }
    return true;
}
```

### Salida esperada

```
cuadrado(7) = 49
--------------------
dano(10)      = 10
dano(10, 5)   = 15
dano(10, 1.5) = 15
--------------------
Salud, aprendiz Kira.
Salud, Artífice Mayor Tesla.
--------------------
Primos hasta 30: 2 3 5 7 11 13 17 19 23 29 
```

### ¿Para qué sirve?

Las funciones son la forma de ordenar cualquier programa que pase de unas decenas de líneas: `calcular_iva`, `validar_dni`, `dibujar_jugador`, `guardar_partida`. Cada una se prueba por separado y se reutiliza. La sobrecarga aparece en todas las bibliotecas de C++: `std::to_string` acepta enteros y decimales, y `std::cout <<` es, en el fondo, una función sobrecargada para cada tipo.

### Errores habituales

**Esqueleto: usar una función antes de declararla.**
```
main.cpp:2:27: error: ‘doble’ was not declared in this scope; did you mean ‘double’?
```
Falta el prototipo arriba, o la función está mal escrita.

**Ogro: un camino sin `return`.**
```
main.cpp:1:68: warning: control reaches end of non-void function [-Wreturn-type]
```
Si ningún `if` se cumple, la función termina sin devolver nada: comportamiento
indefinido.

**Esqueleto: llamada ambigua.** Dos sobrecargas encajan igual de bien:
```
main.cpp:3:25: error: call of overloaded ‘dano(int)’ is ambiguous
main.cpp:1:5: note: candidate: ‘int dano(int, double)’
main.cpp:2:5: note: candidate: ‘int dano(int)’
```
(Una tenía el segundo parámetro por defecto, así que `dano(3)` servía para las dos.)

**Ogro: modificar el parámetro creyendo que cambia el original.** Un parámetro
`int vida` es una **copia**: `vida += 30` dentro de la función no cambia la
variable de `main`. Para eso están las referencias (nodo siguiente).

**Ogro: el `return` adentro del bucle.** En `es_primo`, un `return true` dentro
del `for` terminaría la función en la primera vuelta. El `return true` va
**después** del bucle, cuando ya se probaron todos los divisores.

### Misión R01-N05-M1 · El conversor del puerto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí tres funciones: `metros_a_pies` (× 3.28084), `kilos_a_libras`
(× 2.20462) y `celsius_a_fahrenheit`. Poné `main` **arriba** y las funciones
abajo, con sus prototipos. Mostrá: 12 m, 70 kg, 100 °C y −40 °C convertidos.

#### Criterio de aprobación

- Declara las tres funciones con prototipos antes de `main`.
- Cada función recibe un `double` y devuelve un `double`.

#### Salida esperada

```
12 m = 39.3701 pies
70 kg = 154.323 libras
100 °C = 212 °F
-40 °C = -40 °F
```

#### Solución de referencia

```cpp
// Mision 1 - El conversor de unidades con funciones y prototipos.
#include <iostream>

double metros_a_pies(double metros);
double kilos_a_libras(double kilos);
double celsius_a_fahrenheit(double c);

int main()
{
    std::cout << "12 m = " << metros_a_pies(12) << " pies\n";
    std::cout << "70 kg = " << kilos_a_libras(70) << " libras\n";
    std::cout << "100 °C = " << celsius_a_fahrenheit(100) << " °F\n";
    std::cout << "-40 °C = " << celsius_a_fahrenheit(-40) << " °F\n";
    return 0;
}

double metros_a_pies(double metros)
{
    return metros * 3.28084;
}

double kilos_a_libras(double kilos)
{
    return kilos * 2.20462;
}

double celsius_a_fahrenheit(double c)
{
    return c * 9 / 5 + 32;
}
```

### Misión R01-N05-M2 · El más grande de todos

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí tres versiones sobrecargadas de `maximo`: para dos `int`, para tres `int` y
para dos `double`. La de tres tiene que **reutilizar** la de dos. Probalas con
`(3, 9)`, `(4, 12, 7)` y `(2.5, 1.75)`.

#### Criterio de aprobación

- Hay tres funciones llamadas `maximo`.
- La versión de tres enteros llama a la de dos.

#### Salida esperada

```
maximo(3, 9) = 9
maximo(4, 12, 7) = 12
maximo(2.5, 1.75) = 2.5
```

#### Solución de referencia

```cpp
// Mision 2 - maximo sobrecargado: dos enteros, tres enteros y dos double.
#include <iostream>

int maximo(int a, int b)
{
    return a > b ? a : b;
}

int maximo(int a, int b, int c)
{
    return maximo(maximo(a, b), c);     // reutiliza la version de dos
}

double maximo(double a, double b)
{
    return a > b ? a : b;
}

int main()
{
    std::cout << "maximo(3, 9) = " << maximo(3, 9) << "\n";
    std::cout << "maximo(4, 12, 7) = " << maximo(4, 12, 7) << "\n";
    std::cout << "maximo(2.5, 1.75) = " << maximo(2.5, 1.75) << "\n";
    return 0;
}
```

### Misión R01-N05-M3 · La barra de progreso

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `barra(valor, maximo = 100, ancho = 20, relleno = '#')`, que dibuja una
barra como `[##########..........] 50/100`. Los lugares llenos son
`valor * ancho / maximo`. Si el valor se pasa de los límites, se recorta a 0 o al
máximo. Probala con: `barra(50)`, `barra(30, 40)`, `barra(7, 10, 10)`,
`barra(3, 4, 8, '=')` y `barra(150)`.

#### Criterio de aprobación

- Usa parámetros por defecto para `maximo`, `ancho` y `relleno`.
- Recorta el valor fuera de rango.
- Las cinco barras se ven como en la salida esperada.

#### Salida esperada

```
[##########..........] 50/100
[###############.....] 30/40
[#######...] 7/10
[======..] 3/4
[####################] 100/100
```

#### Solución de referencia

```cpp
// Mision 3 - La barra de progreso con parametros por defecto.
#include <iostream>

void barra(int valor, int maximo = 100, int ancho = 20, char relleno = '#')
{
    if (valor < 0) {
        valor = 0;
    }
    if (valor > maximo) {
        valor = maximo;
    }
    int llenos = valor * ancho / maximo;
    std::cout << "[";
    for (int i = 0; i < ancho; i++) {
        std::cout << (i < llenos ? relleno : '.');
    }
    std::cout << "] " << valor << "/" << maximo << "\n";
}

int main()
{
    barra(50);
    barra(30, 40);
    barra(7, 10, 10);
    barra(3, 4, 8, '=');
    barra(150);
    return 0;
}
```

### Encargo R01-N05-E1 · La cuota del préstamo

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Un banco calcula la cuota fija de un préstamo (sistema francés) con:
`cuota = capital * i * (1 + i)^n / ((1 + i)^n - 1)`, donde `i` es la tasa
**mensual** (la anual / 100 / 12) y `n` la cantidad de cuotas.

Escribí `cuota(capital, tasa_mensual, meses)` (si la tasa es 0, la cuota es
`capital / meses`) y una función `resumen` que muestre las cuotas y el total.
Pedí el capital y la tasa anual y mostrá el resumen para 6, 12 y 24 cuotas.

#### Criterio de aprobación

- Usa `std::pow` de `<cmath>`.
- Separa el cálculo (`cuota`) de la presentación (`resumen`).
- Contempla la tasa 0.

#### Entrada de ejemplo

```
500000
60
```

#### Salida esperada

```
Capital: Tasa anual (%): 
6 cuotas de $98508.73 (total $591052.40)
12 cuotas de $56412.71 (total $676952.46)
24 cuotas de $36235.45 (total $869650.81)
```

#### Solución de referencia

```cpp
// Encargo del Gremio - La cuota de un prestamo (sistema frances) con funciones.
#include <cmath>
#include <iomanip>
#include <iostream>

double cuota(double capital, double tasa_mensual, int meses)
{
    if (tasa_mensual == 0) {
        return capital / meses;
    }
    double factor = std::pow(1 + tasa_mensual, meses);
    return capital * tasa_mensual * factor / (factor - 1);
}

void resumen(double capital, double tasa_anual_pct, int meses)
{
    double c = cuota(capital, tasa_anual_pct / 100 / 12, meses);
    std::cout << meses << " cuotas de $" << c << " (total $" << c * meses << ")\n";
}

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    double capital = 0, tasa = 0;
    std::cout << "Capital: ";
    std::cin >> capital;
    std::cout << "Tasa anual (%): ";
    std::cin >> tasa;
    std::cout << "\n";
    resumen(capital, tasa, 6);
    resumen(capital, tasa, 12);
    resumen(capital, tasa, 24);
    return 0;
}
```

### Prueba del sello

#### ¿Qué pasa con las variables de una función cuando termina?

Dejan de existir: su alcance es la función.

#### ¿Para qué sirve un prototipo?

Para declarar una función antes de usarla, cuando su definición está más abajo en el archivo.

#### ¿Pueden existir `int f(int)` y `int f(double)`? ¿Y `int f(int)` y `double f(int)`?

Las dos primeras sí (distintos parámetros). Las segundas no: solo cambia el tipo que devuelven, y eso no alcanza para distinguirlas.

#### ¿Dónde van los parámetros con valor por defecto?

Al final de la lista. Si hay prototipo, el valor se escribe en el prototipo.

#### Si una función recibe `int vida` y hace `vida = 0`, ¿cambia la variable de quien la llamó?

No: el parámetro es una copia.

### Soluciones (docente)

Material original: `03-C++/04-Funciones` (sobrecarga y valores por defecto), ampliado desde cero con definición, alcance y prototipos.

## R01-N06 · Referencias

```meta
tipo: tema
padre: R01-N05
precio: 10
criatura: troll
```

### Crónica

Tesla te da un plano y te pide que corrijas una medida. La corregís, se lo devolvés… y el plano original, colgado en la pared, sigue con el error.

—Te di una **copia** —sonríe—. Si querés que tu cambio llegue al original, no te tengo que dar una copia: te tengo que dar **el plano mismo**. En C++ eso se llama referencia.

### Objetivos

Entender la diferencia entre pasar por **valor** (copia) y por **referencia**
(`T&`, el original); usar referencias para que una función modifique variables
de afuera o devuelva varios resultados; pasar textos y objetos grandes por
`const T&` para no copiarlos; y dar un primer vistazo a los punteros.

### Antes de empezar

- Funciones y parámetros (Funciones).

### Explicación

#### Por valor: se pasa una copia
```cpp
void curar_copia(int vida) { vida += 30; }
int v = 50;
curar_copia(v);     // v sigue en 50
```
El parámetro `vida` es una variable nueva con una **copia** del valor. La función
trabaja sobre la copia; el original no se entera.

#### Por referencia: se pasa el original
```cpp
void curar(int& vida, int cantidad) { vida += cantidad; }
int v = 50;
curar(v, 30);       // v pasa a 80
```
El `&` después del tipo dice: "`vida` no es una variable nueva, es **otro nombre**
para la variable que me pasen". Todo lo que la función le haga a `vida` le pasa a
`v`. La llamada se escribe igual que siempre.

Una referencia:
- **se ata al nacer** y no se puede re-atar a otra variable;
- **no puede estar vacía**: `int& r;` no compila;
- se usa igual que la variable original (sin símbolos raros).

#### Para qué se usan
1. **Modificar variables de quien llama**: `curar`, `intercambiar(a, b)`.
2. **Devolver más de un resultado**: `bool dividir(int a, int b, int& cociente,
   int& resto)` devuelve si se pudo y además llena dos variables.
3. **No copiar cosas grandes** (siguiente sección).

#### `const T&`: leer sin copiar
Copiar un `int` no cuesta nada, pero copiar un texto largo (o, más adelante, un
vector de mil elementos) sí. Con `const std::string&` la función recibe el
original **sin copiarlo** y el `const` le **prohíbe modificarlo**:
```cpp
void mostrar(const std::string& nombre) { std::cout << nombre; }
```
Regla del curso:
- tipos chicos (`int`, `double`, `bool`, `char`): **por valor**;
- textos, vectores y objetos, si solo se leen: **`const T&`**;
- si la función tiene que modificarlos: **`T&`**.

#### Referencias en el `for` de rango
```cpp
for (char c : grito)  { ... }   // c es una COPIA de cada carácter
for (char& c : grito) { ... }   // c ES cada carácter: cambiarlo cambia el texto
```

#### Una trampa: devolver una referencia a algo local
```cpp
const std::string& nombre() { std::string s = "Kira"; return s; }   // ¡mal!
```
`s` muere al terminar la función; la referencia queda apuntando a nada (una
**referencia colgante**, territorio de trolls). Devolvé por valor: `std::string
nombre()`.

#### Un vistazo a los punteros
Un **puntero** es una variable que guarda una **dirección de memoria**:
```cpp
int engranajes = 7;
int* p = &engranajes;   // &x = "la dirección de x"
*p = 12;                // *p = "lo que hay donde apunta p": engranajes pasa a 12
int* nada = nullptr;    // un puntero PUEDE no apuntar a nada
```
Un puntero se parece a una referencia, pero puede estar vacío (`nullptr`) y puede
cambiar a dónde apunta. En C++ moderno se usan poco "a mano": las referencias
cubren casi todo, y para la memoria dinámica hay punteros inteligentes (los vas a
ver en la rama 3). Por ahora alcanza con reconocerlos: `T*` es un puntero, `&x` da
una dirección, `*p` es lo apuntado, `p->campo` es un campo de lo apuntado.

> **Si venís de C.** En C, para modificar una variable de afuera se pasaba su
> dirección (`curar(&v)` y `p->vida`). En C++ la referencia hace lo mismo sin
> `&` en la llamada ni `*` o `->` adentro, y sin riesgo de un puntero nulo.

### Código de ejemplo

```cpp
/*
 * Referencias: otro nombre para una variable que ya existe.
 * Y un primer vistazo a los punteros.
 */
#include <iostream>
#include <string>

// Por VALOR: la funcion recibe una COPIA. Cambiarla no cambia el original.
void curar_copia(int vida)
{
    vida += 30;
}

// Por REFERENCIA (int&): la funcion trabaja sobre el ORIGINAL.
void curar(int& vida, int cantidad)
{
    vida += cantidad;
}

// El caso clasico: intercambiar dos variables de afuera.
void intercambiar(int& a, int& b)
{
    int tmp = a;
    a = b;
    b = tmp;
}

// const&: se lee el original sin copiarlo y sin poder modificarlo.
void mostrar(const std::string& nombre, int vida)
{
    std::cout << "  " << nombre << ": vida " << vida << "\n";
}

int main()
{
    int vida = 50;
    curar_copia(vida);
    std::cout << "Tras curar_copia: " << vida << " (no cambio)\n";
    curar(vida, 30);
    std::cout << "Tras curar:       " << vida << "\n";

    int x = 1, y = 9;
    intercambiar(x, y);
    std::cout << "x=" << x << " y=" << y << " (intercambiados)\n";

    // Una referencia local es un alias: tocar el alias es tocar el original.
    int& alias = vida;
    alias -= 100;
    std::cout << "Tras alias -= 100: vida = " << vida << "\n";
    mostrar("Kira", vida);

    // for de rango con referencia: modifica cada caracter del texto
    std::string grito = "a la torre";
    for (char& c : grito) {
        if (c >= 'a' && c <= 'z') {
            c = static_cast<char>(c - 'a' + 'A');
        }
    }
    std::cout << grito << "\n";

    // Punteros (vistazo): una variable que guarda una DIRECCION de memoria.
    int engranajes = 7;
    int* p = &engranajes;          // & = "la direccion de"
    *p = 12;                       // * = "lo que hay en esa direccion"
    std::cout << "engranajes = " << engranajes << "\n";
    int* nada = nullptr;           // un puntero puede no apuntar a nada
    std::cout << "¿nada apunta a algo? " << (nada != nullptr ? "si" : "no") << "\n";
    return 0;
}
```

### Salida esperada

```
Tras curar_copia: 50 (no cambio)
Tras curar:       80
x=9 y=1 (intercambiados)
Tras alias -= 100: vida = -20
  Kira: vida -20
A LA TORRE
engranajes = 12
¿nada apunta a algo? no
```

### ¿Para qué sirve?

Las referencias están en todo el C++ profesional: casi todas las funciones reciben sus datos grandes por `const&` para no copiarlos, y las que "devuelven varias cosas" o actualizan un estado (el jugador, la cuenta, el inventario) reciben `&`. En un juego, `mover(Jugador& j)` o `aplicar_gravedad(Particula& p)` trabajan sobre el objeto real, sin copias.

### Errores habituales

**Troll: referencia sin inicializar.**
```
main.cpp:1:19: error: ‘r’ declared as reference but not initialized
```

**Goblin: pasar un número suelto a un `T&`.** Una referencia no constante necesita
una **variable**:
```
main.cpp:2:20: error: cannot bind non-const lvalue reference of type ‘int&’ to an rvalue of type ‘int’
    2 | int main() { curar(5); return 0; }
```
`curar(5)` no tiene sentido: ¿qué variable se curaría?

**Troll: devolver una referencia a una variable local.**
```
main.cpp:2:62: warning: reference to local variable ‘s’ returned [-Wreturn-local-addr]
```

**Ogro: olvidar el `&`.** `void curar(int vida)` compila perfecto… y no cura a
nadie. Si una función "no hace nada", revisá si le falta el `&`.

**Ogro: el `for` de rango sin `&`.** `for (char c : texto) c = 'X';` cambia copias:
el texto queda igual.

**Troll: desreferenciar `nullptr`.** `int* p = nullptr; *p = 3;` hace que el
programa se corte (*Segmentation fault*). Antes de usar un puntero que puede estar
vacío, preguntá `if (p != nullptr)`.

### Misión R01-N06-M1 · Vida con límites

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `recibir_dano(int& vida, int dano)`, que nunca deje la vida bajo 0, y
`curar(int& vida, int cantidad, int maximo)`, que nunca la deje sobre el máximo.
Empezá con 80 de vida (máximo 100): recibí 35 de daño, curá 70 y recibí 250.

#### Criterio de aprobación

- Las dos funciones reciben la vida por referencia.
- La vida se mantiene entre 0 y el máximo.

#### Salida esperada

```
Tras 35 de daño: 45
Tras curar 70: 100
Tras 250 de daño: 0
```

#### Solución de referencia

```cpp
// Mision 1 - recibir_dano y curar por referencia, sin salirse de 0..maximo.
#include <iostream>

void recibir_dano(int& vida, int dano)
{
    vida -= dano;
    if (vida < 0) {
        vida = 0;
    }
}

void curar(int& vida, int cantidad, int maximo)
{
    vida += cantidad;
    if (vida > maximo) {
        vida = maximo;
    }
}

int main()
{
    const int MAXIMO = 100;
    int vida = 80;
    recibir_dano(vida, 35);
    std::cout << "Tras 35 de daño: " << vida << "\n";
    curar(vida, 70, MAXIMO);
    std::cout << "Tras curar 70: " << vida << "\n";
    recibir_dano(vida, 250);
    std::cout << "Tras 250 de daño: " << vida << "\n";
    return 0;
}
```

### Misión R01-N06-M2 · Ordenar tres

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `intercambiar(int& a, int& b)` y, usándola, `ordenar3(int& a, int& b,
int& c)`, que deja las tres variables de menor a mayor. Pedí tres números y
mostralos ordenados.

#### Criterio de aprobación

- `ordenar3` usa `intercambiar`.
- Funciona con cualquier orden de entrada (probá también con repetidos).

#### Entrada de ejemplo

```
42 7 19
```

#### Salida esperada

```
Tres números: 
Ordenados: 7 19 42
```

#### Solución de referencia

```cpp
// Mision 2 - ordenar3: deja tres variables de menor a mayor, usando intercambiar.
#include <iostream>

void intercambiar(int& a, int& b)
{
    int tmp = a;
    a = b;
    b = tmp;
}

void ordenar3(int& a, int& b, int& c)
{
    if (a > b) {
        intercambiar(a, b);
    }
    if (b > c) {
        intercambiar(b, c);
    }
    if (a > b) {
        intercambiar(a, b);
    }
}

int main()
{
    int a = 0, b = 0, c = 0;
    std::cout << "Tres números: ";
    std::cin >> a >> b >> c;
    std::cout << "\n";
    ordenar3(a, b, c);
    std::cout << "Ordenados: " << a << " " << b << " " << c << "\n";
    return 0;
}
```

### Misión R01-N06-M3 · La división con resto

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Escribí `bool dividir(int a, int b, int& cociente, int& resto)`: si `b` es 0,
devuelve `false` y no toca nada; si no, llena cociente y resto y devuelve `true`.
Probala con 47 / 5 y con 10 / 0.

#### Criterio de aprobación

- Devuelve el éxito con `bool` y los resultados por referencia.
- No divide por cero.

#### Salida esperada

```
47 / 5 = 9 resto 2
10 / 0: no se puede
```

#### Solución de referencia

```cpp
// Mision 3 - dividir: devuelve si se pudo, y el cociente y el resto por referencia.
#include <iostream>

bool dividir(int a, int b, int& cociente, int& resto)
{
    if (b == 0) {
        return false;
    }
    cociente = a / b;
    resto = a % b;
    return true;
}

int main()
{
    int cociente = 0, resto = 0;
    if (dividir(47, 5, cociente, resto)) {
        std::cout << "47 / 5 = " << cociente << " resto " << resto << "\n";
    }
    if (!dividir(10, 0, cociente, resto)) {
        std::cout << "10 / 0: no se puede\n";
    }
    return 0;
}
```

### Encargo R01-N06-E1 · Códigos de producto

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

En el depósito, los códigos se cargan de cualquier manera: `ab-12 c9`, `AB12C9`,
`Ab 12-c9`. Escribí `normalizar(std::string& codigo)`, que deja el código en
mayúsculas y sin espacios ni guiones, modificando el texto que recibe. Pedí un
código (con `getline`) y mostralo normalizado con su largo.

#### Criterio de aprobación

- Recibe el texto por referencia y lo modifica.
- Quita espacios y guiones y pasa a mayúsculas.

#### Entrada de ejemplo

```
ab-12 c9 x
```

#### Salida esperada

```
Código: 
Normalizado: AB12C9X (7 caracteres)
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Normalizar codigos de producto: mayusculas y sin espacios.
#include <iostream>
#include <string>

void normalizar(std::string& codigo)
{
    std::string limpio;
    for (char c : codigo) {
        if (c == ' ' || c == '-') {
            continue;
        }
        if (c >= 'a' && c <= 'z') {
            c = static_cast<char>(c - 'a' + 'A');
        }
        limpio += c;
    }
    codigo = limpio;
}

int main()
{
    std::string codigo;
    std::cout << "Código: ";
    std::getline(std::cin, codigo);
    std::cout << "\n";
    normalizar(codigo);
    std::cout << "Normalizado: " << codigo << " (" << codigo.size() << " caracteres)\n";
    return 0;
}
```

### Prueba del sello

#### ¿Qué diferencia hay entre `void f(int x)` y `void f(int& x)`?

La primera recibe una copia; la segunda, el original: los cambios a `x` se ven afuera.

#### ¿Por qué conviene `const std::string&` para un texto que solo se lee?

Porque no copia el texto y el `const` impide modificarlo por error.

#### ¿Por qué no compila `curar(5)` si `curar` recibe `int&`?

Porque una referencia no constante necesita una variable a la que atarse, y `5` no lo es.

#### ¿Qué es una referencia colgante?

Una referencia a algo que ya dejó de existir, como una variable local de una función que ya terminó.

#### ¿Qué hacen `&x` y `*p` con punteros?

`&x` da la dirección de `x`; `*p` es el valor que está en la dirección que guarda `p`.

### Soluciones (docente)

Material original: `03-C++/03-Referencias`, ampliado desde cero. Los punteros se presentan solo como vistazo; se usan en serio con polimorfismo (rama 2) y punteros inteligentes (rama 3).

## R01-N07 · Vectores: listas que crecen

```meta
tipo: tema
padre: R01-N06
precio: 10
criatura: orco
```

### Crónica

En la torre del Reloj, los engranajes están colgados en una cadena: uno detrás del otro, numerados desde cero. Cuando llega uno nuevo, se engancha al final.

—Diez variables para diez engranajes es una locura —dice {mentor}—. Un **vector** los guarda a todos juntos, en orden, y se estira cuando llegan más. Eso sí: el que pide el engranaje número 10 de una cadena de 10… se encuentra con un orco.

### Objetivos

Guardar muchos valores en un `std::vector`: crearlo, agregar y quitar elementos,
acceder por posición, recorrerlo, pasarlo a funciones y usar los algoritmos
básicos de `<algorithm>` (ordenar, buscar, contar, máximo). Armar grillas con
un vector de vectores.

### Antes de empezar

- Bucles y el `for` de rango (Bucles).
- Pasar por `&` y `const&` (Referencias).

### Explicación

#### Crear un vector
`std::vector<T>` (de `<vector>`) es una lista de valores **del mismo tipo**, en
orden, que crece sola:
```cpp
std::vector<int> cargas;                    // vacío
std::vector<int> cargas = {40, 15, 70};     // con valores
std::vector<int> pisos(4, 1);               // 4 elementos, todos en 1
std::vector<std::string> torres = {"Norte", "Reloj"};
```
Entre `< >` va el tipo de los elementos.

#### Acceder y modificar
Los elementos se numeran **desde 0**: en un vector de 5, las posiciones van de 0
a 4.
| Operación | Qué hace |
|---|---|
| `v[i]` | el elemento `i` (sin revisar si existe) |
| `v.at(i)` | el elemento `i`, **revisando**: si no existe, el programa se corta con un error claro |
| `v.front()` / `v.back()` | el primero / el último |
| `v.size()` | cuántos hay |
| `v.empty()` | ¿está vacío? |
| `v.push_back(x)` | agregar `x` al final |
| `v.pop_back()` | quitar el último |
| `v.insert(v.begin() + i, x)` | insertar `x` en la posición `i` |
| `v.erase(v.begin() + i)` | borrar el elemento `i` (los de atrás se corren) |
| `v.clear()` | vaciarlo |

`v.begin()` señala el primer elemento y `v.end()` **el lugar después del último**.
`v.begin() + 2` es la posición 2. (Esas "señales" se llaman **iteradores**; los vas
a conocer a fondo en la rama 4.)

#### Recorrer
```cpp
for (int x : cargas) { ... }             // cada valor (copia)
for (int& x : cargas) { x *= 2; }        // cada valor, para modificarlo
for (std::size_t i = 0; i < cargas.size(); i++) { ... cargas[i] ... }   // con índice
```
El índice se declara `std::size_t` (un entero sin signo) porque `size()` devuelve
ese tipo; con `int`, `g++` avisa que se comparan enteros de distinto signo.

#### Vectores y funciones
Un vector se pasa como cualquier cosa grande:
- solo para leerlo: `const std::vector<int>& v`;
- para modificarlo: `std::vector<int>& v`;
- una función puede **devolver** un vector: `std::vector<int> pares(int n)`.

Y, a diferencia de los arrays de C, un vector se puede **copiar** con `=` y
**comparar** con `==`.

#### Algoritmos de `<algorithm>`
Trabajan sobre un **rango**: de `v.begin()` a `v.end()`.
```cpp
std::sort(v.begin(), v.end());                        // ordenar de menor a mayor
std::reverse(v.begin(), v.end());                     // dar vuelta
std::count(v.begin(), v.end(), 15);                   // cuántas veces aparece 15
*std::max_element(v.begin(), v.end());                // el mayor (ojo: v no vacío)
std::find(v.begin(), v.end(), 55) != v.end();         // ¿está el 55?
```
`find` devuelve dónde está, o `v.end()` si no lo encontró. `max_element` devuelve
**dónde** está el mayor; el `*` de adelante da el valor.

#### Grillas: un vector de vectores
```cpp
std::vector<std::vector<char>> mapa(3, std::vector<char>(5, '.'));   // 3 filas de 5
mapa[1][2] = 'T';     // fila 1, columna 2
```
Es la forma natural de guardar un tablero, un mapa de juego o una planilla.

> **Si venís de C.** `std::vector` reemplaza a los arrays y a todo el
> `malloc`/`realloc`/`free` de un array dinámico: crece solo y se libera solo
> cuando termina su alcance.

### Código de ejemplo

```cpp
/*
 * std::vector: una lista de valores que crece sola.
 */
#include <algorithm>   // std::sort, std::find, std::count, std::max_element
#include <iostream>
#include <string>
#include <vector>

// Recibe el vector por const& : lo lee sin copiarlo.
void mostrar(const std::string& titulo, const std::vector<int>& v)
{
    std::cout << titulo << " (" << v.size() << "):";
    for (int x : v) {
        std::cout << " " << x;
    }
    std::cout << "\n";
}

// Recibe el vector por & : lo modifica.
void duplicar(std::vector<int>& v)
{
    for (int& x : v) {
        x *= 2;
    }
}

int main()
{
    std::vector<int> cargas = {40, 15, 70, 15, 25};   // con valores iniciales
    mostrar("Cargas", cargas);

    cargas.push_back(55);                              // agregar al final
    std::cout << "Primera: " << cargas[0] << ", última: " << cargas.back() << "\n";
    cargas[1] = 18;                                    // cambiar por posicion
    mostrar("Tras agregar y cambiar", cargas);

    cargas.erase(cargas.begin() + 2);                  // borrar la posicion 2 (el 70)
    cargas.insert(cargas.begin(), 5);                  // insertar al principio
    mostrar("Tras borrar e insertar", cargas);

    // Recorrer con indice cuando hace falta la posicion
    for (std::size_t i = 0; i < cargas.size(); i++) {
        if (cargas[i] > 20) {
            std::cout << "  la carga " << i << " pesa " << cargas[i] << "\n";
        }
    }

    // Algoritmos de <algorithm>: trabajan sobre el rango begin()..end()
    std::cout << "Hay " << std::count(cargas.begin(), cargas.end(), 15) << " cargas de 15\n";
    std::cout << "La más pesada: " << *std::max_element(cargas.begin(), cargas.end()) << "\n";
    if (std::find(cargas.begin(), cargas.end(), 55) != cargas.end()) {
        std::cout << "Está la carga de 55\n";
    }
    std::sort(cargas.begin(), cargas.end());
    mostrar("Ordenadas", cargas);

    duplicar(cargas);
    mostrar("Duplicadas", cargas);

    // Un vector de textos, y uno de un tamanio dado
    std::vector<std::string> torres = {"Norte", "Reloj", "Vapor"};
    torres.push_back("Faro");
    std::vector<int> pisos(torres.size(), 1);          // 4 elementos, todos en 1
    pisos[1] = 7;
    for (std::size_t i = 0; i < torres.size(); i++) {
        std::cout << torres[i] << ": " << pisos[i] << " piso(s)\n";
    }

    // Un vector de vectores: una grilla de 3 filas x 5 columnas
    std::vector<std::vector<char>> mapa(3, std::vector<char>(5, '.'));
    mapa[1][2] = 'T';
    for (const std::vector<char>& fila : mapa) {
        for (char c : fila) {
            std::cout << c;
        }
        std::cout << "\n";
    }

    // .at() revisa el indice; [] no.
    std::cout << "cargas.at(0) = " << cargas.at(0) << "\n";
    return 0;
}
```

### Salida esperada

```
Cargas (5): 40 15 70 15 25
Primera: 40, última: 55
Tras agregar y cambiar (6): 40 18 70 15 25 55
Tras borrar e insertar (6): 5 40 18 15 25 55
  la carga 1 pesa 40
  la carga 4 pesa 25
  la carga 5 pesa 55
Hay 1 cargas de 15
La más pesada: 55
Está la carga de 55
Ordenadas (6): 5 15 18 25 40 55
Duplicadas (6): 10 30 36 50 80 110
Norte: 1 piso(s)
Reloj: 7 piso(s)
Vapor: 1 piso(s)
Faro: 1 piso(s)
.....
..T..
.....
cargas.at(0) = 10
```

### ¿Para qué sirve?

Casi todo programa maneja listas: los productos de un carrito, los alumnos de un curso, los enemigos en pantalla, las líneas de un archivo, los puntajes de una tabla. `std::vector` es, por lejos, el contenedor más usado de C++: rápido, simple y seguro. Las grillas de vectores son la base de los mapas de los juegos por casillas y de cualquier planilla.

### Errores habituales

**Orco: fuera de rango con `[]`.** En un vector de 5, `v[5]` no existe. Con `[]`
no hay aviso: se lee memoria ajena (comportamiento indefinido). Con `.at(5)` el
programa se corta y dice por qué:
```
terminate called after throwing an instance of 'std::out_of_range'
  what():  vector::_M_range_check: __n (which is 5) >= this->size() (which is 5)
```

**Orco: `front`, `back` o `max_element` de un vector vacío.** No hay nada que
devolver: comportamiento indefinido. Preguntá antes `if (!v.empty())`.

**Goblin: comparar `int` con `size()`.**
```
main.cpp:2:68: warning: comparison of integer expressions of different signedness: ‘int’ and ‘std::vector<int>::size_type’ {aka ‘long unsigned int’} [-Wsign-compare]
```
Usá `std::size_t` para el índice, o el `for` de rango.

**Ogro: modificar con el `for` de rango sin `&`.** `for (int x : v) x *= 2;` no
cambia el vector.

**Orco: agregar o borrar mientras se recorre con el `for` de rango.**
`push_back` o `erase` dentro de `for (int x : v)` rompe el recorrido. Si necesitás
borrar mientras recorrés, usá índices con cuidado o armá un vector nuevo.

**Troll: pasar un vector por valor sin querer.** `void mostrar(std::vector<int>
v)` copia todo el vector en cada llamada. Para leer, `const std::vector<int>&`.

### Misión R01-N07-M1 · Las notas del curso

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé notas enteras hasta que se termine la entrada (`while (std::cin >> nota)`),
guardando solo las válidas (de 1 a 10). Mostrá cuántas notas válidas hubo, el
promedio, cuántos aprobados (6 o más), las notas ordenadas y la **mediana** (el
elemento del medio de las ordenadas: posición `size() / 2`).

#### Criterio de aprobación

- Guarda las notas en un `std::vector<int>` con `push_back`.
- Descarta las notas fuera de 1 a 10.
- Ordena con `std::sort` y calcula la mediana.

#### Entrada de ejemplo

```
7 4 10 12 6 9 0 3 8
```

#### Salida esperada

```
Notas válidas: 7
Promedio: 6.71429
Aprobados: 5
Ordenadas: 3 4 6 7 8 9 10
Mediana: 7
```

#### Solución de referencia

```cpp
// Mision 1 - Las notas del curso de artifices: leer hasta el final y resumir.
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
    std::vector<int> notas;
    int nota = 0;
    while (std::cin >> nota) {
        if (nota >= 1 && nota <= 10) {
            notas.push_back(nota);
        }
    }
    if (notas.empty()) {
        std::cout << "No hay notas.\n";
        return 0;
    }
    int suma = 0;
    int aprobados = 0;
    for (int n : notas) {
        suma += n;
        if (n >= 6) {
            aprobados++;
        }
    }
    std::sort(notas.begin(), notas.end());
    std::cout << "Notas válidas: " << notas.size() << "\n";
    std::cout << "Promedio: " << static_cast<double>(suma) / notas.size() << "\n";
    std::cout << "Aprobados: " << aprobados << "\n";
    std::cout << "Ordenadas:";
    for (int n : notas) {
        std::cout << " " << n;
    }
    std::cout << "\n";
    std::cout << "Mediana: " << notas[notas.size() / 2] << "\n";
    return 0;
}
```

### Misión R01-N07-M2 · El plano del taller

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La primera línea trae las filas, las columnas y la cantidad de piezas del plano.
Cada pieza viene como `fila columna letra`. Armá una grilla con
`std::vector<std::vector<char>>` llena de `.` y colocá cada pieza. Si una pieza
cae fuera del plano o en una casilla ocupada, avisá y no la coloques. Al final,
dibujá el plano con una función que lo reciba por `const&` y mostrá cuántas
piezas se colocaron.

#### Criterio de aprobación

- Usa un vector de vectores para la grilla.
- Valida los límites y las casillas ocupadas.
- Dibuja con una función que recibe el plano por `const&`.

#### Entrada de ejemplo

```
4 6 5
0 0 T
1 3 G
1 3 R
5 2 X
3 5 R
```

#### Salida esperada

```
Ocupado: 1,3
Fuera del plano: 5,2
T.....
...G..
......
.....R
Piezas colocadas: 3
```

#### Solución de referencia

```cpp
// Mision 2 - El plano del taller: una grilla con vector<vector<char>>.
#include <iostream>
#include <vector>

void dibujar(const std::vector<std::vector<char>>& plano)
{
    for (const std::vector<char>& fila : plano) {
        for (char c : fila) {
            std::cout << c;
        }
        std::cout << "\n";
    }
}

int main()
{
    int filas = 0, columnas = 0, piezas = 0;
    std::cin >> filas >> columnas >> piezas;
    std::vector<std::vector<char>> plano(filas, std::vector<char>(columnas, '.'));
    int colocadas = 0;
    for (int i = 0; i < piezas; i++) {
        int f = 0, c = 0;
        char tipo = ' ';
        std::cin >> f >> c >> tipo;
        if (f < 0 || f >= filas || c < 0 || c >= columnas) {
            std::cout << "Fuera del plano: " << f << "," << c << "\n";
        } else if (plano[f][c] != '.') {
            std::cout << "Ocupado: " << f << "," << c << "\n";
        } else {
            plano[f][c] = tipo;
            colocadas++;
        }
    }
    dibujar(plano);
    std::cout << "Piezas colocadas: " << colocadas << "\n";
    return 0;
}
```

### Misión R01-N07-M3 · La fila del taller

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Empezá con la fila `Bron Lyn Kira Lyn Oto`. Mostrala después de cada paso:
1. Tesla se cuela en la **segunda** posición (`insert`).
2. Se atiende al primero: mostrá su nombre y quitalo (`erase`).
3. Se quitan los nombres repetidos, quedándose con la primera aparición (armá un
   vector nuevo y usá `std::find` para saber si ya estaba).

Al final, mostrá cuántos quedan y quién es el último.

#### Criterio de aprobación

- Usa `insert` y `erase` con `begin() + posición`.
- Quita los repetidos con `std::find`.
- Muestra la fila con una función que recibe `const std::vector<std::string>&`.

#### Salida esperada

```
Fila: Bron Lyn Kira Lyn Oto
Fila: Bron Tesla Lyn Kira Lyn Oto
Atendido: Bron
Fila: Tesla Lyn Kira Lyn Oto
Fila: Tesla Lyn Kira Oto
Quedan 4, el último es Oto
```

#### Solución de referencia

```cpp
// Mision 3 - La fila del taller: insertar, atender y quitar repetidos.
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

void mostrar(const std::vector<std::string>& fila)
{
    std::cout << "Fila:";
    for (const std::string& nombre : fila) {
        std::cout << " " << nombre;
    }
    std::cout << "\n";
}

int main()
{
    std::vector<std::string> fila = {"Bron", "Lyn", "Kira", "Lyn", "Oto"};
    mostrar(fila);

    fila.insert(fila.begin() + 1, "Tesla");          // Tesla se cuela segunda
    mostrar(fila);

    std::cout << "Atendido: " << fila.front() << "\n";
    fila.erase(fila.begin());                        // atender al primero
    mostrar(fila);

    // quitar los repetidos, quedandose con la primera aparicion
    std::vector<std::string> sin_repetir;
    for (const std::string& nombre : fila) {
        if (std::find(sin_repetir.begin(), sin_repetir.end(), nombre) == sin_repetir.end()) {
            sin_repetir.push_back(nombre);
        }
    }
    fila = sin_repetir;
    mostrar(fila);
    std::cout << "Quedan " << fila.size() << ", el último es " << fila.back() << "\n";
    return 0;
}
```

### Encargo R01-N07-E1 · Las ventas de la semana

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

Leé las ventas de los 7 días de la semana (de lunes a domingo). Guardá los nombres
de los días en un vector constante. Mostrá el total, el promedio, el mejor día (con
su venta) y los días que vendieron **más que el promedio**. Si faltan datos, avisá
y terminá con `return 1`.

#### Criterio de aprobación

- Usa un vector para las ventas y otro, constante, para los nombres.
- Encuentra el mejor día por su posición.
- Lista los días sobre el promedio.

#### Entrada de ejemplo

```
12000 9500 15000 11000 22000 30500 8000
```

#### Salida esperada

```
Total: $108000
Promedio: $15428.6
Mejor día: sábado ($30500)
Sobre el promedio: viernes sábado
```

#### Solución de referencia

```cpp
// Encargo del Gremio - Las ventas de la semana: el mejor dia y los dias sobre el promedio.
#include <iostream>
#include <string>
#include <vector>

int main()
{
    const std::vector<std::string> DIAS = {"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"};
    std::vector<double> ventas;
    double v = 0;
    for (std::size_t i = 0; i < DIAS.size() && std::cin >> v; i++) {
        ventas.push_back(v);
    }
    if (ventas.size() != DIAS.size()) {
        std::cout << "Faltan ventas: hacen falta 7.\n";
        return 1;
    }
    double total = 0;
    std::size_t mejor = 0;
    for (std::size_t i = 0; i < ventas.size(); i++) {
        total += ventas[i];
        if (ventas[i] > ventas[mejor]) {
            mejor = i;
        }
    }
    double promedio = total / ventas.size();
    std::cout << "Total: $" << total << "\n";
    std::cout << "Promedio: $" << promedio << "\n";
    std::cout << "Mejor día: " << DIAS[mejor] << " ($" << ventas[mejor] << ")\n";
    std::cout << "Sobre el promedio:";
    for (std::size_t i = 0; i < ventas.size(); i++) {
        if (ventas[i] > promedio) {
            std::cout << " " << DIAS[i];
        }
    }
    std::cout << "\n";
    return 0;
}
```

### Prueba del sello

#### En un vector de 8 elementos, ¿cuál es la primera posición y cuál la última?

La 0 y la 7.

#### ¿Qué diferencia hay entre `v[i]` y `v.at(i)`?

`at` revisa que la posición exista y, si no, corta el programa con un error claro; `[]` no revisa.

#### ¿Qué devuelve `std::find` si no encuentra el valor?

`v.end()`, la posición después del último.

#### ¿Cómo recibe una función un vector que solo va a leer? ¿Y uno que va a modificar?

`const std::vector<T>&` para leer; `std::vector<T>&` para modificar.

#### ¿Cómo se crea una grilla de 3 filas por 5 columnas de `.`?

`std::vector<std::vector<char>> g(3, std::vector<char>(5, '.'));`

### Soluciones (docente)

Material original: `03-C++/11-Vector`, rehecho desde cero. El idioma remove-erase y `sort` con lambda quedan para la rama 3 (lambdas) y la rama 4 (algoritmos).

## R01-N08 · Azar y matemáticas

```meta
tipo: tema
padre: R01-N07
precio: 10
criatura: goblin
```

### Crónica

En la plaza de la Ciudadela hay una máquina de feria: una rueda con números, una palanca y un cartel que dice "Probá tu suerte". Tesla la desarmó una vez.

—No es suerte —te dice—: es un mecanismo que **parece** al azar. Con la misma posición inicial, la rueda da siempre la misma secuencia. Para un juego, eso es una ventaja: podés repetir exactamente una partida.

### Objetivos

Generar números al azar con `<random>` (un generador con semilla y una
distribución), entender por qué una semilla fija da siempre lo mismo, y usar las
funciones matemáticas de `<cmath>` y `<algorithm>` (`sqrt`, `pow`, `hypot`,
`round`, `clamp`, `min`, `max`).

### Antes de empezar

- Funciones y referencias (nodos anteriores).
- Vectores (Vectores: listas que crecen).

### Explicación

#### Números al azar: generador + distribución
En C++ moderno el azar tiene dos piezas (las dos en `<random>`):
1. Un **generador**: una máquina que produce números "al azar" a partir de una
   **semilla**. El más usado es `std::mt19937` (Mersenne Twister).
2. Una **distribución**: convierte esos números en lo que necesitás.
```cpp
std::mt19937 gen(2026);                                // generador con semilla 2026
std::uniform_int_distribution<int> dado(1, 6);         // enteros de 1 a 6, todos igual de probables
int tirada = dado(gen);                                // una tirada
std::uniform_real_distribution<double> azar(0.0, 1.0); // decimales entre 0 y 1
if (azar(gen) < 0.25) { /* pasa el 25% de las veces */ }
```

#### La semilla
Los números no son realmente al azar: son **pseudoaleatorios**. Con la misma
semilla, el generador da **siempre la misma secuencia**. Eso sirve para:
- **probar**: si algo falla, repetís la misma partida;
- **reproducir**: los juegos con "semilla del mundo" (como Minecraft) generan el
  mismo mapa con la misma semilla.

Para que cada ejecución sea distinta, la semilla sale de `std::random_device`:
```cpp
std::random_device rd;
std::mt19937 gen(rd());
```
En las misiones del curso la semilla **se lee de la entrada**, así el resultado es
comprobable. (Las distribuciones pueden dar números distintos con otra biblioteca:
las salidas esperadas son las de `g++` en Linux. Con `clang` en macOS pueden
variar, y eso no es un error tuyo.)

Creá el generador **una sola vez** y pasalo por referencia (`std::mt19937& gen`)
a las funciones que lo usen. Si lo creás de nuevo en cada llamada con la misma
semilla, vas a sacar siempre el mismo número.

#### Mezclar: `std::shuffle`
`std::shuffle(v.begin(), v.end(), gen)` mezcla un vector al azar, como un mazo de
cartas. Para sacar números **sin repetir**, se mezcla y se toman los primeros.

#### Matemática: `<cmath>`
| Función | Qué hace |
|---|---|
| `std::sqrt(x)` | raíz cuadrada |
| `std::pow(b, e)` | b elevado a e |
| `std::hypot(dx, dy)` | distancia: la raíz de `dx² + dy²` |
| `std::abs(x)` | valor absoluto |
| `std::round(x)` / `std::floor(x)` / `std::ceil(x)` | redondear / hacia abajo / hacia arriba |
| `std::sin`, `std::cos`, `std::atan2` | trigonometría (en radianes) |

Y en `<numbers>` (C++20), las constantes: `std::numbers::pi`.

#### Límites: `<algorithm>`
```cpp
std::min(a, b);          // el menor
std::max(a, b);          // el mayor
std::clamp(x, 0, 100);   // x, pero sin salir de 0..100
```
`clamp` reemplaza los dos `if` de "no bajar de 0 ni pasar del máximo".

> **Si venís de C.** `rand() % 6 + 1` y `srand(time(NULL))` funcionan, pero dan
> números peor repartidos. `<random>` es la forma moderna.

### Código de ejemplo

```cpp
/*
 * Azar con <random> y matematica con <cmath>.
 */
#include <algorithm>   // std::clamp, std::min, std::max
#include <cmath>       // std::sqrt, std::pow, std::hypot, std::round
#include <iostream>
#include <numbers>     // std::numbers::pi (C++20)
#include <random>      // std::mt19937, distribuciones

int main()
{
    // Un generador con SEMILLA fija: da siempre la misma secuencia.
    // (Para un juego de verdad, la semilla sale de std::random_device.)
    std::mt19937 gen(2026);
    std::uniform_int_distribution<int> dado(1, 6);       // enteros de 1 a 6, parejos
    std::uniform_real_distribution<double> azar(0.0, 1.0);

    std::cout << "Cinco tiradas:";
    for (int i = 0; i < 5; i++) {
        std::cout << " " << dado(gen);
    }
    std::cout << "\n";

    // Un golpe critico con 25% de probabilidad
    int criticos = 0;
    for (int i = 0; i < 1000; i++) {
        if (azar(gen) < 0.25) {
            criticos++;
        }
    }
    std::cout << "Críticos en 1000 golpes: " << criticos << " (cerca de 250)\n";

    // Matematica
    double dx = 3.0, dy = 4.0;
    std::cout << "\nDistancia (3, 4): " << std::hypot(dx, dy) << "\n";
    std::cout << "Raíz de 2: " << std::sqrt(2.0) << "\n";
    std::cout << "2 a la 10: " << std::pow(2, 10) << "\n";
    std::cout << "Redondeo de 2.5: " << std::round(2.5) << "\n";
    double radio = 1.5;
    std::cout << "Área de un engranaje de radio 1.5: " << std::numbers::pi * radio * radio << "\n";

    // Limitar un valor a un rango
    int vida = 130;
    std::cout << "\nclamp(130, 0, 100) = " << std::clamp(vida, 0, 100) << "\n";
    std::cout << "min(7, 3) = " << std::min(7, 3) << ", max(7, 3) = " << std::max(7, 3) << "\n";
    return 0;
}
```

### Salida esperada

```
Cinco tiradas: 2 5 3 6 6
Críticos en 1000 golpes: 239 (cerca de 250)

Distancia (3, 4): 5
Raíz de 2: 1.41421
2 a la 10: 1024
Redondeo de 2.5: 3
Área de un engranaje de radio 1.5: 7.06858

clamp(130, 0, 100) = 100
min(7, 3) = 3, max(7, 3) = 7
```

### ¿Para qué sirve?

El azar está en todos los juegos (dados, botines, enemigos que aparecen, mapas generados), pero también en simulaciones científicas, en pruebas de software (generar miles de datos de prueba), en sorteos y en muestreos estadísticos. La matemática de `<cmath>` aparece en cualquier cosa con geometría: distancias en un mapa, ángulos de un disparo, física de un juego, cálculos financieros.

### Errores habituales

**Ogro: crear el generador en cada llamada.**
```cpp
int tirar() { std::mt19937 gen(42); std::uniform_int_distribution<int> d(1, 6); return d(gen); }
```
Devuelve **siempre** el mismo número: el generador arranca de cero cada vez. Crealo
una vez y pasalo por referencia.

**Ogro: pasar el generador por valor.** `void tirar(std::mt19937 gen)` usa una
**copia**: el original no avanza y la próxima tirada repite la misma secuencia.
Usá `std::mt19937& gen`.

**Goblin: `std::pow` con enteros grandes.** `std::pow` devuelve `double`: guardar
`std::pow(10, 20)` en un `int` pierde todo. Para potencias enteras chicas, un bucle.

**Goblin: `std::abs` de `<cstdlib>` vs `<cmath>`.** Sin `#include <cmath>`,
`std::abs(-2.5)` puede elegir la versión entera y dar 2. Incluí `<cmath>`.

**Esqueleto: `std::numbers::pi` sin C++20.** Compilando con `-std=c++17`:
```
main.cpp:5:24: error: ‘std::numbers’ has not been declared
```

### Misión R01-N08-M1 · La mesa de dados

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé una semilla y tirá **dos dados** 1200 veces. Contá cuántas veces salió cada suma
(de 2 a 12) en un `std::vector<int> veces(13, 0)` y dibujá un histograma: una `*`
cada 10 veces, y el número exacto al final. Alineá las sumas de un dígito con un
espacio adelante. Al final, mostrá la suma más común.

#### Criterio de aprobación

- Usa `std::mt19937` con la semilla leída y `std::uniform_int_distribution<int>(1, 6)`.
- Cuenta en un vector indexado por la suma.
- Dibuja el histograma y encuentra la suma más común (tiene que ser 7 o muy cerca).

#### Entrada de ejemplo

```
2026
```

#### Salida esperada

```
 2: **** 40
 3: ***** 54
 4: ********* 95
 5: ************ 126
 6: ************** 145
 7: ********************* 210
 8: ***************** 174
 9: ************* 135
10: ********** 104
11: ******* 77
12: **** 40
La suma más común: 7
```

#### Solución de referencia

```cpp
// Mision 1 - La mesa de dados: 1200 tiradas de dos dados y el histograma de sumas.
#include <iostream>
#include <random>
#include <vector>

int main()
{
    unsigned semilla = 0;
    std::cin >> semilla;
    std::mt19937 gen(semilla);
    std::uniform_int_distribution<int> dado(1, 6);
    std::vector<int> veces(13, 0);          // posiciones 0..12; se usan 2..12
    for (int i = 0; i < 1200; i++) {
        veces[dado(gen) + dado(gen)]++;
    }
    int mas_comun = 2;
    for (int suma = 2; suma <= 12; suma++) {
        std::cout << (suma < 10 ? " " : "") << suma << ": ";
        for (int j = 0; j < veces[suma] / 10; j++) {
            std::cout << "*";
        }
        std::cout << " " << veces[suma] << "\n";
        if (veces[suma] > veces[mas_comun]) {
            mas_comun = suma;
        }
    }
    std::cout << "La suma más común: " << mas_comun << "\n";
    return 0;
}
```

### Misión R01-N08-M2 · Distancias entre torres

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

La primera línea trae la posición del taller (`x y`) y la cantidad de torres. Cada
torre viene como `nombre x y`. Mostrá la distancia de cada torre al taller con 2
decimales (usá `std::hypot`) y cuál es la más cercana.

#### Criterio de aprobación

- Calcula la distancia con `std::hypot`.
- Guarda nombres y distancias en vectores.
- Muestra la más cercana.

#### Entrada de ejemplo

```
10 10 4
Norte 10 25
Reloj 4 2
Vapor 13 14
Faro -5 10
```

#### Salida esperada

```
Norte: 15.00
Reloj: 10.00
Vapor: 5.00
Faro: 15.00
La más cercana: Vapor
```

#### Solución de referencia

```cpp
// Mision 2 - Distancias entre torres: la mas cercana al taller.
#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

int main()
{
    double tx = 0, ty = 0;
    int n = 0;
    std::cin >> tx >> ty >> n;
    std::vector<std::string> nombres;
    std::vector<double> distancias;
    for (int i = 0; i < n; i++) {
        std::string nombre;
        double x = 0, y = 0;
        std::cin >> nombre >> x >> y;
        nombres.push_back(nombre);
        distancias.push_back(std::hypot(x - tx, y - ty));
    }
    std::cout << std::fixed << std::setprecision(2);
    std::size_t cerca = 0;
    for (std::size_t i = 0; i < nombres.size(); i++) {
        std::cout << nombres[i] << ": " << distancias[i] << "\n";
        if (distancias[i] < distancias[cerca]) {
            cerca = i;
        }
    }
    if (!nombres.empty()) {
        std::cout << "La más cercana: " << nombres[cerca] << "\n";
    }
    return 0;
}
```

### Misión R01-N08-M3 · Los cofres de la Ciudadela

```meta
entrega: codigo
entorno: local
monedas: 4
xp: 10
```

#### Consigna

Leé una semilla y abrí 10 cofres. Cada cofre tira un número de 1 a 100: hasta 60 es
**común**, hasta 90 **raro** y más de 90 **épico**. Escribí
`std::string abrir_cofre(std::mt19937& gen)` y mostrá cada cofre y el recuento.

#### Criterio de aprobación

- El generador se crea una vez en `main` y se pasa por referencia.
- Las probabilidades salen de una sola tirada de 1 a 100.
- Muestra el recuento de cada tipo.

#### Entrada de ejemplo

```
7
```

#### Salida esperada

```
Cofre 1: común
Cofre 2: común
Cofre 3: raro
Cofre 4: común
Cofre 5: común
Cofre 6: épico
Cofre 7: raro
Cofre 8: común
Cofre 9: épico
Cofre 10: común
Comunes 6, raros 2, épicos 2
```

#### Solución de referencia

```cpp
// Mision 3 - Los cofres de la Ciudadela: botin con probabilidades.
#include <iostream>
#include <random>
#include <string>

std::string abrir_cofre(std::mt19937& gen)
{
    std::uniform_int_distribution<int> tirada(1, 100);
    int t = tirada(gen);
    if (t <= 60) {
        return "común";
    } else if (t <= 90) {
        return "raro";
    }
    return "épico";
}

int main()
{
    unsigned semilla = 0;
    std::cin >> semilla;
    std::mt19937 gen(semilla);
    int comunes = 0, raros = 0, epicos = 0;
    for (int i = 1; i <= 10; i++) {
        std::string botin = abrir_cofre(gen);
        std::cout << "Cofre " << i << ": " << botin << "\n";
        if (botin == "común") {
            comunes++;
        } else if (botin == "raro") {
            raros++;
        } else {
            epicos++;
        }
    }
    std::cout << "Comunes " << comunes << ", raros " << raros << ", épicos " << epicos << "\n";
    return 0;
}
```

### Encargo R01-N08-E1 · La rifa del club

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 15
```

#### Consigna

El club sortea 5 números **distintos** del 1 al 50. Leé una semilla, cargá un
vector con los números del 1 al 50, mezclalo con `std::shuffle` y quedate con los
5 primeros. Mostralos ordenados.

#### Criterio de aprobación

- Usa `std::shuffle` con el generador.
- Los 5 números son distintos (por construcción, no revisando).
- Se muestran ordenados.

#### Entrada de ejemplo

```
1810
```

#### Salida esperada

```
Números ganadores: 3 6 37 45 46
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El sorteo de la rifa: 5 numeros distintos entre 1 y 50.
#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

int main()
{
    unsigned semilla = 0;
    std::cin >> semilla;
    std::mt19937 gen(semilla);
    std::vector<int> bolillero;
    for (int n = 1; n <= 50; n++) {
        bolillero.push_back(n);
    }
    std::shuffle(bolillero.begin(), bolillero.end(), gen);   // mezclar
    std::vector<int> ganadores(bolillero.begin(), bolillero.begin() + 5);
    std::sort(ganadores.begin(), ganadores.end());
    std::cout << "Números ganadores:";
    for (int n : ganadores) {
        std::cout << " " << n;
    }
    std::cout << "\n";
    return 0;
}
```

### Prueba del sello

#### ¿Qué hace la semilla de un generador?

Fija el punto de partida: con la misma semilla, el generador da siempre la misma secuencia.

#### ¿Cómo hacés que cada ejecución sea distinta?

Usando como semilla un valor de `std::random_device`.

#### ¿Por qué conviene pasar el generador por referencia?

Para que todas las funciones usen el mismo generador y la secuencia avance; una copia repetiría los mismos números.

#### ¿Cómo sacás 5 números distintos de 1 a 50?

Poniendo los 50 en un vector, mezclándolo con `std::shuffle` y tomando los primeros 5.

#### ¿Qué hace `std::clamp(x, 0, 100)`?

Devuelve `x`, pero si es menor que 0 devuelve 0 y si es mayor que 100 devuelve 100.

### Soluciones (docente)

Nodo nuevo. Las salidas esperadas con `<random>` son las de `libstdc++` (g++ en Linux): `std::mt19937` está especificado por el estándar, pero las distribuciones y `std::shuffle` no. Un alumno con `clang`/`libc++` (macOS) puede obtener otros números con un programa correcto: corregir leyendo el código.

## R01-N09 · Jefe: el Autómata de Latón

```meta
tipo: jefe
padre: R01-N08
precio: 10
criatura: dragon
insignia: Sello del Autómata
insignia_descripcion: Venciste al Autómata de Latón: dominás los fundamentos de C++.
```

### Crónica

En el centro del patio de pruebas se levanta el **Autómata de Latón**: tres metros de placas remachadas, un corazón de vapor y una tarjeta perforada con una sola orden: "No dejar pasar a nadie que no domine los cimientos".

—Lo construí yo —confiesa {mentor}—, y lo hice terco a propósito. No se vence con fuerza: se vence con un plan. Leé lo que hace, partí el problema en funciones, y probá cada pieza antes de juntarlas.

### Objetivos

Integrar todo lo de la rama en programas completos: entrada validada, decisiones,
bucles, funciones con referencias, vectores y azar con semilla.

### Antes de empezar

- Toda la rama: variables, entrada y salida, decisiones, bucles, funciones,
  referencias, vectores, azar.

### Explicación

#### Cómo se enfrenta a un jefe
Un jefe es un programa más largo que los de las misiones. No se escribe de un
tirón: se **parte**.
1. **Leé la consigna entera** y la salida esperada. Anotá qué datos entran, qué
   sale y qué reglas hay.
2. **Hacé la lista de funciones**: una por cada tarea con nombre ("pedir una
   opción", "aplicar daño", "dibujar la barra"). Si una función no entra en la
   pantalla, partila.
3. **Decidí cómo recibe cada una sus datos**: por valor (números chicos), por
   `const&` (textos y vectores que solo lee), por `&` (lo que modifica).
4. **Escribí y probá de a una.** Compilá seguido: diez errores juntos asustan;
   uno por vez se arreglan en segundos.
5. **Recién al final**, el `main` que las junta.

#### Probar con la entrada de ejemplo
Guardá la entrada de ejemplo en un archivo y probá con
```bash
./programa < entrada.txt > mi_salida.txt
diff mi_salida.txt salida_esperada.txt
```
`diff` no muestra nada si son idénticas; si no, te dice qué líneas difieren.

#### Leer una opción de un menú, bien
Un menú tiene que sobrevivir a lo que escriba el usuario:
```cpp
int pedir_opcion()
{
    int op = 0;
    while (true) {
        std::cout << "Opción: ";
        if (!(std::cin >> op)) {
            return 0;               // se terminó la entrada: salir
        }
        if (op >= 1 && op <= 3) {
            return op;
        }
        std::cout << "Opción inválida.\n";
    }
}
```

### ¿Para qué sirve?

Así se construye cualquier programa real: se parte en funciones chicas y probadas, se valida la entrada y se prueba con datos fijos. Un cajero automático, un sistema de turnos o un juego por turnos tienen exactamente esta forma: un bucle principal que lee una opción, la valida y llama a la función que corresponde.

### Errores habituales

**Ogro: el `main` de 200 líneas.** Todo junto, nada se puede probar por separado y
un error se esconde entre cien líneas. Partilo en funciones.

**Goblin: el menú que enloquece con una letra.** Si `std::cin >> op` falla y no lo
revisás, el bucle gira para siempre mostrando el menú. Revisá la lectura.

**Ogro: el daño que deja vida negativa.** Centralizá el daño en **una** función
(`recibir`) que respete el piso de 0; si lo restás en cinco lugares, en alguno te
vas a olvidar.

**Ogro: el generador que se crea en cada turno.** El Autómata haría siempre el
mismo golpe. Un generador, creado una vez, pasado por referencia.

**Orco: un índice que viene de la entrada.** Si el usuario elige la posición, 
revisá que esté dentro del vector antes de usarla.

### Misión R01-N09-M1 · El duelo

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

Programá el duelo de Kira (60 de vida) contra el Autómata (70 de vida). La
entrada trae una **semilla** y después las opciones de Kira, una por turno.

Reglas:
- Golpes al azar con `std::uniform_int_distribution<int>(6, 12)`.
- Cada turno se muestra el número de turno y dos barras de vida de 10 casillas
  (`#` llenas, `.` vacías; llenas = `vida * 10 / maximo`).
- Opciones: **1** atacar (golpe + 8 por cada carga acumulada, y las cargas vuelven
  a 0), **2** curar 20 sin pasar el máximo (hay 2 pociones; sin pociones se pierde
  el turno), **3** cargar energía (+1 carga). Una opción fuera de 1..3 se vuelve a
  pedir.
- Si el Autómata sigue en pie, responde con un golpe; después se tira una moneda
  (`uniform_int_distribution<int>(0, 1)`): si sale 1, tropieza y su golpe se
  divide por 2.
- El orden de las tiradas importa (así sale igual que la salida esperada): primero
  el golpe de Kira (si ataca), después el golpe del Autómata y por último su
  moneda.
- Si la entrada se termina, Kira se retira.

Escribí al menos las funciones `pedir_opcion`, `recibir(int& vida, int dano)` y
`barra`.

#### Criterio de aprobación

- Separa el programa en funciones con los parámetros correctos (`&` para lo que modifican).
- Valida la opción y sobrevive a que se termine la entrada.
- Usa un único generador con la semilla leída.
- Respeta el orden de las tiradas y las reglas de cargas y pociones.

#### Entrada de ejemplo

```
2026
3
3
1
2
7
1
1
1
1
1
1
```

#### Salida esperada

```
--- Turno 1 ---
Kira     [##########] 60/60
Autómata [##########] 70/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira carga energía (1).
El Autómata tropieza con un engranaje suelto.
El Autómata golpea por 3.
--- Turno 2 ---
Kira     [#########.] 57/60
Autómata [##########] 70/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira carga energía (2).
El Autómata tropieza con un engranaje suelto.
El Autómata golpea por 4.
--- Turno 3 ---
Kira     [########..] 53/60
Autómata [##########] 70/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira golpea por 28.
El Autómata golpea por 12.
--- Turno 4 ---
Kira     [######....] 41/60
Autómata [######....] 42/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira se cura. Pociones restantes: 1.
El Autómata golpea por 10.
--- Turno 5 ---
Kira     [########..] 50/60
Autómata [######....] 42/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Opción inválida.
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira golpea por 6.
El Autómata tropieza con un engranaje suelto.
El Autómata golpea por 6.
--- Turno 6 ---
Kira     [#######...] 44/60
Autómata [#####.....] 36/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira golpea por 7.
El Autómata tropieza con un engranaje suelto.
El Autómata golpea por 5.
--- Turno 7 ---
Kira     [######....] 39/60
Autómata [####......] 29/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira golpea por 8.
El Autómata golpea por 9.
--- Turno 8 ---
Kira     [#####.....] 30/60
Autómata [###.......] 21/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira golpea por 11.
El Autómata golpea por 11.
--- Turno 9 ---
Kira     [###.......] 19/60
Autómata [#.........] 10/70
Tu turno (1 atacar, 2 curar, 3 cargar): 
Kira golpea por 10.
=== ¡Kira vence al Autómata de Latón! ===
```

#### Solución de referencia

```cpp
// Jefe R01 - El duelo contra el Automata de Laton.
#include <algorithm>
#include <iostream>
#include <random>
#include <string>

const int VIDA_KIRA = 60;
const int VIDA_AUTOMATA = 70;

// Lee una opcion entre 1 y 3. Devuelve 0 si la entrada se termino.
int pedir_opcion()
{
    int op = 0;
    while (true) {
        std::cout << "Tu turno (1 atacar, 2 curar, 3 cargar): ";
        if (!(std::cin >> op)) {
            std::cout << "\n";
            return 0;
        }
        std::cout << "\n";
        if (op >= 1 && op <= 3) {
            return op;
        }
        std::cout << "Opción inválida.\n";
    }
}

void recibir(int& vida, int dano)
{
    vida -= dano;
    if (vida < 0) {
        vida = 0;
    }
}

void barra(const std::string& nombre, int vida, int maximo)
{
    std::cout << nombre << " [";
    for (int i = 0; i < 10; i++) {
        std::cout << (i < vida * 10 / maximo ? '#' : '.');
    }
    std::cout << "] " << vida << "/" << maximo << "\n";
}

int main()
{
    unsigned semilla = 0;
    std::cin >> semilla;
    std::mt19937 gen(semilla);
    std::uniform_int_distribution<int> golpe(6, 12);
    std::uniform_int_distribution<int> moneda(0, 1);

    int kira = VIDA_KIRA;
    int automata = VIDA_AUTOMATA;
    int carga = 0;
    int pociones = 2;
    int turno = 1;

    while (kira > 0 && automata > 0) {
        std::cout << "--- Turno " << turno << " ---\n";
        barra("Kira    ", kira, VIDA_KIRA);
        barra("Autómata", automata, VIDA_AUTOMATA);
        int op = pedir_opcion();
        if (op == 0) {
            std::cout << "Kira se retira del duelo.\n";
            return 0;
        }
        if (op == 1) {
            int dano = golpe(gen) + carga * 8;
            carga = 0;
            recibir(automata, dano);
            std::cout << "Kira golpea por " << dano << ".\n";
        } else if (op == 2) {
            if (pociones > 0) {
                pociones--;
                kira = std::min(kira + 20, VIDA_KIRA);
                std::cout << "Kira se cura. Pociones restantes: " << pociones << ".\n";
            } else {
                std::cout << "No quedan pociones: Kira pierde el turno.\n";
            }
        } else {
            carga++;
            std::cout << "Kira carga energía (" << carga << ").\n";
        }
        if (automata > 0) {
            int dano = golpe(gen);
            if (moneda(gen) == 1) {
                dano /= 2;
                std::cout << "El Autómata tropieza con un engranaje suelto.\n";
            }
            recibir(kira, dano);
            std::cout << "El Autómata golpea por " << dano << ".\n";
        }
        turno++;
    }
    std::cout << "=== " << (kira > 0 ? "¡Kira vence al Autómata de Latón!" : "El Autómata gana esta vez.") << " ===\n";
    return 0;
}
```

### Misión R01-N09-M2 · Las placas del Autómata

```meta
entrega: codigo
entorno: local
monedas: 6
xp: 30
```

#### Consigna

El Autómata tiene 7 placas de blindaje: `30 30 40 50 40 30 30`. Cada línea de la
entrada es un golpe: `posición fuerza`. Un golpe resta `fuerza` a su placa y la
**mitad** a cada vecina (la de la izquierda y la de la derecha, si existen y no
están rotas); ninguna baja de 0. Una posición fuera del vector es un golpe al aire.

Después de cada golpe, mostrá cuántas placas se rompieron con ese golpe (si alguna)
y el estado (`[0:30][1:30]…`). Si todas quedan en 0, el Autómata se desarma: mostrá
en cuántos golpes y terminá. Si la entrada se termina antes, mostrá cuántas placas
quedan enteras.

Escribí `int golpear(std::vector<int>& placas, int pos, int fuerza)`, que aplica el
golpe y devuelve cuántas placas nuevas se rompieron.

#### Criterio de aprobación

- `golpear` recibe el vector por referencia y devuelve las placas rotas.
- Respeta los bordes del vector y no baja de 0.
- Termina al romperse todas las placas o al terminarse la entrada.

#### Entrada de ejemplo

```
3 50
2 40
4 40
9 99
0 60
6 60
1 30
5 30
3 10
```

#### Salida esperada

```
[0:30][1:30][2:40][3:50][4:40][5:30][6:30]
Golpe en 3 por 50: ¡1 placa(s) rota(s)!
[0:30][1:30][2:15][3:0][4:15][5:30][6:30]
Golpe en 2 por 40: ¡1 placa(s) rota(s)!
[0:30][1:10][2:0][3:0][4:15][5:30][6:30]
Golpe en 4 por 40: ¡1 placa(s) rota(s)!
[0:30][1:10][2:0][3:0][4:0][5:10][6:30]
Golpe al aire.
Golpe en 0 por 60: ¡2 placa(s) rota(s)!
[0:0][1:0][2:0][3:0][4:0][5:10][6:30]
Golpe en 6 por 60: ¡2 placa(s) rota(s)!
[0:0][1:0][2:0][3:0][4:0][5:0][6:0]
El Autómata se desarma en 6 golpes.
```

#### Solución de referencia

```cpp
// Jefe R01 - Las placas del Automata: reparar los paneles con un vector y funciones.
#include <algorithm>
#include <iostream>
#include <vector>

void mostrar(const std::vector<int>& placas)
{
    for (std::size_t i = 0; i < placas.size(); i++) {
        std::cout << "[" << i << ":" << placas[i] << "]";
    }
    std::cout << "\n";
}

// Aplica un golpe a una placa y a sus vecinas (la mitad). Devuelve las placas rotas nuevas.
int golpear(std::vector<int>& placas, int pos, int fuerza)
{
    int rotas = 0;
    for (int d = -1; d <= 1; d++) {
        int i = pos + d;
        if (i < 0 || i >= static_cast<int>(placas.size()) || placas[i] == 0) {
            continue;
        }
        int dano = (d == 0) ? fuerza : fuerza / 2;
        placas[i] = std::max(0, placas[i] - dano);
        if (placas[i] == 0) {
            rotas++;
        }
    }
    return rotas;
}

int main()
{
    std::vector<int> placas = {30, 30, 40, 50, 40, 30, 30};
    mostrar(placas);
    int pos = 0, fuerza = 0, golpes = 0;
    while (std::cin >> pos >> fuerza) {
        golpes++;
        if (pos < 0 || pos >= static_cast<int>(placas.size())) {
            std::cout << "Golpe al aire.\n";
            continue;
        }
        int rotas = golpear(placas, pos, fuerza);
        std::cout << "Golpe en " << pos << " por " << fuerza;
        if (rotas > 0) {
            std::cout << ": ¡" << rotas << " placa(s) rota(s)!";
        }
        std::cout << "\n";
        mostrar(placas);
        if (std::count(placas.begin(), placas.end(), 0) == static_cast<long>(placas.size())) {
            std::cout << "El Autómata se desarma en " << golpes << " golpes.\n";
            return 0;
        }
    }
    int enteras = static_cast<int>(placas.size() - std::count(placas.begin(), placas.end(), 0));
    std::cout << "Quedan " << enteras << " placas enteras.\n";
    return 0;
}
```

### Encargo R01-N09-E1 · El cajero automático

```meta
entrega: codigo
entorno: local
monedas: 1
xp: 30
```

#### Consigna

Programá un cajero con saldo inicial de $10000 y un menú: **1** depositar, **2**
extraer, **3** ver movimientos, **0** salir. Los montos tienen que ser positivos y
no se puede extraer más que el saldo. Guardá cada movimiento en un
`std::vector<std::string>` como `+5000` o `-2500` (usá `std::to_string`). Al
salir (o si se termina la entrada), mostrá el saldo final y la cantidad de
movimientos. Todo con 2 decimales.

#### Criterio de aprobación

- El menú se repite hasta elegir 0 o hasta que se termine la entrada.
- Valida montos y saldo.
- Guarda los movimientos en un vector.

#### Entrada de ejemplo

```
1
5000
2
20000
2
2500
4
1
-3
3
0
```

#### Salida esperada

```
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Monto: 
Saldo: $15000.00
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Monto: 
Saldo insuficiente.
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Monto: 
Saldo: $12500.00
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Opción inválida.
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Monto: 
Monto inválido.
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Movimientos: +5000 -2500
1 depositar, 2 extraer, 3 movimientos, 0 salir: 
Saldo final: $12500.00 en 2 movimientos.
```

#### Solución de referencia

```cpp
// Encargo del Gremio - El cajero automatico: menu, saldo y movimientos.
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

int leer_opcion()
{
    int op = 0;
    std::cout << "1 depositar, 2 extraer, 3 movimientos, 0 salir: ";
    if (!(std::cin >> op)) {
        op = 0;
    }
    std::cout << "\n";
    return op;
}

bool leer_monto(double& monto)
{
    std::cout << "Monto: ";
    bool ok = static_cast<bool>(std::cin >> monto) && monto > 0;
    std::cout << "\n";
    return ok;
}

int main()
{
    std::cout << std::fixed << std::setprecision(2);
    double saldo = 10000;
    std::vector<std::string> movimientos;
    int op = leer_opcion();
    while (op != 0) {
        double monto = 0;
        if (op == 1) {
            if (leer_monto(monto)) {
                saldo += monto;
                movimientos.push_back("+" + std::to_string(static_cast<int>(monto)));
                std::cout << "Saldo: $" << saldo << "\n";
            } else {
                std::cout << "Monto inválido.\n";
            }
        } else if (op == 2) {
            if (!leer_monto(monto)) {
                std::cout << "Monto inválido.\n";
            } else if (monto > saldo) {
                std::cout << "Saldo insuficiente.\n";
            } else {
                saldo -= monto;
                movimientos.push_back("-" + std::to_string(static_cast<int>(monto)));
                std::cout << "Saldo: $" << saldo << "\n";
            }
        } else if (op == 3) {
            std::cout << "Movimientos:";
            for (const std::string& m : movimientos) {
                std::cout << " " << m;
            }
            std::cout << (movimientos.empty() ? " (ninguno)" : "") << "\n";
        } else {
            std::cout << "Opción inválida.\n";
        }
        op = leer_opcion();
    }
    std::cout << "Saldo final: $" << saldo << " en " << movimientos.size() << " movimientos.\n";
    return 0;
}
```

### Prueba del sello

#### ¿Por qué conviene una sola función `recibir` para restar vida?

Porque la regla (no bajar de 0) queda en un solo lugar: no hay forma de olvidarla en algún rincón del programa.

#### ¿Por qué el duelo da siempre el mismo resultado con la misma entrada?

Porque el generador usa la semilla leída: la misma semilla da la misma secuencia de tiradas.

#### ¿Qué pasa en tu menú si la entrada se termina en medio del duelo?

La lectura falla, `pedir_opcion` devuelve 0 y el programa termina ordenado.

#### En `golpear`, ¿por qué el vector va por referencia?

Porque la función tiene que modificar las placas del vector original, no de una copia.

#### ¿Cómo comparás tu salida con la esperada sin mirar línea por línea?

Guardándola en un archivo y usando `diff`.

### Soluciones (docente)

Jefe de la rama 1. Las tres prácticas integran la rama completa. Los resultados del duelo dependen de la semilla y del orden de las tiradas; con `libc++` (macOS) los números cambian: corregir leyendo el código.
